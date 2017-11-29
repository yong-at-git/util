import requests

"""
This script counts the total GitHub commits an user has pushed to all the repositories belonging to her.
Give it a second try if encountering problem in response.
"""

# Configuration section.

# 1. Generate the token from here: https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/
token = ''
# 2. Specify the target user
github_username = ''

auth_header = {'Authorization': 'token ' + token}
repos_url = 'https://api.github.com/users/' + github_username + '/repos'

session = requests.session()
session.headers.update(auth_header)

all_repos_metadata = session.get(repos_url).json()

commits = []

for repo_meta in all_repos_metadata:
    repo_url = repo_meta['url']
    repo_stats_url = repo_url + '/stats/contributors'

    try:
        repo_stats = session.get(repo_stats_url).json()
        contribution_by_target_user = list(
            filter(lambda contribution: github_username == contribution['author']['login'], repo_stats))

        # now we only have single json representing target user's contribution in the list
        try:
            total_commits_on_repo = contribution_by_target_user[0]['total']

            print('Commits:', total_commits_on_repo, ', on repo: ', repo_url)

            commits.append(total_commits_on_repo)
        except Exception as e:
            raise Exception('Failed to retrieve meta data from: ' + repo_stats_url, ', got resp: ',
                            contribution_by_target_user, e)
    except Exception as e:
        print(e)

print('Total commits: ', sum(commits))
