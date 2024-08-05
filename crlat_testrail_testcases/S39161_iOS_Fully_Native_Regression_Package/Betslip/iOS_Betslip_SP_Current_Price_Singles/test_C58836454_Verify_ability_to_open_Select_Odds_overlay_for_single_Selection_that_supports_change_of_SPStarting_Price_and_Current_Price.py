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
class Test_C58836454_Verify_ability_to_open_Select_Odds_overlay_for_single_Selection_that_supports_change_of_SPStarting_Price_and_Current_Price(Common):
    """
    TR_ID: C58836454
    NAME: Verify ability to open "Select Odds " overlay for single Selection that supports change of SP(Starting Price) and Current Price
    DESCRIPTION: Test case verifies ability to open "Select Odds " overlay for single Selection where the Selection does have ability to switch between SP(Starting Price) and Current price
    DESCRIPTION: **NOTE**: Only for Horse Racing and Greyhounds customers have the option to select either the current price or the SP (starting price).(if configured)
    DESCRIPTION: **Notes**
    DESCRIPTION: ![](index.php?/attachments/get/121008448)
    PRECONDITIONS: Light Theme is enabled on device (Settings-> Display&Brightness->Select Light Theme)
    PRECONDITIONS: App is installed and launched
    PRECONDITIONS: User is on Sportsbook home page
    PRECONDITIONS: User has (Horse Racing or Greyhounds) available event with Selections where there is ability to switch between  SP(Starting Price) and Current price available.
    PRECONDITIONS: Designs
    PRECONDITIONS: https://zpl.io/bLA3XBM - Ladbrokes
    PRECONDITIONS: https://zpl.io/VD038lv - Coral
    """
    keep_browser_open = True

    def test_001__add_any_single_selection_of_any_horse_racing_or_greyhounds_event_to_bet_slip_that_supports__sp_starting_price_and_current_price(self):
        """
        DESCRIPTION: * Add any single Selection of any (Horse Racing or Greyhounds) event to Bet slip that supports  SP (Starting Price) and Current price
        EXPECTED: * Single Selection of  (Horse Racing or Greyhounds)event is added to the Bet slip with SP (Starting Price)  available
        EXPECTED: Collapsed Bet slip displays with added single Selection
        """
        pass

    def test_002__swipe_up__to_expand_bet_slip(self):
        """
        DESCRIPTION: * Swipe up  to expand Bet slip
        EXPECTED: * Bet slip is expanded.
        EXPECTED: * There is a down arrow near the Odds
        EXPECTED: Coral app / Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/109061186) ![](index.php?/attachments/get/109061187)
        """
        pass

    def test_003__user_taps_on_odds_of_the_selection_to_open_select_odds_overlay(self):
        """
        DESCRIPTION: * User taps on Odds of the Selection to open "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay  slides up over Bet slip
        EXPECTED: * "Select Odds" overlay is opened
        EXPECTED: * No cross ('X') button in the left top on header
        EXPECTED: Coral app / Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/109061199)  ![](index.php?/attachments/get/109061200)
        """
        pass

    def test_004_verify_that_select_odds_overlay_displays_as_per_designlight_theme_headerfooter_and_betslip_displays_behind_select_odds_overlay_there_is_no_scrolling_on_select_odds_overlay_current_price_selected_by_default_and_marked_with_a_tick(self):
        """
        DESCRIPTION: Verify that "Select Odds" overlay displays as per design(Light Theme):
        DESCRIPTION: * header,footer and Betslip displays behind "Select Odds" overlay
        DESCRIPTION: * there is no scrolling on "Select Odds" overlay
        DESCRIPTION: * "Current price" selected by default and marked with a tick
        EXPECTED: "Select Odds" overlay displays as per design(Light Theme):
        EXPECTED: * header,footer and Betslip displays behind "Select Odds" overlay
        EXPECTED: * there is no scrolling on "Select Odds" overlay
        EXPECTED: * "Current price" selected by default and marked with the tick (grey tick for Coral, green tick for Ladbrokes)
        """
        pass

    def test_005__go_to_device_setting_and_enable_dark_themesettings__displaybrightness_select_dark_theme(self):
        """
        DESCRIPTION: * Go to device setting and enable Dark Theme
        DESCRIPTION: (Settings-> Display&Brightness->Select Dark Theme)
        EXPECTED: * Dark Theme was successfully enabled on device
        """
        pass

    def test_006_verify_that_select_odds_overlay_displays_as_per_designdarrk_theme_headerfooter_and_betslip_displays_behind_select_odds_overlay_there_is_no_scrolling_on_select_odds_overlay_current_price_selected_by_default_and_marked_marked_with__sign(self):
        """
        DESCRIPTION: Verify that "Select Odds" overlay displays as per design(Darrk Theme):
        DESCRIPTION: * header,footer and Betslip displays behind "Select Odds" overlay
        DESCRIPTION: * there is no scrolling on "Select Odds" overlay
        DESCRIPTION: * "Current price" selected by default and marked marked with  sign
        EXPECTED: "Select Odds" overlay displays as per design(Dark Theme):
        EXPECTED: * header,footer and Betslip displays behind "Select Odds" overlay
        EXPECTED: * there is no scrolling on "Select Odds" overlay
        EXPECTED: * No cross ('X') button in the left top on header
        EXPECTED: * "Current price" selected by default and marked with the tick
        EXPECTED: (white tick for Coral, green tick for Ladbrokes)
        EXPECTED: Coral app / Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/109061270)  ![](index.php?/attachments/get/109061271)
        """
        pass

    def test_007__tap_on_close_in_the_right_top_of_select_odds_overlay(self):
        """
        DESCRIPTION: * Tap on 'Close' in the right top of "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay closes
        EXPECTED: Bet slip remains expanded
        """
        pass

    def test_008__verify_that_expanded_bet_slip_displays_as_per_design_dark_theme(self):
        """
        DESCRIPTION: * Verify that expanded Bet slip displays as per design (Dark Theme)
        EXPECTED: * Bet slip displays correctly and conforms to Dark Theme design
        EXPECTED: Coral app / Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/109061273)  ![](index.php?/attachments/get/109061274)
        """
        pass
