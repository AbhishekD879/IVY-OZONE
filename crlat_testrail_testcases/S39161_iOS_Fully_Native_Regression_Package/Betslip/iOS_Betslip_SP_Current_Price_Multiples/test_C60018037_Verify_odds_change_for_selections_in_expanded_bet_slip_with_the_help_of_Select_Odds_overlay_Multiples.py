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
class Test_C60018037_Verify_odds_change_for_selections_in_expanded_bet_slip_with_the_help_of_Select_Odds_overlay_Multiples(Common):
    """
    TR_ID: C60018037
    NAME: Verify odds change for selections in expanded bet slip with the help of "Select Odds" overlay (Multiples)
    DESCRIPTION: Test case verifies change of  SP & Current Price in expanded bet slip
    DESCRIPTION: **NOTE**: Only for Horse Racing and Greyhounds customers have the option to select either the current price or the SP (starting price).(if configured)
    DESCRIPTION: **Explanation**:
    DESCRIPTION: The difference between SP & Current Price is:
    DESCRIPTION: SP (Starting Price) = The final price the Selection has prior to the race starting. E.G Horse starts the race with price of 4/1 therefore SP will be 4/1
    DESCRIPTION: Current Price = The price offered by the bookmaker for that selection at the time. E.G Horse's current price is 3/1 but the Horse starts at a price of 2/1. The User would receive better Odds.
    DESCRIPTION: **Notes:**
    DESCRIPTION: ![](index.php?/attachments/get/121008402)
    PRECONDITIONS: Light Theme is enabled on device (Settings-> Display&Brightness->Select Light Theme)
    PRECONDITIONS: App is installed and launched
    PRECONDITIONS: User is on Sports book home page
    PRECONDITIONS: User has (Horse Racing or Greyhounds) available event with Selections where there is ability to switch between SP(Starting Price) and Current price .
    PRECONDITIONS: Bet slip contains several selections (more than 2, e.g.:5 selections)
    PRECONDITIONS: Bet slip contains several selections with ability to switch between SP & Current Price  ( e.g.:2 selections)
    PRECONDITIONS: Bet slip collapsed
    PRECONDITIONS: * Designs:
    PRECONDITIONS: Coral: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2a5514c30ae56fabb6929
    PRECONDITIONS: Ladbrokes: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea98b5afda2592706e50595
    """
    keep_browser_open = True

    def test_001__expand_bet_slip(self):
        """
        DESCRIPTION: * Expand Bet slip
        EXPECTED: * Bet slip expanded
        EXPECTED: * There are Accordions at the Odds of selections which support SP & CP
        """
        pass

    def test_002__user_taps_on_odds_of_any_selectionthat_supports_sp__cp_to_open_select_odds_overlay(self):
        """
        DESCRIPTION: * User taps on Odds of any Selection(that supports SP & CP) to open "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay slides up over Bet slip
        EXPECTED: * "Select Odds" overlay is opened
        EXPECTED: * "Current price" selected by default and marked with a tick (as per designs)
        EXPECTED: **NOTE** :
        EXPECTED: This drawer area ("Select Odds" overlay) will appear above the Tab Bar. The Tab Bar will always be on show.
        EXPECTED: Coral app / Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/121008419) ![](index.php?/attachments/get/121008420)
        """
        pass

    def test_003__user_taps_on_sp__starting_price_select_odds_overlay(self):
        """
        DESCRIPTION: * User taps on SP ( Starting Price) "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay remains open
        EXPECTED: SP ( Starting Price) marked with a tick as selected on "Select Odds" overlay
        """
        pass

    def test_004__user_swipes_down_on_select_odds_overlay_to_close_select_odds_overlay(self):
        """
        DESCRIPTION: * User Swipes down on "Select Odds" overlay to close "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay closes
        EXPECTED: * expanded Bet slip remains open
        EXPECTED: * The odds will not change to SP when user returns to bet slip
        """
        pass

    def test_005__user_taps_on_odds_of_another_selection_that_supports_sp__cp_to_open_select_odds_overlay(self):
        """
        DESCRIPTION: * User taps on Odds of another Selection (that supports SP & CP) to open "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay slides up over Bet slip
        EXPECTED: * "Select Odds" overlay is opened
        EXPECTED: * "Current price" selected by default and marked with a tick (as per designs)
        EXPECTED: **NOTE**:
        EXPECTED: This drawer area ("Select Odds" overlay) will appear above the Tab Bar. The Tab Bar will always be on show.
        """
        pass

    def test_006__user_taps_on_sp__starting_price_select_odds_overlay(self):
        """
        DESCRIPTION: * User taps on SP ( Starting Price) "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay remains open
        EXPECTED: SP ( Starting Price) marked with a tick as selected on "Select Odds" overlay
        """
        pass

    def test_007__user_taps_on_confirm_button_in_bottom_of_select_odds_overlay(self):
        """
        DESCRIPTION: * User taps on 'Confirm' button in bottom of "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay slides down to display bet slip expanded with SP ( Starting Price) displaying for Odds
        EXPECTED: * The odds  changed to SP ( Starting Price) in bet slip
        """
        pass

    def test_008__user_taps_on_odds_of_another_selection_that_supports_sp__cp_to_open_select_odds_overlay(self):
        """
        DESCRIPTION: * User taps on Odds of another Selection (that supports SP & CP) to open "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay slides up over Bet slip
        EXPECTED: * "Select Odds" overlay is opened
        EXPECTED: * "Current price" selected by default and marked with a tick (as per designs)
        EXPECTED: **NOTE**:
        EXPECTED: This drawer area ("Select Odds" overlay) will appear above the Tab Bar. The Tab Bar will always be on show.
        """
        pass

    def test_009__tap_on_cross_x_button_in_the_left_top_on_header(self):
        """
        DESCRIPTION: * Tap on cross ('X') button in the left top on header
        EXPECTED: * "Select Odds" overlay closed
        EXPECTED: * Bet slip closed (Collapsed)
        """
        pass

    def test_010__go_to_device_setting_and_enable_dark_themesettings__displaybrightness_select_dark_theme(self):
        """
        DESCRIPTION: * Go to device setting and enable Dark Theme
        DESCRIPTION: (Settings-> Display&Brightness->Select Dark Theme)
        EXPECTED: * Dark Theme was successfully enabled on device
        """
        pass

    def test_011__repeat_steps_1_9(self):
        """
        DESCRIPTION: * Repeat steps 1-9
        EXPECTED: * Results from steps 1-9
        EXPECTED: * Bets lip displays correctly and conforms to Dark Theme design
        """
        pass
