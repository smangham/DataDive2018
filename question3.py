import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap
from collections import Counter


gladys = pd.read_csv('gladys_with_cluster_labels.csv')
# foods = pd.read_csv('top-5-foods-from-survey.csv').dropna()
clusters = pd.read_csv('cluster_names.csv')
survey = pd.read_csv('survey.csv')
survey.replace({
    'Never': 0,
    'Less than once  a month': 1,
    '1 - 3 times a month': 2,
    'At least once or twice a week': 6,
    'More than twice a week but not every day': 16,
    'Daily': 28,
}, inplace=True)
survey.fillna(0, inplace=True)
survey['CLUSTER_NUMBER'] = np.nan

# food_types = []
# for column in foods.columns:
#     food_types += list(foods[column])
#
# food_counts = Counter(food_types).most_common(20)
# print(food_counts)

# Find the columns in the survey that relate to food usage
usage_names = []
for column in survey.columns:
    if column.startswith('usage_') and 'filter' not in column:
        usage_names.append(column)

# Create a list of the cluster names
cluster_names = []
for cluster in clusters.itertuples():
    # For each cluster, match the charities in that cluster to the survey responses and assign clusters
    cluster_names.append(cluster.name)
    for charity in gladys[gladys['CLUSTER_NUMBER'] == cluster.id].itertuples():
        survey['CLUSTER_NUMBER'][survey['gladys_id'] == charity.gladys_id] = cluster.id

# Drop all unclustered survey responses
survey.dropna(inplace=True)

# Now create the empty box for the histograms
data = np.zeros((11, len(usage_names)))
for cluster in clusters.itertuples():
    # For each cluster, find all survey responses in that cluster and get the mean usages within them
    for usage_id, usage_name in enumerate(usage_names):
        data[cluster.id, usage_id] = survey[usage_name][survey['CLUSTER_NUMBER'] == cluster.id].mean()

# Calculate the variance of each column
vars = np.zeros(len(usage_names))
for usage_id in range(len(usage_names)):
    vars[usage_id] = np.var(data[:, usage_id])

# Word wrap the labels
labels_cluster = ['\n'.join(wrap(cluster_name, 24)) for cluster_name in cluster_names]
labels_usage = ['\n'.join(wrap(usage_name.replace('usage_', '').capitalize().replace('_', ' '), 24)) for usage_name in usage_names]

# Make a figure
fig, ((axis_var, axis_dummy), (axis, cax)) = plt.subplots(2, 2, figsize=(20, 10), sharex='col', gridspec_kw = {'height_ratios':[1, 4], 'width_ratios':[20, 1]})
img = axis.imshow(data, aspect='auto')
line = axis_var.bar(list(range(len(usage_names))), vars)
axis_dummy.set_axis_off()
axis_var.set_ylabel('Variance')
axis.set_xlim(-0.5, len(labels_usage)-0.5)
axis_var.set_xlim(-0.5, len(labels_usage)-0.5)
axis.xaxis.set_ticks(list(range(len(labels_usage))))
axis.yaxis.set_ticks(list(range(len(labels_cluster))))
axis.set_xticklabels(labels_usage, size=6, rotation=90)
axis.set_yticklabels(labels_cluster, size=6)
cbar = fig.colorbar(img, cax=cax)
cbar.set_label('Mean days/month food category desired')
fig.tight_layout()
fig.subplots_adjust(hspace=0, wspace=0)
fig.savefig('map_cluster_usage', transparent=False)
