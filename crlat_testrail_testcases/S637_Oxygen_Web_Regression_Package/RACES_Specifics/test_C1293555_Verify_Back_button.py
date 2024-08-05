import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C1293555_Verify_Back_button(Common):
    """
    TR_ID: C1293555
    NAME: Verify Back button
    DESCRIPTION: This test case verifies Back button functionality
    PRECONDITIONS: **JIRA ticket **: BMA-3547, BMA-4830
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_horse_racing_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Horse Racing' icon on the Sports Menu Ribbon
        EXPECTED: 'Horse Racing'  Landing Page is opened
        EXPECTED: 'Featured' tab is opened by default
        """
        pass

    def test_003_go_to_event_details_page(self):
        """
        DESCRIPTION: Go to Event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_navigate_within_the_event_details_page__tap_back_button(self):
        """
        DESCRIPTION: Navigate within the event details page > tap Back Button
        EXPECTED: User is directed to 'Horse Racing' landing page irrespectively to the previously navigated tabs
        """
        pass

    def test_005____make_selection_from_next_4_races_module___open_event_details___place_add_selections_to_the_bet_slip___tap_bet_slip_button(self):
        """
        DESCRIPTION: *   Make selection from "Next 4 Races" module
        DESCRIPTION: *   Open Event details
        DESCRIPTION: *   Place add selection(s) to the Bet Slip
        DESCRIPTION: *   Tap "Bet Slip" button
        EXPECTED: *   User is navigated to the Bet Slip page
        EXPECTED: *   Added selection(s) is/are displayed within Bet Slip
        """
        pass

    def test_006_tap_back_button(self):
        """
        DESCRIPTION: Tap Back button
        EXPECTED: User is navigated back to the Event details page, where selections have been added to the Bet Slip
        """
        pass

    def test_007_go_to_antepost_tab(self):
        """
        DESCRIPTION: Go to 'Antepost' tab
        EXPECTED: 'Antepost' page is opened
        EXPECTED: 'Flat' switcher is selected by default (if available)
        """
        pass

    def test_008_go_to_event_details_page__tab_back_button(self):
        """
        DESCRIPTION: Go to Event details page > Tab Back button
        EXPECTED: User is navigated back to the 'Antepost' page with selected 'Flat' switcher
        """
        pass

    def test_009_select_national_huntinternational_switcher__go_to_event_details_page__tab_back_button(self):
        """
        DESCRIPTION: Select National Hunt/International switcher > Go to event details page > Tab Back button
        EXPECTED: User is navigated back to the 'Antepost' page with selected 'Flat' switcher
        """
        pass

    def test_010_go_to_specials_tab__tab_back_button(self):
        """
        DESCRIPTION: Go to 'Specials' tab > Tab Back button
        EXPECTED: User is directed to the landing page irrespectively to the previously navigated tabs/subcontrols ???
        """
        pass

    def test_011_go_to_yourcall_tab__tab_back_button(self):
        """
        DESCRIPTION: Go to 'YourCall' tab > Tab Back button
        EXPECTED: User is navigated back to the previously navigated page
        """
        pass

    def test_012_go_to_horse_result_tab__by_latest_resultby_meetings__tab_back_button(self):
        """
        DESCRIPTION: Go to Horse 'Result' tab > By Latest Result/By Meetings > Tab back button
        EXPECTED: User is navigated back to the previously navigated page
        """
        pass

    def test_013_go_to_horse_event_details_page__refresh_the_screen(self):
        """
        DESCRIPTION: Go to Horse event details page > Refresh the screen
        EXPECTED: User is still on Horse event details page
        """
        pass

    def test_014_tab_back_button(self):
        """
        DESCRIPTION: Tab Back button
        EXPECTED: User is redirected to the Oxygen Homepage
        """
        pass

    def test_015_go_to_the_app_via_direct_link__navigate_inside_the_app___tap_back_button_several_times(self):
        """
        DESCRIPTION: Go to the app via direct link > navigate inside the app -> tap Back button several times
        EXPECTED: User is redirected to the Oxygen Homepage
        """
        pass
