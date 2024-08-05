import pytest
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.liveserv_updates
@pytest.mark.event_details
@pytest.mark.bet_placement
@pytest.mark.my_bets
@pytest.mark.medium
@pytest.mark.cash_out
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C325661_Verify_Cash_Out_value_change_on_cash_out_button(BaseCashOutTest):
    """
    TR_ID: C325661
    NAME: Cash Out value change on 'CASH OUT' button
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has placed Singles and Multiple bets with available Cash Out offer
    """
    keep_browser_open = True
    bet_amount = 5
    increased_price = '14/1'
    decreased_price = '1/14'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Run Cash Out precondition steps which creates testing data
        EXPECTED: Test event with available Cash Out was created
        """
        self.__class__.events_info = self.create_several_autotest_premier_league_football_events(number_of_events=2)
        self.site.login()

        for event_info in self.events_info:
            self.__class__.selection_ids[event_info.team1] = event_info.selection_ids[event_info.team1]
            self.open_betslip_with_selections(selection_ids=event_info.selection_ids[event_info.team1])

        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiples_section = sections.Singles, sections.Multiples

        for stake in self.zip_available_stakes(section=singles_section, number_of_stakes=2).items():
            self.enter_stake_amount(stake=stake)

        for stake in self.zip_available_stakes(section=multiples_section, number_of_stakes=1).items():
            self.enter_stake_amount(stake=stake)

        betnow_section = self.get_betslip_content().betnow_section
        betnow_section.bet_now_button.click()
        self.site.bet_receipt.footer.click_done()
        self.__class__.single_bet_name = 'SINGLE - [%s]' % list(self.selection_ids.keys())[0]
        self.__class__.multiple_bet_name = 'DOUBLE - [%s]' % ', '.join(self.selection_ids.keys())
        self.__class__.eventID = self.events_info[0].event_id
        self.__class__.team1 = self.events_info[0].team1

    def test_001_navigate_to_event_details_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets from preconditions
        """
        self.navigate_to_edp(self.eventID)
        self.site.sport_event_details.event_user_tabs_list.open_tab(tab_name=self.my_bets_tab_name)

    def test_002_trigger_cash_out_value_increasing_for_single_and_multiple_bet(self):
        """
        DESCRIPTION: Trigger cash out value INCREASING for **Single** bet
        DESCRIPTION: Trigger cash out value INCREASING for **Multiple** bet
        EXPECTED: Corresponding 'Price/Odds' data is not changed
        EXPECTED: Corresponding priceNum/priceDen is changed on SiteServer
        EXPECTED: 'CASH OUT' button immediately displays new cash out value
        """
        self.__class__.bet_sections = \
            self.site.sport_event_details.my_bets.accordions_list.items_as_ordered_dict
        self.assertTrue(self.bet_sections, msg='No one bet section found for event with id: %s' % self.eventID)
        self.assertIn(self.single_bet_name, self.bet_sections.keys())
        single_bet = self.bet_sections[self.single_bet_name]

        initial_single_cashout_value = single_bet.buttons_panel.full_cashout_button.amount.value
        betlegs = single_bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg='No betlegs found')
        betleg_name, betleg = list(betlegs.items())[0]
        initial_odds_value = betleg.odds_value
        self.__class__.bet_sections = self.site.sport_event_details.my_bets.accordions_list.items_as_ordered_dict
        self.assertIn(self.multiple_bet_name, self.bet_sections.keys())
        multiple_bet = self.bet_sections[self.multiple_bet_name]

        initial_multiple_cashout_value = multiple_bet.buttons_panel.full_cashout_button.amount.value

        self.ob_config.change_price(selection_id=self.selection_ids[self.team1], price=self.increased_price)
        self.assertTrue(single_bet.buttons_panel.full_cashout_button.wait_amount_to_change(initial_amount=initial_single_cashout_value),
                        msg='Cashout Amount is not changed')

        new_single_cashout_value = single_bet.buttons_panel.full_cashout_button.amount.value
        self.assertTrue(float(initial_single_cashout_value) > float(new_single_cashout_value),
                        msg='New cashout value "%s" is not lower than "%s"' % (new_single_cashout_value, initial_single_cashout_value))

        betlegs = single_bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg='No betlegs found')
        betleg_name, betleg = list(betlegs.items())[0]
        new_single_odds_value = betleg.odds_value

        self.assertEqual(initial_odds_value, new_single_odds_value,
                         msg='Odds is changed from "%s" to "%s"' % (initial_odds_value, new_single_odds_value))

        self.assertTrue(multiple_bet.buttons_panel.full_cashout_button.wait_amount_to_change(
            initial_amount=initial_multiple_cashout_value), msg='Cashout Amount is not changed')

        new_multiple_cashout_value = multiple_bet.buttons_panel.full_cashout_button.amount.value
        self.assertTrue(float(initial_multiple_cashout_value) > float(new_multiple_cashout_value),
                        msg='New cashout value "%s" is not lower than "%s"'
                            % (initial_multiple_cashout_value, new_multiple_cashout_value))

        betlegs = multiple_bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg='No betlegs found')
        betleg = betlegs.get(self.team1)
        self.assertTrue(betleg, msg='BetLeg %s is not found' % self.team1)
        new_multiple_odds_value = betleg.odds_value

        self.assertEqual(initial_odds_value, new_multiple_odds_value,
                         msg='Odds is changed from "%s" to "%s"' % (initial_odds_value, new_multiple_odds_value))
        self.__class__.initial_odds_value = initial_odds_value
        self.__class__.initial_multiple_cashout_value = new_multiple_cashout_value
        self.__class__.initial_single_cashout_value = new_single_cashout_value

    def test_003_repeat_steps_1_3_with_decreased_cash_out_value(self):
        """
        DESCRIPTION: Trigger cash out value DECREASING for **Single** bet
        DESCRIPTION: Trigger cash out value DECREASING for **Multiple** bet
        EXPECTED: Corresponding 'Price/Odds' data is not changed
        EXPECTED: Corresponding priceNum/priceDen is changed on SiteServer
        EXPECTED: 'CASH OUT' button immediately displays new cash out value
        """
        self.__class__.bet_sections = \
            self.site.sport_event_details.my_bets.accordions_list.items_as_ordered_dict
        self.assertTrue(self.bet_sections, msg='No one bet section found for event with id: %s' % self.eventID)
        self.assertIn(self.single_bet_name, self.bet_sections.keys())
        single_bet = self.bet_sections[self.single_bet_name]

        self.ob_config.change_price(selection_id=self.selection_ids[self.team1], price=self.decreased_price)
        self.assertTrue(single_bet.buttons_panel.full_cashout_button.wait_amount_to_change(initial_amount=self.initial_single_cashout_value),
                        msg='Cashout Amount is not changed')

        new_single_cashout_value = single_bet.buttons_panel.full_cashout_button.amount.value
        self.assertTrue(float(self.initial_single_cashout_value) < float(new_single_cashout_value),
                        msg='New cashout value "%s" is not larger than "%s"' % (new_single_cashout_value, self.initial_single_cashout_value))

        betlegs = single_bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg='No betlegs found')
        betleg_name, betleg = list(betlegs.items())[0]
        new_single_odds_value = betleg.odds_value

        self.assertEqual(self.initial_odds_value, new_single_odds_value,
                         msg='Odds is changed from "%s" to "%s"' % (self.initial_odds_value, new_single_odds_value))

        self.assertIn(self.multiple_bet_name, self.bet_sections.keys())
        multiple_bet = self.bet_sections[self.multiple_bet_name]

        self.assertTrue(multiple_bet.buttons_panel.full_cashout_button.wait_amount_to_change(initial_amount=self.initial_multiple_cashout_value),
                        msg='Cashout Amount is not changed')

        new_multiple_cashout_value = multiple_bet.buttons_panel.full_cashout_button.amount.value
        self.assertTrue(float(self.initial_multiple_cashout_value) < float(new_multiple_cashout_value),
                        msg='New cashout value "%s" is not lower than "%s"' % (self.initial_multiple_cashout_value, new_multiple_cashout_value))

        betlegs = multiple_bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg='No betlegs found')
        betleg = betlegs.get(self.team1)
        self.assertTrue(betleg, msg='BetLeg %s is not found' % self.team1)
        new_multiple_odds_value = betleg.odds_value

        self.assertEqual(self.initial_odds_value, new_multiple_odds_value,
                         msg='Odds is changed from "%s" to "%s"' % (self.initial_odds_value, new_multiple_odds_value))
