import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C44870311_Verify_display_of_promo_icon_and_other_details_for_Extra_Place_races(Common):
    """
    TR_ID: C44870311
    NAME: Verify display of promo icon and other details for Extra Place races.
    DESCRIPTION: 
    PRECONDITIONS: User is logged in the application.
    """
    keep_browser_open = True

    def test_001_navigate_to_landing_page_of_horse_racing_verify(self):
        """
        DESCRIPTION: Navigate to landing page of Horse racing. Verify.
        EXPECTED: 1. 'Extra Place' races (races which offer extra places) consisting of the meeting point and the time are displayed at the top of the page.
        EXPECTED: 2. Promo icon for Extra place is also displayed in the Extra place module/section.
        """
        pass

    def test_002_verify_for_the_meeting_place_and_time(self):
        """
        DESCRIPTION: Verify for the meeting place and time.
        EXPECTED: 1. The meeting place and time are displayed.
        EXPECTED: 2. The time is displayed in 24 hour format.
        """
        pass

    def test_003_click_on_any_time_of_any_meeting_place_in_the_extra_place_module_and_verify(self):
        """
        DESCRIPTION: Click on any time of any meeting place in the 'Extra Place' module and verify.
        EXPECTED: The user is navigated to the respective race card of the event.
        """
        pass

    def test_004_verify_in_the_event_details_pagerace_card(self):
        """
        DESCRIPTION: Verify in the event details page/race card.
        EXPECTED: 1. Each way terms, e.g. Each way: 1/5 Odds - Places 1-2-3-4
        EXPECTED: 2. Type of race (e.g class 6, class 7 etc).
        """
        pass
