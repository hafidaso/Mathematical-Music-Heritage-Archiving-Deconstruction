import os
import sys
import glob
import asyncio
from google.antigravity import Agent, LocalAgentConfig, types

async def main():
    # 1. Search for a test audio file in the Downloads folder
    print("Searching for a test audio file...")
    test_file = None
    possible_files = [
        "/Users/hafida/Downloads/Ride Cymbal Zap.mp3",
        "/Users/hafida/Downloads/Rain_on_the_Boulevard.mp3",
    ] + glob.glob("/Users/hafida/Downloads/*.mp3") + glob.glob("/Users/hafida/Downloads/*.wav")

    for path in possible_files:
        if os.path.exists(path):
            test_file = path
            break

    if not test_file:
        print("Error: No test audio file (.mp3 or .wav) found in /Users/hafida/Downloads/")
        print("Please place a test audio file in Downloads and try again.")
        return

    print(f"Found test audio file: {test_file}")

    # 2. Locate the local MCP server path
    server_path = os.path.abspath("sonic_mcp_server.py")
    if not os.path.exists(server_path):
        print(f"Error: sonic_mcp_server.py not found at {server_path}")
        return

    print(f"Configuring MCP Server with path: {server_path}")

    # 3. Configure the MCP server command (Stdio transport)
    # Using sys.executable ensures it runs in the exact same python environment
    mcp_servers = [
        types.McpStdioServer(
            name="sonic_mcp",
            command=sys.executable,
            args=[server_path]
        )
    ]

    # Initialize agent configuration with English system instructions
    config = LocalAgentConfig(
        mcp_servers=mcp_servers,
        system_instructions=(
            "You are an expert music heritage assistant and mathematical signal analyst. "
            "Your task is to analyze acoustic features of audio files using the local MCP server "
            "(Spectral Centroid, Spectral Flatness, FFT, and Mel-Spectrogram). "
            "Explain microtonal scales, rhythms, and tempo (BPM) using precise mathematical and musicological terms."
        )
    )

    print("Initializing Google Antigravity Agent and connecting to MCP Server...")
    async with Agent(config) as agent:
        prompt = (
            f"Use your available tools to analyze the following audio file and extract its features: {test_file}. "
            "Analyze the dominant frequencies (FFT Peaks), rhythmic fractality, and advanced spectral features (Spectral Centroid and Flatness), "
            "then provide a mathematical explanation of scales, tempo (BPM), and timbre."
        )
        
        print("\n--- Sending Prompt to Agent ---")
        print(prompt)
        print("\n--- Agent Thoughts and Response ---")
        
        # Send prompt and stream the agent's response
        response = await agent.chat(prompt)
        async for token in response:
            print(token, end="", flush=True)
        print("\n-------------------------------")

if __name__ == "__main__":
    # Run async loop for agent execution
    asyncio.run(main())
