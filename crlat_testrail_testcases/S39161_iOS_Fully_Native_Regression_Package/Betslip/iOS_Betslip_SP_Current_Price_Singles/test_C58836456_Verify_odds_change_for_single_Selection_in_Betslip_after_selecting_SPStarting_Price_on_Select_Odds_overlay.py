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
class Test_C58836456_Verify_odds_change_for_single_Selection_in_Betslip_after_selecting_SPStarting_Price_on_Select_Odds_overlay(Common):
    """
    TR_ID: C58836456
    NAME: Verify odds change for single Selection in Betslip after selecting  SP(Starting Price) on "Select Odds " overlay
    DESCRIPTION: Test case verifies ability to change Odds of single Selection  when user selects SP(Starting Price) on  "Select Odds " overlay , when the Selection does support change of SP(Starting Price) and Current Price
    DESCRIPTION: **NOTE**: Only for Horse Racing and Greyhounds customers have the option to select either the current price or the SP(Starting Price).(if configured)
    DESCRIPTION: ***Notes*
    DESCRIPTION: ![](index.php?/attachments/get/121008451)
    PRECONDITIONS: Light Theme is enabled on device (Settings-> Display&Brightness->Select Light Theme)
    PRECONDITIONS: App is installed and launched
    PRECONDITIONS: User is on Sports book home page
    PRECONDITIONS: **Designs**
    PRECONDITIONS: https://zpl.io/bLA3XBM - Ladbrokes
    PRECONDITIONS: https://zpl.io/VD038lv - Coral
    """
    keep_browser_open = True

    def test_001__add_any_single_selection_of_any_horse_racing_and_greyhounds_where_user_has_the_option_to_select_either_the_current_price_or_the_spstarting_price(self):
        """
        DESCRIPTION: * Add any single Selection of any (Horse Racing and Greyhounds) where user has the option to select either the current price or the SP(Starting Price)
        EXPECTED: * Single Selection of (Horse Racing and Greyhounds) event is added to the Bet slip
        EXPECTED: * Collapsed Bet slip displays with added single Selection
        """
        pass

    def test_002__swipe_up_to_expand_bet_slip(self):
        """
        DESCRIPTION: * Swipe up to expand Bet slip
        EXPECTED: * Bet slip is expanded.
        EXPECTED: * There is Accordion at selection Odds
        """
        pass

    def test_003__user_taps_on_odds_accordion_of_the_selection_to_open_select_odds_overlay(self):
        """
        DESCRIPTION: * User taps on Odds Accordion of the Selection to open "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay  slides up over Betslip
        EXPECTED: * "Select Odds" overlay is opened
        EXPECTED: * "Current price" selected by default and marked with a tick (as per designs)
        EXPECTED: **NOTE:** This drawer area ("Select Odds" overlay) will appear above the Tab Bar. The Tab Bar will always be on show.
        EXPECTED: Coral app / Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/109061199)  ![](index.php?/attachments/get/109061200)
        """
        pass

    def test_004__user_taps_on_sp__starting_price_select_odds_overlay(self):
        """
        DESCRIPTION: * User taps on SP ( Starting Price) "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay remains open
        EXPECTED: * SP ( Starting Price) marked with a tick as selected on "Select Odds" overlay
        """
        pass

    def test_005__user_swipes_down_on_select_odds_overlay_to_close_select_odds_overlay(self):
        """
        DESCRIPTION: * User Swipes down on "Select Odds" overlay to close "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay closes
        EXPECTED: * expanded Bet slip remains open
        EXPECTED: * The odds are not changed to SP in bet slip
        """
        pass

    def test_006__user_taps_on_odds_accordion_of_the_selection_to_open_select_odds_overlay(self):
        """
        DESCRIPTION: * User taps on Odds Accordion of the Selection to open "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay  slides up over Bet slip
        EXPECTED: * "Select Odds" overlay is opened
        EXPECTED: * "Current price" selected by default and marked with a tick (as per designs)
        EXPECTED: **NOTE:** This drawer area ("Select Odds" overlay) will appear above the Tab Bar. The Tab Bar will always be on show.
        EXPECTED: Coral app / Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/109061199) ![](index.php?/attachments/get/109061200)
        """
        pass

    def test_007__user_taps_on_sp__starting_price_select_odds_overlay(self):
        """
        DESCRIPTION: * User taps on SP ( Starting Price) "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay remains open
        EXPECTED: * SP ( Starting Price) marked with a tick as selected on "Select Odds" overlay
        """
        pass

    def test_008__user_taps_on__confirm_button_in_bottom__of_select_odds_overlay(self):
        """
        DESCRIPTION: * User taps on  'Confirm' button in bottom  of "Select Odds" overlay
        EXPECTED: * "Select Odds" overlay slides down to display bet slip collapsed with SP ( Starting Price) displaying for Odds
        EXPECTED: * The odds are  changed to SP ( Starting Price) in bet slip
        """
        pass

    def test_009__go_to_device_setting_and_enable_dark_themesettings__displaybrightness_select_dark_theme(self):
        """
        DESCRIPTION: * Go to device setting and enable Dark Theme
        DESCRIPTION: (Settings-> Display&Brightness->Select Dark Theme)
        EXPECTED: * Dark Theme was successfully enabled on device
        """
        pass

    def test_010__verify_that_expanded_bets_lip_with_added_selection_displays_data_correctly_in_conformance_to_dark_theme_design(self):
        """
        DESCRIPTION: * Verify that expanded Bets lip with added Selection displays data correctly in conformance to Dark Theme design
        EXPECTED: * Bet slip displays correctly and conforms to Dark Theme design
        EXPECTED: Coral app / Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/109061273) ![](index.php?/attachments/get/109061274)
        """
        pass
