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
class Test_C11353990_Verify_that_KYC_Failed_flows_are_logged_in_New_Relic(Common):
    """
    TR_ID: C11353990
    NAME: Verify that KYC Failed flows are logged in New Relic
    DESCRIPTION: This test case verifies ability of business user to access KYC Failed flows analytics using New Relic environment
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

    def test_001_in_oxygen_app__set_registration_breakpoint__proceed_with_new_user_registration_until_breakpoint_is_triggered_after_you_click_on_complete_registration_button_you_should_see_paused_in_debugger_popupin_ims__find_just_registered_user_and_change_age_verification_result_to_unknownin_oxygen_app__unpause_debugger_and_finish_registration_click_on_save_my_preferences_button_on_gdpr_screen__in_devtools_verify_response_in__openapi_websocket(self):
        """
        DESCRIPTION: In Oxygen app:
        DESCRIPTION: - Set Registration Breakpoint
        DESCRIPTION: - Proceed with new user **registration** until breakpoint is triggered (after you click on 'Complete Registration' button you should see 'Paused in debugger' popup)
        DESCRIPTION: In IMS:
        DESCRIPTION: - Find just registered user and change 'Age verification result' to **'Unknown'**
        DESCRIPTION: In Oxygen app:
        DESCRIPTION: - Unpause debugger and finish registration (click on Save My Preferences button on GDPR screen)
        DESCRIPTION: - In Devtools verify response in  "openapi" websocket
        EXPECTED: - In "openapi" websocket: 'ageVerificationStatus' = "unknown" is received (in response with "ID":31083)
        EXPECTED: - ‘Verification’ pop up displayed
        EXPECTED: - User is redirected to Failed KYC Flow
        """
        pass

    def test_002_in_new_relic_app__run_nrql_query__in_returned_data_find_newly_registered_username(self):
        """
        DESCRIPTION: In New Relic app:
        DESCRIPTION: - Run NRQL query
        DESCRIPTION: - In returned data find newly registered Username
        EXPECTED: - Corresponding record with newly registered username is present ('username' attribute)
        EXPECTED: - 'kycStartingFlow' attribute = 'register'
        EXPECTED: - 'kycStatus' attribute = 'unknown'
        EXPECTED: - 'kycFlow' attribute = 'failed'
        """
        pass

    def test_003_in_oxygen_app__in_devtools__application__clear_storage__clear_site_data_and_empty_cache_and_hard_reload_page__login_user_with_unknown_age_verification_status_created_in_step_1__in_devtools_verify_response_in__openapi_websocket(self):
        """
        DESCRIPTION: In Oxygen app:
        DESCRIPTION: - In Devtools > Application > Clear storage > Clear site data AND Empty Cache and Hard Reload page
        DESCRIPTION: - **Login** user with **'Unknown'** Age verification status (created in step 1)
        DESCRIPTION: - In Devtools verify response in  "openapi" websocket
        EXPECTED: - In "openapi" websocket: 'ageVerificationStatus' = "unknown" is received (in response with "ID":31083)
        EXPECTED: - ‘Verification’ pop up displayed
        EXPECTED: - User is redirected to Failed KYC Flow
        """
        pass

    def test_004_in_new_relic_app__run_nrql_query__in_returned_data_find_username_youve_logged_in_with(self):
        """
        DESCRIPTION: In New Relic app:
        DESCRIPTION: - Run NRQL query
        DESCRIPTION: - In returned data find Username you've logged in with
        EXPECTED: - Corresponding record with username is present ('username' attribute)
        EXPECTED: - 'kycStartingFlow' attribute = 'login'
        EXPECTED: - 'kycStatus' attribute = 'unknown'
        EXPECTED: - 'kycFlow' attribute = 'failed'
        """
        pass

    def test_005_in_devtools__application__clear_storage__clear_site_data_plus_empty_cache_and_hard_reload_pagerepeat_steps_1___2changing__age_verification_result_to_active_grace_period_in_ims(self):
        """
        DESCRIPTION: In Devtools > Application > Clear storage > Clear site data + Empty Cache and Hard Reload page
        DESCRIPTION: Repeat steps 1 - 2:
        DESCRIPTION: changing  ‘Age verification result’ to **‘Active grace period’** in IMS
        EXPECTED: In In Oxygen app:
        EXPECTED: - In "openapi" websocket: 'ageVerificationStatus' = "inprocess" is received (in response with "ID":31083)
        EXPECTED: - User is redirected to Failed KYC Flow
        EXPECTED: In New Relic app:
        EXPECTED: - Corresponding record with newly registered username is present ('username' attribute)
        EXPECTED: - 'kycStartingFlow' attribute = 'register'
        EXPECTED: - 'kycStatus' attribute = 'activeGracePeriod'
        EXPECTED: - 'kycFlow' attribute = 'failed'
        """
        pass

    def test_006_in_devtools__application__clear_storage__clear_site_data_plus_empty_cache_and_hard_reload_pagerepeat_steps_3___4login_with_user__age_verification_result__active_grace_period_created_in_step_5(self):
        """
        DESCRIPTION: In Devtools > Application > Clear storage > Clear site data + Empty Cache and Hard Reload page
        DESCRIPTION: Repeat steps 3 - 4:
        DESCRIPTION: Login with user  ‘Age verification result’ = **‘Active grace period’** (created in step 5)
        EXPECTED: In In Oxygen app:
        EXPECTED: - In "openapi" websocket: 'ageVerificationStatus' = "inprocess" is received (in response with "ID":31083)
        EXPECTED: - User is redirected to Failed KYC Flow
        EXPECTED: In New Relic app:
        EXPECTED: - Corresponding record with username is present ('username' attribute)
        EXPECTED: - 'kycStartingFlow' attribute = 'login'
        EXPECTED: - 'kycStatus' attribute = 'activeGracePeriod'
        EXPECTED: - 'kycFlow' attribute = 'failed'
        """
        pass
