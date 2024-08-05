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
class Test_C11386090_Verify_that_KYC_Passed_flows_are_logged_in_New_Relic(Common):
    """
    TR_ID: C11386090
    NAME: Verify that KYC Passed flows are logged in New Relic
    DESCRIPTION: This test case verifies ability of business user to access KYC Passed flows analytics using New Relic environment
    DESCRIPTION: Note: Cannot automate as we are not automating NewRelic app
    PRECONDITIONS: 1. Login to New Relic environment at https://insights.newrelic.com (ask your team lead for credentials)
    PRECONDITIONS: 2. In order to see all KYC related events run NRQL query, eg.: "SELECT * FROM PageAction where actionName = ‘KYC’ where appId = ‘54469423’ since last week"
    PRECONDITIONS: =======
    PRECONDITIONS: - In NRQL query 'appId' attribute defines environment (dev, stage, prod, etc.) on which you're requesting analytics. In order to see needed 'appId' for you environment: Open Oxygen app > Devtools > Console > type "newrelic" > press Enter > in returned values expand 'info' section > applicationID: "xxxxxxxx" (e.g. applicationID: "54469423")
    PRECONDITIONS: - Playtech IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - **Registration Breakpoint** setup (registration will pause on this step which gives you time to change user's Age Verification Status in IMS):
    PRECONDITIONS: In browser: Navigate Oxygen Signup page > Devtools > Sources > cmd+O registration-form-mobile.component.ts > find "this.successSignUp(response)" in 'private registerNewUser()' method and set breakpoint:
    PRECONDITIONS: p.s. Please be aware - using breakpoint may cause response timeout issues and affect registration flow
    PRECONDITIONS: - User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    """
    keep_browser_open = True

    def test_001_in_oxygen_app__set_registration_breakpoint__proceed_with_new_user_registration_until_breakpoint_is_triggered_after_you_click_on_complete_registration_button_you_should_see_paused_in_debugger_popupin_ims__find_just_registered_user_and_change_age_verification_result_to_under_reviewin_oxygen_app__unpause_debugger_and_finish_registration_click_on_save_my_preferences_button_on_gdpr_screen__in_devtools_verify_response_in__openapi_websocket(self):
        """
        DESCRIPTION: In Oxygen app:
        DESCRIPTION: - Set Registration Breakpoint
        DESCRIPTION: - Proceed with new user **registration** until breakpoint is triggered (after you click on 'Complete Registration' button you should see 'Paused in debugger' popup)
        DESCRIPTION: In IMS:
        DESCRIPTION: - Find just registered user and change 'Age verification result' to **'Under Review'**
        DESCRIPTION: In Oxygen app:
        DESCRIPTION: - Unpause debugger and finish registration (click on Save My Preferences button on GDPR screen)
        DESCRIPTION: - In Devtools verify response in  "openapi" websocket
        EXPECTED: - In "openapi" websocket: 'ageVerificationStatus' = "review" is received (in response with "ID":31083)
        EXPECTED: - User is redirected to Happy KYC Flow (Deposit page)
        """
        pass

    def test_002_in_new_relic_app__run_nrql_query__in_returned_data_find_newly_registered_username(self):
        """
        DESCRIPTION: In New Relic app:
        DESCRIPTION: - Run NRQL query
        DESCRIPTION: - In returned data find newly registered Username
        EXPECTED: - Corresponding record with newly registered username is present ('username' attribute)
        EXPECTED: - 'kycStartingFlow' attribute = 'register'
        EXPECTED: - 'kycStatus' attribute = 'underReview'
        EXPECTED: - 'kycFlow' attribute = 'passed'
        """
        pass

    def test_003_in_oxygen_app__in_devtools__application__clear_storage__clear_site_data_and_empty_cache_and_hard_reload_page__login_user_with_under_review_age_verification_status_created_in_step_1__in_devtools_verify_response_in_openapi_websocket(self):
        """
        DESCRIPTION: In Oxygen app:
        DESCRIPTION: - In Devtools > Application > Clear storage > Clear site data AND Empty Cache and Hard Reload page
        DESCRIPTION: - **Login** user with **'Under Review'** Age verification status (created in step 1)
        DESCRIPTION: - In Devtools verify response in "openapi" websocket
        EXPECTED: - In "openapi" websocket: 'ageVerificationStatus' = "review" is received (in response with "ID":31083)
        EXPECTED: - User is redirected to Happy KYC Flow (Deposit popup)
        """
        pass

    def test_004_in_new_relic_app__run_nrql_query__in_returned_data_find_username_youve_logged_in_with(self):
        """
        DESCRIPTION: In New Relic app:
        DESCRIPTION: - Run NRQL query
        DESCRIPTION: - In returned data find Username you've logged in with
        EXPECTED: - Corresponding record with newly registered username is present ('username' attribute)
        EXPECTED: - 'kycStartingFlow' attribute = 'login'
        EXPECTED: - 'kycStatus' attribute = 'underReview'
        EXPECTED: - 'kycFlow' attribute = 'passed'
        """
        pass

    def test_005_in_ims__find_registered_user_in_step1_and_change_age_verification_result_to_passedin_oxygen_app__in_devtools__application__clear_storage__clear_site_data_and_empty_cache_and_hard_reload_page__login_user_with_passed_age_verification_status__in_devtools_verify_response_in_openapi_websocket(self):
        """
        DESCRIPTION: In IMS:
        DESCRIPTION: - Find registered user (in Step1) and change 'Age verification result' to 'Passed'
        DESCRIPTION: In Oxygen app:
        DESCRIPTION: - In Devtools > Application > Clear storage > Clear site data AND Empty Cache and Hard Reload page
        DESCRIPTION: - **Login** user with **'Passed'** Age verification status
        DESCRIPTION: - In Devtools verify response in "openapi" websocket
        EXPECTED: - In "openapi" websocket: 'ageVerificationStatus' = "passed" is received (in response with "ID":31083)
        EXPECTED: - User is redirected to Happy KYC Flow
        """
        pass

    def test_006_in_new_relic_app__run_nrql_query__in_returned_data_find_username_youve_logged_in_with(self):
        """
        DESCRIPTION: In New Relic app:
        DESCRIPTION: - Run NRQL query
        DESCRIPTION: - In returned data find Username you've logged in with
        EXPECTED: - Corresponding record with username is present ('username' attribute)
        EXPECTED: - 'kycStartingFlow' attribute = 'login'
        EXPECTED: - 'kycStatus' attribute = 'passed'
        EXPECTED: - 'kycFlow' attribute = 'passed'
        """
        pass
