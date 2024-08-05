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
class Test_C1203369_Verify_Outright_events_and_markets_on_Competitions_Details_page_on_Desktop(Common):
    """
    TR_ID: C1203369
    NAME: Verify Outright events and markets on Competitions Details page on Desktop
    DESCRIPTION: This test case verifies Outright events and markets on Competitions Details page on Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_football_competitions_details_page(self):
        """
        DESCRIPTION: Navigate to Football Competitions Details page
        EXPECTED: * Competition Details page is opened
        EXPECTED: * 'Matches' and 'Outrights' switchers are displayed below Competitions header and Breadcrumbs trail in the same row as 'Market Selector'
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        """
        pass

    def test_003_choose_outrights_switcher_and_verify_outrights_layout_displaying_for_the_league_with_one_event_available_ie_premier_league_championship_etc(self):
        """
        DESCRIPTION: Choose 'Outrights' switcher and verify Outrights Layout displaying for the league with one event available (i.e. 'Premier League', 'Championship', etc.)
        EXPECTED: The following elements are displayed on the page:
        EXPECTED: * Event Name Panel (i.e. 'Premier League 2017/2018')
        EXPECTED: * 'Outrights market' accordions (i.e. 'Top Goalscorer', 'Top 4 Finish', etc.)
        EXPECTED: * Markets card
        """
        pass

    def test_004_verify_outrights_market_accordion_displaying(self):
        """
        DESCRIPTION: Verify 'Outrights Market' accordion displaying
        EXPECTED: The following elements are displayed on 'Outrights Market' accordion:
        EXPECTED: * 'Outrights market name' on accordion (i.e. 'Top Goalscorer', 'Top 4 Finish', etc.) on the left side
        EXPECTED: * 'Chevron' (Up and Down depends on expanding/collapsing of accordion) on the right side
        EXPECTED: * 'Cashout' icon before the Chevron (if applicable)
        EXPECTED: * The first 'Outrights Market' accordion is expanded by default, the rest are collapsed
        """
        pass

    def test_005_hover_the_mouse_over_the_outrights_market_accordion(self):
        """
        DESCRIPTION: Hover the mouse over the 'Outrights Market' accordion
        EXPECTED: * The background color of accordion is changed
        EXPECTED: * Pointer is changed view from 'Normal select' to 'Link select' for realizing the possibility to click on particular area
        """
        pass

    def test_006_click_on_outrights_market_accordion(self):
        """
        DESCRIPTION: Click on 'Outrights Market' accordion
        EXPECTED: * 'Outrights Market' accordion is expandable/collapsible
        EXPECTED: * 'Outrights Market' card is displayed within the expanded 'Outrights Market' accordion
        """
        pass

    def test_007_verify_outrights_market_card(self):
        """
        DESCRIPTION: Verify 'Outrights Market' card
        EXPECTED: The following elements are displayed on 'Outrights Market' card:
        EXPECTED: * 'Each Way' terms on the left side of market header (if applicable)
        EXPECTED: * Event start date is shown in **'<name of the day>, DD-MMM-YY 24 hours HH:MM'** (e.g. 14:00 or 05:00) format on the right side of header for every 'Outright market' card
        EXPECTED: * Selection names and 'Price/Odds' buttons in tile view (from left to right order)
        """
        pass

    def test_008_hover_the_mouse_over_the_priceodds_button(self):
        """
        DESCRIPTION: Hover the mouse over the 'Price/Odds' button
        EXPECTED: * The background color of 'Price/Odds' button is changed
        EXPECTED: * Pointer is changed view from 'Normal select' to 'Link select' for realizing the possibility to click on particular area
        """
        pass

    def test_009_click_on_priceodds_button(self):
        """
        DESCRIPTION: Click on 'Price/Odds' button
        EXPECTED: * 'Price/Odds' button is clickable
        EXPECTED: * 'Price/Odds' button looks as selected (it changes color to green)
        EXPECTED: * Selection is added to the Betslip
        """
        pass

    def test_010_navigate_to_competitions_details_page_outrights_switcher_that_has_several_outright_events_ie_world_cup_2018_europa_cup_copa_america_etc(self):
        """
        DESCRIPTION: Navigate to Competitions Details page ('Outrights' switcher) that has several Outright events (i.e. 'World Cup 2018', 'Europa Cup', 'Copa America' etc.)
        EXPECTED: The following elements are displayed on the page:
        EXPECTED: * 'Outrights event' accordions (i.e. 'Group A', 'Group B', etc.)
        EXPECTED: * Separate markets cards
        """
        pass

    def test_011_verify_outrights_event_accordion(self):
        """
        DESCRIPTION: Verify 'Outrights Event' accordion
        EXPECTED: The following elements are displayed on 'Outrights Event' accordion:
        EXPECTED: * 'Outrights event name' on accordion (i.e. 'Group A', 'Group B', etc.) on the left side
        EXPECTED: * 'Chevron' (Up and Down depends on expanding/collapsing of accordion) on the right side
        EXPECTED: * 'Cashout' icon before the Chevron (if applicable)
        """
        pass

    def test_012_repeat_steps_5_6_for_outrights_event_accordion(self):
        """
        DESCRIPTION: Repeat steps 5-6 for 'Outrights Event' accordion
        EXPECTED: 
        """
        pass

    def test_013_verify_outrights_market_cards(self):
        """
        DESCRIPTION: Verify 'Outrights Market' cards
        EXPECTED: * Every market is displayed in the separate 'Outrights Market' card
        EXPECTED: * The following elements are displayed on 'Outrights Market' card:
        EXPECTED: * Name of market (i.e. 'Group Winner', 'To Qualify', etc.) on the left side of market header
        EXPECTED: * 'Each Way' terms next to 'Market name' (if applicable)
        EXPECTED: * Event start date is shown in **'<name of the day>, DD-MMM-YY 12 hours AM/PM'** format on the right side of header for every 'Outright market' card
        EXPECTED: * Selection names and 'Price/Odds' buttons in tile view (from left to right order)
        """
        pass

    def test_014_repeat_steps_8_9(self):
        """
        DESCRIPTION: Repeat steps 8-9
        EXPECTED: 
        """
        pass

    def test_015_verify_content_of_outrights_page_if_there_are_no_available_events(self):
        """
        DESCRIPTION: Verify content of Outrights page if there are no available events
        EXPECTED: "No events found" is displayed in case there are no available events on Outrights page
        """
        pass
