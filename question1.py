import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap


# ======================================
# SETTINGS
# ======================================
top_n = 10
text_size = 8
wrap_length = 20
# ======================================

gladys = pd.read_csv('gladys.csv')

def simple_histogram(source, column_name, title, top_n=10, text_size=8, wrap_length=20):
    """
    Creates simple histogram
    """
    categories = set(source[column_name])
    category_counts = []

    for category in categories:
        category_counts.append(len(source[source[column_name] == category]))

    result = pd.DataFrame(list(zip(categories, category_counts)),
        columns=['Category', 'Count']).sort_values('Count', ascending=False)

    fig, ax = plt.subplots(1, 1)
    rects1 = ax.bar(result['Category'].head(top_n), result['Count'].head(top_n))

    ax.set_ylabel('Count')
    ax.set_title(title)

    labels = ['\n'.join(wrap(label, wrap_length)) for label in result['Category'].head(top_n)]
    ax.set_xticklabels(labels, size=text_size, rotation=90)

    fig.tight_layout()
    fig.savefig(column_name, transparent=True)

    fig, ax = plt.subplots(1, 1)
    rects1 = ax.bar(result['Category'].head(top_n), result['Count'].head(top_n)*100/len(source))

    ax.set_ylabel('Percentage')
    ax.set_title(title)

    labels = ['\n'.join(wrap(label, 20)) for label in result['Category'].head(top_n)]
    ax.set_xticklabels(labels, size=8, rotation=90)

    fig.tight_layout()
    fig.savefig(column_name+'_perc', transparent=True)

simple_histogram(gladys, 'client_group', 'Top 10 client groups', top_n, text_size=text_size, wrap_length=wrap_length)
simple_histogram(gladys, 'project_nature', 'Top 10 project natures', top_n, text_size=text_size, wrap_length=wrap_length)
simple_histogram(gladys, 'member_service', 'Top 10 member services', top_n, text_size=text_size, wrap_length=wrap_length)
