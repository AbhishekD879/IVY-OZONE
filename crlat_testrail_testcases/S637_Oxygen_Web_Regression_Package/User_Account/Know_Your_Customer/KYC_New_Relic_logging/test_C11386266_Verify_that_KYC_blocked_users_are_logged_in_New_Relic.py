import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C11386266_Verify_that_KYC_blocked_users_are_logged_in_New_Relic(Common):
    """
    TR_ID: C11386266
    NAME: Verify that KYC blocked users are logged in New Relic
    DESCRIPTION: This test case verifies ability of business user to access KYC Failed flows analytics using New Relic environment
    DESCRIPTION: Note: Cannot automate as we are not automating NewRelic app
    PRECONDITIONS: 1. Login to New Relic environment at https://insights.newrelic.com (ask your team lead for credentials)
    PRECONDITIONS: 2. In order to see all KYC related events run NRQL query, eg.: "SELECT * FROM PageAction where actionName = ‘KYC’ where appId = ‘54469423’ since last week"
    PRECONDITIONS: =======
    PRECONDITIONS: - In NRQL query 'appId' attribute defines environment (dev, stage, prod, etc.) on which you're requesting analytics. In order to see needed 'appId' for you environment: Open Oxygen app > Devtools > Console > type "newrelic" > press Enter > in returned values expand 'info' section > applicationID: "xxxxxxxx" (e.g. applicationID: "54469423")
    PRECONDITIONS: - Playtech IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    """
    keep_browser_open = True

    def test_001_in_ims__find_your_test_user_and_change_age_verification_result_to_active_grace_period_and_set_agp_success_upload_tag_value_to__5_eg_6in_oxygen_app__login_with_kyc_blocked_user__in_devtools_verify_response_in__openapi_websocket(self):
        """
        DESCRIPTION: In IMS:
        DESCRIPTION: - Find your test user and change 'Age verification result' to 'Active grace period' and set 'AGP_Success_Upload' tag value to >= 5 (e.g. 6)
        DESCRIPTION: In Oxygen app:
        DESCRIPTION: - Login with KYC blocked user
        DESCRIPTION: - In Devtools verify response in  "openapi" websocket
        EXPECTED: - In "openapi" websocket: 'ageVerificationStatus' = "inprocess" is received (in response with "ID":31083)
        EXPECTED: - 'AGP_Success_Upload' tag value >= 5 (e.g. 6) (in response with ID: 35548)
        EXPECTED: - User is redirected to Failed KYC Flow (Verification Failed overlay with "You have reached the max limit of verification attempts" text)
        """
        pass

    def test_002_in_new_relic_app__run_nrql_query__in_returned_data_find_username_youve_logged_in_with(self):
        """
        DESCRIPTION: In New Relic app:
        DESCRIPTION: - Run NRQL query
        DESCRIPTION: - In returned data find Username you've logged in with
        EXPECTED: - Corresponding record with username is present ('username' attribute)
        EXPECTED: - 'kycStartingFlow' attribute = 'login'
        EXPECTED: - 'kycStatus' attribute = 'accountBlocked'
        EXPECTED: - 'kycFlow' attribute = 'failed'
        """
        pass
