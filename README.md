# sixc API

### User Flow
- Clone this repository.
- Create an `.env` file that follows the `.env.template` template. 
- Go to our [homepage](https://www.sixc.io) and click `Join The Waitlist` to request an account. You should receive an Amazon SES email that you need to approve before signing up. Email `ben@sixc.io` as soon as you submit for faster approval. This needs to happen before you can sign up.
- Sign up via AWS Cognito [here](https://auth.sixc.io/signup?response_type=code&client_id=2ubic58v1u3rbn43b8vdhicvrm&redirect_uri=https://sixc.io). Remember your username and password as you will have to enter them to authenticate & generate a refresh token.
- You do not need to add anything `API_ID_TOKEN` or `API_REFRESH_TOKEN`. Leave the `COGNITO_CLIENT_ID` alone - modifying it will break things.
- Create a virtual environment: `python3 -m venv sixc_api_venv`
- Activate your virtual environment: `source sixc_api_venv/bin/activate`
- Run `pip3 install -r requirements.txt`.
- Read through the API docs below to see which endpoints you'd like to hit! Modify `resource_to_hit`, `request_to_hit` and `event` in  `connecting_with_python.py`'s `__main__()` function in  to configure your connection.
- Run `python3 connecting_with_python.py` when you're ready to hit the API!


Base URL: `https://api.sixc.io`

### Resource: `/login`
#### Method: `post`

Description:
Obtain ID, Access, and Refresh Tokens via username/password login.

Input Data Format:
```
{
    'username': SIXC_USERNAME (str)
    'password': SIXC_PASSWORD (str)
}
```
Successful Return Data Format:
```
{
    'statusCode': 200,
    'body': {
        'AccessToken': COGNITO_ACCESS_TOKEN (str)
        'IdToken': COGNITO_ID_TOKEN (str)
        'AccessToken': COGNITO_REFRESH_TOKEN (str)
    }
}
```


### Resource: `/user`
#### Method: `get`

Description:
Get information about your profile.  

Input Data Format: None expected.

Successful Return Data Format:
```
{
    'statusCode': 200,
    'body': {
        'name': NAME (str)
        'email': EMAIL (str)
        'organization': ORGANIZATION (str)
        'balance': BALANCE (float)
        'emissions': EMISSISONS (float)
    }
}
```
### Resource: `/user`
#### Method: `patch`

Description:
Update user information.

Input Data Format:
```
{
    'name': UPDATED_NAME (str)
    'organization': UPDATED_ORGANIZATION (str)
    'emissions': UPDATED_EMISSIONS (float)
}
```

Successful Return Data Format:
```
{
    'statusCode': 200,
    'body': "User successfully updated!"
}
```

### Resource: `/buy`

#### Method: `put`

Description:
Create a "buy order" in `DRAFT` status of `value` number of allowances. You have no obligations to purchase these allowances and the "buy order" will remain in the draft state until you modify it. 

Input Data Format:
```
{
    'value': NUMBER_OF_ALLOWANCES_TO_PURCHASE (float)
}
```

Successful Return Data Format:
```
{
    'statusCode': 200,
    'body': "Transaction successfully created",
    'transaction_id': TRANSACTION_ID
}
```
### Resource: `/buy`
#### Method: `get`

Description:
List ALL orders associated with your account.

Input Data Format: None expected.

Successful Return Data Format:
```
{
    'statusCode': 200,
    'body': "[ 
        [transaction_id, value, time, status],
        [transaction_id, value, time, status],
        [transaction_id, value, time, status],
        etc....
    ]"
}
```

### Resource: `/buy`
#### Method: `patch`

Description:
Update the `value` of a "buy order" in the `DRAFT` state.

Input Data Format:
```
{
    'transaction_id`: TRANSACTION_ID (int)
    'value': NUMBER_OF_ALLOWANCES_TO_PURCHASE (float)
}
```

Successful Return Data Format:
```
{
    'statusCode': 200,
    'body': "Transaction successfully updated!",
    'transaction_id': TRANSACTION_ID
}
```

### Resource: `/buy`
#### Method: `delete`
Description:
Delete a "buy order". Pre-requisite: "buy order" must be in the `CANCELLED` state.

Input Data Format:
```
{
    'transaction_id`: TRANSACTION_ID (int)
}
```

Successful Return Data Format:
```
{
    'statusCode': 200,
    'body': "Transaction successfully deleted!",
    'transaction_id': TRANSACTION_ID
}
```

### Resource: `/buy/cancel`

#### Method: `post`

Description:
Cancel a "buy order". Pre-requisite: "buy order" must be in the `DRAFT` state.

Input Data Format:
```
{
    'transaction_id`: TRANSACTION_ID (int)
}
```

Successful Return Data Format:
```
{
    'statusCode': 200,
    'body': "Transaction Status: CANCELLED!"
    'transaction_id': TRANSACTION_ID
}
```

### Resource: `buy/place`

#### Method: `post`

Description:
Place a "buy order". This moves a "buy order" into the `PROCESSING` state. Pre-requisite: "buy order" must be in the `DRAFT` state. You are obligated to pay for an order once this request is made. An invoice will be forwarded over email. Once the invoice is completed, the "buy order" will be moved to the `COMPLETED` state and your balance will be credited.

Input Data Format:
```
{
    'transaction_id`: TRANSACTION_ID (int)
}
```

Successful Return Data Format:
```
{
    'statusCode': 200,
    'body': "Transaction Status: PROCESSING!"
    'transaction_id': TRANSACTION_ID
}
```



