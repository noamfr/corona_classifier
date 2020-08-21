import os
from matplotlib import pyplot as plt
import seaborn as sns


def bar_chart(x, y, x_label: str, y_label: str, title: str, output_path: str):
    plt.clf()
    sns.set(style='darkgrid')
    sns.barplot(x=x, y=y, color='salmon')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.ylim(0, 1)
    plt.title(title)
    plt.xticks(rotation=45, ha='right', fontsize=6, weight='bold')
    plt.tight_layout()
    # plt.figure(figsize=(5, 5))
    plt.savefig(fname=os.path.join(output_path, f'{title}.png'), dpi=300)
