import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.bpp_config import BPPConfig
from random import uniform

from voltron.utils.exceptions.failure_exception import TestFailure


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't grant freebets
# @pytest.mark.hl
@pytest.mark.freebets
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.login
@vtest
class Test_C884014_Verify_Free_Bets_within_Quick_Bet(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C884014
    VOL_ID: C23220556
    NAME: Verify Free Bets within Quick Bet
    DESCRIPTION: This test case verifies Free Bets within Quick Bet
    PRECONDITIONS: 1.  Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2.  Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. The user should have free bets added
    PRECONDITIONS: 4. [How to add Free bets to user`s account] [1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: 5. Open Dev Tools -> Network -> XHR filter to see response of **user** request
    """
    keep_browser_open = True
    bpp_config = BPPConfig()
    free_bet_value = f'{uniform(1, 2):.2f}'

    def verify_free_bet_name_presence(self, name: str):
        result = name in list(self.ui_free_bets.keys())
        self.assertTrue(result, msg=f'Free Bet with name "{name}" '
                                    f'is not present in "{list(self.ui_free_bets.keys())}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        self.__class__.eventID = self.ob_config.add_football_event_to_england_championship().event_id
        market_name = self.ob_config.football_config.england.championship.market_name.replace('|', '')
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

    def test_001_log_in_with_user(self):
        """
        DESCRIPTION: Log in with user
        EXPECTED: * User is logged in
        EXPECTED: * All available Free bets are received in **user** response
        """
        user = tests.settings.freebet_user
        self.ob_config.grant_freebet(username=user, freebet_value=self.free_bet_value)
        self.site.login(username=user)

        bpp_token = self.get_local_storage_cookie_value_as_dict('OX.USER')['bppToken']
        self.__class__.network_freebets = self.bpp_config.get_account_freebets(bpp_user_token=bpp_token)
        self.assertTrue(self.network_freebets, msg=f'There is no freebets token for current user')

    def test_002_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        EXPECTED: * "Use Free Bet" link is displayed under event name
        EXPECTED: * "Place Bet" CTA is inactive, "Add to Betslip" active
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)

        self.__class__.quick_bet = self.site.quick_bet_panel.selection.content
        self.assertTrue(self.quick_bet.has_use_free_bet_link(),
                        msg='Use Free Bet link is not present')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='"Place Bet" is enabled')
        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(),
                        msg='"ADD TO BETSLIP" button is not enabled')

    def test_003_tap_use_free_bet_link(self):
        """
        DESCRIPTION: Tap "Use Free Bet" link
        EXPECTED: * Appears 'FreeBet' Pop up with a list of up available FreeBets with check box
        EXPECTED: * Header of the 'FreeBet' Pop up contains the quantity of available free bets (e.g. Free Bets Available (x1))
        EXPECTED: * Each free bet is displayed in next format:
        EXPECTED: <currency symbol> <free bet value> <Free bet name>
        EXPECTED: where <currency symbol>  - currency set during registration
        EXPECTED: *[From OX100]*
        EXPECTED: * 'ADD' CTA is displayed (inactive):
        """
        self.site.quick_bet_panel.selection.content.amount_form.input.click()  # it's needed to hide pop-up message, don't remove this line
        self.quick_bet.use_free_bet_link.click()

        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE, timeout=3, verify_name=False)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" dialog is not shown')

        self.__class__.ui_free_bets = self.dialog.items_as_ordered_dict
        self.assertTrue(self.ui_free_bets, msg='Free Bets are not available in list')
        self.assertEqual(int(self.dialog.free_bet_number), len(self.ui_free_bets.items()),
                         msg=f'Actual Free Bets Available number "{int(self.dialog.free_bet_number)}" '
                             f'!= Expected "{len(self.ui_free_bets.items())}"')
        self.assertIn(self.get_freebet_name(value=self.free_bet_value), self.ui_free_bets.keys(),
                      msg=f'"{self.get_freebet_name(value=self.free_bet_value)}" was not found in "{self.ui_free_bets.keys()}"')

        self.assertTrue(self.dialog.add_button.is_displayed(), msg='"Add" button is not displayed')
        self.assertFalse(self.dialog.add_button.is_enabled(expected_result=False), msg='"Add" button is enabled')

    def test_004_verify_free_bet_token_name(self):
        """
        DESCRIPTION: Verify Free bet token name
        EXPECTED: Free bet token name corresponds to **freebets.data.[i].freebetOfferName** attribute received in **user** response
        EXPECTED: where i - number of free bets returned in response
        """
        for network_free_bet in self.network_freebets:
            if network_free_bet['freebetOfferName'] == self.freebet_name_template and\
                    network_free_bet['freebetTokenValue'] == self.free_bet_value and\
                    network_free_bet.get('tokenPossibleBet', {}).get('name', '') == self.get_freebet_redemption_name():
                name = f'£{network_free_bet["freebetTokenValue"]} {network_free_bet["freebetOfferName"]}' \
                       f' ({network_free_bet.get("tokenPossibleBet", {}).get("name", "")})'
                self.verify_free_bet_name_presence(name=name)
                break
        else:
            raise TestFailure('Freebet name and value were not verified')

    def test_005_verify_free_bet_token_value(self):
        """
        DESCRIPTION: Verify Free bet token value
        EXPECTED: Free bet token value corresponds to **freebets.data.[i].freebetTokenValue** attribute received in **user** response
        EXPECTED: where i - number of free bets returned in response
        """
        #  is verified in previous step
        pass

    def test_006_select_one_of_the_available_free_bets_from_free_bet_pop_up_and_click_add_button(self):
        """
        DESCRIPTION: Select one of the available Free Bets from Free Bet pop up AND click on 'ADD' button.
        EXPECTED: * Freebet radiobutton is checked for applicable freebet
        EXPECTED: * 'ADD' CTA becomes active:
        EXPECTED: * Pop up is closed after tapping 'ADD' CTA
        EXPECTED: * '- Remove Free Bet' link is displayed under the event name in the 'Quick bet'
        EXPECTED: * Total stake is updated with the Freebet value
        EXPECTED: * Free bet icon is displayed near Freebet value in the total stake
        EXPECTED: * Potential returns/Est returns based on odds taken also updated
        EXPECTED: * Free bet icon below the stake box is displayed in the 'Quick bet'
        """
        self.dialog.select_free_bet(free_bet_name=self.get_freebet_name(value=self.free_bet_value))
        self.assertTrue(self.dialog.wait_dialog_closed(),
                        msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" dialog is not closed')
        self.assertTrue(self.site.quick_bet_panel.selection.content.has_remove_free_bet_link(),
                        msg='"Remove Free Bet" link is not shown')

        expected_stake = f'£{self.free_bet_value}'
        stake = self.site.quick_bet_panel.selection.bet_summary.combined_total_stake
        self.assertEqual(stake, expected_stake,
                         msg=f'Actual Total Stake amount value "{stake}" '
                             f'does not match expected "{expected_stake}"')

        actual_est_returns = self.site.quick_bet_panel.selection.bet_summary.total_estimate_returns
        self.verify_estimated_returns(est_returns=actual_est_returns,
                                      odds=[self.ob_config.event.prices['odds_draw']],
                                      bet_amount=0,
                                      freebet_amount=float(self.free_bet_value))

    def test_007_click_remove_free_bet_link(self):
        """
        DESCRIPTION: Click '- Remove Free Bet' link
        EXPECTED: * The previously selected value is cleared
        EXPECTED: * "Use Free Bet" link appears instead '- Remove Free Bet' link
        """
        quick_bet = self.site.quick_bet_panel.selection.content
        quick_bet.remove_free_bet_link.click()
        self.assertTrue(quick_bet.has_use_free_bet_link(), msg='Use Free Bet link is not present')
