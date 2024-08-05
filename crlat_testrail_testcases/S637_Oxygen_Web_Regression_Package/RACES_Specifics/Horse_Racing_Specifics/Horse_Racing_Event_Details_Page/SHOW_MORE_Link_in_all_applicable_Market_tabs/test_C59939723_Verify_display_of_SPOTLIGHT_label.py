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
class Test_C59939723_Verify_display_of_SPOTLIGHT_label(Common):
    """
    TR_ID: C59939723
    NAME: Verify display of "SPOTLIGHT" label
    DESCRIPTION: Verify that User is displayed "SPOTLIGHT" label and Spotlight text below the label in Horse racing Event Details page
    PRECONDITIONS: 1: Racing post verdict should be available for the event
    PRECONDITIONS: 2: SPOTLIGHT, LAST RUN details should be available for the horse from Racing post verdict
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch the APP
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: APP should be opened
        """
        pass

    def test_002_click_on_horse_racing_from_sports_menufor_mobile_click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile: Click on Horse racing from Sports ribbon
        EXPECTED: User should be navigated to Horse racing landing page
        """
        pass

    def test_003_click_on_any_racing_event_from_uk__irish_or_usa_racing_which_has_racing_post_verdict_available(self):
        """
        DESCRIPTION: Click on any racing event from UK & Irish or USA racing which has racing post verdict available
        EXPECTED: User should be navigated to Event details page
        """
        pass

    def test_004_scroll_to_the_selections_horses_and_click_on_show_more_link(self):
        """
        DESCRIPTION: Scroll to the Selections (Horses) and click on "SHOW MORE" link
        EXPECTED: The following information should be displayed
        EXPECTED: 1: SPOTLIGHT
        EXPECTED: 2: LAST RUN (Last 5 races info in tabular format)
        EXPECTED: "SHOW MORE" text should be replaced with "SHOW LESS" in the expanded view
        """
        pass

    def test_005_verify_spotlight_label(self):
        """
        DESCRIPTION: Verify "SPOTLIGHT" label
        EXPECTED: "SPOTLIGHT" label should be displayed
        """
        pass

    def test_006_validate_the_spotlight_text(self):
        """
        DESCRIPTION: Validate the "SPOTLIGHT" text
        EXPECTED: The text should be displayed under the label
        """
        pass

    def test_007_repeat_4_5__6_steps_in_all_market_tabs_applicable(self):
        """
        DESCRIPTION: Repeat 4 ,5 & 6 steps in all market tabs (applicable)
        EXPECTED: 
        """
        pass
