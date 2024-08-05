import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl  - Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.betslip
@pytest.mark.overask
@pytest.mark.slow
@pytest.mark.bet_placement
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C29137_Accepting_traders_offer_with_modified_Odds(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C29137
    NAME: Accepting trader's offer with modified Odds
    DESCRIPTION: This test case verifies accepting trader's offer with modified Odds
    DESCRIPTION: Instruction how modify trader's offer: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955
    PRECONDITIONS: - For selected User Overask functionality is enabled in backoffice tool (see instruction: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983 )
    PRECONDITIONS: - User is logged in to application
    """
    keep_browser_open = True
    username = None

    new_price_1 = '1/7'
    new_price_2 = '3/17'
    new_price_3 = '13/100'
    new_overask_prices = [new_price_1, new_price_2, new_price_3]
    expected_overask_messages = []
    account_id = None
    betslip_id = None
    selection_ids = []
    prices = {0: '1/12'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Events and Login into app
        """
        created_selection_names = []
        self.__class__.event_ids = []
        for i in range(0, 4):
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, max_bet=3, max_mult_bet=3,
                                                              lp_prices=self.prices)
            self.event_ids.append(event_params.event_id)
            created_selection_names.append(list(event_params.selection_ids.keys())[0])
            self.selection_ids.append(list(event_params.selection_ids.values())[0])

        self.__class__.stake_bet_amounts = {
            created_selection_names[2]: self.bet_amount,
            created_selection_names[3]: self.bet_amount + 4
        }
        self.__class__.username = tests.settings.overask_enabled_user
        self.site.login(username=self.username)

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is successfully added
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[:2])

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection(self):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for added selection
        """
        self.__class__.bet_amount = 4

    def test_003_tap_bet_now_button(self, single=False):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: Overask is triggered for the User
        EXPECTED: The bet review notification is shown to the User
        """
        if single:
            self.__class__.account_id, self.__class__.bet_id, self.__class__.betslip_id = \
                self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.event_ids[-1])
        else:
            self.place_multiple_bet(number_of_stakes=1, sp=True)
            self.__class__.expected_betslip_counter_value = 0

            self.__class__.account_id, self.__class__.bet_id, self.__class__.betslip_id = \
                self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.event_ids[0])

        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Overask title message is not shown')
        overask_exceeds_message = self.get_betslip_content().overask.overask_exceeds.is_displayed()
        self.assertTrue(overask_exceeds_message, msg='Overask excedds message is not shown')
        overask_offer_message = self.get_betslip_content().overask.overask_offer.is_displayed()
        self.assertTrue(overask_offer_message, msg='Overask bottom message is not shown')

    def test_004_trigger_odds_modification_by_trader_and_verify_new_odds_value_displaying_in_betslip(self, single=False):
        """
        DESCRIPTION: Trigger Odds modification by Trader and verify new Odds value displaying in Betslip
        EXPECTED: 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: The new Odds value is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: The Estimate returns are updated according to new Odds value
        EXPECTED: 'Cancel' and 'Place a bet' buttons enabled
        """
        if single:
            suggested_max_bet = 2.00
            self.bet_intercept.offer_stake(account_id=self.account_id, bet_id=self.bet_id, betslip_id=self.betslip_id,
                                           max_bet=suggested_max_bet)
        else:
            self.bet_intercept.offer_multiple_prices(account_id=self.account_id, bet_id=self.bet_id,
                                                     betslip_id=self.betslip_id,
                                                     price_1=self.new_price_1, price_2=self.new_price_2,
                                                     price_3=self.new_price_3, max_bet=self.bet_amount)

        overask_trader_message = self.get_betslip_content().overask_trader_section.trader_message
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')
        if single:
            est_returns = self.get_betslip_content().total_estimate_returns
            self.assertNotEqual(est_returns, 'N/A', msg='Est returns is equal "N/A"')
            singles_section = self.get_betslip_sections().Singles
            stake_name, stake = list(singles_section.items())[1]
            self.assertEqual(stake.offered_stake.background_color_value, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                             msg=f'Modified price for "{stake_name}" is not highlighted in yellow')
        else:
            sections = self.get_betslip_sections(multiples=True)
            self.__class__.multiples_section = sections.Multiples
            stakes = self.multiples_section.overask_trader_offer.items_as_ordered_dict
            est_returns = self.multiples_section.overask_trader_offer.stake_content.est_returns
            text = est_returns.value
            self.assertNotEquals(text[1:], 'N/A', msg='The "Est. returns" value is equal "N/A" but should not')

            self.assertTrue(stakes, msg='Cannot find any stakes for Trade Offer')
            for stake_name, stake in stakes.items():
                self.assertEqual(stake.stake_odds.value_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                                 msg=f'Modified price for "{stake_name}" is not highlighted in yellow')

        self.assertTrue(self.get_betslip_content().has_cancel_button(),
                        msg='"Cancel" button is not enabled')
        self.assertTrue(self.get_betslip_content().confirm_overask_offer_button.is_enabled(),
                        msg='"Place Bet" button is not enabled')

    def test_005_tap_accept_bet_number_of_accepted_bets_button(self):
        """
        DESCRIPTION: Tap 'Accept & Bet ([number of accepted bets])'  button
        EXPECTED: The bet is placed as per normal process
        """
        confirm_btn = self.get_betslip_content().confirm_overask_offer_button
        confirm_btn.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_006_add_few_selections_to_the_betslipand_for_one_of_them_enter_stake_value_which_will_trigger_overask_for_the_selection(self):
        """
        DESCRIPTION: Add few selections to the Betslip and for one of them enter stake value which will trigger Overask for the selection
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[2:])
        self.place_single_bet(stake_bet_amounts=self.stake_bet_amounts)

    def test_007_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps 2-5
        EXPECTED: All added selections are placed after Trader Offer confirmation
        """
        self.test_003_tap_bet_now_button(single=True)
        self.test_004_trigger_odds_modification_by_trader_and_verify_new_odds_value_displaying_in_betslip(single=True)
        self.test_005_tap_accept_bet_number_of_accepted_bets_button()
