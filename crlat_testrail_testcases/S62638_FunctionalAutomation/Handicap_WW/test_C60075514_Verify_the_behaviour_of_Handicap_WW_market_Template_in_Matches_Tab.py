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
class Test_C60075514_Verify_the_behaviour_of_Handicap_WW_market_Template_in_Matches_Tab(Common):
    """
    TR_ID: C60075514
    NAME: Verify the behaviour of ‘Handicap WW market’ Template in Matches Tab
    DESCRIPTION: This test case verifies displaying of ‘Handicap WW market’ Template is beaviour in Matches tab
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Total Goals 2-way|,|Puck Line|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Ice Hockey Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) 1) The set of markets should be created in OB system with different 'HandicapValue' (2,2.5,3)etc  using the following Market Template Names:
    PRECONDITIONS: *|Puck Line (Handicap)| - "Puck Line"
    PRECONDITIONS: *|Total Goals 2-way (Over/Under)| - "Total Goals 2-way"
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
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • Primary Market is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Puck Line' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Puck Line' in 'Market selector' Coral
        """
        pass

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets:
        EXPECTED: *Puck Line
        EXPECTED: *Total Goals 2-way
        """
        pass

    def test_003_select_puck_line_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Puck Line' in the 'Market Selector' dropdown list
        EXPECTED: Events for the most favorable market is shown based on the below condition:
        EXPECTED: a) Based on the disporder in OB for Market(- to + )value will get the priority.
        EXPECTED: b) When the display order is same for all the markets, then the market with least handicap value will be displayed.
        EXPECTED: • Values(Labels) on fixture header are changed for each event according to selected market.
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        EXPECTED: a) Handicap value will be displayed in blue color above the odds value in the same box
        EXPECTED: b) If it is a handicap market template then one positive and one negative handicap value will be displayed above the odds.
        EXPECTED: c) If it is an Over/Under market template then both handicap values will be positive which will be displayed above the odds.
        EXPECTED: Note- When multiple markets are created for the any handicap market , then user should be able to see one market for each market type in landing page and in EDP page whole list will be displayed with all the different handicap values for that particular market.
        """
        pass

    def test_004_verify_text_of_the_labels_for_puck_line(self):
        """
        DESCRIPTION: Verify text of the labels for 'Puck Line'
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Labels  '1' & '2'
        """
        pass

    def test_005_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: Team names, date, time, watch signposting, "XX More" markets link are present
        """
        pass

    def test_006_verify_ga_tracking_for_the_puck_line(self):
        """
        DESCRIPTION: Verify GA Tracking for the 'Puck Line'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Puck Line"
        EXPECTED: categoryID: "22"
        EXPECTED: })
        """
        pass

    def test_007_repeat_steps_3_7_for_the_below_markettotal_goals_2_wayexcept_step4(self):
        """
        DESCRIPTION: Repeat steps 3-7 for the below market:
        DESCRIPTION: Total Goals 2-way
        DESCRIPTION: (Except step4)
        EXPECTED: 
        """
        pass

    def test_008_verify_text_of_the_labels_for_total_goals_2_way(self):
        """
        DESCRIPTION: Verify text of the labels for 'Total Goals 2-way
        EXPECTED: Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Labels 'Over' & 'Under'
        """
        pass
