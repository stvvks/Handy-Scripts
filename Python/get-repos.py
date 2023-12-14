import csv, traceback, requests, json
import __init__ as env_vars
from gitrest_py.github_ql import GitHubQL
from util.workday import Workday
from util import github

workday_data = {}


# def get_org_teams(org_name):
    # has_more = True
    # team_list = []
    # url = f"https://api.github.com/orgs/{org_name}/teams?per_page=100&page=1"
    # print(url)
    # while has_more:
    #     github.check_rate_limit('core', env_vars.github_admin_token)
    #     r = requests.get(url,
    #     headers={
    #         'Authorization': 'token ' + env_vars.github_admin_token,
    #         "Accept": "application/vnd.github.v3+json"
    #     })
    #     print(f"rate-limit-used: {r.headers['X-RateLimit-Used']}")
    #     if r.status_code == 200:
    #         teams = r.json()
    #         print(len(teams))
    #         for team in teams:
    #             team_list.append({'name':team['name'], 'slug':team['slug']})
    #             team_list.extend(r.json())
    #         has_more, url = github.get_next_url(r.headers)
    #     else:
    #         raise Exception(f"failed to get org teams, error: {r.status_code}:{r.text}")
    # return team_list

# def get_team_AD_group(org_name, team_slug):
    # retry = 0
    # has_more = True
    # groups = []
    # url = f"https://api.github.com/orgs/{org_name}/teams/{team_slug}/external-groups"
    # while has_more:
    #     try:
    #         if retry >= 3:
    #             break
    #         github.check_rate_limit('core', env_vars.github_admin_token)
    #         r = requests.get(url,
    #             headers={
    #                 'Authorization': 'token ' + env_vars.github_admin_token,
    #                 "Accept": "application/vnd.github.v3+json"
    #         })
    #         print(f"rate-limit-used: {r.headers['X-RateLimit-Used']}")
    #         if r.status_code == 200:
    #             for group in r.json()['groups']:
    #                 groups.append(group['group_name'])
    #             has_more, url = github.get_next_url(r.headers)
    #         else:
    #             print(f"failed to get AD Group for team {team_slug}, error: {r.status_code}:{r.text}")
    #             has_more = False
    #         retry = 0
    #     except:
    #         retry+=1
    #         continue
    # return groups


def get_search_results(search_url):
    has_more = True
    retry = 0
    repos = []
    # url = f"https://api.github.com/orgs/{org_name}/teams/{team_slug}/repos?per_page=100&page=1"

    while has_more:
        try:
            if retry >= 3:
                break
            github.check_rate_limit('core', env_vars.github_admin_token)
            r = requests.get(search_url,
                headers={
                    'Authorization': 'token ' + env_vars.github_admin_token,
                    "Accept": "application/vnd.github.v3+json"
            })
            print(f"rate-limit-used: {r.headers['X-RateLimit-Used']}")
            if r.status_code == 200:
                output = r.json()
                items = output['items']
                for item in items:
                    repos.append({'name':item['repository']['name']})    
                has_more, search_url = github.get_next_url(r.headers)
            else:
                print(f"failed to get more repos, error: {r.status_code}:{r.text}")
                has_more = False
            retry = 0
        except:
            retry+=1
            continue
    return repos


# def find_all_org_repos(org):
    # '''
    # Gets all repos from the org provided as an argument.
    # '''
    # github_ql = GitHubQL(env_vars.github_url, env_vars.lifecycle)
    # fields = ['name','repositoryTopics(first: 100) {edges {node {topic {name}}}}','owner{login}','pushedAt','isPrivate','isArchived','collaborators(first: 100) {edges {node {login} permission}}']
    # repos_list = []
    # temp_topic_list = []
    # repos, errors = github_ql.get_all_org_repos(env_vars.github_admin_token, org, endCursor=None, fields=fields, return_with_errors=True)
    # if len(errors) > len(repos):
    #     raise Exception(f"errors returned on call for org: {org}, errors: {errors}")
    # for repo in repos:
    #     if repo['repositoryTopics']['edges']:
    #         for each in repo['repositoryTopics']['edges']:
    #             temp_topic_list.append(each['node']['topic']['name'].upper())
    #         repo['repositoryTopics']=list(temp_topic_list)
    #     else:
    #         repo['repositoryTopics']=[]
    #     if repo['collaborators'] and repo['collaborators']['edges']:
    #         for collaborator in repo['collaborators']['edges']:
    #             if collaborator['permission'] in repo:
    #                 repo[collaborator['permission']].append(collaborator['node']['login'])
    #             else:
    #                 repo[collaborator['permission']] = [collaborator['node']['login']]
    #     repos_list.append(repo)
    #     temp_topic_list.clear()
    # return repos_list


# def get_search_list(repo_name):
    # has_more = True
    # retry = 0
    # repos = []
    # url = f"https://api.github.com/repos/one-thd/{repo_name}/actions/runs"
    # # while has_more:
    # try:
    #         # if retry >= 3:
    #         #     break
    #         # github.check_rate_limit('core', env_vars.github_admin_token)
    #         print(f"getting repo {repo_name}")
    #         # print(f"url: {url}")
    #         r = requests.get(url,
    #             headers={
    #                 'Authorization': 'token ' + env_vars.github_admin_token,
    #                 "Accept": "application/vnd.github.v3+json"
    #         })
    #         # print(f"rate-limit-used: {r.headers['X-RateLimit-Used']}")
    #         if r.status_code == 200:
    #                 repo = r.json()
    #                 # url_actions=f"https://api.github.com/repos/one-thd/{repo['name']}/actions/runs"
    #                 # r2 = requests.get(url_actions,
    #                 #     headers={
    #                 #         'Authorization': 'token ' + env_vars.github_admin_token,
    #                 #         "Accept": "application/vnd.github.v3+json"
    #                 # })
    #                 # if r2.status_code == 200:
    #                 #     r2_out = r2.json()
    #                 #     print(f"action_runs: {r2_out['total_count']}")
    #                 # repos.append({'name':repo['name'], 'language':repo['language'], 'action_runs':r2_out['total_count']})  
    #                 print("Got Actions Runs!")
    #                 print(repo)
    #                 print(f"total_count: {repo['total_count']}")
    #                 repos.append({'name':repo_name, 'action_runs':repo['total_count']})  
    #                 return repos  
    #             # has_more, url = github.get_next_url(r.headers)
    #         else:
    #             print(f"failed to get repo {repo_name}, error: {r.status_code}:{r.text}")
    #             if r.status_code == 403:
    #                 exit(1)
    #             else:
    #                 repos.append({'name':repo_name, 'action_runs':0})
    #             has_more = False
    #     #     retry = 0
    # except:
    #         print("error")
    #     #     retry+=1
    #     #     continue    
    # return repos

def main():

    search_url = 'https://api.github.com/search/code?q=org:one-thd+one-thd/actions-paved-road/.github/workflows&per_page=100'
    # get all teams
    # team_list = get_org_teams(org_name)
    repo_list = []
    # team_list = [{'name':'developer-tools-admins','slug':'developer-tools-admins'}]
    #   find AD group owners to define team owner
    repo_list = get_search_results(search_url)

    with open("search_output.csv", "w") as team_file:
        delim = '\n'
        team_file_writer = csv.writer(team_file)
        team_file_writer.writerow(['Repo Name with Actions Runs'])
        for repo_name in repo_list:
            # get all repos info
            # if len(repo_info) == 0:
            #     print(f"no repo info for {repo_name}")
            #     # continue
            # repo_data = repo_info[0]
            team_file_writer.writerow([repo_name['name']])

    exit(0)


    # all_repos_list = []
    # org = 'one-thd'

    # print("org: --> ",org)
    # try:
    #     all_repos_list.extend(find_all_org_repos(org))
    # except Exception as e:
    #     print(f"we received the following exception, {e}")
    #     print(traceback.format_exc())
   
    # print(all_repos_list)
    # exit(0)

    # print(f"error_orgs: {error_orgs}")
    # workday_svc = Workday()
    # with open("all_repo.csv", "w") as repo_file:
    #     delim = '\n'
    #     repo_file_writer = csv.writer(repo_file)
    #     repo_file_writer.writerow(["VP(s)","Director(s)","OrgOwners/Auditor","Organization Name","Name","Repository Topic(s)","Last Date Pushed","Is Private","Is Archived","Admin Users","Maintain Users","Read Users","Triage Users","Write Users"])
    #     for repo in all_repos_list:
    #         responsible_users = db_data[repo['owner']['login'].upper()]['org_auditor'].split(', ') or db_data[repo['owner']['login'].upper()]['owners'].split(', ')
    #         responsible_vps, responsible_directors = get_hierarchy(workday_svc, responsible_users)
    #         repo_file_writer.writerow([delim.join(responsible_vps), delim.join(responsible_directors),delim.join(responsible_users),repo['owner']['login'],repo['name'],delim.join(repo['repositoryTopics']),repo['pushedAt'],repo['isPrivate'],repo['isArchived'],delim.join(repo.get('ADMIN', [])),delim.join(repo.get('MAINTAIN', [])),delim.join(repo.get('READ', [])),delim.join(repo.get('TRIAGE', [])),delim.join(repo.get('WRITE', []))])
    # return None

if __name__ == '__main__':
    main()