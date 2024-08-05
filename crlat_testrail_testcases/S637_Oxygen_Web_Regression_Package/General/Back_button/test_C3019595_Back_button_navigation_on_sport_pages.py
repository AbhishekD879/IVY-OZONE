import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C3019595_Back_button_navigation_on_sport_pages(Common):
    """
    TR_ID: C3019595
    NAME: Back button navigation on sport pages
    DESCRIPTION: This test case verifies back button functionality on sports pages, on event details pages and after switching between tabs
    PRECONDITIONS: You should be on a Home page
    """
    keep_browser_open = True

    def test_001___tap_on_any_sport_in_sports_ribbon_eg_football_basketball__tap_back_button(self):
        """
        DESCRIPTION: - Tap on any sport in sports ribbon (e.g. Football, Basketball)
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to Home page
        """
        pass

    def test_002___tap_on_any_sport_in_sports_ribbon_and_switch_between_tabs_on_sport_landing_page_eg_in_play_matches_outrights__tap_back_button(self):
        """
        DESCRIPTION: - Tap on any sport in sports ribbon and switch between tabs on sport landing page (e.g In-Play, Matches, Outrights)
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to Home page
        """
        pass

    def test_003___tap_on_any_sport_in_sports_ribbon_and_open_any_event__tap_back_button(self):
        """
        DESCRIPTION: - Tap on any sport in sports ribbon and open any event
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to the previous page (e.g. sport landing page)
        """
        pass

    def test_004___tap_on_any_sport_in_sports_ribbon_and_open_any_event_and_switch_between_tabs_on_edp_eg_all_markets_main_markets__tap_back_button(self):
        """
        DESCRIPTION: - Tap on any sport in sports ribbon and open any event and switch between tabs on EDP (e.g. All Markets, Main Markets)
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to the previous page (e.g. sport landing page)
        """
        pass
