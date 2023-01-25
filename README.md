# sixc API

### User Flow
- Go to our [homepage](sixc.io) and click `Join The Waitlist` to make an account. Remember your username and password.
- Clone `sixc-Inc/open_sixc_api` on Github - linked (here)[].
- Spin up a project folder. Create an `.env` file that follows the `.env.template` template.
- Copy `connecting_with_python.py` into your project folder. 
- Run `pip install sixc_api/examples/requirements.txt`.


Base URL: `https://api.sixc.io`

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



