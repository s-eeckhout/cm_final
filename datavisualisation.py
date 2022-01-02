from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
CONDITIONS = ["Congruent", "Control", "Incongruent"]

### READ AND EXTRACT DATA ###

# Read wordreading results from file and save as array
RTwr_data = []
RTwr_file = open("RTWR.txt", "r")
n_repeat = int(RTwr_file.readline()[2:])
RTwr_data = np.loadtxt(RTwr_file, comments='#')
RTwr = {condition: None for condition in CONDITIONS}

# Read colornaming results from file and save as array
RTcn_data = []
RTcn_file = open("RTCN.txt", "r")
RTcn_data = np.loadtxt(RTcn_file, comments='#')
RTcn = {condition: None for condition in CONDITIONS}

# Close files
RTwr_file.close()
RTcn_file.close()

# Create Numpy array 
for i, condition in enumerate(CONDITIONS):
    RTcn[condition] = np.array([RTcn_data[j+(i*n_repeat)] for j in range(n_repeat)])
    RTwr[condition] = np.array([RTwr_data[j+(i*n_repeat)] for j in range(n_repeat)])

# Compute mean and standard deviations
RTcn_mean = [np.nanmean(RTcn[condition]) for condition in CONDITIONS]
RTwr_mean = [np.nanmean(RTwr[condition]) for condition in CONDITIONS]
RTcn_std = [np.nanstd(RTcn[condition]) for condition in CONDITIONS]
RTwr_std= [np.nanstd(RTwr[condition]) for condition in CONDITIONS]

### CREATE ERRORBAR PLOT ###

xtick_vals = np.arange(1,len(CONDITIONS)+1)
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.errorbar(
    x=xtick_vals, y=RTcn_mean, yerr=RTcn_std,
    label='color naming', linestyle='-', color='green',
)
ax.errorbar(
    x=xtick_vals, y=RTwr_mean, yerr=RTwr_std,
    label='word reading', linestyle='--', color='darkblue',
)
ax.set_xlim(0, 4)
ax.set_ylabel('Reaction time in ms')
ax.set_xticks(xtick_vals)
ax.set_xticklabels(CONDITIONS)
ax.set_xlabel('Condition')
ax.set_title('RT under various conditions')
h,l = fig.gca().get_legend_handles_labels()
fig.legend(h,l,frameon=True)

fig.savefig('stroop.png')

### CREATE K DENSITY PLOT ### 
fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True, sharey=True,)

for i, condition in enumerate(CONDITIONS):
    temp = sns.kdeplot(RTcn[condition][~np.isnan(RTcn[condition])],shade=True,ax=axes[0])
    sns.kdeplot(RTwr[condition][~np.isnan(RTwr[condition])],shade=True,ax=axes[1])
    axes[0].legend(CONDITIONS, frameon=False)
    axes[0].set_title('Color Naming')
    axes[1].set_title('Word Reading')

axes[1].set_xlabel('Reaction time')
sns.despine() # despine plot
fig.savefig('stroopkde.png') # save figure