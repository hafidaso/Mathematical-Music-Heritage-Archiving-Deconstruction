import streamlit as st
import os
import numpy as np
import matplotlib.pyplot as plt
import sonic_mcp_server

# Page configuration
st.set_page_config(
    page_title="Sonic Heritage Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimalist visual layout styling
st.markdown("""
    <style>
    .reportview-container { background: #FAFAFA; }
    .main .block-container { padding-top: 2rem; }
    h1 { color: #222222; font-weight: 800; }
    h3 { color: #555555; }
    </style>
""", unsafe_allow_html=True)

st.title("Mathematical Deconstruction & Archiving of Musical Heritage")
st.subheader("Local Audio Signal Processing & Cross-Cultural Distance Analysis")
st.write("---")

# Audio file uploader
uploaded_file = st.file_uploader("Select a local heritage audio file to analyze securely", type=["mp3", "wav", "flac", "m4a"])

if uploaded_file:
    # Resolve temporary local path
    temp_path = os.path.join(os.path.expanduser("~"), "Downloads", uploaded_file.name)
    
    # Save the uploaded file locally so librosa can process it via absolute path
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File uploaded and saved securely at: {temp_path}")
    
    # Interactive audio player
    st.audio(temp_path)
    
    # Execution trigger button
    if st.button("Deconstruct Audio & Analyze Similarity"):
        with st.spinner("Executing local MCP server and similarity distance engine..."):
            try:
                # 1. Invoke local signal processing tools
                fft_results = sonic_mcp_server.extract_fft_features(temp_path)
                spectral_results = sonic_mcp_server.extract_advanced_spectral_features(temp_path)
                
                # Invoke the standardized V2 similarity engine
                similarity_data = sonic_mcp_server.compare_heritage_similarity_v2(
                    estimated_bpm=spectral_results['estimated_bpm'],
                    spectral_centroid=spectral_results['spectral_centroid_hz'],
                    spectral_flatness=spectral_results['spectral_flatness']
                )
                
                # 2. Display key metrics (assign larger weight to Closest Match to prevent truncation)
                col1, col2, col3, col4 = st.columns([1, 1, 1, 1.8])
                with col1:
                    st.metric("Spectral Centroid", f"{spectral_results['spectral_centroid_hz']:.1f} Hz")
                with col2:
                    st.metric("Tempo", f"{spectral_results['estimated_bpm']:.1f} BPM")
                with col3:
                    st.metric("Spectral Flatness", f"{spectral_results['spectral_flatness']:.5f}")
                with col4:
                    st.metric("Closest Match", similarity_data['closest_cultural_match'])

                st.write("---")
                
                # 3. Double columns for plots
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.write("### Sonic Fingerprint (Dominant Frequencies)")
                    freqs = fft_results['dominant_frequencies_hz']
                    mags = fft_results['peak_magnitudes']
                    
                    # Sort ascending for plotting
                    idx = np.argsort(freqs)
                    freqs, mags = np.array(freqs)[idx], np.array(mags)[idx]
                    
                    fig1, ax1 = plt.subplots(figsize=(6, 3), facecolor='#FAFAFA')
                    ax1.set_facecolor('#FAFAFA')
                    
                    # Draw clean stem plot representing spectral footprint
                    markerline, stemlines, baseline = ax1.stem(freqs, mags, linefmt='#2C3E50', markerfmt='o', basefmt=' ')
                    plt.setp(markerline, markersize=5, color='#2C3E50', alpha=0.9)
                    plt.setp(stemlines, linewidth=1.2, color='#2C3E50', alpha=0.4)
                    
                    for spine in ['top', 'right', 'left', 'bottom']:
                        ax1.spines[spine].set_visible(False)
                    ax1.grid(axis='y', linestyle='--', linewidth=0.5, color='#E0E0E0')
                    ax1.tick_params(axis='both', colors='#555555', labelsize=8)
                    ax1.set_xlabel('Frequency (Hz)', color='#555555', fontsize=8)
                    ax1.set_ylabel('Magnitude', color='#555555', fontsize=8)
                    
                    st.pyplot(fig1)
                
                with col_right:
                    st.write("### Cross-Cultural Similarity Affinity (%)")
                    # Calculate affinity percentage (100 / (1 + distance)) for intuitive visualization
                    genres = list(similarity_data['standardized_distance_matrix'].keys())
                    distances = list(similarity_data['standardized_distance_matrix'].values())
                    affinities = [float(round(100 / (1 + d), 1)) for d in distances]
                    
                    # Sort so the highest affinity (closest match) is at the top (longest bar)
                    idx_sort = np.argsort(affinities) # Ascending sorts lower affinities first
                    genres = [genres[i] for i in idx_sort]
                    affinities = [affinities[i] for i in idx_sort]
                    
                    fig2, ax2 = plt.subplots(figsize=(6, 3), facecolor='#FAFAFA')
                    ax2.set_facecolor('#FAFAFA')
                    
                    # Clean horizontal bars with muted charcoal gray
                    bars = ax2.barh(genres, affinities, color='#2C3E50', alpha=0.8, height=0.45)
                    
                    for spine in ['top', 'right', 'left', 'bottom']:
                        ax2.spines[spine].set_visible(False)
                    ax2.xaxis.set_visible(False) # Hide x-axis to prevent clutter
                    ax2.tick_params(axis='y', colors='#555555', labelsize=8)
                    
                    # Add exact affinity value label next to each bar
                    for bar in bars:
                        width = bar.get_width()
                        ax2.text(width + 0.5, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', 
                                 va='center', ha='left', fontsize=8, color='#777777')
                    
                    st.pyplot(fig2)
                
                st.write("---")
                st.write(f"🎯 **Acoustic Comparison Result (Z-Score):** The audio file shows structural affinity to **{similarity_data['closest_cultural_match']}** with a confidence score of **{similarity_data['similarity_confidence_score']}%**.")
                st.caption("🔒 All geometric calculations and distance evaluations are processed locally to protect cultural data privacy.")
                
            except Exception as e:
                st.error(f"Error processing audio file: {str(e)}")
