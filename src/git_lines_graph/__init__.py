import argparse
import os

import git
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("git_dir", type=str, help="Git directory")
    parser.add_argument("-b", "--branch", type=str, default=None, help="Branch to browse")

    args = parser.parse_args()
    git_dir = args.git_dir
    branch = args.branch

    try:
        repo = git.repo.Repo(git_dir)
    except git.exc.InvalidGitRepositoryError as e:
        print("Not a valid git project: {}".format(git_dir))
        exit()

    data = []
    for i in reversed(list(repo.iter_commits(rev=branch))):
        diff = i.stats.total
        data.append([i.committed_datetime.isoformat(), diff["insertions"], diff["deletions"]])

    data = pd.DataFrame(data, columns=["date", "add", "remove"])
    data["delta"] = data["add"] - data["remove"]
    data["total"] = data.delta.cumsum()
    data.date = pd.to_datetime(data.date)
    data.set_index(["date"], inplace=True)

    with plt.xkcd():
        plt.figure("Code Lines Progress in project {}".format(os.path.basename(git_dir)))
        plt.ylabel("# of lines")
        ax = data["total"].plot()
        ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter("{x:,.0f}"))
        plt.show()
