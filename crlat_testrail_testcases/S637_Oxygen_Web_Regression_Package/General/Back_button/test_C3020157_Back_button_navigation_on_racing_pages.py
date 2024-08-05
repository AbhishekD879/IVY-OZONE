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
class Test_C3020157_Back_button_navigation_on_racing_pages(Common):
    """
    TR_ID: C3020157
    NAME: Back button navigation on racing pages
    DESCRIPTION: This test case verifies back button functionality on racing pages, on race events details pages and after switching between tabs
    PRECONDITIONS: You should be on a Home page
    """
    keep_browser_open = True

    def test_001___tap_on_any_race_icon_in_sports_ribbon_eg_horse_racing_greyhounds__tap_back_button(self):
        """
        DESCRIPTION: - Tap on any Race icon in sports ribbon (e.g. Horse Racing, Greyhounds)
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to Home page
        """
        pass

    def test_002___tap_on_any_race_icon_in_sports_ribbon_and_switch_between_tabs_on_races_landing_page_eg_antepost_specials_yourcall__tap_back_button(self):
        """
        DESCRIPTION: - Tap on any Race icon in sports ribbon and switch between tabs on races landing page (e.g Antepost, Specials, Yourcall)
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to the previous tab
        """
        pass

    def test_003___tap_on_any_race_in_sports_ribbon_and_open_any_race_event__tap_back_button(self):
        """
        DESCRIPTION: - Tap on any race in sports ribbon and open any race event
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to the previous page
        """
        pass

    def test_004___open_any_race_event_and_switch_between_tabs_eg_win_or_ew_win_only_to_finish__tap_back_button(self):
        """
        DESCRIPTION: - Open any race event and switch between tabs (e.g. Win or E/W, Win Only, To Finish)
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to the previous page
        """
        pass

    def test_005___open_any_race_event_and_switch_to_any_another_race_event_in_race_events_ribbon__tap_back_button(self):
        """
        DESCRIPTION: - Open any race event and switch to any another race event in race events ribbon
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to the previous event
        """
        pass
