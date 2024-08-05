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
class Test_C11386071_Verify_selections_ordering_on_Place_Insurance_market(Common):
    """
    TR_ID: C11386071
    NAME: Verify selections ordering on 'Place Insurance' market
    DESCRIPTION: This test case verifies selections ordering on 'Place Insurance' market
    PRECONDITIONS: 1) Horse Racing events with 'Place Insurance': '2ND'/ 3RD / 4TH' markets (templateMarketName='Insurance 2 Places', templateMarketName="Insurance 3 Places", templateMarketName="Insurance 4 Places") are available
    PRECONDITIONS: 2) To observe LiveServe changes make sure:
    PRECONDITIONS: - LiveServ updates is checked on 'Class' and 'Type' levels in TI
    PRECONDITIONS: - 'Bet In Play List' flag is checked on 'Event' level in TI
    PRECONDITIONS: - 'Bet in Running' is checked on 'Market' level in TI
    PRECONDITIONS: 3) To get information for an event uses the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE Place Insurance markets are combined into 1 tab only for Coral. On Ladbrokes each market is displayed  in separate tab** (https://jira.egalacoral.com/browse/BMA-37026)
    """
    keep_browser_open = True

    def test_001_navigate_to_edp_and_open_place_insurance_market_tab(self):
        """
        DESCRIPTION: Navigate to EDP and open 'Place Insurance' market tab
        EXPECTED: 'Place Insurance' market tab is opened:
        """
        pass

    def test_002_verify_place_insurance_market_headers_coral(self):
        """
        DESCRIPTION: Verify 'Place Insurance' market headers (Coral)
        EXPECTED: 2ND 3RD 4TH 'Place Insurance' market headers are displayed
        """
        pass

    def test_003_verify_selections(self):
        """
        DESCRIPTION: Verify selections
        EXPECTED: * Coral: Available selections are displayed in the grid, odds of each are shown in correct market section (2ND, 3RD, 4TH)
        EXPECTED: Ladbrokes: Available selections in each tab are displayed in the list
        EXPECTED: * Selection name, runner number, silks and trainer are displayed for each selection (if available)
        EXPECTED: * Coral: If some markets are not created or do not contain at least 1 available selection - their header is not displayed
        EXPECTED: * Odds on 'Odds/Prices' buttons are displayed in fractional format by default
        """
        pass

    def test_004_verify_selections_ordering(self):
        """
        DESCRIPTION: Verify selections ordering
        EXPECTED: * Selections are ordered by odds in first available market (e.g. 2ND/3RD/4TH) in ascending order (lowest to highest)
        EXPECTED: * If odds of selections are the same -> display alphabetically by horse name (in ascending order)
        EXPECTED: * If prices are absent for selections - display alphabetically by horse name (in ascending order)
        """
        pass

    def test_005_change_price_format_to_decimal_in_my_account__settings_and_repeat_steps_1___4(self):
        """
        DESCRIPTION: Change price format to Decimal in My Account > Settings and repeat steps 1 - 4
        EXPECTED: 
        """
        pass
