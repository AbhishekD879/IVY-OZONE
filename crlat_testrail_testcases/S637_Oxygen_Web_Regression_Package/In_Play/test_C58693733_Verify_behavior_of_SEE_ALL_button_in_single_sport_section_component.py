import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.in_play
@vtest
class Test_C58693733_Verify_behavior_of_SEE_ALL_button_in_single_sport_section_component(Common):
    """
    TR_ID: C58693733
    NAME: Verify behavior of “SEE ALL >” button in single-sport-section component
    DESCRIPTION: This Test Case verifies behavior of “SEE ALL >” button in single-sport-section component (e.g. /sport/football/live or /in-play/football)
    PRECONDITIONS: Load/Install application
    """
    keep_browser_open = True

    def test_001_go_to_in_play___football_tab_in_playfootball(self):
        """
        DESCRIPTION: Go to In-play -> Football tab (/in-play/football)
        EXPECTED: Football tab is opened
        EXPECTED: “SEE ALL >” button is displayed on the right side on the class accordion
        EXPECTED: ![](index.php?/attachments/get/106905317)
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
        EXPECTED: User is redirected to /in-play/football page
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
