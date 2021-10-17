from requests import get, post, put
import json
import sys


def create_merge_request(kwargs):
    """
    Create a new merge request

    Params REQUIRED:
        project_id
        X user_id
        X gitlab_token
        X title
        X description
        source_branch
        target_branch
    """
    required_params = [
        'url',
        'title',
        'description',
        'user_id',
        'project_id',
        'source_branch',
        'target_branch',
        'gitlab_token']
    result = all(params in required_params for params in kwargs.keys())
    if result is not True:
        raise Exception(
            f'\n\n[ ERROR ] required params: {required_params}\nbut it was passed {result}')

    url: str = f'{kwargs["url"]}/api/v4/projects/{kwargs["project_id"]}/merge_requests'
    headers: dict = {
        'PRIVATE-TOKEN': kwargs['gitlab_token'],
        'Content-Type': 'application/json'
    }

    r = post(url, data=json.dumps(kwargs), headers=headers)
    return r


if __name__ == '__main__':
    required_params = [
        'url',
        'title',
        'description',
        'user_id',
        'project_id',
        'source_branch',
        'target_branch',
        'gitlab_token']
    body: dict = {
        key: value for key, value in zip(required_params, sys.argv[1:])
    }

    create_merge_request(body)

$CI_SERVER_URL 
"AUTO MERGE $CI_COMMIT_BRANCH to test-ci"
"<h1>Merging because test passed</h1><br>-> <h2>$CI_COMMIT_MESSAGE</h2>"
$GITLAB_USER_ID
$CI_PROJECT_ID
$CI_COMMIT_BRANCH
"test-ci"
$TOKEN