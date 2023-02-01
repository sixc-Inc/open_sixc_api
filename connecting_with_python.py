import os, json, dotenv, requests, boto3, getpass
from botocore.config import Config


def get_token_via_username_pwd(
    username, 
    password,
    env_fp,
    key_prefix = ""
):
    URL_TO_HIT = "https://api.sixc.io/login"
    
    data = {
        'username': username,
        'password': password
    }
    dumped_response = requests.post(
        URL_TO_HIT,
        json=data
    )
    response = json.loads(dumped_response.json())
    
    dotenv_file = dotenv.find_dotenv(env_fp)
    dotenv.set_key(dotenv_file, key_prefix+"API_ID_TOKEN", response["body"]["IdToken"])
    dotenv.set_key(dotenv_file, key_prefix+"API_REFRESH_TOKEN", response["body"]["RefreshToken"])
    return response["body"]["IdToken"]

def get_token_via_refresh(
    refresh_token, 
    env_fp,
    key_prefix = ""
):
    URL_TO_HIT = "https://api.sixc.io/login/refresh"
    
    data = {
        'refresh_token': refresh_token
    }
    dumped_response = requests.post(
        URL_TO_HIT,
        json=data
    )
    response = json.loads(dumped_response.json())
    
    dotenv_file = dotenv.find_dotenv(env_fp)
    dotenv.set_key(dotenv_file, key_prefix+"API_ID_TOKEN", response["body"]["IdToken"])
    return response["body"]["IdToken"]

def get_token_via_username_password_curl(
    env_fp,
    key_prefix = ""
):
    init_auth_json_fp = "init_auth.json"
    token_fp = "token.json"
    
    dotenv_file = dotenv.find_dotenv(env_fp)
    config = dotenv.dotenv_values(env_fp)
    url_to_hit = "https://cognito-idp.us-east-1.amazonaws.com/"
    aws_auth_data_json = {
       "AuthParameters" : {
            "USERNAME" : config[key_prefix+"COGNITO_USERNAME"],
            "PASSWORD" : config[key_prefix+"COGNITO_PASSWORD"]
        },
        "AuthFlow" : "USER_PASSWORD_AUTH",
        "ClientId" : config[key_prefix+"COGNITO_CLIENT_ID"]
    }
    with open(init_auth_json_fp, 'w') as f:
        f.write(json.dumps(aws_auth_data_json, indent=4))
    headers = {
        "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth"
    }

    CURL_STR = """
    curl -X POST --data @{} \
    -H 'X-Amz-Target: AWSCognitoIdentityProviderService.InitiateAuth' \
    -H 'Content-Type: application/x-amz-json-1.1' \
    {} > {}
    """.format(
        init_auth_json_fp,
        url_to_hit,
        token_fp
    ).strip()
    os.system(CURL_STR)
    with open(token_fp) as f:
        auth_response = json.load(f)
    dotenv.set_key(dotenv_file, key_prefix+"API_ID_TOKEN", auth_response["AuthenticationResult"]["IdToken"])
    dotenv.set_key(dotenv_file, key_prefix+"API_ACCESS_TOKEN", auth_response["AuthenticationResult"]["AccessToken"])
    os.system("rm {}".format(init_auth_json_fp))
    os.system("rm {}".format(token_fp))
    return auth_response["AuthenticationResult"]["IdToken"]

### DO NOT MODIFY ###

def ping_api(
    token,
    resource,
    request_type, 
    event
):
    # Resources: ['buy', 'buy/place', 'buy/cancel']
    # The `buy` resource enables request types of 'put' (draft order), 'patch' (update order), 'get' (list orders), and 'delete' (delete cancelled orders)
    # The `buy/place` resource enables 'post' request types
    # The `buy/cancel` resource enables 'post' request types
    # Further documention in README.md
    base_url = "https://api.sixc.io/"
    url_to_request = base_url + resource
    header = {
        'Authorization': token
    }
    if request_type.lower() == 'put':
        response = requests.put(
            url_to_request,
            headers=header,
            json=event
        )
    elif request_type.lower() == 'delete':
        response = requests.delete(
            url_to_request,
            headers=header,
            json=event
        )
    elif request_type.lower() == 'get':
        response = requests.get(
            url_to_request,
            headers=header,
            json=event
        )
    elif request_type.lower() == 'patch':
        response = requests.patch(
            url_to_request,
            headers=header,
            json=event
        )
    elif request_type.lower() == 'post':
        response = requests.post(
            url_to_request,
            headers=header,
            json=event
        )
    else:
        raise Exception("Invalid Request Type")
    return response

def pipeline_to_follow():
     ### DO NOT MODIFY ###
    env_fp = ".env"
    key_prefix = ""
    ### DO NOT MODIFY ###
    
    # Variables To Modify
    resource_to_hit = "user" # endpoint to target
    request_to_hit = "get" # request type
    event = {} # data to pass in request

    try:
        config = dotenv.dotenv_values(env_fp)
        id_token = get_token_via_refresh(
            refresh_token=config['API_REFRESH_TOKEN'],
            env_fp=env_fp,
            key_prefix=key_prefix
        )
    except Exception:
        print("Please enter your sixc.io login information below.")
        print("If you've forgotten your login, head to https://auth.sixc.io/forgotPassword?response_type=code&client_id=2ubic58v1u3rbn43b8vdhicvrm&redirect_uri=https://sixc.io")
        uname = input("Enter username: ")
        pwd = getpass.getpass("Enter password (obscured input): ")
        id_token = get_token_via_username_pwd(
            username=uname,
            password=pwd,
            env_fp=env_fp,
            key_prefix = key_prefix
        )
    response = ping_api(
        id_token,
        resource_to_hit,
        request_to_hit,
        event
    )
    
    if response.status_code == 401 or response.status_code == 500:
        print(response.json())
    else:
        print(response.json())
    
if __name__ == '__main__':
   pipeline_to_follow()
