import git
import os
import click
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


@click.command()
@click.argument("git_dir", required=True)
@click.option("-b", "--branch",
              default=None,
              help="branch to browse.")
def run(git_dir, branch):
    repo = git.repo.Repo(git_dir)

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

    plt.figure(f"Code Lines Progress in project {os.path.basename(git_dir)}")
    plt.ylabel("# of lines")
    ax = data['total'].plot()
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    plt.show()


if __name__ == '__main__':
    run()
