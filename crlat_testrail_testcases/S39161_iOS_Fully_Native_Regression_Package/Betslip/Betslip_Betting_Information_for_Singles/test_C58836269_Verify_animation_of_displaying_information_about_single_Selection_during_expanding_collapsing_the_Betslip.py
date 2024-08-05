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
class Test_C58836269_Verify_animation_of_displaying_information_about_single_Selection_during_expanding_collapsing_the_Betslip(Common):
    """
    TR_ID: C58836269
    NAME: Verify animation of displaying information about single Selection during expanding/collapsing the Betslip
    DESCRIPTION: Test case verifies animation of displaying  information about single Selection when user collapsed/expanded Betslip
    PRECONDITIONS: Light Theme is enabled on device (Settings-> Display&Brightness->Select Light Theme)
    PRECONDITIONS: Application is installed and launched
    PRECONDITIONS: One selection is added to the Betslip
    """
    keep_browser_open = True

    def test_001_expand_collapse_the_bet_slip(self):
        """
        DESCRIPTION: Expand /collapse the bet slip
        EXPECTED: Relevant animation of displaying data about Selection is correctly applied during expand/collapse regarding  (Light Theme)
        EXPECTED: Video of data animation during expand/collapse Betslip
        EXPECTED: (Coral):  https://bit.ly/2BrOqu3
        EXPECTED: !!!WARNING animation provided  for Coral (On Ladbrokes animation should work the same way as on Coral)
        """
        pass

    def test_002_go_to_device_setting_and_enable_dark_themesettings__displaybrightness_select_dark_theme(self):
        """
        DESCRIPTION: Go to device setting and enable Dark Theme
        DESCRIPTION: (Settings-> Display&Brightness->Select Dark Theme)
        EXPECTED: Dark Theme was successfully enabled on device
        """
        pass

    def test_003_expand_collapse_the_bet_slip(self):
        """
        DESCRIPTION: Expand /collapse the bet slip
        EXPECTED: Relevant animation of displaying data about Selection is correctly applied during expand/collapse regarding  (Dark Theme)
        EXPECTED: Video of data animation during expand/collapse Betslip
        EXPECTED: (Coral):  https://bit.ly/2BrOqu3
        EXPECTED: !!!WARNING animation provided  for Coral (On Ladbrokes animation should work the same way as on Coral)
        """
        pass

    def test_004_go_to_device_setting_and_enable_light_themesettings__displaybrightness_select_light_theme(self):
        """
        DESCRIPTION: Go to device setting and enable Light Theme
        DESCRIPTION: (Settings-> Display&Brightness->Select Light Theme)
        EXPECTED: Light Theme was successfully enabled on device
        """
        pass

    def test_005_repeat_1_3_steps_when_single_selection_has_long_name_details_about_event(self):
        """
        DESCRIPTION: Repeat 1-3 steps when single Selection has long name details about event
        EXPECTED: Relevant animation of displaying data about Selection is correctly applied during expand/collapse
        EXPECTED: Video of data animation during expand/collapse Betslip
        EXPECTED: (Coral):  https://bit.ly/2BrOqu3
        EXPECTED: !!!WARNING animation provided  for Coral (On Ladbrokes animation should work the same way as on Coral)
        """
        pass
