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
class Test_C9608119_Verify_Outright_events_and_markets_on_Basketball_Competition_Details_page_on_Desktop(Common):
    """
    TR_ID: C9608119
    NAME: Verify Outright events and markets on Basketball Competition Details page on Desktop
    DESCRIPTION: This test case verifies Outright events and markets on Basketball Competition Details page on Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: Two different Basketball types should be configured in the following way:
    PRECONDITIONS: 1 type - has one outright event available
    PRECONDITIONS: 2 type - has several outright events available
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Basketball landing page > Competitions tab
    PRECONDITIONS: 3. Expand class accordion under test
    """
    keep_browser_open = True

    def test_001_click_on_1st_type_under_test_see_preconditions(self):
        """
        DESCRIPTION: Click on 1st type under test (see preconditions)
        EXPECTED: * Respective Competition Details page is opened
        """
        pass

    def test_002_choose_outrights_switcher_and_verify_outrights_layout_displaying_for_the_league_with_one_event_available(self):
        """
        DESCRIPTION: Choose 'Outrights' switcher and verify Outrights Layout displaying for the league with one event available
        EXPECTED: The following elements are displayed below 'Outrights' switcher:
        EXPECTED: * Event Name Panel (e.g. '2019 NBA Regular Season')
        EXPECTED: * 'Outrights market' accordion (e.g. 'Award winner')
        EXPECTED: * Markets card
        """
        pass

    def test_003_verify_outrights_market_accordion_displaying(self):
        """
        DESCRIPTION: Verify 'Outrights Market' accordion displaying
        EXPECTED: The following elements are displayed on 'Outrights Market' accordion:
        EXPECTED: * 'Outrights market name' on accordion (e.g. 'Award winner') on the left side
        EXPECTED: * 'Chevron' (Up and Down depends on expanding/collapsing of accordion) on the right side
        EXPECTED: * 'Cashout' icon before the Chevron (if applicable)
        EXPECTED: * The first 'Outrights Market' accordion is expanded by default, the rest are collapsed
        """
        pass

    def test_004_verify_outrights_market_card(self):
        """
        DESCRIPTION: Verify 'Outrights Market' card
        EXPECTED: The following elements are displayed on 'Outrights Market' card:
        EXPECTED: * 'Each Way' terms on the left side of market header (if applicable)
        EXPECTED: * Event start date is shown in **'<name of the day>, DD-MMM-YY 24 hours HH:MM'** (e.g. 14:00 or 05:00) format on the right side of header for every 'Outright market' card
        EXPECTED: * Selection names and 'Price/Odds' buttons in tile view (from left to right order)
        """
        pass

    def test_005_navigate_to_basketball_competition_landing_page_and_click_on_2nd_type_under_test_see_preconditions(self):
        """
        DESCRIPTION: Navigate to Basketball Competition landing page and click on 2nd type under test (see preconditions)
        EXPECTED: Respective Competition Details page is opened
        EXPECTED: The following elements are displayed on the page:
        EXPECTED: * 'Outrights event' accordions (e.g. '2019 NBA Championship', '2019 Atlantic Division', etc.)
        EXPECTED: * Separate markets cards
        """
        pass

    def test_006_verify_outrights_event_accordion(self):
        """
        DESCRIPTION: Verify 'Outrights Event' accordion
        EXPECTED: The following elements are displayed on 'Outrights Event' accordion:
        EXPECTED: * 'Outrights event name' on accordion (e.g. '2019 NBA Championship', '2019 Atlantic Division', etc.) on the left side
        EXPECTED: * 'Chevron' (Up and Down depends on expanding/collapsing of accordion) on the right side
        EXPECTED: * 'Cashout' icon before the Chevron (if applicable)
        """
        pass

    def test_007_verify_outrights_market_cards(self):
        """
        DESCRIPTION: Verify 'Outrights Market' cards
        EXPECTED: * Every market is displayed in the separate 'Outrights Market' card
        EXPECTED: * The following elements are displayed on 'Outrights Market' card:
        EXPECTED: * Name of market (e.g. 'Conference Winner', 'Division Winner', etc.) on the left side of market header
        EXPECTED: * 'Each Way' terms next to 'Market name' (if applicable)
        EXPECTED: * Event start date is shown in **'<name of the day>, DD-MMM-YY 12 hours AM/PM'** format on the right side of header for every 'Outright market' card
        EXPECTED: * Selection names and 'Price/Odds' buttons in tile view (from left to right order)
        """
        pass

    def test_008_verify_content_of_outrights_page_if_there_are_no_available_events(self):
        """
        DESCRIPTION: Verify content of Outrights page if there are no available events
        EXPECTED: "No events found" is displayed in case there are no available events on Outrights page
        """
        pass
