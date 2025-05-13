import streamlit as st
from flow import create_initial_processing_flow, create_finalization_flow

st.title("PocketFlow HITL with Streamlit")

# Initialize session state variables if they don't exist
if 'stage' not in st.session_state:
    st.session_state.stage = "initial"
    st.session_state.error_message = None
    st.session_state.task_input = ""
    # Flow-related data will be added directly as needed
    print("Initialized session state.")

# --- Helper Function to Reset State ---
def reset_state():
    # Keep essential Streamlit state keys if necessary, or clear selectively
    keys_to_clear = [k for k in st.session_state.keys() if k not in ['stage', 'error_message', 'task_input']]
    for key in keys_to_clear:
        del st.session_state[key]
        
    st.session_state.stage = "initial"
    st.session_state.error_message = None
    st.session_state.task_input = ""
    print("Reset session state (keeping core stage/error keys).")

# --- Display Area for Shared Data (now the entire session state) ---
with st.expander("Show Session State (Shared Data)"):
    # Convert to dict for clean JSON display, excluding internal Streamlit keys if desired
    display_state = {k: v for k, v in st.session_state.items() if not k.startswith("_")}
    st.json(display_state)

# --- Stage: Initial Input ---
if st.session_state.stage == "initial":
    st.header("1. Submit Data for Processing")
    # Use st.session_state.task_input directly for the text area's value
    task_input_value = st.text_area("Enter data to process:", value=st.session_state.task_input, height=150)
    
    if st.button("Submit"):
        if not task_input_value.strip():
            st.error("Please enter some data to process.")
        else:
            print(f"Submit button clicked. Input: '{task_input_value[:50]}...'")
            # Store input directly in session state
            st.session_state.task_input = task_input_value 
            st.session_state.error_message = None
            # Clear previous results if any
            if "processed_output" in st.session_state: del st.session_state.processed_output
            if "final_result" in st.session_state: del st.session_state.final_result
            if "input_used_by_process" in st.session_state: del st.session_state.input_used_by_process
            
            try:
                with st.spinner("Processing initial task..."):
                    initial_flow = create_initial_processing_flow()
                    # Pass the entire session state as shared data
                    initial_flow.run(st.session_state)
                
                # Check if processing was successful (output exists directly in session state)
                if "processed_output" in st.session_state:
                    st.session_state.stage = "awaiting_review"
                    print("Initial processing complete. Moving to 'awaiting_review' stage.")
                    st.rerun()
                else:
                    st.session_state.error_message = "Processing failed to produce an output."
                    print("Error: Processing failed, no output found.")
                    # Keep stage as initial to allow retry/correction

            except Exception as e:
                st.session_state.error_message = f"An error occurred during initial processing: {e}"
                print(f"Exception during initial processing: {e}")
                # Keep stage as initial

# --- Stage: Awaiting Review ---
elif st.session_state.stage == "awaiting_review":
    st.header("2. Review Processed Output")
    # Get processed output directly from session state
    processed_output = st.session_state.get("processed_output", "Error: Processed output not found!")
    
    st.subheader("Output to Review:")
    st.markdown(f"```\n{str(processed_output)}\n```") # Display as markdown code block
    
    col1, col2, _ = st.columns([1, 1, 5]) # Layout buttons
    with col1:
        if st.button("Approve"):
            print("Approve button clicked.")
            st.session_state.error_message = None
            try:
                with st.spinner("Finalizing result..."):
                    finalization_flow = create_finalization_flow()
                    # Pass the entire session state
                    finalization_flow.run(st.session_state)
                
                # Check for final result directly in session state
                if "final_result" in st.session_state:
                    st.session_state.stage = "completed"
                    print("Approval processed. Moving to 'completed' stage.")
                    st.rerun()
                else:
                     st.session_state.error_message = "Finalization failed to produce a result."
                     print("Error: Finalization failed, no final_result found.")
                     # Stay in review stage and show error.

            except Exception as e:
                st.session_state.error_message = f"An error occurred during finalization: {e}"
                print(f"Exception during finalization: {e}")
                # Stay in review stage
                st.rerun() # Rerun to show error message

    with col2:
        if st.button("Reject"):
            print("Reject button clicked.")
            st.session_state.error_message = None # Clear previous errors
            # Go back to initial stage to allow modification/resubmission
            st.session_state.stage = "initial"
            # Keep the rejected output visible in the input field for modification
            st.session_state.task_input = st.session_state.get("processed_output", st.session_state.task_input)
            # Clear the processed output so it doesn't linger
            if "processed_output" in st.session_state: del st.session_state.processed_output
            if "final_result" in st.session_state: del st.session_state.final_result
            st.info("Task rejected. Modify the input below and resubmit.")
            print("Task rejected. Moving back to 'initial' stage.")
            st.rerun()

# --- Stage: Completed ---
elif st.session_state.stage == "completed":
    st.header("3. Task Completed")
    # Get final result directly from session state
    final_result = st.session_state.get("final_result", "Error: Final result not found!")
    st.subheader("Final Result:")
    st.success("Task approved and completed successfully!")
    st.text_area("", value=str(final_result), height=200, disabled=True)
    
    if st.button("Start Over"):
        print("Start Over button clicked.")
        reset_state()
        st.rerun()

# --- Stage: Rejected ---
elif st.session_state.stage == "rejected_final":
    st.header("3. Task Rejected")
    st.error("The processed output was rejected.")
    # Get rejected output directly from session state
    rejected_output = st.session_state.get("processed_output", "")
    if rejected_output:
        st.text_area("Rejected Output:", value=str(rejected_output), height=150, disabled=True)
        
    if st.button("Start Over"):
        print("Start Over button clicked.")
        reset_state()
        st.rerun()

# --- Display Error Messages ---
if st.session_state.error_message:
    st.error(st.session_state.error_message)

# --- Add a button to reset state anytime (for debugging) ---
# st.sidebar.button("Reset State", on_click=reset_state) # Removed sidebar
