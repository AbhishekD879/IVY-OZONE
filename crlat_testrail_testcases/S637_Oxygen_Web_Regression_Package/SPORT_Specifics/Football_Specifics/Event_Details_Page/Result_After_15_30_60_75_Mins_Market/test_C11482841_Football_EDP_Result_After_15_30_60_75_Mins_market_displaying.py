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
class Test_C11482841_Football_EDP_Result_After_15_30_60_75_Mins_market_displaying(Common):
    """
    TR_ID: C11482841
    NAME: Football EDP: 'Result After 15, 30, 60 & 75 Mins' market displaying
    DESCRIPTION: This test case verifies displaying 'Result After 15, 30, 60 & 75 Mins' market based on '15 Minutes Betting', '30 Minutes Betting', '60 Minutes Betting', '75 Minutes Betting' market templates
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have an active Football event with active markets added from '15 Minutes Betting', '30 Minutes Betting', '60 Minutes Betting', '75 Minutes Betting' market templates and with added selections
    PRECONDITIONS: - You should be on event details page
    """
    keep_browser_open = True

    def test_001_verify_result_after_15_30_60__75_mins_market_displaying(self):
        """
        DESCRIPTION: Verify 'Result After 15, 30, 60 & 75 Mins' market displaying
        EXPECTED: - 'Result After 15, 30, 60 & 75 Mins' market accordeon is displayed
        EXPECTED: - The market includes 4 tabs: '15 Mins', '30 Mins', '60 Mins', '75 Mins'
        EXPECTED: - '15 Mins' tab is selected by default
        """
        pass

    def test_002_collapse_and_expand_the_accordeon(self):
        """
        DESCRIPTION: Collapse and expand the accordeon
        EXPECTED: Accordeon is collapsable and expandable
        """
        pass

    def test_003_switch_between_15_mins_30_mins_60_mins_75_mins_tabs_and_verify_selections_displaying(self):
        """
        DESCRIPTION: Switch between '15 Mins', '30 Mins', '60 Mins', '75 Mins' tabs and verify selections displaying
        EXPECTED: Each tab includes selections from respective market
        """
        pass

    def test_004___in_ti_tool_undisplay_one_of_the_markets_eg_75_minutes_betting__in_application_refresh_the_page_and_tap_the_tab_of_the_undisplayed_market__verify_displaying_of_the_selections(self):
        """
        DESCRIPTION: - In TI tool undisplay one of the markets (e.g. '75 Minutes Betting')
        DESCRIPTION: - In application refresh the page and tap the tab of the undisplayed market
        DESCRIPTION: - Verify displaying of the selections
        EXPECTED: 'No events found' message is displayed instead of the selections
        """
        pass
