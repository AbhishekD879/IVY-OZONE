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
class Test_C58836079_Verify_information_about_single_Selection_in_Betslip_Expanded(Common):
    """
    TR_ID: C58836079
    NAME: Verify information about single Selection in Betslip (Expanded)
    DESCRIPTION: Test case verifies displaying of information about single Selection in Betslip (Expanded)
    PRECONDITIONS: Light Theme is enabled on device (Settings-> Display&Brightness->Select Light Theme)
    PRECONDITIONS: App is installed and launched
    PRECONDITIONS: User is on Sportsbook home page
    PRECONDITIONS: Designs
    PRECONDITIONS: https://zpl.io/bLA3XBM - Ladbrokes
    PRECONDITIONS: https://zpl.io/VD038lv - Coral
    """
    keep_browser_open = True

    def test_001_add_any_single_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add any single Selection to the Betslip
        EXPECTED: selection is added to the Betslip
        EXPECTED: Collapsed Betslip displays with added Selection
        """
        pass

    def test_002_expand_betslip_with_added_single_selectionswipe_up_or_tap_on_stake_box__to_expand_betslip(self):
        """
        DESCRIPTION: Expand Betslip with added single Selection
        DESCRIPTION: (Swipe up or tap on Stake Box  to expand Betslip)
        EXPECTED: Betslip is expanded
        """
        pass

    def test_003_verify_that_betslip_with_added_single_selection_in_expanded_mode_display_next_data_correctly_selection_name_market_name_event_name_odds_fractional_or_decimal_depending_on_user_preference_stake_box(self):
        """
        DESCRIPTION: Verify that Betslip with added single Selection in expanded mode display next data correctly:
        DESCRIPTION: * Selection Name
        DESCRIPTION: * Market Name
        DESCRIPTION: * Event Name
        DESCRIPTION: * Odds (Fractional or Decimal depending on user preference)
        DESCRIPTION: * Stake Box
        EXPECTED: Betslip cdisplays correctly information about single Selection and conforms to Light Theme design
        EXPECTED: Coral app:
        EXPECTED: ![](index.php?/attachments/get/109047097)
        EXPECTED: Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/109047098)
        """
        pass

    def test_004_tap_on_stake_box_of_the_selection_on_collapsed_betslip(self):
        """
        DESCRIPTION: Tap on Stake Box of the Selection on collapsed Betslip
        EXPECTED: Stake Box is tappable
        """
        pass

    def test_005_repeat_1_4_steps_when_single_selection_has_long_name_details_about_event(self):
        """
        DESCRIPTION: Repeat 1-4 steps when single Selection has long name details about event
        EXPECTED: Betslip displays correctly information about Selection and conforms to Light Theme design
        EXPECTED: Coral app:
        EXPECTED: ![](index.php?/attachments/get/109049939)
        EXPECTED: Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/109049942)
        """
        pass

    def test_006_go_to_device_setting_and_enable_dark_themesettings__displaybrightness_select_dark_theme(self):
        """
        DESCRIPTION: Go to device setting and enable Dark Theme
        DESCRIPTION: (Settings-> Display&Brightness->Select Dark Theme)
        EXPECTED: Dark Theme was successfully enabled on device
        """
        pass

    def test_007_verify__expanded_betslip_with_added_single_selection_that_has_long_name_details___displays_next_data_correctly_selection_name_market_name_event_name_odds_fractional_or_decimal_depending_on_user_preference_stake_box_tappable(self):
        """
        DESCRIPTION: Verify  Expanded Betslip with added single Selection that has long name details   displays next data correctly:
        DESCRIPTION: * Selection Name
        DESCRIPTION: * Market Name
        DESCRIPTION: * Event Name
        DESCRIPTION: * Odds (Fractional or Decimal depending on user preference)
        DESCRIPTION: * Stake Box (tappable)
        EXPECTED: Betslip displays correctly information about single Selection that has long name details and conforms to Dark Theme design
        EXPECTED: Coral app:
        EXPECTED: ![](index.php?/attachments/get/109059280)
        EXPECTED: Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/109059281)
        """
        pass
