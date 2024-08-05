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
class Test_C9770746_Matches_tab_content(Common):
    """
    TR_ID: C9770746
    NAME: Matches tab content
    DESCRIPTION: This test case verifies the Matches tab load and content when navigating to <sport> landing page for sports  that are Tier I.
    PRECONDITIONS: The list of sports that are tier I/II/III is available here: https://docs.google.com/spreadsheets/d/1dLDjAkrGpCPRzhVbojt2_tfd8upB82uoU0E-CYojkfY/edit?ts=5c0f928b#gid=0
    PRECONDITIONS: Oxygen app is running
    PRECONDITIONS: User is on Home page (for example)
    """
    keep_browser_open = True

    def test_001_click_on_any_sport_in_menu_ribbon(self):
        """
        DESCRIPTION: Click on any sport in menu ribbon
        EXPECTED: *Mobile*:
        EXPECTED: Sport landing page loads: 'Matches' tab loads by default
        EXPECTED: *Desktop*:
        EXPECTED: Sport landing page loads: 'Matches'-> Today tab loads by default
        """
        pass

    def test_002_verify_tab_content(self):
        """
        DESCRIPTION: Verify tab content
        EXPECTED: The tab content consists of:
        EXPECTED: - No sub tabs 'Today/Tomorrow/Future' (for mobile only)
        EXPECTED: - 'In Play' module with leagues expanded by default
        EXPECTED: - Upcoming Module(with Market selector in module header) below the In-play Module with types and all the pre-play Events of those Types
        """
        pass

    def test_003_verify_in_play_module(self):
        """
        DESCRIPTION: Verify 'In-Play' Module
        EXPECTED: In-Play Module consist of:
        EXPECTED: - 'In-Play' name in the header of the module
        EXPECTED: - 'See All' link in header of the module on the right with number of available quantity of events that redirects to In-Play page (for Football, tennis and basketball)
        EXPECTED: - Fixture header with league name, home/draw/away names
        EXPECTED: - Event available for today and tomorrow (23:59 Hrs ) with 'Watch live' or 'Live' icon under event name
        EXPECTED: - 'N- more' link (with more events available) on the right of event card (if available)
        """
        pass

    def test_004_verify_upcoming_module_with_market_selector(self):
        """
        DESCRIPTION: Verify Upcoming Module (with market selector)
        EXPECTED: Upcoming Module consist of:
        EXPECTED: - Market selector in the header of the module
        EXPECTED: - 'Change' button that opens market selector in module header
        EXPECTED: - Type accordion (league) with 'See All' link on the right (that redirects to competition page of that tuype)
        EXPECTED: - First 3 types are expanded by default, the rest collapsed
        EXPECTED: - Fixture header with date (eg. Tomorrow) and home/draw/away names
        EXPECTED: - Events available with 'Watch' icon, date of event and 'N - more' link (if available) on event card
        """
        pass

    def test_005_click_on_arrows_of_any_league_that_is_collapsed_by_default(self):
        """
        DESCRIPTION: Click on arrows of any league that is collapsed by default
        EXPECTED: - League becomes expandable
        EXPECTED: - 'See all' link becomes visible with the chevron pointing to the right that redirects to competitions of that type
        """
        pass

    def test_006_click_on_see_all_x_link_in_the_in_play_module_header(self):
        """
        DESCRIPTION: Click on 'See All (x)' link in the 'In-Play' module header
        EXPECTED: User is redirected to In-Play page
        """
        pass

    def test_007_click_on_see_all_link_within_the_upcoming_module_with_market_selector(self):
        """
        DESCRIPTION: Click on 'See All' link within the upcoming module (with market selector)
        EXPECTED: User is redirected to Competition page (for football, tennis and basketball only)
        """
        pass

    def test_008_click_on_change_button_in_market_selector_within_module_header(self):
        """
        DESCRIPTION: Click on 'Change' button in market selector within module header
        EXPECTED: - Drop down with other markets available is shown
        EXPECTED: - Chevron points upwards when dropdown is opened
        """
        pass

    def test_009_verify_the_message_on_the_page_when_no_events_are_available(self):
        """
        DESCRIPTION: Verify the message on the page when no events are available
        EXPECTED: "No events found" is displayed in case no events are available
        """
        pass
