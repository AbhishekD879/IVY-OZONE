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
class Test_C60075543_Verify_Market_Selector_sticky_behavior_in_Matches_tab_in_Ice_Hockey_landing_page(Common):
    """
    TR_ID: C60075543
    NAME: Verify 'Market Selector'  sticky behavior in Matches tab in Ice Hockey landing page
    DESCRIPTION: This test case verifies 'Market Selector' sticky behavior on Ice Hockey landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Total Goals 2-way|,|Puck Line|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Ice Hockey landing page -> 'Matches' tab
    PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
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
    """
    keep_browser_open = True

    def test_001_verify_that_market_selector_is_sticky_when_scrolling_the_page_down(self):
        """
        DESCRIPTION: Verify that 'Market Selector' is sticky when scrolling the page down
        EXPECTED: Tablet/Mobile:
        EXPECTED: • 'Market Selector' is sticky. It remains at the top of the scrolling page
        EXPECTED: • Market selector functionality remains the same
        EXPECTED: **Note:**
        EXPECTED: For the Desktop 'Market Selector' is NOT sticky. It becomes hidden together with Date Selector panel
        """
        pass

    def test_002_verify_that_market_selector_is_sticky_when_scrolling_the_page_up(self):
        """
        DESCRIPTION: Verify that 'Market Selector' is sticky when scrolling the page up
        EXPECTED: Tablet/Mobile:
        EXPECTED: • 'Market Selector' is sticky. It remains at the top of the scrolling page
        EXPECTED: • Market selector functionality remains the same
        EXPECTED: **Note:**
        EXPECTED: For the Desktop 'Market Selector' is NOT sticky. It becomes hidden together with Date Selector panel
        """
        pass
