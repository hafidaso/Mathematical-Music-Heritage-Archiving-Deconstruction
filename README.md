# Mathematical Music Heritage Archiving & Deconstruction

An integrated and secure system designed to analyze and archive traditional musical heritage locally using the Model Context Protocol (MCP) and integrated with the **Google Antigravity SDK** framework.

This project ensures secure processing of heritage audio files, extracting mathematical features and comparing them to local taxonomy matrices without sending raw audio data to external servers, protecting both user privacy and intellectual property.

---

## 🏗️ System Architecture

The project consists of two main environments optimized for local execution:

1. **Local Development & DSP Environment:**
   * **Local MCP Server (`sonic_mcp_server.py`):** Built using the official `FastMCP` framework, interfacing with local DSP algorithms (FFT, Spectral Centroid, Spectral Flatness, and Rhythmic Fractality) via `librosa` and `numpy`.
   * **Interactive Dashboard (`app.py`):** A clean Streamlit dashboard allowing users to upload local audio files and visualize dominant frequencies and cross-cultural distance matrices.
2. **ADK & Antigravity IDE Environment:**
   * **Multi-Agent Orchestrator (`main_agent_orchestrator.py`):** Orchestrates a debate loop between a Mathematician Agent and a Cultural Historian Agent using the **Google Antigravity SDK** to analyze results and resolve data discrepancies.
   * **Antigravity IDE Integration:** Integrates the local server tools directly into the Antigravity IDE sidebar panel for interactive prompting.
   * **Standalone Test Client (`sonic_agent.py`):** A quick validation client connecting the Antigravity SDK directly to the stdio server.

---

## 🔒 Security Hardening

To ensure complete compliance with security standards, the local server implements:
* **Directory Traversal Protection:** The `validate_file` function resolves absolute paths and eliminates symlinks using `os.path.realpath` to prevent path traversal exploits.
* **Extension Whitelisting:** Limits file processing exclusively to safe audio formats: `wav, mp3, ogg, flac, m4a, aac, wma`.
* **Safe Error Handling:** Audio library exceptions are caught and sanitized before being returned to the LLM to avoid exposing internal directory structures.

---

## ⚡ Data & Token Efficiency

Large language models (LLMs) cannot process millions of raw audio samples. The server utilizes efficient dimensional reduction techniques:
1. **FFT Compression:** Extracts only the positive frequencies and returns the **top 10 dominant peaks** (frequencies and magnitudes) to plot the sonic fingerprint.
2. **Advanced Spectral Features:** Extracts **Spectral Centroid** (identifying acoustic register and brightness, e.g., high violin strings vs. deep wooden drums) and **Spectral Flatness** (identifying noise vs. pure tonal notes) to represent the physical properties of instruments.
3. **Rhythmic Fractality:** Calculates the **Hurst Exponent** of the RMS energy envelope to capture temporal complexity and polyrhythms.
4. **Standardized Euclidean Distance:** Compares the local feature vector to a reference Moroccan/Sahara regional taxonomy using Z-score standardization (simplified Mahalanobis distance) to normalize features and prevent scaling issues.

---

## 🛠️ Prerequisites & Setup

1. Install the required packages in your local environment:
   ```bash
   pip install mcp librosa numpy scipy google-antigravity streamlit matplotlib
   ```
2. Configure your Gemini API key:
   ```bash
   export GEMINI_API_KEY="your_actual_api_key_here"
   ```

---

## 📂 Project Structure

* **`sonic_mcp_server.py`:** The local FastMCP server containing audio processing and distance matching tools.
* **`main_agent_orchestrator.py`:** Runs the multi-agent asynchronous debate loop.
* **`app.py`:** The interactive Streamlit dashboard.
* **`sonic_agent.py`:** A standalone client to test agent connectivity.
* **`test_plot.py`:** A utility script to verify Matplotlib drawing in headless setups.

---

## 🚀 Execution & Verification

### 1. Launch the Streamlit Dashboard
Run the following command to start the interactive web UI:
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser to test uploading audio files and analyzing similarity.

### 2. Inspect the MCP Server via CLI
Verify server tools and schemas using the official MCP Inspector:
```bash
mcp dev sonic_mcp_server.py
```

### 3. Run the Standalone Client
Run the quick verification client to check LLM agent tool integration:
```bash
python3 sonic_agent.py
```

### 4. Integrate with Antigravity IDE (GUI)
To load these tools directly in your Antigravity IDE:
1. Open the IDE MCP configuration file at:
   `~/.gemini/antigravity-ide/mcp_config.json`
2. Add the custom server definition, ensuring paths match your workspace:
   ```json
   {
     "mcpServers": {
       "sonic-heritage-analyzer": {
         "command": "/Users/hafida/.platformio/penv/bin/python3",
         "args": [
           "/Users/hafida/Downloads/Archiving and deconstructing musical heritage mathematically/sonic_mcp_server.py"
         ],
         "env": {}
       }
     }
   }
   ```
3. Open the **Antigravity IDE** application. The tools will register in the sidebar automatically.
