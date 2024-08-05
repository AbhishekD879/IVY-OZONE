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
class Test_C59939722_Verify_display_of_SHOW_LESS_link(Common):
    """
    TR_ID: C59939722
    NAME: Verify display of " SHOW LESS" link
    DESCRIPTION: Verify "SHOW LESS" link functionality in a Horse Racing EDP (racecard)
    PRECONDITIONS: 1: Racing Post Verdict should be available for the event
    PRECONDITIONS: 2: SPOTLIGHT and Last Run information should be available for the Horses
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: Ladbrokes/Coral URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
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

    def test_005_click_on_show_less_link_from_the_horseslink(self):
        """
        DESCRIPTION: Click on "SHOW LESS" Link from the Horseslink
        EXPECTED: "SHOW LESS" text should be replaced with "SHOW MORE" in the collapsed view
        """
        pass

    def test_006_repeat_4__5_steps_in_all_market_tabs_applicable(self):
        """
        DESCRIPTION: Repeat 4 & 5 steps in all market tabs (applicable)
        EXPECTED: 
        """
        pass