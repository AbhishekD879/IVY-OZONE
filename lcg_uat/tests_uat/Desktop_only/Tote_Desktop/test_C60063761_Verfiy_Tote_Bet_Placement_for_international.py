import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_011_RACES_Specifics.Horse_Racing_Specifics.Horse_Racing_Event_Details_Page.Tote_Pool_tab.BaseInternationalTote import BaseInternationalTote
from collections import OrderedDict


@pytest.mark.desktop
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.tote
@pytest.mark.uat
@vtest
class Test_C60063761_Verfiy_Tote_Bet_Placement_for_international(BaseInternationalTote, BaseBetSlipTest):
    """
    TR_ID: C60063761
    NAME: Verfiy Tote Bet Placement for international
    PRECONDITIONS: International Tote events are available on the front end
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    selection_name = f'{vec.tote.WN} {vec.tote.TOTEPOOL}'
    exchange_rates = {}
    second_int_tote = False

    def int_tote_adding_to_betslip(self):
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.pool.items_as_ordered_dict
        self.assertTrue(all(outcomes), msg='No outcomes found')
        active_outcomes = [(outcome_name, outcome) for (outcome_name, outcome) in outcomes.items() if
                           outcome.is_enabled()]
        _temp = []
        for outcome_name, outcome in active_outcomes[:2]:
            cells = outcome.items
            self.assertTrue(cells, msg=f'No cells found for "{outcome_name}"')
            cell = cells[0]
            cell.click()
            self.assertTrue(cell.is_selected(timeout=2),
                            msg=f'Place cell is not selected for "{outcome_name}" runner')
            _temp.append((outcome_name, outcome.runner_number if outcome.runner_number else None))

        self.added_runners = OrderedDict(_temp)

        bet_builder = section.bet_builder
        self.assertTrue(bet_builder.is_displayed(timeout=3), msg='Bet builder is not shown')
        self.assertTrue(bet_builder.summary.add_to_betslip_button.is_enabled(timeout=3),
                        msg=f'"{vec.quickbet.BUTTONS.add_to_betslip}" button is not clickable')
        bet_builder.summary.add_to_betslip_button.click()
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.selection_name, singles_section, msg='Tote Place bet is not added to BetSlip')
        self.__class__.place_tote_stake = singles_section[self.selection_name]

    def adding_to_betslip_error_for_place(self):
        outcomes = self.get_single_leg_outcomes(event_id=self.eventID, tab_name=vec.tote.TOTE_TABS.place)
        first_outcome_name, first_outcome_value = outcomes[0]
        first_outcome_value.items[0].click()
        self.assertTrue(first_outcome_value.items[0].is_selected(timeout=2),
                        msg=f'Place cell is not selected for "{first_outcome_name}" runner')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        bet_builder = section.bet_builder
        self.assertTrue(bet_builder.is_displayed(timeout=3), msg='Bet builder is not shown')
        self.assertTrue(bet_builder.summary.add_to_betslip_button.is_enabled(timeout=3),
                        msg=f'"{vec.quickbet.BUTTONS.add_to_betslip}" button is not clickable')
        bet_builder.summary.add_to_betslip_button.click()
        self.site.wait_content_state_changed()
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_BETSLIP_LIMITATION,
                                           verify_name=False)
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
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_003_select_a_international_tote_meeting_which_contains_tote_markets_availableeg_quadpotplacepotjackpottricastexca_etc(self):
        """
        DESCRIPTION: Select a International Tote meeting which contains Tote markets available
        DESCRIPTION: (e.g Quadpot/Placepot/Jackpot/Tricast,Exca etc)
        EXPECTED: User has selected International Tote meeting (e.g Quadpot/Placepot/Jackpot/Tricast,Exca etc)
        """
        if not self.second_int_tote:
            event = self.get_int_tote_event(int_tote_win=True)
        else:
            event = self.get_int_tote_event(int_tote_place=True)
        self._logger.info(f'*** Found event with parameters "{event}"')
        self.__class__.eventID = event.event_id
        bet_amount = event.min_total_stake
        self.__class__.less_than_min = bet_amount - 0.03
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        tab_content = self.site.racing_event_details.tab_content
        tab_opened = tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg=f'"{vec.racing.RACING_EDP_MARKET_TABS.totepool}" tab is not opened')
        sections = tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        if not self.second_int_tote:
            win_tab_opened = section.grouping_buttons.click_button(vec.tote.TOTE_TABS.win)
            self.assertTrue(win_tab_opened, msg=f'"{vec.tote.TOTE_TABS.win}" tab is not opened for "{section_name}"')
        else:
            place_tab_opened = section.grouping_buttons.click_button(vec.tote.TOTE_TABS.place)
            self.assertTrue(place_tab_opened, msg=f'"{vec.tote.TOTE_TABS.place}" tab is not opened for "{section_name}"')
            self.__class__.second_int_tote = True

    def test_004_place_bet(self):
        """
        DESCRIPTION: Place bet
        EXPECTED: Bet placed successfully
        """
        self.int_tote_adding_to_betslip()
        self.enter_stake_amount(stake=(self.place_tote_stake.name, self.place_tote_stake))
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_005_verify_minimum_bets_for_eg_quadpotplacepotjackpottricastexca_etc(self):
        """
        DESCRIPTION: Verify Minimum bets for (e.g Quadpot/Placepot/Jackpot/Tricast,Exca etc)
        EXPECTED: User is prompted with minimum bet value for (e.g Quadpot/Placepot/Jackpot/Tricast,Exca etc) when attempting to place bet below this amount.
        """
        self.int_tote_adding_to_betslip()
        self.enter_stake_amount(stake=(self.place_tote_stake.name, self.place_tote_stake),
                                stake_bet_amounts={self.place_tote_stake.name: self.less_than_min, })
        self.get_betslip_content().bet_now_button.click()
        actual_error_message = self.get_betslip_content().bet_amount_warning_message
        expected_error_message = vec.betslip.BET_REJECTED_ERROR.split("by")
        self.assertIn(actual_error_message, expected_error_message[0],
                      msg='Incorrect error message is displayed when entering bet amount'
                          f'Actual error message is "{actual_error_message}"\n'
                          f'Expected error message is "{expected_error_message[0]}"')
        self.enter_stake_amount(stake=(self.place_tote_stake.name, self.place_tote_stake))

    def test_006_verify_only_1_tote_bet_can_be_placed_at_a_time_in_the_betslip(self):
        """
        DESCRIPTION: Verify only 1 tote bet can be placed at a time in the betslip
        EXPECTED: User displayed with only 1 tote bet in betslip and can only place 1 tote bet a time.
        """
        self.test_003_select_a_international_tote_meeting_which_contains_tote_markets_availableeg_quadpotplacepotjackpottricastexca_etc()
        self.adding_to_betslip_error_for_place()
