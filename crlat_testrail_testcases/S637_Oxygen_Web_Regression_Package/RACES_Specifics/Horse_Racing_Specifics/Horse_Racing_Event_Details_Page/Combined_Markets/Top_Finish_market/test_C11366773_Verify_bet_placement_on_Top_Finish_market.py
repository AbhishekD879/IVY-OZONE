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
class Test_C11366773_Verify_bet_placement_on_Top_Finish_market(Common):
    """
    TR_ID: C11366773
    NAME: Verify bet placement on 'Top Finish' market
    DESCRIPTION: This test case verifies bet placement on 'Top Finish' market
    PRECONDITIONS: * Horse Racing events with Top Finish 'Top 2 / Top 3 / Top 4' markets (templateMarketName='Top 2 Finish', templateMarketName="Top 3 Finish", templateMarketName="Top 4 Finish") are available
    PRECONDITIONS: * To get information for an event uses the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_login(self):
        """
        DESCRIPTION: Login
        EXPECTED: User is logged in
        """
        pass

    def test_002_navigate_to_edp_and_open_top_finish_market_tab(self):
        """
        DESCRIPTION: Navigate to EDP and open 'Top Finish' market tab
        EXPECTED: 'Top Finish' market tab is opened
        """
        pass

    def test_003_for_mobileclick_on_a_bet_button_of_one_of_the_selections(self):
        """
        DESCRIPTION: For mobile:
        DESCRIPTION: Click on a bet button of one of the selections
        EXPECTED: Quick bet overlay is opened
        EXPECTED: Odds are shown in fractional format
        """
        pass

    def test_004_for_mobileenter_stake_and_place_bet(self):
        """
        DESCRIPTION: For mobile:
        DESCRIPTION: Enter stake and place bet
        EXPECTED: Bet is placed. Bet receipt is displayed
        EXPECTED: Balance is decreased by stake amount
        """
        pass

    def test_005_click_on_a_bet_button_of_one_of_the_selections(self):
        """
        DESCRIPTION: Click on a bet button of one of the selections
        EXPECTED: For mobile:
        EXPECTED: Quick bet overlay is opened
        EXPECTED: For desktop:
        EXPECTED: Selection is added to the Betslip
        """
        pass

    def test_006_for_mobileclick_on_add_to_betslip_button(self):
        """
        DESCRIPTION: For mobile:
        DESCRIPTION: Click on 'Add to Betslip' button
        EXPECTED: Quick bet overlay is closed
        EXPECTED: Betslip counter is 1
        """
        pass

    def test_007_open_betslip_enter_stake_and_press_bet_now(self):
        """
        DESCRIPTION: Open betslip, enter stake and press 'Bet Now'
        EXPECTED: Bet receipt is displayed
        EXPECTED: Odds are shown in fractional format
        EXPECTED: Balance is decreased by stake amount
        """
        pass

    def test_008_change_price_format_to_decimal_in_my_account__settings_and_repeat_steps_2_7(self):
        """
        DESCRIPTION: Change price format to Decimal in My Account > Settings and repeat steps 2-7
        EXPECTED: 
        """
        pass
