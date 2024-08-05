import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.p3
@pytest.mark.betslip
@vtest
class Test_C44870418__Verify_Display_of_betslip_header_it_should_have____Betslip____My_Bets__Cash_Out______________Open_Bets______________Settled_Bets(Common):
    """
    TR_ID: C44870418
    NAME: "-Verify Display of betslip header,  it should have        Betslip        My Bets --> Cash Out                           Open Bets                           Settled Bets"
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User is logged in
        """
        self.site.login()

    def test_001_verify_betslip_header_should_havebetslip________my_bets____cash_out___________________________open_bets___________________________settled_bets(self):
        """
        DESCRIPTION: Verify Betslip header should have
        DESCRIPTION: Betslip        My Bets --> Cash Out                           Open Bets                           Settled Bets"
        EXPECTED: User Sees Following Bet slip headers in Tab.
        EXPECTED: Betslip     My Bets (Sub Headers:  Cash Out, Open Bets, Settled Bets)
        """
        betslip_headers = list(self.site.betslip.betslip_tabs.items_as_ordered_dict)
        expected_headers = [vec.BetHistory.BET_SLIP_TAB_NAME.replace(" ", ""), vec.BetHistory.TAB_TITLE.upper()]
        self.assertEqual(betslip_headers, expected_headers,
                         msg=f'Actual tab: "{betslip_headers}" is not as'
                             f'Expected tab: "{expected_headers}"')
        self.site.open_my_bets()
        tabs = self.site.betslip.tabs_menu.items_names
        self.assertTrue(tabs, msg='Tabs are not found')
        for tab in tabs:
            if self.brand == 'ladbrokes':
                if tab == vec.bet_history.CASH_OUT_TAB_NAME:
                    continue
                self.assertIn(tab,
                              [vec.bet_history.OPEN_BETS_TAB_NAME, vec.bet_history.SETTLED_BETS_TAB_NAME, vec.bet_history.IN_SHOP_BETS_TAB_NAME],
                              msg=f'Tab "{tab}"is not found in "{[vec.bet_history.OPEN_BETS_TAB_NAME, vec.bet_history.SETTLED_BETS_TAB_NAME, vec.bet_history.IN_SHOP_BETS_TAB_NAME]}"')
            else:
                self.assertIn(tab,
                              [vec.bet_history.CASH_OUT_TAB_NAME, vec.bet_history.OPEN_BETS_TAB_NAME, vec.bet_history.SETTLED_BETS_TAB_NAME, vec.bet_history.IN_SHOP_BETS_TAB_NAME],
                              msg=f'Tab "{tab}"is not found in "{[vec.bet_history.CASH_OUT_TAB_NAME, vec.bet_history.OPEN_BETS_TAB_NAME, vec.bet_history.SETTLED_BETS_TAB_NAME], vec.bet_history.IN_SHOP_BETS_TAB_NAME}"')
