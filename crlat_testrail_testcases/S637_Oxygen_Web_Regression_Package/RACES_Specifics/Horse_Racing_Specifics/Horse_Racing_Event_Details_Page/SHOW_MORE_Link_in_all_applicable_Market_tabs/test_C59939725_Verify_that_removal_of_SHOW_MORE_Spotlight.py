import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C59939725_Verify_that_removal_of_SHOW_MORE_Spotlight(Common):
    """
    TR_ID: C59939725
    NAME: Verify that removal of SHOW MORE-Spotlight
    DESCRIPTION: CORAL(Mobile) : Verify that removal of "SHOW MORE & SHOW LESS" links within the Spotlight text
    PRECONDITIONS: 1: Racing Post Verdict should be available for the event
    PRECONDITIONS: 2: SPOTLIGHT and LAST RUN should be available for the Horses
    """
    keep_browser_open = True

    def test_001_launch_the_app(self):
        """
        DESCRIPTION: Launch the app
        EXPECTED: User should be able to launch the app
        """
        pass

    def test_002_click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        pass

    def test_003_click_on_any_horse_race_event_from_uk__irish_races(self):
        """
        DESCRIPTION: Click on any Horse race event from UK / Irish races
        EXPECTED: User should be navigated to Event details page
        """
        pass

    def test_004_scroll_to_the_selections_horses_and_click_on_show_more_link(self):
        """
        DESCRIPTION: Scroll to the Selections (Horses) and click on "SHOW MORE" link
        EXPECTED: The following information should be displayed
        EXPECTED: 1: SPOTLIGHT
        EXPECTED: 2: LAST RUN
        EXPECTED: "SHOW MORE" text should be replaced with "SHOW LESS" in the expanded view
        """
        pass

    def test_005_verify_spotlight_text_under_the_spotlight_label(self):
        """
        DESCRIPTION: Verify SPOTLIGHT text under the "SPOTLIGHT" label
        EXPECTED: User should not be displayed "SHOW MORE" link for SPOTLIGHT text and all the information should be displayed.
        """
        pass

    def test_006_repeat_45_steps_in_all_market_tabs(self):
        """
        DESCRIPTION: Repeat 4,5 steps in all market tabs
        EXPECTED: 
        """
        pass
