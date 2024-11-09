import matplotlib.pyplot as plt
import numpy as np

# Synthetic demo data
years = np.arange(2019, 2025)
seed_medians = [0.9, 1.0, 1.1, 1.2, 1.2, 1.2]
series_a_medians = [2.1, 2.3, 2.5, 2.7, 2.8, 2.9]
series_b_medians = [3.9, 4.2, 4.4, 4.5, 4.6, 4.7]
series_c_medians = [5.3, 5.7, 5.9, 6.1, 6.3, 6.4]
series_d_medians = [6.1, 6.5, 7.0, 7.4, 7.8, 8.1]

# Synthetic data percentiles for each series
seed_25th = [0.2, 0.3, 0.4, 0.5, 0.5, 0.6]
seed_75th = [2.2, 2.3, 2.3, 2.3, 2.4, 2.5]
series_a_25th = [1.0, 1.1, 1.3, 1.5, 1.6, 1.8]
series_a_75th = [4.0, 4.2, 4.4, 4.4, 4.5, 4.6]
series_b_25th = [2.5, 2.6, 2.7, 2.8, 2.8, 2.9]
series_b_75th = [5.6, 5.7, 5.8, 5.9, 6.0, 6.1]
series_c_25th = [3.9, 4.0, 4.2, 4.5, 4.6, 4.8]
series_c_75th = [8.0, 8.1, 8.2, 8.3, 8.4, 8.5]
series_d_25th = [4.5, 5.0, 5.5, 6.0, 6.2, 6.3]
series_d_75th = [9.0, 9.2, 9.3, 9.4, 9.5, 10.0]

# Plot
plt.figure(figsize=(10, 6))
plt.grid(visible=False)  # Hide grid to match the style

# Colors for each series
colors = ['#A5E6BA', '#6DDF91', '#5CB1D6', '#F5C875', '#F7A96C']
labels = ['Seed', 'Series A', 'Series B', 'Series C', 'Series D']

# Plot the 25th and 75th percentile as shaded regions
plt.fill_between(years, seed_25th, seed_75th, color=colors[0], alpha=0.3)
plt.fill_between(years, series_a_25th, series_a_75th, color=colors[1], alpha=0.3)
plt.fill_between(years, series_b_25th, series_b_75th, color=colors[2], alpha=0.3)
plt.fill_between(years, series_c_25th, series_c_75th, color=colors[3], alpha=0.3)
plt.fill_between(years, series_d_25th, series_d_75th, color=colors[4], alpha=0.3)

# Plot median lines for each funding round
plt.plot(years, seed_medians, label='Seed', color=colors[0], marker='o', linewidth=2)
plt.plot(years, series_a_medians, label='Series A', color=colors[1], marker='o', linewidth=2)
plt.plot(years, series_b_medians, label='Series B', color=colors[2], marker='o', linewidth=2)
plt.plot(years, series_c_medians, label='Series C', color=colors[3], marker='o', linewidth=2)
plt.plot(years, series_d_medians, label='Series D', color=colors[4], marker='o', linewidth=2)

# Annotations for selected data points
plt.text(2024, seed_medians[-1] + 0.1, f"{seed_medians[-1]:.1f}Y", color=colors[0])
plt.text(2024, series_a_medians[-1] + 0.1, f"{series_a_medians[-1]:.1f}Y", color=colors[1])
plt.text(2024, series_b_medians[-1] + 0.1, f"{series_b_medians[-1]:.1f}Y", color=colors[2])
plt.text(2024, series_c_medians[-1] + 0.1, f"{series_c_medians[-1]:.1f}Y", color=colors[3])
plt.text(2024, series_d_medians[-1] + 0.1, f"{series_d_medians[-1]:.1f}Y", color=colors[4])

# Highlight 25th and 75th percentiles
plt.axhline(y=2.3, xmin=0, xmax=0.2, linestyle="--", color="gray", label="75th percentile (Seed)")
plt.axhline(y=2.5, xmin=0.2, xmax=0.4, linestyle="--", color="gray", label="25th percentile (Series B)")

# Set chart title and labels
plt.title("Startups are getting older")
plt.xlabel("Year")
plt.ylabel("Median years from incorporation to primary round by stage")

# Customize tick labels and remove grid lines
plt.xticks(years)
plt.yticks(np.arange(0, 11, 1))
plt.ylim(0, 10)

# Add legend
plt.legend(title="Funding Round", loc="upper left", bbox_to_anchor=(1.05, 1))

# Display the plot
plt.tight_layout()
plt.show()
