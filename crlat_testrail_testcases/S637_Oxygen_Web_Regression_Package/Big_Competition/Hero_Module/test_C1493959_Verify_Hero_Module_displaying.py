import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C1493959_Verify_Hero_Module_displaying(Common):
    """
    TR_ID: C1493959
    NAME: Verify Hero Module displaying
    DESCRIPTION: This test case verifies Hero Module (Next Events Module for Live Events) displaying
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * Module with type = 'NEXT_EVENTS' should be created, enabled and set up with Live Events ONLY in CMS
    PRECONDITIONS: * To check response open DEV Tools -> select 'Network' tab -> 'XHR' -> set 'competition' filter and select GET tab/subtab/module by ID request
    PRECONDITIONS: * User is logged out
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_competition_page(self):
        """
        DESCRIPTION: Navigate to Competition page
        EXPECTED: * Competition page is opened
        EXPECTED: * Default Tab is opened (e.g. Featured)
        """
        pass

    def test_003_go_to_hero_module_next_events_module_for_live_events(self):
        """
        DESCRIPTION: Go to Hero Module (Next Events Module for Live Events)
        EXPECTED: 
        """
        pass

    def test_004_verify_hero_module_displaying(self):
        """
        DESCRIPTION: Verify Hero Module displaying
        EXPECTED: Hero Module consists of for each event:
        EXPECTED: * 'Favourites' icon
        EXPECTED: * 'Live Stream' icon (if available)
        EXPECTED: * Team flags
        EXPECTED: * Team abbreviations
        EXPECTED: * Live Scores (if available) / 'Live' icon
        EXPECTED: * Match Time (if available)
        EXPECTED: * '+ n markets' link
        EXPECTED: * Primary market name
        EXPECTED: * Primary market price odds
        """
        pass

    def test_005_verify_scroll_within_hero_module(self):
        """
        DESCRIPTION: Verify scroll within Hero Module
        EXPECTED: Its possible to scroll left/right within Hero Module
        """
        pass

    def test_006_tap_favourites_icon_for_some_event(self):
        """
        DESCRIPTION: Tap 'Favourites' icon for some event
        EXPECTED: 'Log in' pop-up is displayed
        """
        pass

    def test_007_enter_valid_credentials_and_log_in(self):
        """
        DESCRIPTION: Enter valid credentials and log in
        EXPECTED: * User is logged in
        EXPECTED: * 'Favourites' icon is selected
        EXPECTED: * Event is added to 'Favourites' list
        """
        pass

    def test_008_tap_favourites_icon_one_more_time(self):
        """
        DESCRIPTION: Tap 'Favourites' icon one more time
        EXPECTED: * 'Favourites' icon is NOT selected anymore
        EXPECTED: * Event is NOT present in 'Favourites' list
        """
        pass

    def test_009_tap_plus_n_markets_link(self):
        """
        DESCRIPTION: Tap '+ n markets' link
        EXPECTED: The user is navigated to Event Details page after tapping '+ n markets' link
        """
        pass
