import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.build_your_bet
@vtest
class Test_C1391524_Tracking_of_navigation_to_Build_Your_Bet_tab_within_event_detail_pages(Common):
    """
    TR_ID: C1391524
    NAME: Tracking of navigation to 'Build Your Bet' tab within event detail pages
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of user's navigation to 'Build Your Bet'/'Bet Builder' (Coral/Ladbrokes respectively) tab within event detail pages
    PRECONDITIONS: 1. Browser console should be opened
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Navigate to the BYB/Bet Builder section/tab on the Homepage
    """
    keep_browser_open = True

    def test_001_clicktap_on_event_link_within_the_byb_sectiontab(self):
        """
        DESCRIPTION: Click/tap on 'Event' link within the BYB section/tab
        EXPECTED: - Event details page is opened
        EXPECTED: - 'Build Your Bet/Bet Builder' tab is opened by default
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'content-view',
        EXPECTED: 'screen_name' : '<< PAGE URL >>' }
        EXPECTED: )
        """
        pass

    def test_003_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: Football Landing page is opened
        """
        pass

    def test_004_go_to_the_event_details_page_with_the_byb_leagues_with_available_byb_are_marked_with_byb_icon_on_accordion(self):
        """
        DESCRIPTION: Go to the Event details page with the BYB (Leagues with available BYB are marked with BYB icon on accordion)
        EXPECTED: - Event details page is opened
        EXPECTED: - 'Main Markets' tab (Coral)/'All Markets' tab (Ladbrokes) is opened by default
        """
        pass

    def test_005_clicktap_on_build_your_betbet_builder_tab(self):
        """
        DESCRIPTION: Click/tap on 'Build Your Bet/Bet Builder' tab
        EXPECTED: 'Build Your Bet/Bet Builder' tab is opened
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'content-view',
        EXPECTED: 'screen_name' : '<< PAGE URL >>' }
        EXPECTED: )
        """
        pass
