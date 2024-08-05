import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C59535363_Verify_the_display_order_of_meeting_on_navigating_from_EDP(Common):
    """
    TR_ID: C59535363
    NAME: Verify the display order of meeting on navigating from EDP
    DESCRIPTION: This Test case verifies first race in a meeting is about to start in next 10 minutes then that Meeting should raise above within the specific Country panel on navigating from meeting EDP to meetings landing page
    PRECONDITIONS: 1: First race in a meeting should start in Next 10 minutes
    PRECONDITIONS: 2: No other meeting within that Country panel should be Active
    PRECONDITIONS: ACTIVE: If the first race within a meeting starts in Next 10 minutes
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch App
        EXPECTED: URL should be launched
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

    def test_003_click_on_the_horse_race_meeting_on_event_which_is_going_to_start_in_next_10_minutes(self):
        """
        DESCRIPTION: Click on the Horse race meeting on event (which is going to start in next 10 minutes)
        EXPECTED: User should be navigated to event detail page
        """
        pass

    def test_004_navigate_back_to_horse_landing_page(self):
        """
        DESCRIPTION: Navigate back to Horse landing page
        EXPECTED: User should be able to see that meeting panel at top within the Country panel
        EXPECTED: (Which starts in next 10 minutes)
        """
        pass
