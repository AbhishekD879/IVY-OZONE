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
class Test_C60017979_Verify_displaying_of_SP_Current_Price_in_expanded_bet_slip_Multiples(Common):
    """
    TR_ID: C60017979
    NAME: Verify displaying of SP & Current Price in expanded bet slip (Multiples)
    DESCRIPTION: Test case verifies SP & Current Price in expanded bet slip
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
    PRECONDITIONS: Bet slip contains several selections (more than 2, e.g.:5 selections)
    PRECONDITIONS: Bet slip contains several selections with ability to switch between SP & Current Price  ( e.g.:2 selections)
    PRECONDITIONS: Bet slip collapsed
    PRECONDITIONS: User has (Horse Racing or Greyhounds) available event with Selections where there is ability to switch between SP(Starting Price) and Current price .
    PRECONDITIONS: Designs:
    PRECONDITIONS: Coral: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2a5514c30ae56fabb6929
    PRECONDITIONS: Ladbrokes: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea98b5afda2592706e50595
    """
    keep_browser_open = True

    def test_001__expand_bet_slip_verify_that_view_of_selections_that_support_spstarting_price_and_current_price_conforms_to_coral__ladbrokes_designs_light_theme(self):
        """
        DESCRIPTION: * Expand bet slip
        DESCRIPTION: * Verify that view of selections that support SP(Starting Price) and Current price conforms to Coral / Ladbrokes designs (Light theme)
        EXPECTED: * Bet slip expanded
        EXPECTED: * There is a down arrow near the Odds of selections that support SP(Starting Price) and Current price
        EXPECTED: * view of selections that support SP(Starting Price) and Current price conforms to Coral / Ladbrokes designs (Light theme)
        EXPECTED: ![](index.php?/attachments/get/121008369) ![](index.php?/attachments/get/121008370)
        """
        pass

    def test_002__user_taps_on_odds_of_any__selection_that_supports_spstarting_price_and_current_price__to_open_select_odds_overlay(self):
        """
        DESCRIPTION: * User taps on Odds of any  Selection that supports SP(Starting Price) and Current price  to open "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay slides up over Betslip
        EXPECTED: * "Select Odds" overlay is opened
        EXPECTED: Coral app / Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/121008375) ![](index.php?/attachments/get/121008376)
        """
        pass

    def test_003_verify_that_select_odds_overlay_displays_as_per_designlight_theme_headerfooter_and_betslip_displays_behind_select_odds_overlay_there_is_no_scrolling_on_select_odds_overlay_current_price_selected_by_default_and_marked_with_a_tick(self):
        """
        DESCRIPTION: Verify that "Select Odds" overlay displays as per design(Light Theme):
        DESCRIPTION: * header,footer and Betslip displays behind "Select Odds" overlay
        DESCRIPTION: * there is no scrolling on "Select Odds" overlay
        DESCRIPTION: * "Current price" selected by default and marked with a tick
        EXPECTED: "Select Odds" overlay displays as per design(Light Theme):
        EXPECTED: * header,footer and Betslip displays behind "Select Odds" overlay
        EXPECTED: * there is no scrolling on "Select Odds" overlay
        EXPECTED: * "Current price" selected by default and marked with tick  (grey tick for Coral, green tick for Ladbrokes)
        """
        pass

    def test_004__go_to_device_setting_and_enable_dark_themesettings__displaybrightness_select_dark_theme(self):
        """
        DESCRIPTION: * Go to device setting and enable Dark Theme
        DESCRIPTION: (Settings-> Display&Brightness->Select Dark Theme)
        EXPECTED: * Dark Theme was successfully enabled on device
        """
        pass

    def test_005_verify_that_select_odds_overlay_displays_as_per_designdark_theme_headerfooter_and_bets_lip_displays_behind_select_odds_overlay_there_is_no_scrolling_on_select_odds_overlay_current_price_selected_by_default_and_marked_marked_with_sign(self):
        """
        DESCRIPTION: Verify that "Select Odds" overlay displays as per design(Dark Theme):
        DESCRIPTION: * header,footer and Bets lip displays behind "Select Odds" overlay
        DESCRIPTION: * there is no scrolling on "Select Odds" overlay
        DESCRIPTION: * "Current price" selected by default and marked marked with sign
        EXPECTED: "Select Odds" overlay displays as per design(Dark Theme):
        EXPECTED: * header,footer and Bets lip displays behind "Select Odds" overlay
        EXPECTED: * there is no scrolling on "Select Odds" overlay
        EXPECTED: * "Current price" selected by default and marked with the tick  (white tick for Coral, green tick for Ladbrokes)
        EXPECTED: ![](index.php?/attachments/get/121008383) ![](index.php?/attachments/get/121008384)
        """
        pass

    def test_006__tap_on_close_in_the_right_top_of_select_odds_overlay(self):
        """
        DESCRIPTION: * Tap on 'Close' in the right top of "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay closes
        EXPECTED: * Bet slip remains expanded
        """
        pass

    def test_007__verify_that_expanded_bet_slip_displays_as_per_design_dark_theme(self):
        """
        DESCRIPTION: * Verify that expanded Bet slip displays as per design (Dark Theme)
        EXPECTED: * Bet slip displays correctly and conforms to Dark Theme design
        EXPECTED: * Coral app / Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/121008386) ![](index.php?/attachments/get/121008387)
        """
        pass
