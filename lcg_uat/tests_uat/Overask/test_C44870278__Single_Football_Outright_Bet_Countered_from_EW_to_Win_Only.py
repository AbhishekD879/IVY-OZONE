import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.open_bets
@pytest.mark.uat
# @pytest.mark.prod # Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.overask
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C44870278__Single_Football_Outright_Bet_Countered_from_EW_to_Win_Only(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C44870278
    NAME: - Single Football Outright Bet Countered from EW to Win Only
    """
    keep_browser_open = True
    max_bet = 1.5
    suggested_max_bet = 1.25

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_outright_event(ew_terms=self.ew_terms, selections_number=1, max_bet=self.max_bet)
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_place_an_overask_each_way_bet_on_a_football_outright_market(self):
        """
        DESCRIPTION: Place an overask Each Way bet on a Football outright market
        EXPECTED: You should have placed a bet which has gone to Overask
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_bet + 0.1
        self.place_single_bet(number_of_stakes=1, each_way=True)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_in_the_ti_change_the_type_of_the_bet_from_each_way_to_win_only(self):
        """
        DESCRIPTION: In the TI, change the type of the bet from Each Way to Win Only
        EXPECTED: You should have changed EW to Win Only
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.change_bet_to_each_way_or_win(account_id=account_id, bet_id=bet_id, betslip_id=betslip_id,
                                                         bet_amount=self.suggested_max_bet, leg_type='W')
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

    def test_003_check_that_the_counter_offer_shows_that1_your_stake_is_highlighted2_you_see_the_win_only_signposting3_the_potential_returns_are_correct(self):
        """
        DESCRIPTION: Check that the counter offer shows that:
        DESCRIPTION: 1. Your stake is highlighted
        DESCRIPTION: 2. You see the Win Only signposting
        DESCRIPTION: 3. The potential returns are correct
        EXPECTED: You should see that
        EXPECTED: 1. The stake is highlighted
        EXPECTED: 2. The Win Only signposting
        EXPECTED: 3. The correct potential returns
        """
        sections = self.get_betslip_sections()
        multiples_section = sections.Singles
        odd = multiples_section.overask_trader_offer.stake_content.odd_value.value
        odd = odd.strip('x')
        self.assertEqual(multiples_section.overask_trader_offer.stake_content.stake_value.value_color,
                         vec.colors.OVERASK_MODIFIED_PRICE_COLOR, msg='Modified price for stake is not highlighted in yellow')
        self.__class__.expected_return = self.get_betslip_content().total_estimate_returns
        self.verify_estimated_returns(est_returns=self.expected_return, bet_amount=self.suggested_max_bet, odds=odd)
        self.assertEqual(multiples_section.overask_trader_offer.stake_content.win_only_sign_post, 'Win Only',
                         msg='"Win Only" sign posting is not present')

    def test_004_place_the_bet_and_check_that_the_bet_receipt_shows_the_correct_stake_and_potential_returns_and_does_not_show_any_each_way_terms_and_places_eg_12_1_2_3(self):
        """
        DESCRIPTION: Place the bet and check that the bet receipt shows the correct stake and potential returns AND does not show any Each Way terms and places e.g. 1/2, 1-2-3
        EXPECTED: The receipt should show the correct stake and potential returns and no Each Way terms should be seen
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found.')
        single_section = bet_receipt_sections.get(vec.bet_history.SINGLE)
        self.assertTrue(single_section, msg='No Single sections found.')
        selections = single_section.items_as_ordered_dict
        self.assertTrue(selections, msg='No stakes found in singles section.')
        selection = list(selections.values())[0]
        ew_terms = selection.ew_terms
        self.assertFalse(ew_terms,
                         msg='"Each Way terms and places" are present in the betslip')
        actual_stake = self.site.bet_receipt.footer.total_stake
        actual_est_returns = self.site.bet_receipt.footer.total_estimate_returns
        self.assertEqual(actual_stake, str(self.suggested_max_bet),
                         msg=f'Actual stake: "{actual_stake}" is not same as '
                             f'Expected stake:"{str(self.suggested_max_bet)}"')
        self.assertEqual(actual_est_returns, self.expected_return,
                         msg=f'Actual Returns: "{actual_est_returns}" is not same as '
                             f'Expected Returns:"{self.expected_return}"')
        self.site.bet_receipt.close_button.click()

    def test_005_check_that_bet_shows_the_correct_stake_and_potential_returns_in_my_bets_open_bets(self):
        """
        DESCRIPTION: Check that bet shows the correct stake and potential returns in My Bets->Open Bets
        EXPECTED: The correct stake and potential returns should be shown for this bet in My Bets->Open Bets
        """
        self.site.open_my_bets_open_bets()
        open_bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(open_bets,
                        msg='No bets found in open bet')
        bet = list(open_bets.values())[0]
        actual_stake = bet.stake.stake_value
        actual_est_returns = bet.est_returns.stake_value
        self.assertEqual(actual_stake, str(self.suggested_max_bet),
                         msg=f'Actual stake: "{actual_stake}" is not same as '
                             f'Expected stake:"{str(self.suggested_max_bet)}"')
        self.assertEqual(actual_est_returns, self.expected_return,
                         msg=f'Actual Returns: "{actual_est_returns}" is not same as '
                             f'Expected Returns:"{self.expected_return}"')
