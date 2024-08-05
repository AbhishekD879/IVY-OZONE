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
class Test_C59889795_Verify_Event_name_and_Time_Day_selector_tab(Common):
    """
    TR_ID: C59889795
    NAME: Verify Event name and Time- Day selector tab
    DESCRIPTION: Verify horse racing event name and time in each selector tab are matching with EDP page
    PRECONDITIONS: 1: Login to TI and schedule races for Today, Tomorrow, Day 3 and Day 4
    """
    keep_browser_open = True

    def test_001_click_on_horse_racing_button_from_main_menu(self):
        """
        DESCRIPTION: Click on 'Horse Racing' button from main menu
        EXPECTED: Horse Racing Page is loaded
        EXPECTED: Meetings tab is selected by default
        EXPECTED: "UK & IRE" section is displayed followed by "International" ( divided by coutries)
        EXPECTED: "Enhanced Multiples" module (if available) is displayed below "International"
        EXPECTED: The Horse Racing meetings with video stream available should be marked with "Play" icon(Coral) and 'Watch' label(Ladbrokes)
        """
        pass

    def test_002_click_on_any_horse_race_event_under_today_selector_tab(self):
        """
        DESCRIPTION: Click on any horse race event under 'Today selector tab
        EXPECTED: + Appropriate Horse Racing event race card is loaded
        EXPECTED: + Meeting name in top of the page should be same as horse race landing page
        EXPECTED: + The Date in top of the page should be **today's date** (eg: Tuesday 5th May)
        EXPECTED: + The event selector (time ribbon) is displayed right under the meeting selector
        """
        pass

    def test_003_navigate_back_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate back to Horse racing Landing Page
        EXPECTED: 
        """
        pass

    def test_004_click_on_any_horse_race_event_under_tomorrow_selector_tab(self):
        """
        DESCRIPTION: Click on any horse race event under 'Tomorrow selector tab
        EXPECTED: + Appropriate Horse Racing event race card is loaded
        EXPECTED: + Meeting name in top of the page should be same as horse race landing page
        EXPECTED: + The Date in top of the page should be **tomorrow's date**
        EXPECTED: (eg: **Wednesday 6th May** if today is Tuesday 5th may)
        EXPECTED: + The event selector (time ribbon) is displayed right under the meeting selector
        """
        pass

    def test_005_navigate_back_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate back to Horse racing Landing Page
        EXPECTED: 
        """
        pass

    def test_006_click_on_any_horse_race_event_under_next_following_day_or_day3_selector_tab(self):
        """
        DESCRIPTION: Click on any horse race event under 'Next following day' or 'Day3' selector tab
        EXPECTED: + Appropriate Horse Racing event race card is loaded
        EXPECTED: + Meeting name in top of the page should be same as horse race landing page
        EXPECTED: + The Date in top of the page should be **Day after tomorrow's date**
        EXPECTED: (eg: **Thursday 7th May** if today is Tuesday 5th may)
        EXPECTED: + The event selector (time ribbon) is displayed right under the meeting selector
        """
        pass
