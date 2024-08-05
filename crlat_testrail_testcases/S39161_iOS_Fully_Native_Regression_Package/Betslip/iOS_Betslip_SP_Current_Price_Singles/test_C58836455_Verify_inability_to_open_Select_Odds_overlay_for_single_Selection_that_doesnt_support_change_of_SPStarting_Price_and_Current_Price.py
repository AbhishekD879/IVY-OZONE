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
class Test_C58836455_Verify_inability_to_open_Select_Odds_overlay_for_single_Selection_that_doesnt_support_change_of_SPStarting_Price_and_Current_Price(Common):
    """
    TR_ID: C58836455
    NAME: Verify inability to open "Select Odds " overlay for single Selection that doesn't support change of SP(Starting Price) and Current Price
    DESCRIPTION: Test case verifies inability to open "Select Odds " overlay for single Selection where the Selection does not support change of SP(Starting Price) and Current Price
    DESCRIPTION: **NOTE**: Only for Horse Racing and Greyhounds customers have the option to select either the current price or the SP (starting price).(if configured)
    DESCRIPTION: **Notes**:
    DESCRIPTION: ![](index.php?/attachments/get/121008449)
    PRECONDITIONS: Light Theme is enabled on device (Settings-> Display&Brightness->Select Light Theme)
    PRECONDITIONS: App is installed and launched
    PRECONDITIONS: User is on Sportsbook home page
    PRECONDITIONS: User has (Horse Racing or Greyhounds) event with Selections where there is no ability to switch between  SP(Starting Price) and Current price.
    PRECONDITIONS: **Designs**
    PRECONDITIONS: https://zpl.io/bLA3XBM - Ladbrokes
    PRECONDITIONS: https://zpl.io/VD038lv - Coral
    """
    keep_browser_open = True

    def test_001__add_any_single_selection_of_any_horse_racing_or_greyhounds_event__to_the_bets_lip_where_selection_does_not_support_change_of_spstarting_price_and_current_price(self):
        """
        DESCRIPTION: * Add any single Selection of any (Horse Racing or Greyhounds) event  to the Bets lip where Selection does not support change of SP(Starting Price) and Current Price
        EXPECTED: * Single Selection of (Horse Racing or Greyhounds) event to the Bet slip
        EXPECTED: * Collapsed Bet slip displays with added single Selection
        """
        pass

    def test_002__swipe_up_to_expand_bet_slip(self):
        """
        DESCRIPTION: * Swipe up to expand Bet slip
        EXPECTED: * Bet slip is expanded.
        EXPECTED: * There is no Accordion at the Odds
        EXPECTED: * Bet slip displays correct information about Selection and conforms to Light Theme design
        EXPECTED: Coral app / Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/109061279)  ![](index.php?/attachments/get/109061280)
        """
        pass

    def test_003__user_taps_on_odds_of_current_selection_to_open_select_odds_overlay(self):
        """
        DESCRIPTION: * User taps on Odds of current Selection to open "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay is not opened
        EXPECTED: * Users remains on expanded Bet slip
        """
        pass

    def test_004__go_to_device_setting_and_enable_dark_themesettings__displaybrightness_select_dark_theme(self):
        """
        DESCRIPTION: * Go to device setting and enable Dark Theme
        DESCRIPTION: (Settings-> Display&Brightness->Select Dark Theme)
        EXPECTED: * Dark Theme was successfully enabled on device
        """
        pass

    def test_005__verify_that_expanded_bet_slip_with_added_selection_displays_in_conformance_to_dark_theme(self):
        """
        DESCRIPTION: * Verify that expanded Bet slip with added Selection, displays in conformance to Dark Theme
        EXPECTED: * Bet slip displays correctly information about Selection and conforms to Dark Theme design
        EXPECTED: Coral app / Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/109061283)  ![](index.php?/attachments/get/109061285)
        """
        pass

    def test_006__user_taps_on_odds_of_current_selection_to_open_select_odds_overlay(self):
        """
        DESCRIPTION: * User taps on Odds of current Selection to open "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay is not opened
        EXPECTED: Users remains on expanded Bet slip
        """
        pass
