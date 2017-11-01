import requests

# See: https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/
token = ''

auth_header = {'Authorization': 'token ' + token}

github_username = ''  # the target user
repos_url = 'https://api.github.com/users/' + github_username + '/repos'
all_repos_metadata = requests.get(repos_url, headers=auth_header).json()

commits = []

for repo_meta in all_repos_metadata:
    repo_url = repo_meta['url']
    repo_stats_url = repo_url + '/stats/contributors'
    print('requesting: ', repo_stats_url)
    repo_stats = requests.get(repo_stats_url, headers=auth_header).json()
    countribution_by_target_user = list(
        filter(lambda contribution: github_username == contribution['author']['login'], repo_stats))

    # now we only have single json representing target user's contribution in the list
    total_commits_on_repo = countribution_by_target_user[0]['total']
    commits.append(total_commits_on_repo)

print('Total commits: ', sum(commits))
