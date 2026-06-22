import matplotlib.pyplot as plt
import numpy as np

# Sample frequencies and magnitudes extracted from the MCP server
frequencies = [97.25, 108.46, 97.19, 105.86, 65.67, 105.84, 108.67, 104.83, 105.29, 116.94]
magnitudes = [16479.12, 15964.08, 15241.70, 14717.81, 14554.95, 14284.13, 14117.47, 13927.20, 13899.03, 13888.17]

# Sort data ascending by frequency for a clean stem plot
sorted_indices = np.argsort(frequencies)
frequencies = np.array(frequencies)[sorted_indices]
magnitudes = np.array(magnitudes)[sorted_indices]

# Set up clean canvas (focus on white space and negative space layout)
plt.figure(figsize=(10, 5), facecolor='#FAFAFA')
ax = plt.axes()
ax.set_facecolor('#FAFAFA')

# Draw the vertical lines representing spectral fingerprint (Muted Charcoal Gray)
markerline, stemlines, baseline = plt.stem(
    frequencies, magnitudes, 
    linefmt='#2C3E50', markerfmt='o', basefmt=' '
)

# Customize stem elements
plt.setp(markerline, markersize=6, color='#2C3E50', alpha=0.9)
plt.setp(stemlines, linewidth=1.5, color='#2C3E50', alpha=0.4)

# Remove unnecessary frames to enhance negative space
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)

# Add axes labels and title
plt.xlabel('Frequency (Hz)', fontsize=10, fontweight='bold', color='#555555', labelpad=10)
plt.ylabel('Magnitude (Absolute Energy)', fontsize=10, fontweight='bold', color='#555555', labelpad=10)
plt.title('Sonic Fingerprint: Dominant Heritage Frequencies', fontsize=12, fontweight='bold', color='#222222', pad=20, loc='left')

# Setup light background grid
plt.grid(axis='y', linestyle='--', linewidth=0.5, color='#E0E0E0')
ax.tick_params(axis='both', colors='#777777', labelsize=9)

# Save the plot locally
plt.tight_layout()
plt.savefig('sonic_fingerprint.png', facecolor='#FAFAFA')
print("Successfully generated sonic_fingerprint.png")
