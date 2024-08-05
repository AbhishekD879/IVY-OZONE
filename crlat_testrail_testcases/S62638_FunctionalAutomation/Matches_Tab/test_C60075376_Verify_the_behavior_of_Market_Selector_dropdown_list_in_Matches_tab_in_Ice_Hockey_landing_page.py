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
class Test_C60075376_Verify_the_behavior_of_Market_Selector_dropdown_list_in_Matches_tab_in_Ice_Hockey_landing_page(Common):
    """
    TR_ID: C60075376
    NAME: Verify the behavior of 'Market Selector' dropdown list in Matches tab in Ice Hockey landing page
    DESCRIPTION: Verify the behavior of 'Market Selector' dropdown list
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Money Line|,|60 Minute betting|,|Total Goals 2-way|,|Puck Line|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Baseball Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: *|Money Line (WW)|- Money Line
    PRECONDITIONS: *|60 Minutes Betting (WDW)|- 60 Minute Betting
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

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Money Line' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Money Line' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Money Line'  in 'Market selector' Coral
        """
        pass

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: • 'Market Selector' dropdown list opens
        EXPECTED: • List of markets are displayed
        EXPECTED: • The chevron near 'Change' button is pointed upwards
        """
        pass

    def test_003_verify_the_behavior_of_the_market_drop_down_list(self):
        """
        DESCRIPTION: Verify the behavior of the market drop down list
        EXPECTED: User should be able to mouse over the markets in the list,The market which is in focus will get highlighted.
        """
        pass

    def test_004_click_on_market_which_is_highlighted(self):
        """
        DESCRIPTION: Click on market which is highlighted
        EXPECTED: selected market should be selected
        """
        pass

    def test_005_clicktap_on_the_change_button_again_and_mouse_over_the_content(self):
        """
        DESCRIPTION: Click/Tap on the 'Change' button again and mouse over the content
        EXPECTED: • 'Market Selector' dropdown list opens
        EXPECTED: • List the Markets will be displayed
        EXPECTED: • The chevron near 'Change' button is pointed upwards
        """
        pass
