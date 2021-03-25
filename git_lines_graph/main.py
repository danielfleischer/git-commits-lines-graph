import git
import os
import sys
import click
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


@click.command()
@click.argument("git_dir", required=True)
@click.option("-b", "--branch",
              default=None,
              help="branch to browse.")
def main(git_dir, branch):
    try:
        repo = git.repo.Repo(git_dir)
    except:
        print("Exception of type: {}\nDir. not a valid git project: {}".
              format(sys.exc_info()[0], git_dir))
        exit()

    data = []
    for i in reversed(list(repo.iter_commits(rev=branch))):
        diff = i.stats.total
        data.append([i.committed_datetime.isoformat(),
                     diff['insertions'],
                     diff['deletions']])

    data = pd.DataFrame(data, columns=["date", "add", "remove"])
    data['delta'] = data['add'] - data['remove']
    data['total'] = data.delta.cumsum()
    data.date = pd.to_datetime(data.date)
    data.set_index(['date'], inplace=True)

    plt.figure("Code Lines Progress in project {}".
               format(os.path.basename(git_dir)))
    plt.ylabel("# of lines")
    ax = data['total'].plot()
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    plt.show()
