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
class Test_C493192_Verify_content_of_YourCall_Special_Markets_on_Sports_Event_Details_Page(Common):
    """
    TR_ID: C493192
    NAME: Verify content of #YourCall Special Markets on Sport's Event Details Page
    DESCRIPTION: This test case verifies content of #YourCall Special Markets on Sport's Event Details Page
    DESCRIPTION: Note: #YourCall - Coral
    DESCRIPTION: #GetAPrice - Ladbrokes
    PRECONDITIONS: 1) To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) In order to add new market use ti tool http://backoffice-tst2.coral.co.uk/ti/
    PRECONDITIONS: 3) In order to create new market use |YourCallSpecials| Market Template in ti tool
    PRECONDITIONS: 4) For Featured selections |Featured| market must be created using |YourCallSpecials| Market Template. All selections for this Market will be considered as Featured selections.
    PRECONDITIONS: 5) Position (tab of displaying) of #YourCallMarkets is depending on TI settings for |YourCallSpecials| Market Template
    PRECONDITIONS: 6) There is no restriction for selections displaying within Markets depending on price range on front-end side, all should be configured properly in TI Tool by Traders team
    PRECONDITIONS: 7) |YourCallSpecials| market template is available in TI tool for the following Football leagues:
    PRECONDITIONS: **Test 2:**
    PRECONDITIONS: Premier League - 597276
    PRECONDITIONS: La Liga - 599078
    PRECONDITIONS: Serie A - 599077
    PRECONDITIONS: Champions League - 599079
    PRECONDITIONS: **Stage:**
    PRECONDITIONS: Premier League 832526
    PRECONDITIONS: La Liga 832527
    PRECONDITIONS: Serie A 832528
    PRECONDITIONS: Champions League 832529
    PRECONDITIONS: **Production:**
    PRECONDITIONS: Premier League - 2308603
    PRECONDITIONS: La Liga - 2308604
    PRECONDITIONS: Serie A - 2308606
    PRECONDITIONS: Champions League - 2308607
    PRECONDITIONS: 8) |YourCallSpecials| market template is available in TI tool for the following leagues:
    PRECONDITIONS: NFL (American Football)
    PRECONDITIONS: NBA (Basketball)
    PRECONDITIONS: MLB (Baseball)
    PRECONDITIONS: AFL (Aussie Rules)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_event_details_page_of_sports_event(self):
        """
        DESCRIPTION: Navigate to Event Details page of Sport's event
        EXPECTED: * Event Details page is opened successfully representing available markets
        EXPECTED: * 'Main Markets' tab is selected by default
        """
        pass

    def test_003_choose_all_markets_tab(self):
        """
        DESCRIPTION: Choose 'All Markets' tab
        EXPECTED: * 'All Markets' tab is selected
        EXPECTED: * List of all available markets received in response from OB is displayed
        """
        pass

    def test_004_find_any_of_yourcall_market_accordions(self):
        """
        DESCRIPTION: Find any of '#YourCall' market accordions
        EXPECTED: * '#YourCall' market accordion is present on Event Details Page;
        """
        pass

    def test_005_expand_yourcall_market_accordion(self):
        """
        DESCRIPTION: Expand '#YourCall' market accordion
        EXPECTED: Market is expanded, List of all available selections that are received in response from OB is displayed;
        EXPECTED: * The name of selection is displayed on the left side of card
        EXPECTED: * The text displayed within the selection extends to more than one line and not truncated
        """
        pass
