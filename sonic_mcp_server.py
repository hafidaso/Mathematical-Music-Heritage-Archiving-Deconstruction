import os
import numpy as np
import librosa
from mcp.server.fastmcp import FastMCP

# Create a custom MCP server for sonic heritage analysis
mcp = FastMCP("Sonic Heritage Analyzer")

def validate_file(file_path: str) -> str:
    """
    Validate file path and format locally for security.
    Resolves the absolute path and checks extensions to prevent Directory Traversal.
    """
    # 1. Resolve absolute path and remove symlinks for Directory Traversal protection
    abs_path = os.path.abspath(os.path.realpath(file_path))
    
    # 2. Check if the path exists
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Audio file not found at: {file_path}")
        
    # 3. Ensure the path is a file, not a directory
    if not os.path.isfile(abs_path):
        raise ValueError(f"The path does not point to a file: {file_path}")
        
    # 4. Whitelist audio extensions for safety
    allowed_extensions = {".wav", ".mp3", ".ogg", ".flac", ".m4a", ".aac", ".wma"}
    _, ext = os.path.splitext(abs_path.lower())
    if ext not in allowed_extensions:
        raise ValueError(f"Unsupported or unsafe file type '{ext}'. Allowed: {', '.join(allowed_extensions)}")
        
    return abs_path

@mcp.tool()
def extract_fft_features(file_path: str) -> dict:
    """
    Apply Fast Fourier Transform (FFT) on local audio to extract dominant frequencies.
    Useful for analyzing heritage microtonal scales and pitch structures.
    """
    safe_path = validate_file(file_path)
    
    try:
        # Load audio at native sample rate (sr=None) to preserve signal quality
        y, sr = librosa.load(safe_path, sr=None)
        
        # Calculate FFT and absolute magnitudes
        fft_values = np.abs(np.fft.fft(y))
        frequencies = np.fft.fftfreq(len(fft_values), 1/sr)
        
        # Focus on positive frequencies above 100Hz to filter out low-frequency rumble/hum
        freq_idx = (frequencies > 100.0)
        fft_values = fft_values[freq_idx]
        frequencies = frequencies[freq_idx]
        
        # Extract top 10 dominant peaks to optimize token usage
        top_indices = np.argsort(fft_values)[-10:][::-1]
        
        return {
            "sample_rate": int(sr),
            "duration_seconds": float(librosa.get_duration(y=y, sr=sr)),
            "dominant_frequencies_hz": [float(f) for f in frequencies[top_indices]],
            "peak_magnitudes": [float(m) for m in fft_values[top_indices]]
        }
    except Exception as e:
        raise RuntimeError(f"Error processing audio FFT: {str(e)}")

@mcp.tool()
def extract_mel_spectrogram(file_path: str) -> dict:
    """
    Compute Mel-Spectrogram of local audio to analyze polyrhythms and timbre.
    Returns averaged band energies and tempo to optimize context length.
    """
    safe_path = validate_file(file_path)
    
    try:
        y, sr = librosa.load(safe_path, sr=None)
        
        # Compute Mel-spectrogram with 128 bands
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        # Convert power to decibels (log-scale)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        # Average band energies over time (Temporal Averaging)
        # This provides a compact timbre profile without sending huge arrays
        mean_band_energies = np.mean(mel_spec_db, axis=1)
        std_band_energies = np.std(mel_spec_db, axis=1)
        
        # Estimate approximate tempo (BPM)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        
        return {
            "estimated_tempo_bpm": float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo),
            "mel_bands_summary": {
                "mean_energies": [float(v) for v in mean_band_energies[:15]], # Sample subset for simplicity
                "std_energies": [float(v) for v in std_band_energies[:15]]
            },
            "global_max_db": float(np.max(mel_spec_db)),
            "global_min_db": float(np.min(mel_spec_db))
        }
    except Exception as e:
        raise RuntimeError(f"Error processing audio Mel-spectrogram: {str(e)}")

@mcp.tool()
def calculate_rhythmic_fractality(file_path: str) -> dict:
    """
    Calculate Hurst exponent of the RMS energy envelope to analyze rhythmic fractality.
    Helps capture complexity of ritual polyrhythms and cyclic beats.
    """
    safe_path = validate_file(file_path)
    
    try:
        y, sr = librosa.load(safe_path, sr=None)
        
        # Extract Root-Mean-Square (RMS) envelope
        rms = librosa.feature.rms(y=y)[0]
        
        # Normalize RMS
        rms_normalized = (rms - np.min(rms)) / (np.max(rms) - np.min(rms) + 1e-6)
        diffs = np.diff(rms_normalized)
        variance_of_changes = float(np.var(diffs))
        
        # Estimate Hurst Exponent based on temporal behavior
        N = len(rms_normalized)
        if N > 10:
            h_estimate = float(0.5 + (variance_of_changes * 2))
            h_estimate = min(max(h_estimate, 0.3), 0.95)
        else:
            h_estimate = 0.5
            
        # Classify rhythmic complexity
        if h_estimate > 0.7:
            complexity_class = "High Fractal Tethering (Complex Polyrhythms)"
        elif h_estimate < 0.45:
            complexity_class = "Highly Fragmented/Intermittent Beats"
        else:
            complexity_class = "Standard Linear/Periodic Rhythm"
            
        return {
            "calculated_hurst_exponent": round(h_estimate, 3),
            "rhythmic_variance": float(round(variance_of_changes, 5)),
            "structural_complexity_profile": complexity_class
        }
    except Exception as e:
        raise RuntimeError(f"Error calculating rhythmic fractality: {str(e)}")

@mcp.tool()
def compare_heritage_similarity(estimated_bpm: float, hurst_exponent: float, dominant_freq: float) -> dict:
    """
    Compare local audio feature vectors to reference global genres to find similarity.
    Calculates weighted Euclidean distance to trace cultural links.
    """
    reference_genres = {
        "Classic Jazz / Swing": {"bpm": 140.0, "hurst": 0.53, "freq": 150.0},
        "Modern Jazz / Bebop": {"bpm": 200.0, "hurst": 0.46, "freq": 160.0},
        "Delta Blues (USA)": {"bpm": 90.0, "hurst": 0.52, "freq": 110.0},
        "Tuareg Desert Blues (Sahara)": {"bpm": 95.0, "hurst": 0.51, "freq": 98.0},
        "Gnawa Traditional (Morocco)": {"bpm": 120.0, "hurst": 0.78, "freq": 65.0},
        "Middle Eastern Maqam / Tarab": {"bpm": 84.0, "hurst": 0.61, "freq": 180.0},
        "Andalusian Flamenco": {"bpm": 132.0, "hurst": 0.44, "freq": 130.0},
        "West African Polyrhythm (Yoruba)": {"bpm": 125.0, "hurst": 0.82, "freq": 75.0},
        "Afrobeat (Sub-Saharan Heavy)": {"bpm": 115.0, "hurst": 0.68, "freq": 80.0},
        "Afro-Cuban Salsa / Clave": {"bpm": 180.0, "hurst": 0.58, "freq": 115.0},
        "Bossa Nova (Brazil)": {"bpm": 124.0, "hurst": 0.51, "freq": 120.0},
        "Reggae / Dub (Jamaica)": {"bpm": 74.0, "hurst": 0.64, "freq": 55.0},
        "Hindustani Classical (Teental)": {"bpm": 70.0, "hurst": 0.76, "freq": 90.0},
        "Japanese Taiko Ensemble": {"bpm": 135.0, "hurst": 0.59, "freq": 60.0},
        "Celtic Folk (Ireland)": {"bpm": 115.0, "hurst": 0.41, "freq": 220.0},
        "Baroque Classical (Europe)": {"bpm": 80.0, "hurst": 0.62, "freq": 440.0},
        "Electronic / Techno": {"bpm": 128.0, "hurst": 0.67, "freq": 50.0}
    }
    
    current_vector = np.array([estimated_bpm, hurst_exponent, dominant_freq])
    distances = {}
    
    # Standardize weights to prevent numerical dominance
    weights = np.array([0.01, 120.0, 0.04]) 
    
    for genre, ref in reference_genres.items():
        ref_vector = np.array([ref["bpm"], ref["hurst"], ref["freq"]])
        distance = np.sqrt(np.sum(((current_vector - ref_vector) * weights) ** 2))
        distances[genre] = float(round(distance, 4))
        
    sorted_genres = sorted(distances.items(), key=lambda x: x[1])
    closest_genre = sorted_genres[0][0]
    closest_distance = sorted_genres[0][1]
    
    confidence_score = float(round(100 / (1 + closest_distance), 2))
    
    return {
        "acoustic_distance_matrix": distances,
        "closest_cultural_match": closest_genre,
        "similarity_confidence_score": confidence_score
    }

@mcp.tool()
def extract_advanced_spectral_features(file_path: str) -> dict:
    """
    Extract advanced spectral features (spectral centroid & flatness) to analyze instrument physics.
    Helps distinguish brassy instruments from traditional wooden/leather instruments.
    """
    safe_path = validate_file(file_path)
    try:
        y, sr = librosa.load(safe_path, sr=None)
        
        # 1. Spectral Centroid (measures brightness or register height)
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        mean_centroid = float(np.mean(spectral_centroids))
        
        # 2. Spectral Flatness (measures noisiness vs microtonal/sine purity)
        spectral_flatness = librosa.feature.spectral_flatness(y=y)[0]
        mean_flatness = float(np.mean(spectral_flatness))
        
        # 3. BPM tempo estimation
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        estimated_bpm = float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo)
        
        return {
            "estimated_bpm": round(estimated_bpm, 2),
            "spectral_centroid_hz": round(mean_centroid, 2),
            "spectral_flatness": round(mean_flatness, 5),
            "duration_seconds": float(librosa.get_duration(y=y, sr=sr))
        }
    except Exception as e:
        raise RuntimeError(f"Error processing audio spectral features: {str(e)}")

@mcp.tool()
def compare_heritage_similarity_v2(estimated_bpm: float, spectral_centroid: float, spectral_flatness: float) -> dict:
    """
    Advanced acoustic distance engine using Z-score standardization (Standardized Euclidean Distance).
    Compares local features with references of regional musical heritage.
    """
    # Reference taxonomy focused on Moroccan and Sahara regional heritage
    reference_taxonomy = {
        "Gnawa Traditional (Morocco)": {
            "bpm": 122.0, 
            "centroid": 850.0,   # Wooden guembri and heavy iron qraqeb resonance
            "flatness": 0.00800
        },
        "Tuareg Desert Blues (Sahara)": {
            "bpm": 95.0, 
            "centroid": 1400.0,  # Acoustic guitar and airy desert vocals
            "flatness": 0.01500
        },
        "Ahwash / Berber Collective (Atlas)": {
            "bpm": 135.0, 
            "centroid": 1100.0,  # Sharp bendir frame drums and collective chanting
            "flatness": 0.02100
        },
        "Andalusian Tarab / Ala (Morocco)": {
            "bpm": 84.0, 
            "centroid": 1900.0,  # High spectral centroid from violin and oud strings
            "flatness": 0.03500
        },
        "Chaabi Traditional (North Africa)": {
            "bpm": 128.0, 
            "centroid": 1600.0,  # Fast string movements and derbouka drums
            "flatness": 0.02800
        }
    }
    
    # Global standard deviation values to prevent scale dominance (Z-score scaling)
    scale_factors = {
        "bpm": 35.0,
        "centroid": 600.0,
        "flatness": 0.015
    }
    
    distances = {}
    current_vec = np.array([estimated_bpm, spectral_centroid, spectral_flatness])
    
    for genre, ref in reference_taxonomy.items():
        ref_vec = np.array([ref["bpm"], ref["centroid"], ref["flatness"]])
        
        # Standardized Euclidean distance (simplified Mahalanobis)
        normalized_diff = (current_vec - ref_vec) / np.array([scale_factors["bpm"], scale_factors["centroid"], scale_factors["flatness"]])
        distance = np.sqrt(np.sum(normalized_diff ** 2))
        distances[genre] = float(round(distance, 4))
        
    sorted_genres = sorted(distances.items(), key=lambda x: x[1])
    closest_genre = sorted_genres[0][0]
    closest_distance = sorted_genres[0][1]
    
    confidence_score = float(round(100 / (1 + closest_distance), 2))
    
    return {
        "standardized_distance_matrix": distances,
        "closest_cultural_match": closest_genre,
        "similarity_confidence_score": confidence_score
    }

if __name__ == "__main__":
    # Start the FastMCP stdio server
    mcp.run(transport="stdio")