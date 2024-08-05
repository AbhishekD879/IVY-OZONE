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
class Test_C60017896_Verify_displaying_of_notification_messageFree_Bets_when_bet_slip_expanded_Multiples(Common):
    """
    TR_ID: C60017896
    NAME: Verify displaying of notification message(Free Bets) when bet slip expanded (Multiples)
    DESCRIPTION: Test case verifies view if of notification message(Free Bets) when bet slip expanded (Multiples)
    PRECONDITIONS: Light Theme is enabled on tested device (Setting -> Display & Brightness -> Select "Light" theme)
    PRECONDITIONS: Install native app
    PRECONDITIONS: Open the app
    PRECONDITIONS: User is on Home page
    PRECONDITIONS: User has Free bets
    PRECONDITIONS: Betslip is empty
    PRECONDITIONS: Bet slip contains several selections (more than 2, e.g.: 5 selections)
    PRECONDITIONS: Coral: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2b112b404f05777b64a74
    PRECONDITIONS: Ladbrokes: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea99a2471f61ebb869f0445
    """
    keep_browser_open = True

    def test_001__add_several_selections_to_bet_slip_more_than_2_eg_5_selections(self):
        """
        DESCRIPTION: * Add several selections to Bet slip (more than 2, e.g.: 5 selections)
        EXPECTED: * Bet slip contains several selections (more than 2, e.g.: 5 selections)
        EXPECTED: *Betslip collapsed
        EXPECTED: * notification message about Free Bets is not displayed
        """
        pass

    def test_002__expand_bet_slip(self):
        """
        DESCRIPTION: * Expand bet slip
        EXPECTED: * Bet slip expanded with selected selection
        EXPECTED: notification message about Free Bets displays along top of the bet slip with close option
        """
        pass

    def test_003__verify_that_notification_message_about_free_bets_displays_correctly_and_conforms_to_light_theme_designs(self):
        """
        DESCRIPTION: * Verify that Notification message about Free Bets displays correctly and conforms to Light theme designs
        EXPECTED: * Notification message about Free Bets displays correctly and conforms to Light theme designs
        EXPECTED: Coral/Ladbrokes designs:
        EXPECTED: ![](index.php?/attachments/get/121004858) ![](index.php?/attachments/get/121004859)
        """
        pass

    def test_004__wait_5_seconds(self):
        """
        DESCRIPTION: * Wait 5 seconds
        EXPECTED: * Notification message about Free Bets closes automatically after passing 5 seconds
        """
        pass

    def test_005__collapse_bet_slip(self):
        """
        DESCRIPTION: * Collapse bet slip
        EXPECTED: * Betslip collapsed
        EXPECTED: * Notification message about Free Bets is not displayed
        """
        pass

    def test_006__expand_betslip(self):
        """
        DESCRIPTION: * Expand betslip
        EXPECTED: * Bet slip is expanded with current single selection
        EXPECTED: * Notification message about Free Bets is not displayed
        """
        pass

    def test_007__remove_selection_from_bet_slip_kill_the_app_enable_dark_theme_on_tested_device_settings___display__brightness___select_dark_theme(self):
        """
        DESCRIPTION: * Remove selection from bet slip
        DESCRIPTION: * Kill the app
        DESCRIPTION: * Enable Dark Theme on tested device (Settings -> Display & Brightness -> Select "Dark" theme)
        EXPECTED: * selection was removed from Bet slip
        EXPECTED: * The app was killed
        EXPECTED: * Dark Theme enabled on tested device
        """
        pass

    def test_008__repeat_steps_1_2(self):
        """
        DESCRIPTION: * Repeat steps 1-2
        EXPECTED: * Result from steps 1-2
        """
        pass

    def test_009__verify_that_notification_message_about_free_bets_displays_correctly_and_conforms_to_dark_theme_designs(self):
        """
        DESCRIPTION: * Verify that Notification message about Free Bets displays correctly and conforms to Dark theme designs
        EXPECTED: * Notification message about Free Bets displays correctly and conforms to Dark theme designs
        EXPECTED: * Coral/Ladbrokes designs:
        EXPECTED: ![](index.php?/attachments/get/121004860) ![](index.php?/attachments/get/121004861)
        """
        pass
