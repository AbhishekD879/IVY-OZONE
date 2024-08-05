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
class Test_C11353994_Verify_liveserve_updates_on_Top_Finish_market(Common):
    """
    TR_ID: C11353994
    NAME: Verify liveserve updates on 'Top Finish' market
    DESCRIPTION: This test case verifies liveserve updates on 'Top Finish' market
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * Horse Racing events with Top Finish 'Top 2 / Top 3 / Top 4' markets (templateMarketName='Top 2 Finish', templateMarketName="Top 3 Finish", templateMarketName="Top 4 Finish") are available
    PRECONDITIONS: * To get information for an event uses the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_navigate_to_edp_and_open_top_finish_market_tab(self):
        """
        DESCRIPTION: Navigate to EDP and open 'Top Finish' market tab
        EXPECTED: 'Top Finish' market tab is opened
        """
        pass

    def test_002_in_ti_change_price_for_one_of_the_selections_with_enabled_liveserve_updates_see_preconditions(self):
        """
        DESCRIPTION: In TI: Change price for one of the selections with enabled liveServe updates (see Preconditions)
        EXPECTED: 
        """
        pass

    def test_003_in_application_observe_changes_on_the_top_finish_market_tab(self):
        """
        DESCRIPTION: In application: observe changes on the 'Top Finish' market tab
        EXPECTED: - Corresponding 'Price/Odds' buttons immediately display new prices and for a few seconds they will change their color to:
        EXPECTED: * blue color if price has decreased
        EXPECTED: * pink color if price has increased
        EXPECTED: - Previous Odds, under Price/Odds button, are updated/added respectively
        """
        pass

    def test_004_in_ti_suspend_market(self):
        """
        DESCRIPTION: In TI: Suspend market
        EXPECTED: 
        """
        pass

    def test_005_in_application_observe_changes_on_the_top_finish_market_tab(self):
        """
        DESCRIPTION: In application: observe changes on the 'Top Finish' market tab
        EXPECTED: All Price/Odds buttons under specific market column are displayed immediately as greyed out and become disabled for selected market but still displaying the prices
        """
        pass

    def test_006_in_ti_suspend_one_of_the_selections_with_enabled_liveserve_updates_see_preconditions(self):
        """
        DESCRIPTION: In TI: Suspend one of the selections with enabled liveServe updates (see Preconditions)
        EXPECTED: 
        """
        pass

    def test_007_in_application_observe_changes_on_the_top_finish_market_tab(self):
        """
        DESCRIPTION: In application: observe changes on the 'Top Finish' market tab
        EXPECTED: Price/Odds button of changed outcome are displayed immediately as greyed out and become disabled
        EXPECTED: The rest outcomes and market tabs are not changed
        """
        pass

    def test_008_in_ti_undisplay_all_top_finish_markets(self):
        """
        DESCRIPTION: In TI: Undisplay all 'Top Finish' markets
        EXPECTED: 
        """
        pass

    def test_009_in_application_observe_changes_on_the_top_finish_market_tab(self):
        """
        DESCRIPTION: In application: observe changes on the 'Top Finish' market tab
        EXPECTED: 'Top Finish' collection tab is available and is empty
        """
        pass

    def test_010_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: 'Top Finish' collection tab disappears
        """
        pass

    def test_011_change_price_format_to_decimal_in_my_account__settings_and_repeat_steps_1___10(self):
        """
        DESCRIPTION: Change price format to Decimal in My Account > Settings and repeat steps 1 - 10
        EXPECTED: 
        """
        pass
