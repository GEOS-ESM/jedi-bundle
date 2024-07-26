import os
import yaml
import requests
from datetime import datetime as dt
from jedi_bundle.utils.yaml import load_yaml
from jedi_bundle.utils.logger import Logger
from jedi_bundle.utils.git import get_github_username_token
from jedi_bundle.config.config import return_config_path


def update_hash(logger: Logger, date: dt) -> None:

    # Load pinned versions for repo list
    path_to_pinned_versions = os.path.join(return_config_path(), 'pinned_versions.yaml')
    pinned_versions = load_yaml(logger, 'pinned_versions.yaml')

    # Load build order from jedi_bundle for repo aliases
    aliases = load_yaml(logger, os.path.join(return_config_path(), 'bundles', 'build-order.yaml'))

    # Get git credentials ready
    _, token = get_github_username_token(logger)

    urls = [f'https://api.github.com/repos/jcsda-internal/',
            f'https://api.github.com/repos/geos-esm/',
            f'https://api.github.com/repos/jcsda/']

    # Update each repo commit hash if applicable
    for i in range(len(pinned_versions)):
        repo_alias = ''
        repo_dict = pinned_versions[i]
        repo_name = list(repo_dict.keys())[0]

        # convert name to repo alias if needed
        for j in range(len(aliases)):
            if repo_name in aliases[j]:
                if 'repo_url_name' in aliases[j][repo_name]:
                    repo_alias = aliases[j][repo_name]['repo_url_name']
                    break

        if 'commit' in repo_dict[repo_name]:
            if repo_dict[repo_name]['commit']:

                auth_header = {
                    'Authorization': f'token {token}',
                }

                for url in urls:
                    if repo_alias:
                        url += f'{repo_alias}/commits'
                    else:
                        url += f'{repo_name}/commits'
                    response = requests.get(url, headers=auth_header)
                    data = response.json()
                    if isinstance(data, list):
                        break

                if isinstance(data, dict):
                    logger.abort(f'Failed to retrieve commit history for {repo_name} from {urls}')

                # Perform search to find first commit earlier than date provided
                left, right = 0, len(data) - 1
                while left < right:
                    mid = (left + right) // 2
                    curr_date = dt.strptime(data[mid]['commit']['author']['date'],
                                            '%Y-%m-%dT%H:%M:%S%z')
                    if curr_date < date:
                        right = mid
                    else:
                        left = mid + 1

                # Throw error if commit previous to given date cannot be found
                curr_date = dt.strptime(data[left]['commit']['author']['date'],
                                        '%Y-%m-%dT%H:%M:%S%z')
                if curr_date > date:
                    logger.abort(f'Unable to find commit with date before {date}')

                # Update repo dict with new commit hash
                updated_commit = data[left]['sha']
                pinned_versions[i][repo_name]['branch'] = updated_commit
                logger.info(f'{repo_name}, date: {curr_date}, hash: {updated_commit}')

    # Update pinned_versions.yaml
    with open(path_to_pinned_versions, 'w') as out:
        yaml.dump(pinned_versions, out)
