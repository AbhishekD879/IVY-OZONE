import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.tote
@vtest
class Test_C44870422_Verfiy_Tote_Bet_Placement_for_UK(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C44870422
    NAME: Verfiy Tote Bet Placement for UK
    PRECONDITIONS: Tote events are available on the front end
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    selection_outcomes = []
    currency = '£'
    selection_name = f'{vec.tote.PL} {vec.tote.TOTEPOOL}'
    second_tote = False

    def adding_to_betslip_for_quadtote(self):
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, self.__class__.section = list(sections.items())[0]
        pool = self.section.pool
        outcomes = list(pool.items_as_ordered_dict.items())
        self.assertTrue(outcomes, msg='No outcomes found')
        pool_legs = pool.grouping_buttons.items_as_ordered_dict
        self.assertTrue(pool_legs, 'Pool section: "%s" not contains any leg' % section_name)

        for pool_leg_name, pool_leg in pool_legs.items():
            pool.grouping_buttons.click_button(button_name=pool_leg_name)
            outcomes = pool.items_as_ordered_dict
            self.assertTrue(outcomes, msg='No outcomes found for pool leg: "%s"' % pool_leg_name)
            outcome_name, outcome = list(outcomes.items())[0]
            if outcome.runner_number:
                selection_name = '%s: %s - %s. %s' % (pool_leg_name.title(), pool.race_title,
                                                      outcome.runner_number, outcome_name)
            else:
                # there is no runner number for 'Unnamed Favourite'
                selection_name = '%s: %s - %s' % (pool_leg_name.title(), pool.race_title, outcome_name)
            self.__class__.selection_outcomes.append(selection_name)
            outcome.select()
            self.assertTrue(self.section.bet_builder.summary.no_lines.value,
                            msg='"No. Lines" values is: "%s"' % self.section.bet_builder.summary.no_lines.value)
        bet_builder = self.section.bet_builder
        for pool_leg_name, pool_leg in pool_legs.items():
            pool_leg.scroll_to()
            self.assertTrue(pool_leg.is_filled(),
                            msg='Pool leg switch button: "%s" not selected after adding selection' % pool_leg_name)
        bet_builder.summary.input.value = self.bet_amount
        bet_builder.summary.add_to_betslip_button.click()
        self.__class__.betslip_counter = self.site.header.bet_slip_counter.counter_value
        self.assertFalse(bet_builder.is_displayed(expected_result=False),
                         msg='Bet builder not disappears')
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        selections_count = self.get_betslip_content().selections_count
        self.assertEqual(selections_count, self.betslip_counter,
                         msg=f'BetSlip counter in section name "{selections_count}" and '
                             f'counter "{self.betslip_counter}" doesn\'t match')
        stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.assertTrue(self.stake.remove_button.is_displayed(),
                        msg=f'Remove button was not found for "{stake_name}"')

    def adding_to_betslip_error_for_extracta(self):
        for index, (outcome_name, outcome) in enumerate(self.outcomes[:2]):
            self.__class__.selection_outcomes.append(f'{index + 1} {outcome_name}')
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg=f'No checkboxes found for "{outcome_name}"')
            checkbox_name, checkbox = list(checkboxes.items())[index]
            checkbox.click()
            self.assertTrue(checkbox.is_selected(),
                            msg=f'Checkbox "{checkbox_name}" is not selected for "{outcome_name}" after click')
        bet_builder = self.section.bet_builder
        self.assertTrue(bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP button is not enabled')
        bet_builder.summary.add_to_betslip_button.click()
        self.site.wait_content_state_changed()
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_BETSLIP_LIMITATION, verify_name=False)
        self.assertTrue(dialog, msg='Betslip limitation popup did not appeared')
        betslip_limitiation_message = dialog.message.split("\n")
        self.assertEqual(betslip_limitiation_message[0], vec.betslip.BETSLIP_LIMITATION_MESSAGE,
                         msg=f'Actual bet slip limitation message "{betslip_limitiation_message[0]}" is not equal with '
                             f'Expected limitation message "{vec.betslip.BETSLIP_LIMITATION_MESSAGE}"')

    def test_001_open_httpsmsportsladrokescom(self):
        """
        DESCRIPTION: Open https://msports.ladrokes.com
        EXPECTED: Ladbrokes application launched
        """
        self.site.login()

    def test_002_click_on_hr(self):
        """
        DESCRIPTION: Click on HR
        EXPECTED: User navigated to HR LP
        """
        # step covered in test_003

    def test_003_select_a_uk_tote_meeting_which_contains_tote_markets_availableeg_quadpotplacepotjackpottricastexca_etc(self):
        """
        DESCRIPTION: Select a UK Tote meeting which contains Tote markets available
        DESCRIPTION: (e.g Quadpot/Placepot/Jackpot/Tricast,Exca etc)
        EXPECTED: User has selected UK Tote meeting (e.g Quadpot/Placepot/Jackpot/Tricast,Exca etc)
        """
        if not self.second_tote:
            event = self.get_uk_tote_event(uk_tote_quadpot=True)
        else:
            event = self.get_uk_tote_event(uk_tote_exacta=True)
        eventID = event.event_id
        bet_amount = event.min_total_stake
        min_stake_per_line = event.min_stake_per_line
        self.__class__.less_than_min = bet_amount - 0.03
        self.__class__.min_stake_error_message = vec.betslip.TOTE_BET_ERRORS.small_stake.format(
            stake_per_line='%.2f' % min_stake_per_line,
            stake_per_bet='%.2f' % bet_amount,
            currency=self.currency)
        self.navigate_to_edp(event_id=eventID, sport_name='horse-racing')
        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg=f'"{vec.racing.RACING_EDP_MARKET_TABS.totepool}" tab is not opened')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        self.__class__.section_name, self.__class__.section = list(sections.items())[0]
        if not self.second_tote:
            quadpot_opened = self.section.grouping_buttons.click_button(vec.uk_tote.UK_TOTE_TABS.quadpot)
            self.assertTrue(quadpot_opened, msg=f'"{vec.uk_tote.UK_TOTE_TABS.quadpot}" tab is not opened')
            self.__class__.second_tote = True
        else:
            exacta_opened = self.section.grouping_buttons.click_button(vec.uk_tote.UK_TOTE_TABS.exacta)
            self.assertTrue(exacta_opened, msg='Exacta tab is not opened')
            self.__class__.outcomes = list(self.section.pool.items_as_ordered_dict.items())
            self.assertTrue(self.outcomes, msg='No outcomes found')

    def test_004_place_bet(self):
        """
        DESCRIPTION: Place bet
        EXPECTED: Bet placed successfully
        """
        self.adding_to_betslip_for_quadtote()
        self.enter_stake_amount(stake=(self.stake.name, self.stake), stake_bet_amounts={self.stake.name: 1.00, })
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_005_verify_minimum_bets_for_eg_quadpotplacepotjackpottricastexca_etc(self):
        """
        DESCRIPTION: Verify Minimum bets for (e.g Quadpot/Placepot/Jackpot/Tricast,Exca etc)
        EXPECTED: User is prompted with minimum bet value for (e.g Quadpot/Placepot/Jackpot/Tricast,Exca etc) when attempting to place bet below this amount.
        """
        self.adding_to_betslip_for_quadtote()
        self.enter_stake_amount(stake=(self.stake.name, self.stake),
                                stake_bet_amounts={self.stake.name: self.less_than_min, })
        self.get_betslip_content().bet_now_button.click()
        actual_error_message = self.get_betslip_content().bet_amount_warning_message
        self.assertEqual(actual_error_message, self.min_stake_error_message,
                         msg=f'Incorrect error message is displayed when entering bet amount "{self.bet_amount}".\n'
                             f'Actual error message is "{actual_error_message}"\n'
                             f'Expected error message is "{self.min_stake_error_message}"')
        self.enter_stake_amount(stake=(self.stake.name, self.stake))

    def test_006_verify_only_1_tote_bet_can_be_placed_at_a_time_in_the_betslip(self):
        """
        DESCRIPTION: Verify only 1 tote bet can be placed at a time in the betslip
        EXPECTED: User displayed with only 1 tote bet in betslip and can only place 1 tote bet a time.
        """
        self.test_003_select_a_uk_tote_meeting_which_contains_tote_markets_availableeg_quadpotplacepotjackpottricastexca_etc()
        self.adding_to_betslip_error_for_extracta()
