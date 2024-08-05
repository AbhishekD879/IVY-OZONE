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
class Test_C60079460_Verify_previously_selected_WW_Market_Template_is_saved_when_user_is_switching_between_Today_Tomorrow_Future_on_Volleyball_landing_page(Common):
    """
    TR_ID: C60079460
    NAME: Verify previously selected ‘WW Market’ Template is saved when user is switching between Today/Tomorrow/Future on Volleyball  landing page
    DESCRIPTION: This test case verifies that previously selected ‘WW Market’ Template is saved when user is switching between Today/Tomorrow/Future on Volleyball landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Match Betting|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Volleyball Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: |Match Betting (WW)| - "Match Result"
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
        EXPECTED: • 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Match Result' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Match Result' in 'Market selector' **Coral**
        """
        pass

    def test_002_verify_displaying_of_preplay_events_for_match_result(self):
        """
        DESCRIPTION: Verify displaying of Preplay events for 'Match Result'
        EXPECTED: Preplay events should be displayed
        EXPECTED: Note: If there are no events Market Selector dropdown should not display
        """
        pass

    def test_003_verify_text_of_the_labels_for_match_result(self):
        """
        DESCRIPTION: Verify text of the labels for 'Match Result'
        EXPECTED: • The events for the Match Result market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        """
        pass

    def test_004_switch_to_the_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: Match Result)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        EXPECTED: Note:
        EXPECTED: If there are no events Market Selector dropdown should not display and 'No events found' msg should display(Applies to Today/Tomorrow/Future)
        """
        pass

    def test_005_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_34_for_the_future_tab(self):
        """
        DESCRIPTION: Repeat steps 3,4 for the 'Future' tab
        EXPECTED: 
        """
        pass

    def test_007_switch_back_to_today_tab(self):
        """
        DESCRIPTION: Switch back to 'Today' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2
        """
        pass
