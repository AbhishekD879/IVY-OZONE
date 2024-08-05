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
class Test_C60075382_Verify_WDW_market_Template_is_displaying_for_Ice_Hockey_Competition_page_under_Market_Selector_Dropdown(Common):
    """
    TR_ID: C60075382
    NAME: Verify ‘WDW market’ Template is displaying for Ice Hockey Competition page  under Market Selector Dropdown
    DESCRIPTION: This test case verifies displaying of ‘WDW market’ Template is displaying for Ice Hockey Competition page under Market Selector Dropdown
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |60 Minutes Betting|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Ice Hockey Landing Page -> 'Click on Competition Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: *|60 Minutes Betting (WDW)|- "60 Minutes Betting"
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
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • Market Selector' is displayed next to (Matches/Outrights) on the right side
        EXPECTED: • '60 Minutes Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to '60 Minutes Betting' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to '60 Minutes Betting' in 'Market selector' Coral
        """
        pass

    def test_002_verify_text_of_the_labels_for_60_minutes_betting(self):
        """
        DESCRIPTION: Verify text of the labels for '60 Minutes Betting'
        EXPECTED: • The events for the '60 Minutes Betting' market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' , 'Tie' & '2' and corresponding Odds are present under Label 1 , tie and 2.
        """
        pass

    def test_003_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: •Preplay: Team names, date, time, watch signposting, "XX More" markets link are present
        EXPECTED: •Inplay: Team names, date,timer,scoreline,watch live/Live signposting, "XX More" markets link are present
        """
        pass

    def test_004_verify_displaying_of_preplay_and_inplay_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay and Inplay events
        EXPECTED: Events will be displayed as per the below conditions
        EXPECTED: • 60 Minutes Betting (Preplay and Inplay market)
        EXPECTED: Note:
        EXPECTED: If the market is preplay only preplay events will display
        EXPECTED: If the market is Inplay only Inplay events will display
        EXPECTED: If the market is both then both Preplay and Inplay events will display
        """
        pass

    def test_005_verify_ga_tracking_for_the_60_minutes_betting(self):
        """
        DESCRIPTION: Verify GA Tracking for the '60 Minutes Betting'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "60 Minutes Betting"
        EXPECTED: categoryID: "22"
        EXPECTED: })
        """
        pass
