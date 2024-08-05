import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28434_Verify_Back_button(Common):
    """
    TR_ID: C28434
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

    def test_002_tap_sport_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon on the Sports Menu Ribbon
        EXPECTED: *   <Sport> Landing Page is opened
        EXPECTED: *   'Matches' tab is opened by default
        """
        pass

    def test_003_go_to_event_details_page(self):
        """
        DESCRIPTION: Go to Event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: User is directed to <Sport> Landing Page to the previously navigated tab
        """
        pass

    def test_005_navigate_to_the_event_details_page(self):
        """
        DESCRIPTION: Navigate to the Event Details page
        EXPECTED: Event Details page is opened
        """
        pass

    def test_006_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: User is directed to <Sport> Landing page irrespectively to the previously navigated tab
        """
        pass

    def test_007_navigate_inside_sport_landing_page(self):
        """
        DESCRIPTION: Navigate inside <Sport> landing page
        EXPECTED: <Sport> Landing page is opened
        """
        pass

    def test_008_restart_the_app_via_browser_refresh_button(self):
        """
        DESCRIPTION: Restart the app via browser Refresh button
        EXPECTED: App is refreshed
        """
        pass

    def test_009_tap_back_button(self):
        """
        DESCRIPTION: Tap Back button
        EXPECTED: User is redirected to the Homepage
        """
        pass

    def test_010_go_to_the_sport_landing_page_via_direct_link(self):
        """
        DESCRIPTION: Go to the <Sport> landing page via direct link
        EXPECTED: <Sport> landing page is opened
        """
        pass

    def test_011_tap_back_button(self):
        """
        DESCRIPTION: Tap back button
        EXPECTED: User is redirected to the Homepage (user is not thrown out from the app)
        """
        pass

    def test_012_go_to_the_app_via_direct_link(self):
        """
        DESCRIPTION: Go to the app via direct link
        EXPECTED: Oxygen app is opened
        """
        pass

    def test_013_navigate_inside_the_app(self):
        """
        DESCRIPTION: Navigate inside the app
        EXPECTED: User is successfully navigated inside the app
        """
        pass

    def test_014_tap_back_button_several_times(self):
        """
        DESCRIPTION: Tap Back button several times
        EXPECTED: User is redirected to the Oxygen Homepage (user is not thrown out from the app)
        """
        pass

    def test_015_go_to_in_play_page_from_sports_menu_ribbon(self):
        """
        DESCRIPTION: Go to 'In-Play' page from Sports Menu Ribbon
        EXPECTED: 'In-Play' page is opened
        """
        pass

    def test_016_navigate_within_in_play_page_through_the_sportrace_tabs(self):
        """
        DESCRIPTION: Navigate within 'In-Play' page (through the Sport/Race tabs)
        EXPECTED: Sport/Race tab is opened on In-Play Landing page
        """
        pass

    def test_017_navigate_to_the_sportrace_event_details_page(self):
        """
        DESCRIPTION: Navigate to the Sport/Race Event Details page
        EXPECTED: Sport/Race Event Details page is opened
        """
        pass

    def test_018_tap_on_back_button(self):
        """
        DESCRIPTION: Tap on Back button
        EXPECTED: Appropriate Sport/Race tab on In-Play Landing page is opened
        """
        pass

    def test_019_tap_on_back_button_one_more_time(self):
        """
        DESCRIPTION: Tap on Back button one more time
        EXPECTED: * User is redirected to the 'In-Play' view
        EXPECTED: * The 'In-Play' icon the user navigated from is selected
        """
        pass

    def test_020_go_to_a_z_page_from_sports_menu_ribbon___navigate_within_a_z_view___tap_back_button(self):
        """
        DESCRIPTION: Go to 'A-Z' page from Sports Menu Ribbon -> navigate within 'A-Z' view -> tap Back button
        EXPECTED: User is redirected to the 'A-Z' page from Sports Menu Ribbon he/she navigated from
        """
        pass
