import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C59918235_Verify_displaying_of_notification_messageFree_Bets_when_bet_slip_expanded_Single(Common):
    """
    TR_ID: C59918235
    NAME: Verify displaying of notification message(Free Bets) when bet slip expanded (Single)
    DESCRIPTION: Test case verifies appearance of notification message about Free Bets availability
    PRECONDITIONS: Light Theme is enabled on tested device (Setting -> Display & Brightness -> Select "Light" theme)
    PRECONDITIONS: Install native app
    PRECONDITIONS: Open the app
    PRECONDITIONS: User is on Home page
    PRECONDITIONS: Betslip is empty
    PRECONDITIONS: Coral design: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/dashboard?sid=5eaa983ae1344bbac8b9f021
    PRECONDITIONS: Ladbrokes design: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/dashboard?sid=5ea97d244f68f62598af7515
    """
    keep_browser_open = True

    def test_001__user_adds__a_single__qualifying_selection_to_betslip(self):
        """
        DESCRIPTION: * User adds  a single  qualifying selection to Betslip
        EXPECTED: * single selection was added to Betslip
        EXPECTED: * Betslip collapsed
        EXPECTED: * notification message about Free Bets is not displayed
        """
        pass

    def test_002__user_taps_on_selection_in_betslip(self):
        """
        DESCRIPTION: * User taps on selection in Betslip
        EXPECTED: * Betslip expanded with selected selection
        EXPECTED: * notification message about Free Bets displays  along top of the bet slip with close option
        """
        pass

    def test_003__verify_that_notification_message_about_free_bets_displays_correctly_and_conforms_to_light_theme_designs(self):
        """
        DESCRIPTION: * Verify that Notification message about Free Bets displays correctly and conforms to Light theme designs
        EXPECTED: Notification message about Free Bets displays correctly and conforms to Light theme designs
        EXPECTED: * Coral/Ladbrokes designs:
        EXPECTED: ![](index.php?/attachments/get/119425589) ![](index.php?/attachments/get/119425590)
        """
        pass

    def test_004__wait_5_seconds(self):
        """
        DESCRIPTION: * Wait 5 seconds
        EXPECTED: * Notification message about Free Bets closes automatically after passing 5 seconds
        """
        pass

    def test_005__collapse_betslip(self):
        """
        DESCRIPTION: * Collapse betslip
        EXPECTED: * Betslip collapsed
        EXPECTED: * Notification message about Free Bets is not displayed
        """
        pass

    def test_006_expand_betslip(self):
        """
        DESCRIPTION: Expand betslip
        EXPECTED: * Betslip is expanded with current single selection
        EXPECTED: * Notification message about Free Bets is not displayed
        """
        pass

    def test_007__remove_selection_from_betslip_kill_the_app_enable_dark_theme__on_tested_device_settings___display__brightness___select_dark_theme(self):
        """
        DESCRIPTION: * Remove selection from betslip
        DESCRIPTION: * Kill the app
        DESCRIPTION: * Enable Dark Theme  on tested device (Settings -> Display & Brightness -> Select "Dark" theme)
        EXPECTED: * selection was removed from Betslip
        EXPECTED: * The app was killed
        EXPECTED: * Dark Theme enabled on tested device
        """
        pass

    def test_008_repeat_steps_1_2(self):
        """
        DESCRIPTION: Repeat steps 1-2
        EXPECTED: Result from steps 1-2
        """
        pass

    def test_009__verify_that_notification_message_about_free_bets_displays_correctly_and_conforms_to_dark_theme_designs(self):
        """
        DESCRIPTION: * Verify that Notification message about Free Bets displays correctly and conforms to Dark theme designs
        EXPECTED: Notification message about Free Bets displays correctly and conforms to Dark theme designs
        EXPECTED: * Coral/Ladbrokes designs:
        EXPECTED: ![](index.php?/attachments/get/119425591) ![](index.php?/attachments/get/119425592)
        """
        pass
