1. enter repos folder: `cd ./repos`
2. clone semestar repos:
    * 25 Spring: `gh classroom clone student-repos -a 749620`
    * 24 Spring: `gh classroom clone student-repos -a 558214`
    * 23 Spring: `gh classroom clone student-repos -a 403123`
    * ......
3. back to main folder: `cd ..`
4. gather data from local repos (Obtain commit data and line status data): `python .\scripts\gather_data_from_local_repos.py`
5. gather data from remote repos (PR and Merge data):
   * set github token: `$env:GITHUB_TOKEN = "YOUR GITHUB TOKEN"`
   * gather pr data: `python .\scripts\gather_pr_from_remote_repos.py`
   * gather issue data: `python .\scripts\gather_issue_from_remote_repos.py`
6. prepare data to draw charts: `python .\scripts\generate_graph_data.py`