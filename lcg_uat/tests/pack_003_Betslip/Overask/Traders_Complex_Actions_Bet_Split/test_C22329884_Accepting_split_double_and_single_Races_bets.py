import pytest
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result
from time import sleep


# @pytest.mark.prod # can't trigger Overask appearance on prod
# @pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C22329884_Accepting_split_double_and_single_Races_bets(BaseBetSlipTest):
    """
    TR_ID: C22329884
    NAME: Accepting split double and single Races bets
    DESCRIPTION: This test case verifies accepting split double and single bets without linked parts
    PRECONDITIONS: * For selected User Overask functionality is enabled in backoffice tool (see instruction: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983 )
    PRECONDITIONS: * User is logged in to the application
    """
    keep_browser_open = True
    stake_part1 = 0.5
    price_part1 = 1.50
    stake_part2 = 0.5
    price_part2 = 1.50
    selection_ids = []
    selection_ids_names = []
    event_ids = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Events are created
        """
        self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]
        for i in range(0, 2):
            event_params = self.ob_config.add_UK_racing_event(max_bet=self.max_bet)
            eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.selection_ids_names.append(list(selection_ids.keys())[0])
            self.event_ids.append(eventID)
        self.site.login()

    def test_001_add_2_race_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add 2 race selections from different events to the Betslip
        EXPECTED: Selections are successfully added
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=[self.selection_ids[0], self.selection_ids[1]])

    def test_002__enter_stakes_into_double_field_and_into_singles_fields_value_which_is_higher_than_the_maximum_limit_for_added_selections_tap_ew_checkbox_for_1_single_and_multiple_tap_button_place_bet(self, each_way=True):
        """
        DESCRIPTION: * Enter stakes into Double field and into Singles fields value which is higher than the maximum limit for added selections
        DESCRIPTION: * Tap 'E/W' checkbox for 1 Single and Multiple
        DESCRIPTION: * Tap button 'Place Bet'
        EXPECTED: * Overask is triggered for the User
        EXPECTED: * The bet review notification is shown to the User
        """
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[0]
        stake.amount_form.input.value = self.max_bet + 0.10
        self.assertIn(self.selection_ids_names[0], singles_section,
                      msg=f'Horse name "{self.selection_ids_names[0]}" is not present in "{singles_section.keys()}"')
        stake_1 = singles_section[self.selection_ids_names[0]]
        self.assertTrue(stake_1.each_way_checkbox.is_displayed(), msg='Each way check box is not displayed')
        self.assertEqual(stake_1.each_way_checkbox.each_way_label, 'E/W',
                         msg=f'E/W label is incorrect, actual is : "{stake_1.each_way_checkbox.each_way_label}"')
        if each_way:
            stake_1.each_way_checkbox.click()
        multiples_section = self.get_betslip_sections(multiples=True).Multiples
        _, stake = list(multiples_section.items())[0]
        stake.amount_form.input.value = self.max_bet + 0.10
        self.assertTrue(stake.has_each_way_checkbox,
                        msg=f'Stake does not have Each Way checkbox')
        self.assertEqual(stake.each_way_checkbox.each_way_label, 'E/W',
                         msg=f'E/W label is incorrect, actual is : "{stake_1.each_way_checkbox.each_way_label}"')
        if each_way:
            stake.each_way_checkbox.click()
        self.get_betslip_content().bet_now_button.click()
        overask_overlay = wait_for_result(
            lambda: self.get_betslip_content().overask, name='Overask overlay to appear', timeout=10)
        self.assertTrue(overask_overlay, msg='Overask overlay is not shown')
        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Bet review notification is not shown to the user')

    def test_003__trigger_bet_split_and_stakeoddsprice_type_modification_by_trader_for_1_single_and_multiple_trigger_leg_type_modification_for_both_bets_from_1_splitted_single_and__for_all_splitted_multiple_from_ewto_win_only(self):
        """
        DESCRIPTION: * Trigger Bet Split and Stake/Odds/Price Type modification by Trader for 1 Single and Multiple
        DESCRIPTION: * Trigger Leg type modification for both bets from 1 splitted Single and  for all splitted Multiple from 'E/W'to 'Win Only'
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Bets are splitted according to design for single and double selections
        EXPECTED: * 'Win Only'is shown for both bets from 1 splitted Single and all splitted Multiple
        EXPECTED: * The changed bets are shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        """
        bets_details = self.bet_intercept.find_bets_for_review(events_id=[self.event_ids[0], self.event_ids[1]])
        account_id = bets_details['acct_id']
        betslip_id = bets_details['bet_group_id']
        bet_id1 = (list(bets_details.keys())[0])
        bet_id2 = (list(bets_details.keys())[3])
        self.bet_intercept.split_bet(account_id=account_id, event_id=self.event_ids,
                                     bet_id=[bet_id1, bet_id2], betslip_id=betslip_id,
                                     stake_part1=self.stake_part1, price_part1=self.price_part1,
                                     stake_part2=self.stake_part2, price_part2=self.price_part2,
                                     Number_of_selections=[1, 2])

        overask_trader_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.trader_message,
            name='Overask trader message to appear', timeout=10)
        self.assertTrue(overask_trader_message, msg=f'Overask trader message has not appeared')

        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" '
                             f'is not as expected: "{cms_overask_trader_message}" from CMS')

        sleep(2)
        self.__class__.sections = self.get_betslip_content().overask_trader_section.items
        is_selection_splitted = wait_for_result(lambda: len(self.sections) == 8,
                                                timeout=10,
                                                name='Selections to become splitted into 2 parts')
        self.assertTrue(is_selection_splitted, msg='Selection is not splitted into 2 parts')
        for section in range(len(self.sections)):
            if section in [0, 1]:
                self.assertTrue(self.sections[section].has_remove_button(),
                                msg=f'Remove button is not present for "{self.sections[section].name}"')
            if section in [0, 1, 4, 7]:
                odds = float(self.sections[section].stake_value.text.replace('£', ""))
                self.assertEqual(odds, self.stake_part1,
                                 msg=f'Actuals odds:"{odds}" is not same as Expected odds: "{self.stake_part1}"')
                price_color = self.sections[section].stake_value.background_color_value
                self.assertEqual(price_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                                 msg=f'"Modified price" is not highlighted in yellow')

            if section in [4, 7]:
                self.assertEquals(self.sections[section].name, vec.betslip.DBL,
                                  msg=f'section is not present for "{self.sections[section].name}"')
                self.assertTrue(self.sections[section].has_remove_button(),
                                msg=f'Remove button is not present for "{self.sections[section].name}"')

        est_returns_after = self.get_betslip_content().total_estimate_returns
        est_returns_stake_1 = self.calculate_estimated_returns(odds=[self.stake_part1],
                                                               bet_amount=self.price_part1)
        est_returns_stake_2 = self.calculate_estimated_returns(odds=[self.price_part2, self.price_part2],
                                                               bet_amount=self.stake_part1, is_double=True)
        self.assertAlmostEqual((float(est_returns_stake_1) + float(est_returns_stake_1) + float(est_returns_stake_2) + float(est_returns_stake_2)), float(est_returns_after), delta=0.04,
                               msg=f'Actual estimated returns "{(float(est_returns_stake_1) + float(est_returns_stake_1) + float(est_returns_stake_2) + float(est_returns_stake_2))}" doesn\'t match expected'
                                   f'"{float(est_returns_after)}" within "{0.04}" delta')

        place_bet_button = self.get_betslip_content().confirm_overask_offer_button
        self.assertTrue(place_bet_button.is_enabled(), msg=f'"{place_bet_button.name}" button is disabled')

        cancel_button = self.get_betslip_content().cancel_button
        self.assertTrue(cancel_button.is_enabled(), msg=f'"{cancel_button.name}" button is disabled')

    def test_004_tap_place_bet_or_cancel_buttons(self):
        """
        DESCRIPTION: Tap 'Place bet' or 'Cancel' buttons
        EXPECTED: The bets are placed as per normal process
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No BetReceipt sections found')

        single_section = sections.get(vec.betslip.BETSLIP_SINGLES_NAME)
        self.assertTrue(single_section, msg='No Betslip sections found')
        self.assertEqual(len(single_section.items_as_ordered_dict.items()), 2,
                         msg=f'Bet receipt section should not 2 placed bets found: "{vec.betslip.BETSLIP_SINGLES_NAME}"')

        multiple_section = sections.get(vec.betslip.DBL)
        self.assertTrue(multiple_section, msg='No Betslip sections found')
        self.assertEqual(len(multiple_section.items_as_ordered_dict.items()), 2,
                         msg=f'Bet receipt section should not 2 placed bets found: "{vec.betslip.DBL}"')

    def test_005_repeat_steps_1_4_for_not_enabled_ew_checkbox(self):
        """
        DESCRIPTION: Repeat steps 1-4 for NOT enabled 'E/W' checkbox
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Bets are splitted according to design for single and double selections
        EXPECTED: * 'E/W' is shown for both bets from 1 splitted Singlee and all splitted Multiple
        EXPECTED: * The changed bets are shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        """
        self.navigate_to_page('homepage')
        self.test_001_add_2_race_selections_from_different_events_to_the_betslip()
        self.test_002__enter_stakes_into_double_field_and_into_singles_fields_value_which_is_higher_than_the_maximum_limit_for_added_selections_tap_ew_checkbox_for_1_single_and_multiple_tap_button_place_bet(each_way=False)
        self.test_003__trigger_bet_split_and_stakeoddsprice_type_modification_by_trader_for_1_single_and_multiple_trigger_leg_type_modification_for_both_bets_from_1_splitted_single_and__for_all_splitted_multiple_from_ewto_win_only()
        self.test_004_tap_place_bet_or_cancel_buttons()
