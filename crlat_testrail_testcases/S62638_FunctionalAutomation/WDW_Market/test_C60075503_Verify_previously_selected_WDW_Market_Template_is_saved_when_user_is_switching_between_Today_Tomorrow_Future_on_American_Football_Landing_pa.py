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
class Test_C60075503_Verify_previously_selected_WDW_Market_Template_is_saved_when_user_is_switching_between_Today_Tomorrow_Future_on_American_Football_Landing_page(Common):
    """
    TR_ID: C60075503
    NAME: Verify previously selected ‘WDW Market’ Template is saved when user is switching between Today/Tomorrow/Future on American Football Landing page
    DESCRIPTION: This test case verifies that previously selected ‘WDW Market’ Template is saved when user is switching between Today/Tomorrow/Future on American Football Landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the American Football Landing page -> 'Matches' tab
    PRECONDITIONS: 3. Select the 'Today' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) Below market should be created in OB system using the following Market Template Name:
    PRECONDITIONS: * |60 Minute Betting(WDW)| - "60 Minute Betting"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: • 'Market Selector' is displayed next to Days Selector on the right side
        EXPECTED: • '60 Minute Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to '60 Minute Betting'
        EXPECTED: **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to '60 Minute Betting' in 'Market selector' **Coral**
        """
        pass

    def test_002_verify_displaying_of_preplay_events_for_60_minute_betting(self):
        """
        DESCRIPTION: Verify displaying of Preplay events for '60 Minute Betting'
        EXPECTED: Only Preplay events should display
        """
        pass

    def test_003_verify_text_of_the_labels_for_60_minute_betting(self):
        """
        DESCRIPTION: Verify text of the labels for '60 Minute Betting'
        EXPECTED: • The events for the 60 Minute Betting market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' 'Tie' '2' and corresponding Odds are present under Label 1 Tie 2.
        """
        pass

    def test_004_verify_ga_tracking_for_the_60_minute_betting(self):
        """
        DESCRIPTION: Verify GA Tracking for the '60 Minute Betting'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "60 Minute Betting"
        EXPECTED: categoryID: "1"
        EXPECTED: })
        """
        pass

    def test_005_switch_to_the_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: 60 Minute Betting)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' 'Tie' '2' and corresponding Odds are present under Label 1 Tie 2
        EXPECTED: Note: If there are no events Market Selector dropdown should not display and 'No events found' msg should display(Applies to Today/Tomorrow/Future)
        """
        pass

    def test_006_repeat_steps_34(self):
        """
        DESCRIPTION: Repeat steps 3,4
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_345_for_the_future_tab(self):
        """
        DESCRIPTION: Repeat steps 3,4,5 for the 'Future' tab
        EXPECTED: 
        """
        pass

    def test_008_switch_back_to_today_tab(self):
        """
        DESCRIPTION: Switch back to 'Today' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' 'Tie' '2' and corresponding Odds are present under Label 1 Tie 2
        """
        pass
