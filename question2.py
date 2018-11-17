import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap


def create_top_n_list(source, column_name, top_n=10):
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


def create_2d_plot(data, labels_x, labels_y, title, filename, total, top_n=10, text_size=7, transparent=False, wrap_length=24):
    fig, ax = plt.subplots()
    img = ax.imshow(data.T)
    ax.xaxis.set_ticks(list(range(top_n)))
    ax.yaxis.set_ticks(list(range(top_n)))
    ax.set_title(title)
    ax.set_xticklabels(labels_x, size=text_size, rotation=90)
    ax.set_yticklabels(labels_y, size=text_size)
    cbar = fig.colorbar(img)
    cbar.set_label('Count')
    fig.tight_layout()
    fig.savefig(filename, transparent=transparent)

    # Generate Chi2
    analysis = np.zeros(data.shape)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            predicted = (np.sum(data[i, :]) * np.sum(data[:, j])) / total
            actual = data[i, j]
            analysis[i, j] = np.power(actual - predicted, 2) / predicted

    # Divide by number of measurements
    analysis /= (top_n * top_n)
    # Convert to Cramer's V
    analysis = np.sqrt(analysis / (top_n-1))

    fig, ax = plt.subplots()
    img = ax.imshow(analysis.T, cmap='plasma', vmin=0, vmax=1)
    ax.xaxis.set_ticks(list(range(top_n)))
    ax.yaxis.set_ticks(list(range(top_n)))
    ax.set_title(title)
    ax.set_xticklabels(labels_x, size=text_size, rotation=90)
    ax.set_yticklabels(labels_y, size=text_size)
    cbar = fig.colorbar(img)
    cbar.set_label("Cramer's V")
    fig.tight_layout()
    fig.savefig(filename+'_cramer', transparent=transparent)

# SETTINGS
top_n = 10  # We select the top N categories

text_size = 7  # The text size
transparent = False  # Do the plots have transparent backgrounds?
wrap_length = 24  # How long a line of text should be

# READ IN DATA FILE
gladys = pd.read_csv('gladys.csv')

clients = create_top_n_list(gladys, 'client_group', top_n)
natures = create_top_n_list(gladys, 'project_nature', top_n)
services = create_top_n_list(gladys, 'member_service', top_n)

c_n = np.zeros((top_n, top_n))
c_s = np.zeros((top_n, top_n))
n_s = np.zeros((top_n, top_n))

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


labels_c = ['\n'.join(wrap(client, wrap_length)) for client in clients]
labels_n = ['\n'.join(wrap(nature, wrap_length)) for nature in natures]
labels_s = ['\n'.join(wrap(service, wrap_length)) for service in services]

create_2d_plot(c_n, labels_c, labels_n, 'Client group vs project nature', 'map_cn', total=len(gladys), top_n=top_n, text_size=text_size, transparent=transparent, wrap_length=wrap_length)
create_2d_plot(c_s, labels_c, labels_s, 'Client group vs member service', 'map_cs', total=len(gladys), top_n=top_n, text_size=text_size, transparent=transparent, wrap_length=wrap_length)
create_2d_plot(n_s, labels_n, labels_s, 'Project nature vs member service', 'map_ns', total=len(gladys), top_n=top_n, text_size=text_size, transparent=transparent, wrap_length=wrap_length)
