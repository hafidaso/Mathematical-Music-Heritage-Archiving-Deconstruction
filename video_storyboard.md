# Video Storyboard & Script (5 Mins Demonstration)

**Suggested Video Title:** *Humanizing Heritage Acoustics Mathematically using Antigravity and MCP*

* **Goal:** Demonstrate ease of deployment, security, and multi-agent capabilities in a live recording of under 5 minutes utilizing the **Antigravity IDE** and **Streamlit** dashboard.

---

## ⏱️ Timeline Overview

| Time | Section | Visual Focus | Voiceover (V.O.) Script |
| :--- | :--- | :--- | :--- |
| **0:00 - 1:00** | Introduction & Concept | Heritage visuals / Project Workspace | Preserving North African/Sahara oral musical heritage mathematically. |
| **1:00 - 2:00** | System Architecture & MCP | Architectural diagrams / Code walkthrough | How FastMCP exposes local DSP calculations to the LLM. |
| **2:00 - 4:00** | Live Demo: IDE & Dashboard | Antigravity IDE and Streamlit Dashboard | Running the multi-agent pipeline, uploading audio, and displaying results. |
| **4:00 - 5:00** | Security & Conclusion | `validate_file` code / Closing slides | Security measures, Z-score standardization, and academic value. |

---

## 🎬 Detailed Scene-by-Scene Script

### Section 1: Problem & Concept (0:00 - 1:00)
* **Visuals:** Close-up of the host or a title screen showing the workspace, followed by scrolling through [README.md](file:///Users/hafida/Downloads/Archiving%20and%20deconstructing%20musical%20heritage%20mathematically/README.md).
* **V.O. Script:**
  > *"Welcome. The rich oral music traditions of North Africa and the Sahara are fading due to a lack of formal notation. Our project addresses this challenge: **Mathematical Music Heritage Archiving & Deconstruction**. Instead of just compression, we humanize signal processing by translating acoustics into deep cultural and anthropological narratives locally and securely using generative AI agents."*

---

### Section 2: System Architecture & MCP (1:00 - 2:00)
* **Visuals:** Walkthrough of [sonic_mcp_server.py](file:///Users/hafida/Downloads/Archiving%20and%20deconstructing%20musical%20heritage%20mathematically/sonic_mcp_server.py) in the code editor.
* **V.O. Script:**
  > *"The backbone of our system is a local MCP server built with FastMCP. It runs DSP code using librosa and numpy directly on the user's hardware to guarantee privacy. To achieve data and token efficiency, we extract top-10 dominant frequency peaks, rhythmic fractality (the Hurst Index), and advanced physical descriptors like Spectral Centroid and Spectral Flatness to feed compact numerical vectors into the LLM, avoiding context window explosions."*

---

### Section 3: Live Demo in Antigravity & Streamlit (2:00 - 4:00)
* **Visuals:** Walkthrough of [main_agent_orchestrator.py](file:///Users/hafida/Downloads/Archiving%20and%20deconstructing%20musical%20heritage%20mathematically/main_agent_orchestrator.py) running in the terminal showing agent outputs, then switching to the browser showing the Streamlit UI.
* **V.O. Script:**
  > *"Let's see the system in action. Using the Antigravity SDK, we orchestrate a debate loop between a Mathematician Agent and a Cultural Historian Agent. The agents check each other's work and resolve data conflicts dynamically. For user deployment, we built a Streamlit app. Uploading a local audio file instantly returns the Spectral Centroid, Tempo, and Flatness. Crucially, it displays Z-score standardized distances to regional music traditions like Tuareg Desert Blues and Gnawa, highlighting cultural links mathematically."*

---

### Section 4: Security & Conclusion (4:00 - 5:00)
* **Visuals:** Highlighting `validate_file` code in the editor, showing traversal checks and extension filters.
* **V.O. Script:**
  > *"Security is built-in. Our validate_file tool prevents Directory Traversal by resolving real path symlinks and whitelisting audio formats. In conclusion, combining local MCP servers with Google Antigravity agents opens a secure, efficient path for archiving oral human culture. Thank you."*

---

## 💡 Recording Tips:
1. **Clear Audio:** Use a good external microphone. Since the project is about acoustics, clean sound in the recording is highly appreciated by the judges.
2. **Smooth Transitions:** Speed up loading times in post-production if file analysis takes a few seconds so that the demonstration feels instant.
3. **High Definition:** Export in 1080p MP4 format and host on a reliable cloud platform.
