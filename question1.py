import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap


gladys = pd.read_csv('gladys.csv')

def simple_histogram(source, column_name, title, top_n=10):
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

    labels = ['\n'.join(wrap(label, 20)) for label in result['Category'].head(top_n)]
    ax.set_xticklabels(labels, size=8, rotation=90)

    fig.tight_layout()
    fig.savefig(column_name, transparent=True)

simple_histogram(gladys, 'client_group', 'Top 10 client groups')
simple_histogram(gladys, 'project_nature', 'Top 10 project natures')
simple_histogram(gladys, 'member_service', 'Top 10 member services')
