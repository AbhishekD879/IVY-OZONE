import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.overask
@pytest.mark.uat
@pytest.mark.medium
@vtest
class Test_C59898488_Counter_offer_by_stake_an_OA_bet_placed_with_an_Odds_boost_token(BaseBetSlipTest):
    """
    TR_ID: C59898488
    NAME: Counter offer by stake an OA bet placed with an Odds boost token
    PRECONDITIONS: You should have an Odds Boost token to use
    """
    keep_browser_open = True
    max_bet = 0.2
    suggested_max_bet = 0.25
    prices = {0: '1/2', 1: '1/10', 2: '1/9'}
    username = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            self.cms_config.update_odds_boost_config(enabled=True)
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices,
                                                                                 default_market_name='|Draw No Bet|',
                                                                                 max_bet=self.max_bet)
        self.__class__.eventID = event_params.event_id
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.event_name = event_params.team1
        if self.username is None:
            self.__class__.username = tests.settings.betplacement_user
            self.site.login(self.username, async_close_dialogs=False)
            self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.selection_id)

    def test_001_add_a_selection_to_bet_slip_or_quick_bet_boost_your_odds_and_trigger_overask(self, validate_odds_boost=True):
        """
        DESCRIPTION: Add a selection to bet slip or Quick Bet, boost your odds and trigger Overask.
        EXPECTED: Your bet should have entered the Overask flow.
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        selections = self.get_betslip_sections().Singles
        self.assertTrue(selections, msg=f'"{selections}" is not added to the betslip')
        if validate_odds_boost:
            odds_boost_header = self.get_betslip_content().odds_boost_header
            self.assertTrue(odds_boost_header.boost_button.is_displayed(),
                            msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not displayed')
            odds_boost_header.boost_button.click()
            odds_boost_header = self.get_betslip_content().odds_boost_header
            result = wait_for_result(lambda: odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                     name='"BOOST" button to become "BOOSTED" button with animation',
                                     timeout=2)
            self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')

            stake = list(selections.values())[0]
            self.__class__.new_price = stake.boosted_odds_container.price_value
        self.__class__.bet_amount = self.max_bet + 0.5
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_in_ti_counter_offer_bet_by_stake(self):
        """
        DESCRIPTION: In TI, counter offer bet by stake.
        EXPECTED: You should have given a counter offer by stake.
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.suggested_max_bet)
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=10)
        self.assertFalse(overask, msg='Overask is not closed')

        cms_overask_trader_message = self.get_overask_trader_offer()
        overask_trader_message = self.get_betslip_content().overask_trader_section.trader_message
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')

    def test_003_in_the_front_end_verify_that_you_see_the_new_stake_and_that_it_is_highlighted_in_yellow_and_that_the_new_potential_returns_are_correct(self):
        """
        DESCRIPTION: In the front end, verify that you see the new stake and that it is highlighted in yellow and that the new potential returns are correct.
        EXPECTED: The counter offer should show the new stake and it should be highlighted in yellow and the new potential returns should be correct.
        """
        sections = self.get_betslip_sections().Singles
        self.__class__.amount = float((sections.overask_trader_offer.stake_content.stake_value.value).strip('£'))
        self.assertEqual(self.amount, self.suggested_max_bet,
                         msg=f'The value of suggested stake "{self.suggested_max_bet}" is not present in '
                             f'the "Stake" field, the value is: "{self.amount}"')
        self.assertEqual(sections.overask_trader_offer.stake_content.stake_value.value_color,
                         vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg=f'Modified price for stake is not highlighted in yellow')
        self.__class__.expected_return = self.get_betslip_content().total_estimate_returns
        self.verify_estimated_returns(est_returns=self.expected_return, bet_amount=self.amount, odds=self.new_price)

    def test_004_if_you_accept_the_bet_then_you_should_see_the_bet_receipt_with_the_new_stake_and_correct_potential_returns_and_the_bet_should_be_in_my_bets_open_bets(self):
        """
        DESCRIPTION: If you accept the bet, then you should see the bet receipt, with the new stake and correct potential returns, and the bet should be in My Bets->Open Bets
        EXPECTED: You should see the bet receipt and the bet should be seen in My Bets->Open Bets.
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        actual_stake = self.site.bet_receipt.footer.total_stake
        actual_est_returns = self.site.bet_receipt.footer.total_estimate_returns
        self.assertEqual(actual_stake, str(self.amount),
                         msg=f'Actual stake: "{actual_stake}" is not same as '
                             f'Expected stake:"{str(self.amount)}"')
        self.assertEqual(actual_est_returns, self.expected_return,
                         msg=f'Actual Returns: "{actual_est_returns}" is not same as '
                             f'Expected Returns:"{self.expected_return}"')
        self.site.bet_receipt.close_button.click()

        self.site.open_my_bets_open_bets()
        open_bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(open_bets,
                        msg='No bets found in open bet')
        bet = list(open_bets.values())[0]
        actual_stake = bet.stake.stake_value
        self.assertEqual(actual_stake, str(self.amount),
                         msg=f'Actual stake: "{actual_stake}" is not same as '
                             f'Expected stake:"{str(self.amount)}"')

    def test_005_if_you_decline_the_counter_offer_then_the_counter_offer_should_close_and_no_bet_should_have_been_placed_check_the_my_bets_open_bets_and_verify_there_is_no_sign_of_this_bet_there(self):
        """
        DESCRIPTION: If you decline the counter offer, then the counter offer should close and no bet should have been placed. Check the My Bets->Open Bets and verify there is no sign of this 'bet' there.
        EXPECTED: The counter offer should close and the bet should not have been placed and no bet should appear in My Bets->Open Bets.
        """
        self.site.go_to_home_page()
        self.test_000_preconditions()
        self.test_001_add_a_selection_to_bet_slip_or_quick_bet_boost_your_odds_and_trigger_overask(validate_odds_boost=False)
        self.test_002_in_ti_counter_offer_bet_by_stake()
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()
        self.verify_bet_in_open_bets(bet_type='SINGLE', event_name=self.event_name, bet_in_open_bets=False)
