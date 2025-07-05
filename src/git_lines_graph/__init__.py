import argparse
import os
import logging

import git
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

logging.getLogger("matplotlib").setLevel(logging.ERROR)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "git_dir",
        type=str,
        nargs="?",
        default=os.getcwd(),
        help="Git directory (default: git root of current directory)",
    )
    parser.add_argument("-b", "--branch", type=str, default=None, help="Branch to browse")

    args = parser.parse_args()

    try:
        repo = git.Repo(args.git_dir, search_parent_directories=True)
    except git.exc.InvalidGitRepositoryError:
        print("Not part of a valid git project: {}".format(args.git_dir))
        exit()

    data = []
    for i in reversed(list(repo.iter_commits(rev=args.branch))):
        diff = i.stats.total
        data.append([i.committed_datetime.isoformat(), diff["insertions"], diff["deletions"]])

    data = pd.DataFrame(data, columns=["date", "add", "remove"])
    data["delta"] = data["add"] - data["remove"]
    data["total"] = data.delta.cumsum()
    data.date = pd.to_datetime(data.date, utc=True)
    data.set_index(["date"], inplace=True)

    with plt.xkcd():
        plt.figure()
        plt.title("Code Lines Progress in project {}".format(os.path.basename(repo.working_tree_dir)), pad=10)
        plt.ylabel("# of lines")
        ax = data["total"].plot()
        ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter("{x:,.0f}"))
        plt.show()
