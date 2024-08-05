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
class Test_C58836078_Verify_information_about_single_Selection_in_Betslip_Collapsed(Common):
    """
    TR_ID: C58836078
    NAME: Verify information about single  Selection in Betslip (Collapsed)
    DESCRIPTION: Test case verifies displaying of information about single Selection in Betslip (Collapsed)
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
        EXPECTED: Selection is added to the Betslip
        EXPECTED: Collapsed Betslip displays with added Selection
        """
        pass

    def test_002_verify_that_collapsed_betslip_with_added_selection_displays_next_data_correctly_selection_name_odds_fractional_or_decimal_depending_on_user_preference_settings_stake_box(self):
        """
        DESCRIPTION: Verify that collapsed Betslip with added Selection displays next data correctly:
        DESCRIPTION: * Selection Name
        DESCRIPTION: * Odds (Fractional or Decimal depending on user preference settings)
        DESCRIPTION: * Stake Box
        EXPECTED: Betslip displays correctly information about single Selection and conforms to Light Theme design
        EXPECTED: Coral app:
        EXPECTED: ![](index.php?/attachments/get/109046944)
        EXPECTED: Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/109046943)
        """
        pass

    def test_003_tap_on_stake_box_of_the_selection__on_collapsed_betslip(self):
        """
        DESCRIPTION: Tap on Stake Box of the Selection  on collapsed Betslip
        EXPECTED: Stake Box is tappable
        EXPECTED: Betslip expanded after tap
        """
        pass

    def test_004_swipe_down_to_collapse_betslip(self):
        """
        DESCRIPTION: Swipe down to collapse Betslip
        EXPECTED: Betslip collapsed
        """
        pass

    def test_005_go_to_device_setting_and_enable_dark_themesettings__displaybrightness_select_dark_theme(self):
        """
        DESCRIPTION: Go to device setting and enable Dark Theme
        DESCRIPTION: (Settings-> Display&Brightness->Select Dark Theme)
        EXPECTED: Dark Theme  was successfully enabled on device
        """
        pass

    def test_006_verify_that_collapsed_betslip_with_added_selection_displays_next_data_correctly__selection_name_odds_fractional_or_decimal_depending_on_user_preference_settings_stake_box_tappable(self):
        """
        DESCRIPTION: Verify that collapsed Betslip with added Selection displays next data correctly :
        DESCRIPTION: * Selection Name
        DESCRIPTION: * Odds (Fractional or Decimal depending on user preference settings)
        DESCRIPTION: * Stake Box (tappable)
        EXPECTED: Betslip displays correctly information about Selection and conforms to Dark Theme design
        EXPECTED: Coral app:
        EXPECTED: ![](index.php?/attachments/get/109046950)
        EXPECTED: Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/109046949)
        """
        pass

    def test_007_remove_single_selection_from_betslipeg_swipe_selection_to_the_left_in_betslip_the_way_to_remove_selection_may_differ(self):
        """
        DESCRIPTION: Remove single Selection from Betslip
        DESCRIPTION: (e.g. Swipe Selection to the left in Betslip, the way to remove selection may differ)
        EXPECTED: Single selection was successfully removed from Betslip
        EXPECTED: BetSlip is not displayed in the bottom
        """
        pass

    def test_008_add_any_single_selection_that_has_a_long_name__to_the_betslip(self):
        """
        DESCRIPTION: Add any single Selection that has a long name  to the Betslip
        EXPECTED: single Selection that has a long name is added to the Betslip
        EXPECTED: Collapsed Betslip displays with added Selection
        """
        pass

    def test_009_verify_that_collapsed_betslip_with_added_single_selection_displays_correctly__and_contains_next_data_selection_name_odds_fractional_or_decimal_depending_on_user_preference_settings_stake_box_tappable(self):
        """
        DESCRIPTION: Verify that collapsed Betslip with added single Selection displays correctly  and contains next data:
        DESCRIPTION: * Selection Name
        DESCRIPTION: * Odds (Fractional or Decimal depending on user preference settings)
        DESCRIPTION: * Stake Box (tappable)
        EXPECTED: Collapsed Betslip with added single Selection that has a long name displays correctly with correct data and conforms to Dark Theme
        EXPECTED: Coral app:
        EXPECTED: ![](index.php?/attachments/get/109059271)
        EXPECTED: Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/109059270)
        """
        pass

    def test_010_go_to_device_setting_and_enable_ligh_themesettings__displaybrightness_select_light_theme(self):
        """
        DESCRIPTION: Go to device setting and enable Ligh Theme
        DESCRIPTION: (Settings-> Display&Brightness->Select Light Theme)
        EXPECTED: Light Theme  was successfully enabled on device
        """
        pass

    def test_011_verify_that_collapsed_betslip_with_added_single_selection_displays_correctly__and_contains_next_data_selection_name_odds_fractional_or_decimal_depending_on_user_preference_settings_stake_box_tappable(self):
        """
        DESCRIPTION: Verify that collapsed Betslip with added single Selection displays correctly  and contains next data:
        DESCRIPTION: * Selection Name
        DESCRIPTION: * Odds (Fractional or Decimal depending on user preference settings)
        DESCRIPTION: * Stake Box (tappable)
        EXPECTED: Collapsed Betslip with added single Selection that has a long name displays correctly with correct data and conforms to Light Theme
        EXPECTED: Coral app:
        EXPECTED: ![](index.php?/attachments/get/109059277)
        EXPECTED: Ladbrokes app:
        EXPECTED: ![](index.php?/attachments/get/109059276)
        """
        pass
