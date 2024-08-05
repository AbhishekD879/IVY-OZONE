import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.slow
@pytest.mark.overask
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898480_Treble_bet_is_split_into_two_trebles_with_the_price_of_one_treble_being_LP_and_the_other_being_SP_Stakes_are_divided_between_the_two_treblesUnlinked(BaseBetSlipTest):
    """
    TR_ID: C59898480
    NAME: Treble bet is split into two trebles, with the price of one treble being LP and the other being SP. Stakes are divided between the two trebles.(Unlinked)
    DESCRIPTION:
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    username = tests.settings.betplacement_user
    max_bet = 2
    prices = {0: '1/2'}
    selection_ids, eventIDs, event_names = [], [], []
    stake_part1 = 1.00
    price_part1 = 1.50
    stake_part2 = 0.09
    price_part2 = 1.50
    sp_price = "SP"

    def test_000_preconditions(self):
        """
        DESCRIPTION: Lauch application and login
        """
        self.site.login(username=self.username)

    def test_001_add_treble_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add treble selections to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        self.selection_ids.clear()
        self.eventIDs.clear()
        self.event_names.clear()
        for i in range(3):
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, max_bet=self.max_bet, lp_prices=self.prices)
            eventID, selection_ids = event_params.event_id, event_params.selection_ids
            event_name = event_params.ss_response['event']['name']
            self.eventIDs.append(eventID)
            self.selection_ids.append(list(selection_ids.values())[0])
            self.event_names.append(event_name)
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_bet + 1
        self.place_multiple_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='"Overask" is not triggered for the User')

    def test_002_split_the_treble_bets_into_two_trebles_with_the_price_of_1st_treble_being_lp_and_the_2nd_being_sp_unlinkedstakes_are_divided_between_the_two_trebles(self, parent='L'):
        """
        DESCRIPTION: Split the treble bets into two trebles, with the price of 1st treble being LP and the 2nd being SP (Unlinked)
        DESCRIPTION: Stakes are divided between the two trebles.
        EXPECTED: Customer sees in the counter offer 2 treble bets, with the original stake being spread over the two bets - the first will be offered at unchanged LP prices, so only the stake will be highlighted
        EXPECTED: The second at SP prices, so both price and stake are highlighted.
        """
        bets_details = self.bet_intercept.find_bets_for_review(events_id=self.eventIDs)
        account_id = bets_details['acct_id']
        betslip_id = bets_details['bet_group_id']
        bet_id = list(bets_details.keys())[0]
        if parent == "L":
            self.bet_intercept.split_bet(account_id=account_id, event_id=self.eventIDs, bet_id=[bet_id],
                                         betslip_id=betslip_id,
                                         stake_part1=self.stake_part1, price_part1=self.price_part1,
                                         stake_part2=self.stake_part2, price_part2=self.price_part2,
                                         price_type_parent1="L", price_type_parent2="L",
                                         price_type_parent3="L",
                                         price_type_child_0_1="S", price_type_child_0_2="S",
                                         price_type_child_0_3="S",
                                         Number_of_selections=[3])
            overask_trader_message = wait_for_result(
                lambda: self.get_betslip_content().overask_trader_section.trader_message,
                name='Overask trader message to appear', timeout=10)
            self.assertTrue(overask_trader_message, msg=f'"{overask_trader_message}" trader message has not appeared')
            self.__class__.sections = self.get_betslip_content().overask_trader_section.items
            self.assertTrue(len(self.sections) == 8,
                            msg=f'"{vec.betslip.TBL}" bet has not splitted into Two "{vec.betslip.TBL}" bets')
            for section in range(len(self.sections)):
                if section in [0, 1, 2]:
                    odds = self.sections[section].stake_odds.name
                    self.assertEqual(odds, self.prices[0],
                                     msg=f'Actuals odds:"{odds}" is not same as Expected odds: "{self.prices[0]}"')
                elif section in [4, 5, 6]:
                    odds = self.sections[section].stake_odds.value
                    self.assertEqual(odds, self.sp_price,
                                     msg=f'Actuals odds:"{odds}" is not same as Expected odds: "{self.sp_price}"')
                    price_color = self.sections[section].stake_odds.value_color
                    self.assertEqual(price_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                                     msg='Modified price for stake is not highlighted in "yellow"')
        else:
            self.bet_intercept.split_bet(account_id=account_id, event_id=self.eventIDs, bet_id=[bet_id],
                                         betslip_id=betslip_id,
                                         stake_part1=self.stake_part1, price_part1=self.price_part1,
                                         stake_part2=self.stake_part2, price_part2=self.price_part2,
                                         price_type_parent1="S", price_type_parent2="S",
                                         price_type_parent3="S",
                                         price_type_child_0_1="L", price_type_child_0_2="L",
                                         price_type_child_0_3="L",
                                         Number_of_selections=[3])
            overask_trader_message = wait_for_result(
                lambda: self.get_betslip_content().overask_trader_section.trader_message,
                name='Overask trader message to appear', timeout=10)
            self.assertTrue(overask_trader_message, msg=f'"{overask_trader_message}" has not appeared')
            self.__class__.sections = self.get_betslip_content().overask_trader_section.items
            self.assertTrue(len(self.sections) == 8,
                            msg=f'"{vec.betslip.TBL}" bet has not splitted into Two "{vec.betslip.TBL}" bets')
            for section in range(len(self.sections)):
                if section in [0, 1, 2]:
                    odds = self.sections[section].stake_odds.value
                    self.assertEqual(odds, self.sp_price,
                                     msg=f'Actuals odds:"{odds}" is not same as Expected odds: "{self.sp_price}"')
                    price_color = self.sections[section].stake_odds.value_color
                    self.assertEqual(price_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                                     msg='Modified price for stake is not highlighted in "yellow"')
                elif section in [4, 5, 6]:
                    odds = self.sections[section].stake_odds.name
                    self.assertEqual(odds, self.prices[0],
                                     msg=f'Actuals odds:"{odds}" is not same as Expected odds: "{self.prices[0]}"')

    def test_003_check_the_potential_returns(self):
        """
        DESCRIPTION: Check the potential Returns
        EXPECTED: For the treble at SP prices, potential returns should be N/A
        EXPECTED: For the treble at LP prices, potential returns should be displayed correctly
        EXPECTED: Total potential returns will be N/A
        """
        Treble1_est_returns_text = self.sections[3].est_returns.text
        self.assertTrue(Treble1_est_returns_text, msg='"Treble Est. Returns" value not found')
        Treble2_est_returns_text = self.sections[7].est_returns.text.split(":")
        self.assertEqual(Treble2_est_returns_text[1], 'N/A',
                         msg=f'Total estimate returns value "{Treble2_est_returns_text[1]}" is not the same as expected "N/A"')
        total_est_returns = self.get_betslip_content().total_estimate_returns
        self.assertEqual(total_est_returns, 'N/A',
                         msg=f'Total estimate returns value "{total_est_returns}" is not the same as expected "N/A"')

    def test_004_customer_is_able_to_accept_remove_one_of_the_offers_or_decline_the_counter_offer(self):
        """
        DESCRIPTION: Customer is able to accept, remove one of the offers, or decline the counter offer.
        """
        # covered in test_005, test_006 and test_007

    def test_005_if_customer_removes_one_treble_and_accepted_other(self):
        """
        DESCRIPTION: If customer removes one Treble and accepted other
        EXPECTED: The bet receipt should show only one Treble bet with the updated potential returns
        EXPECTED: Only one bet is shown in My Bets and Account History.
        """
        self.sections[7].remove_btn.click()
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items
        self.assertTrue(receipt_sections, msg='No "receipt sections" found in BetReceipt')
        self.assertEqual(len(receipt_sections), 1, msg=f'More than one "{vec.betslip.TBL}" bet has been placed')
        receipt_bet_type_section = receipt_sections[0]
        self.assertEqual(receipt_bet_type_section.bet_type, vec.betslip.TBL,
                         msg=f'Actual bet type: "{receipt_bet_type_section.bet_type}" is not same as expected bet type: "{vec.betslip.TBL}"')
        self.assertTrue(receipt_bet_type_section.estimate_returns,
                        msg=f'Potential returns: "{receipt_bet_type_section.estimate_returns}" are not displayed')
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_names[0], bet_type=vec.betslip.TBL.upper())
        self.verify_bet_in_open_bets(event_name=self.event_names[1], bet_type=vec.betslip.TBL.upper())
        self.verify_bet_in_open_bets(event_name=self.event_names[2], bet_type=vec.betslip.TBL.upper())
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(event_name=self.event_names[0], bet_type=vec.betslip.TBL.upper())
        self.verify_bet_in_open_bets(event_name=self.event_names[1], bet_type=vec.betslip.TBL.upper())
        self.verify_bet_in_open_bets(event_name=self.event_names[2], bet_type=vec.betslip.TBL.upper())

    def test_006_if_customer_accepts_the_bet(self, parent="L"):
        """
        DESCRIPTION: If Customer accepts the bet
        EXPECTED: The two bets are placed and the user is taken to the bet receipt where two bets are shown in My Bets and Account History
        EXPECTED: Balance should be updated correctly
        """
        self.test_001_add_treble_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake()
        self.test_002_split_the_treble_bets_into_two_trebles_with_the_price_of_1st_treble_being_lp_and_the_2nd_being_sp_unlinkedstakes_are_divided_between_the_two_trebles(parent)
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed(timeout=20)
        receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items
        self.assertTrue(receipt_sections, msg='No "BetReceipt sections" found')
        self.assertEqual(len(receipt_sections), 2, msg=f'Less than two "{vec.betslip.TBL}" bet has been placed')
        receipt_bet_type_section1 = receipt_sections[0]
        receipt_bet_type_section2 = receipt_sections[1]
        self.assertEqual(receipt_bet_type_section1.bet_type, vec.betslip.TBL,
                         msg=f'Actual bet type: "{receipt_bet_type_section1.bet_type}" is not same as expected bet type: "{vec.betslip.TBL}"')
        self.assertTrue(receipt_bet_type_section1.estimate_returns,
                        msg=f'Potential returns: "{receipt_bet_type_section1.estimate_returns}" are not displayed')
        self.assertEqual(receipt_bet_type_section2.bet_type, vec.betslip.TBL,
                         msg=f'Actual bet type: "{receipt_bet_type_section2.bet_type}" is not same as expected bet type: "{vec.betslip.TBL}"')
        self.assertTrue(receipt_bet_type_section2.estimate_returns,
                        msg=f'Potential returns: "{receipt_bet_type_section2.estimate_returns}" are not displayed')
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_names[0], bet_type=vec.betslip.TBL.upper())
        self.verify_bet_in_open_bets(event_name=self.event_names[1], bet_type=vec.betslip.TBL.upper())
        self.verify_bet_in_open_bets(event_name=self.event_names[2], bet_type=vec.betslip.TBL.upper())
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(event_name=self.event_names[0], bet_type=vec.betslip.TBL.upper())
        self.verify_bet_in_open_bets(event_name=self.event_names[1], bet_type=vec.betslip.TBL.upper())
        self.verify_bet_in_open_bets(event_name=self.event_names[2], bet_type=vec.betslip.TBL.upper())

    def test_007_if_customer_declines_the_offer(self, parent="L"):
        """
        DESCRIPTION: If Customer declines the offer
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History
        """
        self.test_001_add_treble_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake()
        self.test_002_split_the_treble_bets_into_two_trebles_with_the_price_of_1st_treble_being_lp_and_the_2nd_being_sp_unlinkedstakes_are_divided_between_the_two_trebles(parent)
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_names[0], bet_type=vec.betslip.TBL.upper(), bet_in_open_bets=False)
        self.verify_bet_in_open_bets(event_name=self.event_names[1], bet_type=vec.betslip.TBL.upper(), bet_in_open_bets=False)
        self.verify_bet_in_open_bets(event_name=self.event_names[2], bet_type=vec.betslip.TBL.upper(), bet_in_open_bets=False)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(event_name=self.event_names[0], bet_type=vec.betslip.TBL.upper(), bet_in_open_bets=False)
        self.verify_bet_in_open_bets(event_name=self.event_names[1], bet_type=vec.betslip.TBL.upper(), bet_in_open_bets=False)
        self.verify_bet_in_open_bets(event_name=self.event_names[2], bet_type=vec.betslip.TBL.upper(), bet_in_open_bets=False)

    def test_008_split_the_treble_bets_into_two_trebles_with_the_price_of_1st_treble_being_sp_and_the_2nd_being_lp_unlinkedstakes_are_divided_between_the_two_trebles(self):
        """
        DESCRIPTION: Split the treble bets into two trebles, with the price of 1st treble being SP and the 2nd being LP (Unlinked)
        DESCRIPTION: Stakes are divided between the two trebles.
        EXPECTED: Customer sees in the counter offer 2 treble bets, with the original stake being spread over the two bets - the first will be offered at SP, so both price and stake are highlighted and 2nd treble unchanged at LP prices, so only the stake will be highlighted
        """
        self.test_001_add_treble_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake()
        self.test_002_split_the_treble_bets_into_two_trebles_with_the_price_of_1st_treble_being_lp_and_the_2nd_being_sp_unlinkedstakes_are_divided_between_the_two_trebles(parent="S")

    def test_009_repeat_steps_3_to_5(self):
        """
        DESCRIPTION: Repeat steps 3 to 5.
        """
        Treble1_est_returns_text = self.sections[3].est_returns.text.split(":")
        self.assertEqual(Treble1_est_returns_text[1], 'N/A',
                         msg=f'Total estimate returns value "{Treble1_est_returns_text[1]}" is not the same as expected "N/A"')
        Treble2_est_returns_text = self.sections[7].est_returns.text
        self.assertTrue(Treble2_est_returns_text, msg='"Treble Est. Returns" value not found')
        total_est_returns = self.get_betslip_content().total_estimate_returns
        self.assertEqual(total_est_returns, 'N/A',
                         msg=f'Total estimate returns value "{total_est_returns}" is not the same as expected "N/A"')
        self.test_005_if_customer_removes_one_treble_and_accepted_other()
        self.test_006_if_customer_accepts_the_bet(parent="S")
        self.test_007_if_customer_declines_the_offer(parent="S")
