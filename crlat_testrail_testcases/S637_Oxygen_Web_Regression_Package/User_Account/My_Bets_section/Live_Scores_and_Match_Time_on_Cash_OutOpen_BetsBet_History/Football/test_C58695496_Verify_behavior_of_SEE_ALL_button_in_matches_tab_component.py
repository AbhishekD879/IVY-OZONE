import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C58695496_Verify_behavior_of_SEE_ALL_button_in_matches_tab_component(Common):
    """
    TR_ID: C58695496
    NAME: Verify behavior of “SEE ALL >” button in matches-tab component
    DESCRIPTION: This Test Case verifies behavior of “SEE ALL >” button in matches-tab component (e.g. /sport/football/matches)
    DESCRIPTION: Testing on Desktop is valid only for Ladbrokes brand
    PRECONDITIONS: Load/Install application
    """
    keep_browser_open = True

    def test_001_go_to_football_page(self):
        """
        DESCRIPTION: Go to Football page
        EXPECTED: Matches tab is opened
        EXPECTED: “SEE ALL >” button is displayed on the right side on the sports accordion
        EXPECTED: ![](index.php?/attachments/get/106955879)
        """
        pass

    def test_002_tap_on_see_all__button_for_first_class_accordion(self):
        """
        DESCRIPTION: Tap on “SEE ALL >” button for first class accordion
        EXPECTED: User is redirected to /competitions/football/class-name page
        """
        pass

    def test_003_tap_on__back_button(self):
        """
        DESCRIPTION: Tap on "<" (back) button
        EXPECTED: User is redirected to /sport/football/matches page
        """
        pass

    def test_004_tap_on_any_class_accordion(self):
        """
        DESCRIPTION: Tap on any class accordion
        EXPECTED: Section is collapsed
        EXPECTED: “SEE ALL >” button is not visible
        """
        pass

    def test_005_tap_on_the_same_sports_accordion_one_more_time(self):
        """
        DESCRIPTION: Tap on the same sports accordion one more time
        EXPECTED: Section is expanded
        EXPECTED: “SEE ALL >” button is visible
        """
        pass
