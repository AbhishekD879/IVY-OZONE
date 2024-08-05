import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C518700_Verify_ACCA_Suggested_Notification_appearing_depending_on_its_Active_Inactive_option_value(Common):
    """
    TR_ID: C518700
    NAME: Verify ACCA Suggested Notification appearing depending on its Active/Inactive option value
    DESCRIPTION: Verify ACCA Suggested Notification appearing depending on it's Active/Inactive option value
    DESCRIPTION: Jira tikets:
    DESCRIPTION: * BMA-10234 ACCA Suggested Notification on Betslip
    DESCRIPTION: * BMA-10235 ACCA Eligibility Notification on Betslip
    DESCRIPTION: * BMA-17369 Reactivating Suggested Notifications for ACCA Insurance
    DESCRIPTION: Note: Cannot automate as we are not editing/deleting/disabling anything in CMS that may affect other users and tests
    PRECONDITIONS: There are events with available ACCA Offers.
    PRECONDITIONS: For configuration of ACCA offers, please, use the following instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=MOB&title=How+to+setup+ACCA+offers
    PRECONDITIONS: To verify ACCA Offer details please check requests:
    PRECONDITIONS: - BuildBet  -> Bets-> Bet Offer
    """
    keep_browser_open = True

    def test_001_log_in_to_cms(self):
        """
        DESCRIPTION: Log in to CMS
        EXPECTED: 
        """
        pass

    def test_002_go_to_system_configuration_section_in_cms(self):
        """
        DESCRIPTION: Go to 'System configuration' section in CMS
        EXPECTED: 'System configuration' section is opened
        """
        pass

    def test_003_open_betslip_section_in_cms(self):
        """
        DESCRIPTION: Open 'Betslip' section in CMS
        EXPECTED: *   'Betslip' section is opened
        EXPECTED: *   supperACCA row with checkbox is displayed
        """
        pass

    def test_004_tick_checkbox_in_supperacca_row_and_click_on_submit_button(self):
        """
        DESCRIPTION: Tick checkbox in supperACCA row and click on 'Submit' button
        EXPECTED: *   Checkbox is ticked
        EXPECTED: *   Changes are saved
        """
        pass

    def test_005_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Home page is opened
        """
        pass

    def test_006_login_with_useraccount_with_gbp_or_eur_currency(self):
        """
        DESCRIPTION: Login with useraccount with GBP or EUR currency
        EXPECTED: User is logged in
        """
        pass

    def test_007_add_at_least_three_selections_to_betslip_that_are_applicable_for_acca_insurance(self):
        """
        DESCRIPTION: Add at least three selections to Betslip that are applicable for ACCA Insurance
        EXPECTED: ACCA Offer is received from Open Bet for the user
        EXPECTED: ACCA Notification message is displayed
        """
        pass

    def test_008_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is Logged out
        """
        pass

    def test_009_login_with_useraccount_with_usd_or_sek_currency(self):
        """
        DESCRIPTION: Login with useraccount with USD or SEK currency
        EXPECTED: User is logged in
        """
        pass

    def test_010_repeat_steps_7_8(self):
        """
        DESCRIPTION: Repeat steps #7-8
        EXPECTED: ACCA Notification is NOT displayed for user with USD or SEK currency even if in OpenBet response ACCA Offer is present
        """
        pass

    def test_011_go_back_to_cms_untick_checkbox_in_supperacca_row_and_click_on_submit_button(self):
        """
        DESCRIPTION: Go back to CMS, untick checkbox in supperACCA row and click on 'Submit' button
        EXPECTED: *   Checkbox is unticked
        EXPECTED: *   Changes are saved
        """
        pass

    def test_012_repeat_steps_5_8(self):
        """
        DESCRIPTION: Repeat steps #5-8
        EXPECTED: ACCA Offer is received from Open Bet for the user
        EXPECTED: ACCA Notification message is NOT displayed
        """
        pass
