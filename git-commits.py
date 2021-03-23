#!/usr/bin/env python3

import git, sys, os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

project = sys.argv[1]
repo = git.repo.Repo(project)

data = []

for i in reversed(list(repo.iter_commits())):
    diff = i.stats.total
    data.append([i.committed_datetime.isoformat(), diff['insertions'], diff['deletions']])

data = pd.DataFrame(data, columns=["date","add","remove"])
data['delta'] = data['add'] - data['remove']
data['total'] = data.delta.cumsum()
data.date = pd.to_datetime(data['date'])
data.set_index(['date'],inplace=True)

plt.figure(f"Code Lines Progress in project {os.path.basename(project)}")
plt.ylabel("# of lines")
ax = data['total'].plot()
ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
plt.show()
