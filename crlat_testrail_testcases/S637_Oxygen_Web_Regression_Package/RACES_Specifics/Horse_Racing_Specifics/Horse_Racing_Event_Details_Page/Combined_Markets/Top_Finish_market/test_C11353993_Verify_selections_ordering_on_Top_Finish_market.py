import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C11353993_Verify_selections_ordering_on_Top_Finish_market(Common):
    """
    TR_ID: C11353993
    NAME: Verify selections ordering on 'Top Finish' market
    DESCRIPTION: This test case verifies selections ordering on 'Top Finish' market
    PRECONDITIONS: Horse Racing events with Top Finish 'Top 2 / Top 3 / Top 4' markets (templateMarketName='Top 2 Finish', templateMarketName="Top 3 Finish", templateMarketName="Top 4 Finish") are available
    PRECONDITIONS: To get information for an event uses the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_navigate_to_edp_and_open_top_finish_market_tab(self):
        """
        DESCRIPTION: Navigate to EDP and open 'Top Finish' market tab
        EXPECTED: 'Top Finish' market tab is opened
        """
        pass

    def test_002_verify_top_finish_market_headers(self):
        """
        DESCRIPTION: Verify 'Top Finish' market headers
        EXPECTED: 'TOP 2' 'TOP 3' 'TOP 4' market headers are displayed
        """
        pass

    def test_003_verify_selections(self):
        """
        DESCRIPTION: Verify selections
        EXPECTED: * Available selections are displayed in the grid, odds of each are shown in correct market section (TOP 2, TOP 3, TOP 4)
        EXPECTED: * Selection name, runner number, silks and trainer are displayed for each selection (if available)
        EXPECTED: * If some markets are not created or do not contain at least 1 available selection - their header is not displayed
        EXPECTED: * Odds on 'Odds/Prices' buttons are displayed in fractional format by default
        """
        pass

    def test_004_verify_selections_ordering(self):
        """
        DESCRIPTION: Verify selections ordering
        EXPECTED: * Selections are ordered by odds in first available market (e.g. TOP 2/TOP 3/TOP 4) in ascending order (lowest to highest)
        EXPECTED: * If odds of selections are the same -> display by runnerNumber (in ascending order)
        EXPECTED: * If prices are absent for selections - display by runnerNumber (in ascending order)
        """
        pass

    def test_005_change_price_format_to_decimal_in_my_account__settings_and_repeat_steps_1___4(self):
        """
        DESCRIPTION: Change price format to Decimal in My Account > Settings and repeat steps 1 - 4
        EXPECTED: 
        """
        pass
