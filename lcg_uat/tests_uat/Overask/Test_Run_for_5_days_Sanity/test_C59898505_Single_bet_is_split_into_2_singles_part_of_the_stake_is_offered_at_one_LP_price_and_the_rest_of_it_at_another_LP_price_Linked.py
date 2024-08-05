import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.overask
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C59898505_Single_bet_is_split_into_2_singles_part_of_the_stake_is_offered_at_one_LP_price_and_the_rest_of_it_at_another_LP_price_Linked(BaseBetSlipTest):
    """
    TR_ID: C59898505
    NAME: Single bet is split into 2 singles: part of the stake is offered at one LP price and the rest of it at another LP price. (Linked)
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 3.00
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
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=self.prices, max_bet=self.max_bet)
        self.__class__.event_name = event_params.ss_response['event']['name']
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]
        self.site.login(username=self.username)
        self.site.close_all_dialogs()

    def test_001_add_hr_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add HR selection to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( try to place bet, with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_bet + 0.1
        self.place_single_bet(number_of_stakes=1, each_way=True)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Over ask is not triggered for the User')

    def test_002_split_the_single_bet_into_2_1st_part_of_the_stake_is_offered_at_original_lp_and_the_2nd_part_at_another_lplinked(self, price1="L", price2="L"):
        """
        DESCRIPTION: Split the single bet into 2: 1st part of the stake is offered at original LP and the 2nd part at another LP.(Linked)
        EXPECTED: Customer should see in the counter offer for 2 singles, with the stakes being highlighted for both the selections
        EXPECTED: Customer is able to accept, remove second offer, or decline the counter offer.
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{[bet_id]}", betslip id "{betslip_id}"')
        self.bet_intercept.split_bet(account_id=account_id, event_id=self.eventID,
                                     bet_id=[bet_id], betslip_id=betslip_id,
                                     stake_part1=self.stake_part1, price_part1=self.price_part1,
                                     stake_part2=self.stake_part2, price_part2=self.price_part2, linked=True,
                                     price_type1=price1, price_type2=price2)
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
        stake_name2, self.__class__.stake2 = list(singles_section.items())[1]
        expected_stake_value2 = float(self.stake2.offered_stake.name.strip('£'))
        self.assertEqual(expected_stake_value2, self.stake_part2,
                         msg=f'Changed amount should be present, get "{expected_stake_value2}" instead')
        self.assertTrue(self.stake2.has_remove_button(), msg=f'Remove button is not present for "{stake_name2}"')

        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" '
                             f'is not as expected: "{cms_overask_trader_message}" from CMS')
        betslip_section = self.get_betslip_content()
        place_bet_button = betslip_section.confirm_overask_offer_button
        self.assertTrue(place_bet_button.is_enabled(), msg=f'"{place_bet_button.name}" button is disabled')
        cancel_button = betslip_section.cancel_button
        self.assertTrue(cancel_button.is_enabled(), msg=f'"{cancel_button.name}" button is disabled')

    def test_003_if_customer_removes_second_single_and_accepted_other_single(self):
        """
        DESCRIPTION: If customer removes second single and accepted other single
        EXPECTED: The bet receipt should show only one single bet with updated potential returns and only one single bet is shown in My Bets and Account History.
        """
        self.stake2.scroll_to()
        self.stake2.select()
        self.assertTrue(self.stake2.undo_button.is_displayed(), msg='UNDO button is not displayed')
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
        self.device.navigate_to(url=tests.HOSTNAME)
        self.site.wait_content_state('HomePage')

    def test_004_if_customer_accepts_the_offer_without_removing_any_single(self):
        """
        DESCRIPTION: If Customer accepts the offer (without removing any single)
        EXPECTED: The two bets are placed and the user is taken to the bet receipt where two bets are shown in My Bets and Account History
        """
        self.test_001_add_hr_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake()
        self.test_002_split_the_single_bet_into_2_1st_part_of_the_stake_is_offered_at_original_lp_and_the_2nd_part_at_another_lplinked(price1="S", price2="L")
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
        self.device.navigate_to(url=tests.HOSTNAME)
        self.site.wait_content_state('HomePage')

    def test_005_if_the_offer_is_declined(self):
        """
        DESCRIPTION: If the offer is declined
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History.
        """
        self.test_001_add_hr_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake()
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.decline_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)
        self.site.wait_content_state_changed(timeout=15)
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        section = list(betreceipt_sections.values())[0]
        overask_warning_message = section.declined_bet.stake_content.stake_message
        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual message "{overask_warning_message}" is not same as'
                             f'Expected message "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')
        self.device.navigate_to(url=tests.HOSTNAME)
        self.site.wait_content_state('HomePage')

    def test_006_split_the_single_bet_into_2_1st_part_of_the_stake_is_offered_at_sp_and_the_2nd_part_at_another_lplinked(self):
        """
        DESCRIPTION: Split the single bet into 2: 1st part of the stake is offered at SP and the 2nd part at another LP.(Linked)
        EXPECTED: Customer should see in the counter offer for 2 singles, with the stakes being highlighted for both the selections
        EXPECTED: Customer  is able to accept, remove second offer, or decline the counter offer.
        """
        self.test_001_add_hr_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake()
        self.test_002_split_the_single_bet_into_2_1st_part_of_the_stake_is_offered_at_original_lp_and_the_2nd_part_at_another_lplinked(price1="S", price2="L")

    def test_007_repeat_step_3_to_5(self):
        """
        DESCRIPTION: Repeat step 3 to 5.
        EXPECTED:
        """
        self.test_003_if_customer_removes_second_single_and_accepted_other_single()
        self.test_004_if_customer_accepts_the_offer_without_removing_any_single()
        self.test_005_if_the_offer_is_declined()
