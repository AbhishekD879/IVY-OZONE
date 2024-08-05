
def open_api_login(env):
    open_api_prod_session = SioClient()
    open_api_prod_session.connect()
    session_token_response = open_api_prod_session.process_request(
        'sessionToken',
        userName=sys.argv[1],
        password=sys.argv[2]
    )
    if session_token_response['ID'] == 31010:
        #there is session token in "terms and conditions" response so we can reassign the response data
        session_token_response = open_api_prod_session.process_request(
            'termsAndConditions',
            termVersionReference=session_token_response['data']['termVersionReference']
        )
    balance = open_api_prod_session.process_request('balance')

    temp_auth_token_response = open_api_prod_session.process_request(
        'tempAuthToken',
        userName=session_token_response['data']['username'],
        sessionToken=session_token_response['data']['sessionToken']
    )
    if temp_auth_token_response['ID'] == 30002:
        print temp_auth_token_response['data']['token']