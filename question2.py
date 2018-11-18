import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap
import more_itertools

# ======================================
# SETTINGS
# ======================================
top_n = 10  # We select the top N categories

text_size = 7  # The text size
transparent = False  # Do the plots have transparent backgrounds?
wrap_length = 24  # How long a line of text should be
v_threshold = 0.05  # Cramer's V threshold for 'strong correlation'
# ======================================


def create_top_n_list(source, column_name):
    """
    Returns the top N in a category
    """
    categories = set(source[column_name])
    category_counts = []

    for category in categories:
        category_counts.append(len(source[source[column_name] == category]))

    result = pd.DataFrame(list(zip(categories, category_counts)),
                          columns=['Category', 'Count']).sort_values('Count', ascending=False)
    return list(result['Category'].head(top_n))


def create_2d_plot(source, data, column_x, column_y, categories_x, categories_y, title, filename):
    """
    Creates a 2d plot for a given pair lists- both count, relative occurance, and builds clusters based on them.
    """
    # Create word-wrapped labels
    labels_x = ['\n'.join(wrap(category, wrap_length)) for category in categories_x]
    labels_y = ['\n'.join(wrap(category, wrap_length)) for category in categories_y]

    fig, axis = plt.subplots()
    img = axis.imshow(data.T)
    axis.xaxis.set_ticks(list(range(top_n)))
    axis.yaxis.set_ticks(list(range(top_n)))
    axis.set_title(title)
    axis.set_xticklabels(labels_x, size=text_size, rotation=90)
    axis.set_yticklabels(labels_y, size=text_size)
    cbar = fig.colorbar(img)
    cbar.set_label('Count')
    fig.tight_layout()
    fig.savefig('map_'+filename, transparent=transparent)

    # Generate Chi2
    total = len(source)
    analysis = np.zeros(data.shape)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            predicted = (np.sum(data[i, :]) * np.sum(data[:, j])) / total
            actual = data[i, j]
            analysis[i, j] = np.power(actual - predicted, 2) / predicted

    # Divide by number of measurements
    analysis /= total
    # Convert to Cramer's V
    analysis = np.sqrt(analysis / (top_n-1))

    # We want to find the strongest correlations and assume these are a 'cluster'
    print('Strongest correlations for: ' + title)
    cluster_number = 0
    source[filename+'_id'] = np.zeros(len(source))
    source[filename+'_id'] = np.nan

    f = open('cluster_id_'+filename+'.csv', 'w')
    f.write('cramers_v, cluster, '+filename+'_id\n')
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if analysis[i, j] >= v_threshold:
                # If we've found one of the high significance associations, call it a cluster
                print('{:.2f} - {} && {}'.format(analysis[i, j], categories_x[i], categories_y[j]))
                # And save all entries in the dataframe
                f.write('{:.2f}, "{} && {}", {}\n'.format(analysis[i, j], categories_x[i], categories_y[j], cluster_number))
                source[filename+'_id'][(source[column_x] == categories_x[i]) & (source[column_y] == categories_y[j])] = cluster_number
                cluster_number += 1
    print('')
    f.close()

    # Now we plot the 2-d histogram of the Cramer's V
    fig, axis = plt.subplots()
    img = axis.imshow(analysis.T, cmap='plasma', vmin=0)
    axis.xaxis.set_ticks(list(range(top_n)))
    axis.yaxis.set_ticks(list(range(top_n)))
    axis.set_title(title)
    axis.set_xticklabels(labels_x, size=text_size, rotation=90)
    axis.set_yticklabels(labels_y, size=text_size)
    cbar = fig.colorbar(img)
    cbar.set_label("Cramer's V")
    fig.tight_layout()
    fig.savefig('map_'+filename+'_cramer', transparent=transparent)

# READ IN DATA FILE
gladys = pd.read_csv('gladys.csv')

clients = create_top_n_list(gladys, 'client_group')
natures = create_top_n_list(gladys, 'project_nature')
services = create_top_n_list(gladys, 'member_service')

c_n = np.zeros((top_n, top_n))
c_s = np.zeros((top_n, top_n))
n_s = np.zeros((top_n, top_n))
cns = np.zeros((top_n, top_n, top_n))

# Build up 3 2d histograms of 
for row in gladys.itertuples():
    index_c = -1
    index_s = -1
    index_n = -1
    c = row.client_group
    n = row.project_nature
    s = row.member_service
    if c in clients:
        index_c = clients.index(c)
    if s in services:
        index_s = services.index(s)
    if n in natures:
        index_n = natures.index(n)

    if index_n >= 0 and index_s >= 0:
        n_s[index_n, index_s] += 1
    if index_c >= 0 and index_s >= 0:
        c_s[index_c, index_s] += 1
    if index_n >= 0 and index_s >= 0:
        c_n[index_c, index_n] += 1
    if index_c >= 0 and index_n >= 0 and index_s >= 0:
        cns[index_c, index_n, index_s] += 1

# Create the plots and generate the clusters for each pairing
create_2d_plot(gladys, c_n, 'client_group', 'project_nature', clients, natures, 'Client group vs project nature', 'cn')
create_2d_plot(gladys, c_s, 'client_group', 'member_service', clients, services, 'Client group vs member service', 'cs')
create_2d_plot(gladys, n_s, 'project_nature', 'member_service', natures, services, 'Project nature vs member service', 'ns')
gladys.to_csv('gladys_cluster.csv', na_rep='nan')
