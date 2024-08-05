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
class Test_C58693732_Verify_behavior_of_SEE_ALL_button_in_multiple_sports_section_component(Common):
    """
    TR_ID: C58693732
    NAME: Verify behavior of  “SEE ALL >” button in multiple-sports-section component
    DESCRIPTION: This Test Case verifies behavior of “SEE ALL >” button in multiple-sports-section component (e.g. /home/in-play or /in-play/watchlive)
    PRECONDITIONS: Load/Install application
    """
    keep_browser_open = True

    def test_001_go_to_home___in_play_tab_homein_play(self):
        """
        DESCRIPTION: Go to Home -> In-play tab (/home/in-play)
        EXPECTED: In-play tab is opened
        EXPECTED: “SEE ALL >” button is displayed on the right side on the sports accordion
        EXPECTED: ![](index.php?/attachments/get/106905240)
        """
        pass

    def test_002_tap_on_see_all__button_for_football(self):
        """
        DESCRIPTION: Tap on “SEE ALL >” button for Football
        EXPECTED: User is redirected to /sport/football/competitions page
        """
        pass

    def test_003_tap_on__back_button(self):
        """
        DESCRIPTION: Tap on "<" (back) button
        EXPECTED: User is redirected to /home/in-play page
        """
        pass

    def test_004_tap_on_any_sports_accordion_eg_football(self):
        """
        DESCRIPTION: Tap on any sports accordion (e.g. Football)
        EXPECTED: Section is collapsed
        EXPECTED: “SEE ALL >” button is not visible
        """
        pass

    def test_005_tap_on_the_same_sports_accordion_eg_football_one_more_time(self):
        """
        DESCRIPTION: Tap on the same sports accordion (e.g. Football) one more time
        EXPECTED: Section is expanded
        EXPECTED: “SEE ALL >” button is visible
        """
        pass
