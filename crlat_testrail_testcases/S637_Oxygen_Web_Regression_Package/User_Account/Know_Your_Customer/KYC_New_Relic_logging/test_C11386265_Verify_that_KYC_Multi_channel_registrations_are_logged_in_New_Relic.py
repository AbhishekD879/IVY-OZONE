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
class Test_C11386265_Verify_that_KYC_Multi_channel_registrations_are_logged_in_New_Relic(Common):
    """
    TR_ID: C11386265
    NAME: Verify that KYC Multi-channel registrations are logged in New Relic
    DESCRIPTION: This test case verifies ability of business user to access KYC Registrations/Multi-channel analytics in New Relic environment
    DESCRIPTION: Note: Cannot automate as we are not automating NewRelic app
    PRECONDITIONS: 1. Login to New Relic environment at https://insights.newrelic.com (ask your team lead for credentials)
    PRECONDITIONS: 2. In order to see all KYC related events run NRQL query, eg.: "SELECT * FROM PageAction where actionName = ‘KYC’ where appId = ‘54469423’ since last week"
    PRECONDITIONS: 3. Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    PRECONDITIONS: 4. How to create In-shop user https://confluence.egalacoral.com/display/SPI/Create+In-Shop+user
    PRECONDITIONS: =======
    PRECONDITIONS: - In NRQL query 'appId' attribute defines environment (dev, stage, prod, etc.) on which you're requesting analytics. In order to see needed 'appId' for you environment: Open Oxygen app > Devtools > Console > type "newrelic" > press Enter > in returned values expand 'info' section > applicationID: "xxxxxxxx" (e.g. applicationID: "54469423")
    PRECONDITIONS: - Playtech IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - **Upgrade Breakpoint** setup (registration will pause on this step which gives you time to change user's Age Verification Status in IMS):
    PRECONDITIONS: In browser: Login with In-shop user > Devtools > Sources > cmd+O upgrade-account-provider.service.ts > find "this.kycService.upgradeVerificationTimer()" in 'upgradeAccount' method and set breakpoint
    PRECONDITIONS: p.s. Please be aware - using breakpoint may cause response timeout issues and affect registration flow
    PRECONDITIONS: - User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    """
    keep_browser_open = True

    def test_001_in_oxygen_app__set_upgrade_breakpoint__upgrade_in_shop_user_login__open_connect_in_header__use_connect_online__fill_all_required_fields_correctly_use_unique_data_for_mail_and_phone_number__tap_confirm_button_breakpoint_should_be_triggered_at_this_point___paused_in_debugger_popupin_ims__find_just_upgraded_user_and_change_age_verification_result_to_under_reviewin_oxygen_app__unpause_debugger_and_finish_upgrade__in_devtools_verify_response_in_openapi_websocket(self):
        """
        DESCRIPTION: In Oxygen app:
        DESCRIPTION: - Set Upgrade Breakpoint
        DESCRIPTION: - Upgrade In-Shop user: Login > Open 'Connect' in header > 'Use Connect Online' > Fill all required fields correctly (use unique data for mail and phone number) > Tap 'Confirm' button (Breakpoint should be triggered at this point - 'Paused in debugger' popup)
        DESCRIPTION: In IMS:
        DESCRIPTION: - Find just upgraded user and change 'Age verification result' to **'Under Review'**
        DESCRIPTION: In Oxygen app:
        DESCRIPTION: - Unpause debugger and finish upgrade
        DESCRIPTION: - In Devtools verify response in "openapi" websocket
        EXPECTED: - In "openapi" websocket: 'ageVerificationStatus' = "review" is received (in response with "ID":31083)
        EXPECTED: - Success upgrade popup displayed
        EXPECTED: - User is redirected to Happy KYC Flow (Deposit page)
        """
        pass

    def test_002_in_new_relic_app__run_nrql_query__in_returned_data_find_username_youve_upgraded(self):
        """
        DESCRIPTION: In New Relic app:
        DESCRIPTION: - Run NRQL query
        DESCRIPTION: - In returned data find Username you've upgraded
        EXPECTED: - Corresponding record with newly registered username is present ('username' attribute)
        EXPECTED: - 'kycStartingFlow' attribute = 'upgrade'
        EXPECTED: - 'kycStatus' attribute = 'underReview'
        EXPECTED: - 'kycFlow' attribute = 'passed'
        """
        pass

    def test_003_in_devtools__application__clear_storage__clear_site_data_plus_empty_cache_and_hard_reload_pagerepeat_steps_1_2changing__age_verification_result_to_passed_in_ims(self):
        """
        DESCRIPTION: In Devtools > Application > Clear storage > Clear site data + Empty Cache and Hard Reload page
        DESCRIPTION: Repeat steps 1-2:
        DESCRIPTION: changing  ‘Age verification result’ to **'Passed'** in IMS
        EXPECTED: In Oxygen app:
        EXPECTED: - In "openapi" websocket: 'ageVerificationStatus' = "passed" is received (in response with "ID":31083)
        EXPECTED: - Success popup displayed
        EXPECTED: - User is redirected to Happy KYC Flow (Deposit page)
        EXPECTED: In New Relic app:
        EXPECTED: - Corresponding record with newly registered username is present ('username' attribute)
        EXPECTED: - 'kycStartingFlow' attribute = 'upgrade'
        EXPECTED: - 'kycStatus' attribute = 'passed'
        EXPECTED: - 'kycFlow' attribute = 'passed'
        """
        pass

    def test_004_in_devtools__application__clear_storage__clear_site_data_plus_empty_cache_and_hard_reload_pagerepeat_steps_1_2changing__age_verification_result_to_unknown_in_ims(self):
        """
        DESCRIPTION: In Devtools > Application > Clear storage > Clear site data + Empty Cache and Hard Reload page
        DESCRIPTION: Repeat steps 1-2:
        DESCRIPTION: changing  ‘Age verification result’ to **'Unknown'** in IMS
        EXPECTED: In Oxygen app:
        EXPECTED: - In "openapi" websocket: 'ageVerificationStatus' = "unknown" is received (in response with "ID":31083)
        EXPECTED: - Success upgrade popup displayed
        EXPECTED: - User is redirected to Failed KYC Flow (documents upload)
        EXPECTED: In New Relic app:
        EXPECTED: - Corresponding record with newly registered username is present ('username' attribute)
        EXPECTED: - 'kycStartingFlow' attribute = 'upgrade'
        EXPECTED: - 'kycStatus' attribute = 'unknown'
        EXPECTED: - 'kycFlow' attribute = 'failed'
        """
        pass

    def test_005_in_devtools__application__clear_storage__clear_site_data_plus_empty_cache_and_hard_reload_pagerepeat_steps_1_2changing__age_verification_result_to_active_grace_period_in_ims(self):
        """
        DESCRIPTION: In Devtools > Application > Clear storage > Clear site data + Empty Cache and Hard Reload page
        DESCRIPTION: Repeat steps 1-2:
        DESCRIPTION: changing  ‘Age verification result’ to **'Active Grace Period'** in IMS
        EXPECTED: In Oxygen app:
        EXPECTED: - In "openapi" websocket: 'ageVerificationStatus' = "inprocess" is received (in response with "ID":31083)
        EXPECTED: - Success upgrade popup displayed
        EXPECTED: - User is redirected to Failed KYC Flow (documents upload)
        EXPECTED: In New Relic app:
        EXPECTED: - Corresponding record with newly registered username is present ('username' attribute)
        EXPECTED: - 'kycStartingFlow' attribute = 'upgrade'
        EXPECTED: - 'kycStatus' attribute = 'activeGracePeriod'
        EXPECTED: - 'kycFlow' attribute = 'failed'
        """
        pass
