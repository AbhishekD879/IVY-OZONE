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
class Test_C59939740_Verify_WDW_MT_on_Competitions_Tab_for_Rugby_Union(Common):
    """
    TR_ID: C59939740
    NAME: Verify 'WDW’ MT on Competitions Tab for Rugby Union
    DESCRIPTION: This test case verifies displaying of ‘WDW market’ Template is displaying by default for Rugby Union Competition Landing page under Market Selector Dropdown
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Rugby Union-> 'Click on Competition Tab'
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) Below market should be created in OB system using the following Market Template Name:
    PRECONDITIONS: * |Match Betting(WDW)| - "Match Result"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the MS dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to (Matches/Outrights) on the right side
        EXPECTED: • 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Match Result' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Match Result' in 'Market selector' Coral
        """
        pass

    def test_002_tap_on_match_result_from_the_market_selector_dropdown(self):
        """
        DESCRIPTION: Tap on 'Match Result' from the Market Selector dropdown
        EXPECTED: 'Match Result' should be selected
        """
        pass

    def test_003_verify_displaying_of_preplayinplay_or_both_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay/Inplay or both events
        EXPECTED: Events will be displayed as per the below conditions
        EXPECTED: Match Result (Preplay and Inplay)
        EXPECTED: Note:
        EXPECTED: If the market is preplay only preplay events will display
        EXPECTED: If the market is Inplay only Inplay events will display
        EXPECTED: If the market is both then both Preplay and Inplay events will display
        """
        pass

    def test_004_verify_text_of_the_labels_for_match_result(self):
        """
        DESCRIPTION: Verify text of the labels for 'Match Result
        EXPECTED: • The events for the Match Result market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'Home' 'Draw' 'Away' and corresponding Odds are present under Labels Home Draw Away
        """
        pass

    def test_005_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Preplay: Team names, date, time, watch signposting, "XX More" markets link are present
        EXPECTED: • Inplay: Team names, date,timer,scoreline,watch live/Live signposting, "XX More" markets link are present
        """
        pass

    def test_006_verify_ga_tracking_for_the_match_result(self):
        """
        DESCRIPTION: Verify GA Tracking for the 'Match Result'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Match Result"
        EXPECTED: categoryID: "31"
        EXPECTED: })
        """
        pass