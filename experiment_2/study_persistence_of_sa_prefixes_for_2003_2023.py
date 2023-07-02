import itertools
import statsmodels.api as sm
import os
import json
import numpy as np
import matplotlib.pyplot as plt

# Define the years range
years = range(2003, 2024)

####################################################################
# Initialize lists to store the data
data = []
for year in years:
    folder_name = 'prevalence/' + str(year) + '/'
    year_data = []
    for file_name in os.listdir(folder_name):
        if file_name.startswith("intersection") and file_name.endswith("sa_origin_announcements_from_the_provider_pov.json"):
            with open(os.path.join(folder_name, file_name)) as f:
                file_data = json.load(f)
            year_data.extend(list(file_data.values()))
    data.append(year_data)


# Create the boxplot and save it as a .png file
plt.figure()
FONT_SIZE = 13
plt.rcParams.update({'font.size': FONT_SIZE})
plt.boxplot(data)
plt.xticks(np.arange(len(years))+1, years, rotation=90)
plt.ylabel("SA origin ratio")
plt.title("SA origins persistence for intersection of providers")
plt.ylim(-0.005, 1)
plt.tight_layout()
plt.grid()
plt.savefig("persistence/per_year/all_sa_origins_provider_pov_boxplot.png")


####################################################################
####################################################################
# Initialize lists to store the data
data = []
for year in years:
    folder_name = 'prevalence/' + str(year) + '/'
    year_data = []
    for file_name in os.listdir(folder_name):
        if file_name.startswith("union_of_customers_for_all") and file_name.endswith("customer_pov.json"):
            with open(os.path.join(folder_name, file_name)) as f:
                file_data = json.load(f)
            year_data.extend(list(file_data.values()))
    data.append(year_data)

# Create subplots for each year
fig, axs = plt.subplots(nrows=5, ncols=4, figsize=(
    16, 12), sharex=True, sharey=True)
for i in range(20):
    row = i // 4
    col = i % 4
    ecdf = sm.distributions.ECDF(data[i])
    axs[row, col].step(ecdf.x, ecdf.y, where='post', color='black')
    axs[row, col].set_xlabel("SA prefixes ratio")
    axs[row, col].set_ylabel("CDF of SA origins")
    axs[row, col].set_title(str(years[i]))
    axs[row, col].set_xlim(-0.05, 1.05)
    axs[row, col].set_ylim(-0.05, 1.05)
    axs[row, col].grid()

# Adjust spacing between subplots
fig.tight_layout()
plt.savefig("persistence/per_year/union_sa_prefixes_customer_pov_ecdf_per_year.png")

# Create the ECDF for data[20]
fig, ax = plt.subplots()
ecdf = sm.distributions.ECDF(data[20])
# Now plot the 2023 separately
# Plot the ECDF
ax.step(ecdf.x, ecdf.y, where='post', color='black')
ax.set_xlabel("SA prefixes ratio")
ax.set_ylabel("CDF of SA origins")
ax.set_title(str(years[20]))
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.05)
ax.grid()
plt.rcParams.update({'font.size': FONT_SIZE})

# Save the plot
plt.savefig("persistence/per_year/union_sa_prefixes_customer_pov_ecdf_2023.png")
########################################################################
# Initialize lists to store the data
data = []
for year in years:
    folder_name = 'prevalence/' + str(year) + '/'
    year_data = []
    for file_name in os.listdir(folder_name):
        if file_name.startswith("intersection") and file_name.endswith("sa_prefix_announcements_from_the_provider_pov.json"):
            with open(os.path.join(folder_name, file_name)) as f:
                file_data = json.load(f)
            sorted_values = [value for _, value in sorted(file_data.items())]
            year_data.extend(sorted_values)
    data.append(year_data)


# Create the boxplot and save it as a .png file
plt.figure()
FONT_SIZE = 13
plt.rcParams.update({'font.size': FONT_SIZE})
plt.boxplot(data)
plt.xticks(np.arange(len(years))+1, years, rotation=90)
plt.ylabel("SA prefix ratio")
plt.title("SA prefixes persistence for intersection of providers")
plt.ylim(-0.005, 1)
plt.tight_layout()
plt.grid()
plt.savefig("persistence/per_year/all_sa_prefixes_provider_pov_boxplot.png")

plt.figure()
FONT_SIZE = 13
plt.rcParams.update({'font.size': FONT_SIZE})
# cycle through the marker styles
colors = itertools.cycle([(0.0, 0.0, 0.0), (0.2, 0.2, 0.2),
                         (0.4, 0.4, 0.4), (0.5, 0.5, 0.5), (0.7, 0.7, 0.7)])

markers = itertools.cycle(['o', 's', '^', 'd', 'p'])
data_t = list(zip(*data))  # transpose the data list
for i in range(len(data_t)):
    plt.plot(data_t[i], marker=next(markers), color = next(colors))
plt.xticks(np.arange(len(years)), years, rotation=90)
plt.ylabel("SA prefix ratio")
plt.title("SA prefixes persistence for intersection of providers")
plt.ylim(-0.005, 1)
plt.tight_layout()
plt.legend(['AS3257', 'AS3292', 'AS3549', 'AS5511', 'AS7018'],
           loc='upper left', fontsize='small')
plt.grid()
plt.savefig("persistence/per_year/all_sa_prefixes_provider_pov_lineplot.png")

plt.figure()
FONT_SIZE = 13
plt.rcParams.update({'font.size': FONT_SIZE})

# Define the x-axis labels and their positions
x_labels = years
x_positions = np.arange(len(x_labels))

# Define the data for each provider
data_by_provider = list(zip(*data))  # transpose the data list
providers = ['AS3257', 'AS3292', 'AS3549', 'AS5511', 'AS7018']

# Cycle through the colors
colors = itertools.cycle([(0.0, 0.0, 0.0), (0.3, 0.3, 0.3),
                         (0.5, 0.5, 0.5), (0.8, 0.8, 0.8), (1, 1, 1)])

group_width = 0.8
bar_width = group_width / len(providers)
# Create the bar chart for each provider
for i, provider_data in enumerate(data_by_provider):
    plt.bar(x_positions - group_width/2 + i * bar_width, provider_data, width=bar_width,
            color=next(colors), edgecolor='black', label=providers[i])

# Set the axis labels, title, and legend
plt.xticks(x_positions, x_labels, rotation=90)
plt.ylabel("SA prefix ratio")
plt.title("SA prefixes persistence for intersection of providers")
plt.ylim(-0.005, 1)
plt.tight_layout()
plt.legend(loc='upper left', fontsize='small')
plt.grid()
plt.gca().xaxis.grid(False)

# Save the plot to a file
plt.savefig("persistence/per_year/all_sa_prefixes_provider_pov_barplot.png")
# ####################################################################
