import os, json, dotenv, requests, boto3
from botocore.config import Config


### DO NOT MODIFY ###
def get_token_via_username_password_w_boto3(
    boto3_client,
    env_fp,
    key_prefix = ""
):
    dotenv_file = dotenv.find_dotenv(env_fp)
    config = dotenv.dotenv_values(env_fp)
    response = boto3_client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            "USERNAME" : config[key_prefix+"COGNITO_USERNAME"],
            "PASSWORD" : config[key_prefix+"COGNITO_PASSWORD"]
        },
        ClientId=config[key_prefix+"COGNITO_CLIENT_ID"],
    )
    dotenv.set_key(dotenv_file, key_prefix+"API_ID_TOKEN", response["AuthenticationResult"]["IdToken"])
    dotenv.set_key(dotenv_file, key_prefix+"API_REFRESH_TOKEN", response["AuthenticationResult"]["RefreshToken"])
    return response["AuthenticationResult"]["IdToken"]

def get_token_via_refresh_w_boto3(
    boto3_client,
    env_fp,
    key_prefix = ""
):
    dotenv_file = dotenv.find_dotenv(env_fp)
    config = dotenv.dotenv_values(env_fp)
    response = boto3_client.initiate_auth(
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters={
            "REFRESH_TOKEN" : config[key_prefix+"API_REFRESH_TOKEN"]
        },
        ClientId=config[key_prefix+"COGNITO_CLIENT_ID"],
    )
    dotenv.set_key(dotenv_file, key_prefix+"API_ID_TOKEN", response["AuthenticationResult"]["IdToken"])
    return response["AuthenticationResult"]["IdToken"]

def get_token_via_username_password(
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
        response = requests.patch(
            url_to_request,
            headers=header,
            json=event
        )
    else:
        raise Exception("Invalid Request Type")
    return response
    
if __name__ == '__main__':
    env_fp = ".env"
    resource_to_hit = "buy"
    request_to_hit = "put"
    token_key = "API_ID_TOKEN"
    key_prefix = ""
    event = {}
    
    config = dotenv.dotenv_values(env_fp)
    
    my_config = Config(
        region_name = 'us-east-1'
    )

    client = boto3.client('cognito-idp', config=my_config)
    try:
        id_token = get_token_via_refresh_w_boto3(
            boto3_client=client,
            env_fp=env_fp,
            key_prefix=key_prefix
        )
    except Exception:
        id_token = get_token_via_username_password_w_boto3(
            boto3_client=client,
            env_fp=env_fp,
            key_prefix=key_prefix
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