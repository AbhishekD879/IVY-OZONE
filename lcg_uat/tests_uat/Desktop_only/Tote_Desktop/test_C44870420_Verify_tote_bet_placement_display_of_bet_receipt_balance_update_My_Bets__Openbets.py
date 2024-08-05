import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870420_Verify_tote_bet_placement_display_of_bet_receipt_balance_update_My_Bets__Openbets(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C44870420
    NAME: Verify tote bet placement, display of bet receipt , balance update, My Bets -> Openbets
    PRECONDITIONS: User is logged in.
    """
    keep_browser_open = True

    def test_001_launch_application(self):
        """
        DESCRIPTION: Launch Application.
        EXPECTED: Application is launched.
        """
        self.site.login()
        self.site.wait_content_state(state_name="Homepage")

    def test_002_navigate_to_totepool_market_from_any_hr_event_or_international_tote_pool(self):
        """
        DESCRIPTION: Navigate to Totepool market from any HR event or international Tote Pool.
        EXPECTED: Totepool market is opened.
        """
        event = self.get_uk_tote_event(uk_tote_win=True)
        eventID = event.event_id
        self.__class__.event_typename = event.event_typename.strip()
        self.__class__.bet_amount = '{0:.2f}'.format(event.min_total_stake)
        self.navigate_to_edp(event_id=eventID, sport_name='horse-racing')

        self.__class__.tab_content = self.site.racing_event_details.tab_content
        tab_opened = self.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg='"%s" tab is not opened' % vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.__class__.event_off_time = self.tab_content.event_off_times_list.selected_item

    def test_003_click_on_any_win_selection(self):
        """
        DESCRIPTION: Click on any win selection
        EXPECTED: A bar is opened at bottom which shows
        EXPECTED: 1 Win Selection
        EXPECTED: 2 Clear Selection
        EXPECTED: 3 Add to Betslip button in Green
        """
        sections = self.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')

        section_name, section = list(sections.items())[0]
        outcomes = section.pool.items_as_ordered_dict
        self.assertTrue(all(outcomes), msg='No outcomes found')
        outcome_name, outcome = list(outcomes.items())[0]

        if outcome.runner_number:
            self.__class__.runner_info = '%s %s' % (outcome.runner_number, outcome_name)
        else:
            self.__class__.runner_info = '%s' % outcome_name
        cells = outcome.items
        self.assertTrue(cells, msg=f'No cells found for "{outcome_name}"')
        cell = cells[0]
        cell.click()
        self.assertTrue(cell.is_selected(timeout=2),
                        msg=f'Win cell is not selected for "{outcome_name}" runner')

        self.__class__.bet_builder = section.bet_builder
        self.assertTrue(self.bet_builder.summary.add_to_betslip_button.is_enabled(timeout=3),
                        msg=f'"{vec.quickbet.BUTTONS.add_to_betslip}" button is not clickable')
        self.assertTrue(self.bet_builder.summary.description_title,
                        msg=f'"{vec.quickbet.BUTTONS.add_to_betslip}" button is not clickable')
        self.assertTrue(self.bet_builder.summary.clear_selection_button.is_enabled(timeout=3),
                        msg=f'"{vec.quickbet.BUTTONS.add_to_betslip}" button is not clickable')

    def test_004_click_on_add_to_betslip(self):
        """
        DESCRIPTION: Click on ADD TO BETSLIP
        EXPECTED: Your selection is added to the betslip.
        """
        self.bet_builder.summary.add_to_betslip_button.click()
        self.verify_betslip_counter_change(expected_value=1)

    def test_005_verify_details_on_betslip(self):
        """
        DESCRIPTION: Verify details on betslip
        EXPECTED: User is able to see
        EXPECTED: 1 Win Totepool
        EXPECTED: 1 Win Selection
        EXPECTED: your selection name
        EXPECTED: Time, Event Name
        EXPECTED: Today
        EXPECTED: Stake Box
        EXPECTED: Potential Returns: N/A
        EXPECTED: Total Stake  £0.00
        EXPECTED: Total Potential Returns N/A
        """
        self.__class__.user_balance = self.site.header.user_balance
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertIn(f'{vec.uk_tote.WN} {vec.uk_tote.TOTEPOOL.title()}', singles_section,
                      msg='Tote Win bet is not added to BetSlip')
        self.__class__.win_tote_stake = singles_section[f'{vec.uk_tote.WN} {vec.uk_tote.TOTEPOOL.title()}']
        self.assertEqual(self.win_tote_stake.outcome_name, f'{vec.uk_tote.WN} {vec.uk_tote.TOTEPOOL.title()}',
                         msg='Actual outcome name "%s" is not the same as expected "%s"' %
                             (self.win_tote_stake.outcome_name, f'{vec.uk_tote.WN} {vec.uk_tote.TOTEPOOL.title()}'))

        self.assertEqual(self.win_tote_stake.market_name, vec.uk_tote.ONE_SELECTION_WIN_BET,
                         msg='Actual bet type "%s" is not the same as expected "%s"' %
                             (self.win_tote_stake.market_name, vec.uk_tote.ONE_SELECTION_WIN_BET))

        selection_outcomes = self.win_tote_stake.tote_outcomes.items_as_ordered_dict
        self.assertTrue(selection_outcomes, msg='No UK Tote selections found')
        self.assertEqual(list(selection_outcomes.keys())[0], self.runner_info,
                         msg='Selected runner "%s" is not the same as expected "%s"' %
                             (list(selection_outcomes.keys())[0], self.runner_info))

        self.__class__.expected_event_title = '%s %s' % (self.event_off_time, self.event_typename)
        self.assertEqual(self.win_tote_stake.event_name, self.expected_event_title,
                         msg='Actual event name "%s" is not the same as expected "%s"' %
                             (self.win_tote_stake.event_name, self.expected_event_title))

        self.assertIn(self.win_tote_stake.event_date, ['Today', 'Tomorrow'],
                      msg='Actual event date: "%s" is not is not matched with: "Today"or "Tomorrow"' %
                      self.win_tote_stake.event_date)

        self.assertEqual(self.win_tote_stake.est_returns, 'N/A',
                         msg=f'Est. Returns value: "{self.win_tote_stake.est_returns}" is not the same as expected: "N/A"')

        total_stake = self.get_betslip_content().total_stake
        self.assertEqual(total_stake, "0.00",
                         msg='Actual total stake amount value "%s" is not the same as expected "%s"' %
                             (total_stake, "0.00"))

        total_estimate_returns = self.get_betslip_content().total_estimate_returns
        self.assertEqual(total_estimate_returns, 'N/A',
                         msg=f'Total Est. Returns is "{total_estimate_returns}" not "N/A"')

    def test_006_enter_stake_and_place_bet_minimum_stake_is_200(self):
        """
        DESCRIPTION: Enter Stake and place bet (Minimum stake is £2.00)
        EXPECTED: User is able to seedata-crlat="totalEstReturns"
        EXPECTED: 1 Win Totepool
        EXPECTED: 1 Win Selection
        EXPECTED: your selection name
        EXPECTED: Time, Event Name
        EXPECTED: Today
        EXPECTED: Stake for this bet: £2:00
        EXPECTED: Pot. Returns: N/A
        EXPECTED: Total Stake  £2.00
        EXPECTED: Total Potential Returns N/A
        """
        self.enter_stake_amount(stake=(self.win_tote_stake.name, self.win_tote_stake))
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()

        receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(receipt_sections, msg='No receipt sections found in BetReceipt')
        receipt_bet_type_section = receipt_sections.get(vec.betslip.SINGLE)
        section_items = receipt_bet_type_section.items_as_ordered_dict
        self.assertTrue(section_items, msg='No bets found in BetReceipt')
        bet_info = list(section_items.values())[0]

        self.assertEqual(bet_info.name, f'{vec.uk_tote.WN} {vec.uk_tote.TOTEPOOL.title()}',
                         msg='Actual outcome name "%s" is not the same as expected "%s"' %
                             (bet_info.name, f'{vec.uk_tote.WN} {vec.uk_tote.TOTEPOOL.title()}'))

        self.assertEqual(bet_info.event_market_name, self.expected_event_title,
                         msg='Actual event name "%s" is not the same as expected "%s"' %
                             (bet_info.event_market_name, self.expected_event_title))

        self.assertEqual(bet_info.estimate_returns, 'N/A',
                         msg=f'Est. Returns value: "{bet_info.estimate_returns}" is not the same as expected: "N/A"')

        self.assertEqual(bet_info.total_stake, self.bet_amount,
                         msg='Actual total stake amount value "%s" is not the same as expected "%s"' %
                             (bet_info.total_stake, self.bet_amount))

        self.assertEqual(self.site.bet_receipt.footer.total_estimate_returns, 'N/A',
                         msg=f'Total Est. Returns is "{self.site.bet_receipt.footer.total_estimate_returns}" not "N/A"')

        self.assertEqual(self.site.bet_receipt.footer.total_stake, self.bet_amount,
                         msg='Actual total stake amount value "%s" is not the same as expected "%s"' %
                             (self.site.bet_receipt.footer.total_stake, self.bet_amount))

    def test_007_verify_your_balance_update(self):
        """
        DESCRIPTION: verify your balance update
        EXPECTED: Balance should be updated accordingly.
        """
        updated_balance = self.site.header.user_balance
        self.assertEqual(updated_balance, self.user_balance - float(self.bet_amount),
                         msg=f'Actual balance: "{updated_balance}" is not updated as Expected balance: "{self.user_balance - float(self.bet_amount)}"')
