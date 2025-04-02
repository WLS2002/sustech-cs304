import os
import json
import jsonpath
from datetime import datetime, timedelta
import pytz
from collections import Counter

china_tz = pytz.timezone("Asia/Shanghai")


def commit_time_distribution_date(semester, semester_file):
    data = json.load(open(semester_file, "r", encoding="utf-8"))
    all_commits = []
    [all_commits.extend(repo["commits"]) for repo in data]

    date_list = []
    for commit in all_commits:
        dt = datetime.fromisoformat(commit["committed_datetime"])
        dt_china = dt.astimezone(china_tz)
        date_str = dt_china.date().isoformat()
        date_list.append(date_str)
    
    commit_counter = Counter(date_list)

    if not date_list:
        return [], []
    start_date = datetime.fromisoformat(min(date_list))
    end_date = datetime.fromisoformat(max(date_list))

    full_dates = []
    counts = []
    current = start_date
    while current <= end_date:
        date_str = current.date().isoformat()
        full_dates.append(date_str)
        counts.append(commit_counter.get(date_str, 0))
        current += timedelta(days=1)

    final_res = {
        "full_dates": full_dates,
        "counts": counts
    }

    os.makedirs(f"./output/{semester}", exist_ok=True)
    with open(f"./output/{semester}/commit_time_distribution_date.json", "w", encoding="utf-8") as f:
        json.dump(final_res, f, indent=2, ensure_ascii=False)


def commit_time_distribution_hourly(semester, semester_file):
    with open(semester_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    all_commits = []
    [all_commits.extend(repo["commits"]) for repo in data]

    hour_list = []
    for commit in all_commits:
        dt = datetime.fromisoformat(commit["committed_datetime"])
        dt_china = dt.astimezone(china_tz)
        hour = dt_china.hour
        hour_list.append(hour)

    commit_counter = Counter(hour_list)

    # 构建完整的 0~23 小时范围
    full_hours = list(range(24))
    counts = [commit_counter.get(h, 0) for h in full_hours]

    final_res = {
        "hours": full_hours,
        "counts": counts
    }

    os.makedirs(f"./output/{semester}", exist_ok=True)
    with open(f"./output/{semester}/commit_time_distribution_hourly.json", "w", encoding="utf-8") as f:
        json.dump(final_res, f, indent=2, ensure_ascii=False)



def commit_count_per_repo(semester, semester_file):
    data = json.load(open(semester_file, "r", encoding="utf-8"))

    repo_names = []
    commit_counts = []

    for repo in data:
        repo_name = repo["repo_name"]
        commit_num = len(repo["commits"])

        repo_names.append(repo_name)
        commit_counts.append(commit_num)

    # 计算平均 commit 数量（保留 2 位小数）
    avg_commit_count = round(sum(commit_counts) / len(commit_counts), 2) if commit_counts else 0

    result = {
        "repo_names": repo_names,
        "commit_counts": commit_counts,
        "average_commit_count": avg_commit_count
    }

    os.makedirs(f"./output/{semester}", exist_ok=True)
    with open(f"./output/{semester}/commit_count_per_repo.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


def repo_active_contributor_distribution(semester, semester_file):
    with open(semester_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    repo_active_counts = []
    active_count_bucket = Counter()

    for repo in data:
        repo_name = repo.get("repo_name")
        commits = repo.get("commits", [])
        contributors = set(commit["author_email"] for commit in commits)
        active_count = len(contributors)

        repo_active_counts.append({
            "repo_name": repo_name,
            "active_contributor_count": active_count
        })

        active_count_bucket[active_count] += 1

    # 准备饼图数据
    pie_chart_data = {
        str(k): v for k, v in sorted(active_count_bucket.items())
    }

    # 保存结果
    output_dir = f"./output/{semester}"
    os.makedirs(output_dir, exist_ok=True)

    with open(f"{output_dir}/repo_active_contributor_count.json", "w", encoding="utf-8") as f:
        json.dump(repo_active_counts, f, indent=2, ensure_ascii=False)

    with open(f"{output_dir}/active_contributor_pie_chart.json", "w", encoding="utf-8") as f:
        json.dump(pie_chart_data, f, indent=2, ensure_ascii=False)

    return repo_active_counts, pie_chart_data

def repo_code_line_distribution(semester, semester_file):
    with open(semester_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    repo_names = []
    code_line_counts = []

    for repo in data:
        repo_name = repo["repo_name"]
        total_lines = repo.get("code_line_data", {}).get("total_lines", 0)

        repo_names.append(repo_name)
        code_line_counts.append(total_lines)

    if not code_line_counts:
        average_lines = 0
    else:
        average_lines = sum(code_line_counts) / len(code_line_counts)

    result = {
        "repo_names": repo_names,
        "total_lines": code_line_counts,
        "average_lines": average_lines
    }

    os.makedirs(f"./output/{semester}", exist_ok=True)
    with open(f"./output/{semester}/code_line_per_repo.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return repo_names, code_line_counts, average_lines

def gather_language_distribution(semester, semester_file):
    with open(semester_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    language_counter = Counter()

    for repo in data:
        code_data = repo.get("code_line_data", {})
        lang_data = code_data.get("lines_by_language", {})
        for lang, count in lang_data.items():
            language_counter[lang] += count

    # 排序：行数最多的语言在前
    sorted_lang = sorted(language_counter.items(), key=lambda x: x[1], reverse=True)
    languages = [lang for lang, _ in sorted_lang]
    counts = [count for _, count in sorted_lang]

    final_res = {
        "languages": languages,
        "counts": counts
    }

    os.makedirs(f"./output/{semester}", exist_ok=True)
    with open(f"./output/{semester}/language_distribution.json", "w", encoding="utf-8") as f:
        json.dump(final_res, f, indent=2, ensure_ascii=False)

    return languages, counts

def pr_count_per_repo(semester, semester_file):
    with open(semester_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    pr_counts = {}
    for repo in data:
        repo_name = repo["repo_name"]
        pr_file_path = f"./tmp/pr/{repo_name}.json"
        if not os.path.exists(pr_file_path):
            print(f"PR file for {repo_name} not found, skipping.")
            continue

        pr_list = json.load(open(pr_file_path, "r", encoding="utf-8"))
        pr_counts[repo_name] = len(pr_list)

    # 构造图表所需数据
    repo_names = sorted(pr_counts.keys())
    pr_values = [pr_counts[name] for name in repo_names]

    # 计算平均 PR 数
    avg_pr = sum(pr_values) / len(pr_values) if pr_values else 0

    result = {
        "repo_names": repo_names,
        "pr_counts": pr_values,
        "average_pr": avg_pr
    }

    # 保存结果为 json 文件
    os.makedirs(f"./output/{semester}", exist_ok=True)
    output_path = f"./output/{semester}/pr_count_per_repo.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


def pr_status_distribution(semester, semester_file):
    with open(semester_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 初始化统计计数
    status_counter = {
        "merged": 0,
        "closed": 0,
        "open": 0
    }

    for repo in data:
        repo_name = repo["repo_name"]
        pr_file_path = f"./tmp/pr/{repo_name}.json"
        if not os.path.exists(pr_file_path):
            print(f"PR file for {repo_name} not found, skipping.")
            continue

        pr_list = json.load(open(pr_file_path, "r", encoding="utf-8"))
        for pr in pr_list:
            if pr.get("mergedAt"):
                status_counter["merged"] += 1
            elif pr.get("closedAt"):
                status_counter["closed"] += 1
            else:
                status_counter["open"] += 1

    # 保存结果为 json 文件
    os.makedirs(f"./output/{semester}", exist_ok=True)
    output_path = f"./output/{semester}/pr_status_distribution.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(status_counter, f, indent=2, ensure_ascii=False)


def issue_count_per_repo(semester, semester_file):
    with open(semester_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    issue_counts = {}
    for repo in data:
        repo_name = repo["repo_name"]
        issue_file_path = f"./tmp/issues/{repo_name}.json"
        if not os.path.exists(issue_file_path):
            print(f"Issue file for {repo_name} not found, skipping.")
            continue

        issue_list = json.load(open(issue_file_path, "r", encoding="utf-8"))
        issue_counts[repo_name] = len(issue_list)

    # 构造图表所需数据
    repo_names = sorted(issue_counts.keys())
    issue_values = [issue_counts[name] for name in repo_names]

    # 计算平均 ISSUE 数
    avg_issue = sum(issue_values) / len(issue_values) if issue_values else 0

    result = {
        "repo_names": repo_names,
        "issue_counts": issue_values,
        "average_issues": avg_issue
    }

    # 保存结果为 json 文件
    os.makedirs(f"./output/{semester}", exist_ok=True)
    output_path = f"./output/{semester}/issue_count_per_repo.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

def issue_status_distribution(semester, semester_file):
    with open(semester_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    status_counter = {
        "open": 0,
        "closed": 0
    }

    for repo in data:
        repo_name = repo["repo_name"]
        issue_file_path = f"./tmp/issues/{repo_name}.json"
        if not os.path.exists(issue_file_path):
            print(f"Issue file for {repo_name} not found, skipping.")
            continue

        issue_list = json.load(open(issue_file_path, "r", encoding="utf-8"))
        for issue in issue_list:
            if issue.get("closedAt"):
                status_counter["closed"] += 1
            else:
                status_counter["open"] += 1

    # 保存统计结果
    os.makedirs(f"./output/{semester}", exist_ok=True)
    output_path = f"./output/{semester}/issue_status_distribution.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(status_counter, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    semester_dicts = {
        "25 Spring": r".\tmp\team-project-25spring-submissions_local_data.json",
        "24 Spring": r".\tmp\team-project-24spring-submissions_local_data.json",
        "23 Spring": r".\tmp\team-project-23spring-submissions_local_data.json",
    }

    for semester, semester_file in semester_dicts.items():
        commit_time_distribution_date(semester, semester_file)
        commit_time_distribution_hourly(semester, semester_file)
        commit_count_per_repo(semester, semester_file)
        repo_active_contributor_distribution(semester, semester_file)
        repo_code_line_distribution(semester, semester_file)
        gather_language_distribution(semester, semester_file)
        pr_count_per_repo(semester, semester_file)
        pr_status_distribution(semester, semester_file)
        issue_count_per_repo(semester, semester_file)
        issue_status_distribution(semester, semester_file)