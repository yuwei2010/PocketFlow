# PocketFlow Parallel Batch Translation Example

This example demonstrates translating a document (the main PocketFlow README.md) into multiple target languages concurrently using PocketFlow's parallel batch processing capabilities (`AsyncParallelBatchNode` and `AsyncFlow`).

It showcases how to leverage asynchronous operations and parallelism to potentially speed up I/O-bound tasks, such as making multiple LLM API calls simultaneously.

## Goal

Translate the content of `PocketFlow/README.md` into a predefined list of languages:
`["Chinese", "Spanish", "Japanese", "German", "Russian", "Portuguese", "French", "Korean"]`

The primary focus is to execute these translation tasks *in parallel* and measure the total time taken, allowing for comparison with a sequential approach (like the one demonstrated in the standard `pocketflow-batch` example).

## PocketFlow Concepts Used

-   **`AsyncParallelBatchNode`**: Processes an iterable (the list of target languages) by running an asynchronous task (translation using an LLM) for each item concurrently.
-   **`AsyncFlow`**: Manages the execution of flows containing asynchronous nodes.
-   **Asynchronous Utility**: A helper function (`call_llm_async`) that interacts with the Anthropic API asynchronously.

## File Structure

```
pocketflow-parallel-batch/
├── main.py           # Defines the PocketFlow node and flow, orchestrates the parallel translation
├── utils.py          # Contains the asynchronous `call_llm_async` utility using Anthropic API
├── requirements.txt  # Dependencies: pocketflow, anthropic, python-dotenv, httpx
└── README.md         # This explanation file
```

## Setup

1.  **Navigate to the example directory**:
    ```bash
    cd cookbook/pocketflow-parallel-batch
    ```
2.  **Create and activate a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up Anthropic API Key**: Create a `.env` file in this directory:
    ```
    ANTHROPIC_API_KEY=your_anthropic_api_key_here
    ```
    Or, set the `ANTHROPIC_API_KEY` environment variable.

## Running the Example

Execute the main script from within the `pocketflow-parallel-batch` directory:

```bash
python main.py
```

The script will:
1.  Read the content of `../../README.md`.
2.  Initiate the `AsyncFlow`.
3.  The `ParallelTranslateReadme` node will concurrently request translations for the README content into each target language via the Anthropic API.
4.  Print status messages for each requested and received translation.
5.  Report the list of languages for which translations were successfully generated.
6.  Display the total time taken for the entire parallel process.

## Parallel vs. Sequential Comparison

Note the total execution time reported by this script. Compare it to the time it would take if each language translation were performed one after the other (sequentially). For tasks involving multiple independent API calls like this, the parallel approach using `AsyncParallelBatchNode` is expected to be significantly faster, limited primarily by the LLM API's response time and potential rate limits, rather than the sum of individual call durations. 