import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C59551308_Verify_betradar_scoreboard__color_schemaLadbrokes_and_Coral(Common):
    """
    TR_ID: C59551308
    NAME: Verify betradar scoreboard - color schema(Ladbrokes and Coral)
    DESCRIPTION: Test case verifies betradar scoreboard color schema for both the brands
    PRECONDITIONS: 1. Table Tennis event(s) should subscribe to Betradar Scoreboards
    PRECONDITIONS: 2. Event should be in InPlay state
    PRECONDITIONS: How to check event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_url_and_navigate_to_futsal_event_landing_page_from_a_z_menu___table_tennis___inplay(self):
        """
        DESCRIPTION: Launch ladbrokes URL and Navigate to Futsal event landing page from A-Z menu - table tennis - inplay
        EXPECTED: 
        """
        pass

    def test_002_click_on_inplay_event_which_is_subscribed_to_betradar_scoreboard(self):
        """
        DESCRIPTION: click on inplay event which is subscribed to betradar scoreboard
        EXPECTED: Futsal event detail page should display
        """
        pass

    def test_003_click_on_any_tabstatistics_in_scoreboard_and_verify_color_schema(self):
        """
        DESCRIPTION: click on any tab(Statistics) in scoreboard and verify color schema
        EXPECTED: The colour scheme should match with colors those have across our apps. as shown in screenshot
        EXPECTED: ![](index.php?/attachments/get/106671084)
        """
        pass

    def test_004_repeat_above_steps_in_coral_application_and_verify_color_schema(self):
        """
        DESCRIPTION: Repeat above steps in coral application and verify color schema
        EXPECTED: the colour scheme should match with colors those have across our apps. as shown in screenshot
        EXPECTED: ![](index.php?/attachments/get/106671130)
        """
        pass
