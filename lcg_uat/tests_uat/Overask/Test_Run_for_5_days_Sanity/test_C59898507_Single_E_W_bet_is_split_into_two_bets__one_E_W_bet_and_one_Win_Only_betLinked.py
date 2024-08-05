import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.overask
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898507_Single_E_W_bet_is_split_into_two_bets__one_E_W_bet_and_one_Win_Only_betLinked(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C59898507
    NAME: Single E/W bet is split into two bets - one E/W bet and one Win Only bet.(Linked)
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 3.00
    max_mult_bet = 4.00
    bet_amount = 3.00
    stake_part1 = 1.50
    price_part1 = 1.50
    stake_part2 = 0.50
    price_part2 = 0.50
    suggested_max_bet = 0.25
    prices = {0: '1/12'}
    username = tests.settings.betplacement_user

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event for HR
        EXPECTED: Event Created
        """
        event_params = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1, lp_prices=self.prices, max_bet=self.max_bet)
        self.__class__.event_name = event_params.ss_response['event']['name']
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]
        self.site.login(username=self.username)
        self.site.close_all_dialogs()

    def test_001_add_selection_from_any_outright_event_to_quick_betbetsliptrigger_overask__select_ew_checkbox_and_try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add selection from any outright event to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( Select E/W checkbox and try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_bet + 0.1
        self.place_single_bet(number_of_stakes=1, each_way=True)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Over ask is not triggered for the User')

    def test_002_split_the_single_ew_bet_into_two_bets___one_ew_bet_and_one_win_only_bet_with_the_price_of_1st_single_being_lp_and_the_2nd_single_being_splinkedstakes_are_divided_between_the_two_singles(self, price1="L", price2="S", leg_type1="E", leg_type2="W"):
        """
        DESCRIPTION: Split the single E/W bet into two bets - one E/W bet and one Win Only bet, with the price of 1st single being LP and the 2nd single being SP.(Linked)
        DESCRIPTION: Stakes are divided between the two singles.
        EXPECTED: Customer sees in the counter offer 2 bets, with the original stake being spread over the two bets - the first will be E/W and the second will be win only and the stake and price will be highlighted for 2nd part and stake for 1st part.
        EXPECTED: Customer is able to accept, remove second offer, or decline the counter offer.
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(
            username=self.username, event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{[bet_id]}", betslip id "{betslip_id}"')
        self.bet_intercept.split_bet(account_id=account_id, event_id=self.eventID,
                                     bet_id=[bet_id], betslip_id=betslip_id,
                                     stake_part1=self.stake_part1, price_part1=self.price_part1,
                                     stake_part2=self.stake_part2, price_part2=self.price_part2, linked=True,
                                     price_type1=price1, price_type2=price2,
                                     leg_type1=leg_type1, leg_type2=leg_type2)
        overask_trader_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.trader_message,
            name='Overask trader message to appear', timeout=10)

        self.assertTrue(overask_trader_message, msg=f'Overask trader message has not appeared')
        is_selection_splitted = wait_for_result(lambda: len(self.get_betslip_sections().Singles) == 2,
                                                timeout=5,
                                                name='Selections to become splitted into 2 parts')
        self.assertTrue(is_selection_splitted, msg='Selection is not splitted into 2 parts')
        singles_section = self.get_betslip_sections().Singles
        for stake_name, stake in singles_section.items():
            self.assertEqual(stake.offered_stake.background_color_value, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                             msg=f'Modified price for "{stake_name}" is not highlighted in yellow')
        stake_name1, stake1 = list(singles_section.items())[0]
        expected_stake_value1 = float(stake1.offered_stake.name.strip('£'))
        self.assertEqual(expected_stake_value1, self.stake_part1,
                         msg=f'Changed amount should be present, get "{expected_stake_value1}" instead')
        self.assertFalse(stake1.has_remove_button(expected_result=False),
                         msg=f'Remove button is present for "{stake_name1}"')
        self.__class__.stake_name2, self.__class__.stake2 = list(singles_section.items())[1]
        expected_stake_value2 = float(self.stake2.offered_stake.name.strip('£'))
        self.assertEqual(expected_stake_value2, self.stake_part2,
                         msg=f'Changed amount should be present, get "{expected_stake_value2}" instead')
        self.assertTrue(self.stake2.has_remove_button(), msg=f'Remove button is not present for "{self.stake_name2}"')
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" '
                             f'is not as expected: "{cms_overask_trader_message}" from CMS')
        betslip_section = self.get_betslip_content()
        place_bet_button = betslip_section.confirm_overask_offer_button
        self.assertTrue(place_bet_button.is_enabled(), msg=f'"{place_bet_button.name}" button is disabled')
        cancel_button = betslip_section.cancel_button
        self.assertTrue(cancel_button.is_enabled(), msg=f'"{cancel_button.name}" button is disabled')

    def test_003_if_customer_removes_one_single_and_accepted_other_single(self):
        """
        DESCRIPTION: If customer removes one single and accepted other single
        EXPECTED: The bet receipt should show only one single bet with updated potential returns and only one single bet is shown in My Bets and Account History.
        """
        self.stake2.scroll_to()
        self.stake2.select()
        self.assertTrue(self.stake2.undo_button.is_displayed(), msg=f'UNDO button is not displayed for {self.stake_name2}')
        place_bet_button = self.get_betslip_content().confirm_overask_offer_button
        self.assertTrue(place_bet_button.is_enabled(), msg=f'"{place_bet_button.name}" button is disabled')
        place_bet_button.click()
        self.check_bet_receipt_is_displayed()
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        if self.device_type == 'mobile':
            self.navigate_to_page('homepage')
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_name, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(event_name=self.event_name, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)

    def test_004_if_customer_accepts_the_offer_without_removing_any_single(self):
        """
        DESCRIPTION: If Customer accepts the offer (without removing any single)
        EXPECTED: The two bets are placed and the user is taken to the bet receipt where two bets are shown in My Bets and Account History
        """
        self.test_001_add_selection_from_any_outright_event_to_quick_betbetsliptrigger_overask__select_ew_checkbox_and_try_to_place_bet_with_higher_stake_than_a_max_allowed_stake()
        self.test_002_split_the_single_ew_bet_into_two_bets___one_ew_bet_and_one_win_only_bet_with_the_price_of_1st_single_being_lp_and_the_2nd_single_being_splinkedstakes_are_divided_between_the_two_singles()
        singles_section = self.get_betslip_sections().Singles
        for stake_name, stake in singles_section.items():
            self.assertEqual(stake.offered_stake.background_color_value, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                             msg=f'Modified price for "{stake_name}" is not highlighted in yellow')
        betslip_section = self.get_betslip_content()
        place_bet_button = betslip_section.confirm_overask_offer_button
        self.assertTrue(place_bet_button.is_enabled(), msg=f'"{place_bet_button.name}" button is disabled')
        place_bet_button.click()
        self.check_bet_receipt_is_displayed()
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        single_section = bet_receipt_sections.get(vec.betslip.SINGLE).items_as_ordered_dict
        len_of_expected_singles = 2
        self.assertEqual(len(single_section), len_of_expected_singles,
                         msg=f'Length of singles section "{len(single_section)}" '
                             f'is not same as Expected length of singles "{len_of_expected_singles}"')
        if self.device_type == 'mobile':
            self.navigate_to_page('homepage')
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_name, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(event_name=self.event_name, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)

    def test_005_if_the_offer_is_declined(self):
        """
        DESCRIPTION: If the offer is declined
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History.
        """
        self.test_001_add_selection_from_any_outright_event_to_quick_betbetsliptrigger_overask__select_ew_checkbox_and_try_to_place_bet_with_higher_stake_than_a_max_allowed_stake()
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(
            username=self.username, event_id=self.eventID)
        self.bet_intercept.decline_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)
        self.site.wait_content_state_changed(timeout=15)
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        section = list(betreceipt_sections.values())[0]
        overask_warning_message = section.declined_bet.stake_content.stake_message
        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual message "{overask_warning_message}" is not same as'
                             f'Expected message "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')

    def test_006_split_the_single_ew_bet_into_two_bets___one_ew_bet_and_one_win_only_bet_with_the_price_of_1st_single_being_sp_and_the_2nd_single_being_lplinkedstakes_are_divided_between_the_two_singles(self):
        """
        DESCRIPTION: Split the single E/W bet into two bets - one E/W bet and one Win Only bet, with the price of 1st single being SP and the 2nd single being LP.(Linked)
        DESCRIPTION: Stakes are divided between the two singles.
        EXPECTED: Customer sees in the counter offer 2 bets, with the original stake being spread over the two bets - the first will be E/W and the second will be win only and the stake and price will be highlighted for 1st part and just stake for 2nd part.
        EXPECTED: Customer is able to accept, remove second offer, or decline the counter offer.
        """
        self.test_001_add_selection_from_any_outright_event_to_quick_betbetsliptrigger_overask__select_ew_checkbox_and_try_to_place_bet_with_higher_stake_than_a_max_allowed_stake()
        self.test_002_split_the_single_ew_bet_into_two_bets___one_ew_bet_and_one_win_only_bet_with_the_price_of_1st_single_being_lp_and_the_2nd_single_being_splinkedstakes_are_divided_between_the_two_singles(price1="S", price2="L")

    def test_007_repeat_steps_3_to_5(self):
        """
        DESCRIPTION: Repeat steps 3 to 5.
        """
        self.test_003_if_customer_removes_one_single_and_accepted_other_single()
        self.test_004_if_customer_accepts_the_offer_without_removing_any_single()
        self.test_005_if_the_offer_is_declined()
