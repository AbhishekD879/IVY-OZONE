import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C62799660_Verify_displaying_of_self_exclusion_message_for_login_user_in_Quick_bet(Common):
    """
    TR_ID: C62799660
    NAME: Verify displaying of self-exclusion message for login user in  Quick bet
    DESCRIPTION: This test case verifies Self exclusion message in Quick bet
    PRECONDITIONS: User should be logged in to view 'Self Exclusion' message
    """
    keep_browser_open = True

    def test_001_login_to_application(self):
        """
        DESCRIPTION: Login to Application
        EXPECTED: User should login successfully
        """
        pass

    def test_002_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right Menu Icon
        EXPECTED: Right Menu slides in from the right
        """
        pass

    def test_003_tap_my_account_item(self):
        """
        DESCRIPTION: Tap 'My account' item
        EXPECTED: My account' page is opened with full list of items
        """
        pass

    def test_004_tap_responsible_gambling(self):
        """
        DESCRIPTION: Tap 'Responsible Gambling'
        EXPECTED: The 'Responsible Gambling' page is opened
        """
        pass

    def test_005_navigate_to_account_closer_reopen(self):
        """
        DESCRIPTION: Navigate to 'Account closer& reopen
        EXPECTED: Check 'Account closer& reopen' is available
        """
        pass

    def test_006_click_on__account_closer_reopen__link(self):
        """
        DESCRIPTION: Click on  'Account closer& reopen'  link
        EXPECTED: Account closer& reopen page opens
        """
        pass

    def test_007_click_on_sports_close_button(self):
        """
        DESCRIPTION: Click on sports close button
        EXPECTED: Pop up appears click on continue button
        """
        pass

    def test_008_enter_the_duration_from_the_drop_down_and_press_continue(self):
        """
        DESCRIPTION: Enter the duration from the drop down and press continue
        EXPECTED: Account closed successfully
        """
        pass

    def test_009_navigate_to_any_sport_and_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Navigate to any sport and add selection to quick bet
        EXPECTED: Messaging component permanently on quick bet
        """
        pass
