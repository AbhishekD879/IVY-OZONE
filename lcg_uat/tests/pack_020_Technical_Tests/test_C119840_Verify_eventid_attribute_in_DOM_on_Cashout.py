import pytest

from tests.base_test import vtest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.cash_out
@pytest.mark.evergage
@pytest.mark.bet_placement
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.login
@vtest
class Test_C119840_Verify_eventID_attribute_in_DOM_on_Cashout(BaseCashOutTest):
    """
    TR_ID: C119840
    NAME: Verify 'eventid' attribute in the DOM/HTML on Cashout page
    DESCRIPTION: This Test Case verifies 'eventid' attribute in the DOM/HTML on Cashout page.
    """
    keep_browser_open = True
    bet_amount = 1.00
    created_events = None

    def test_001_run_cashout_preconditions(self):
        """
        DESCRIPTION: Run Cashout preconditions:
        DESCRIPTION: - Create 2 events
        DESCRIPTION: - Login and place a bet on multiples selection
        DESCRIPTION: - Place a bet on a singles and multiples selection
        EXPECTED: Bet on multiple selections is placed
        """
        system_config = self.get_initial_data_system_configuration()
        cashout_cms = system_config.get('CashOut')
        if not cashout_cms:
            cashout_cms = self.cms_config.get_system_configuration_item('CashOut')
        if not cashout_cms:
            raise CmsClientException('CashOut section not found in System Configuration')
        is_cashout_tab_enabled = cashout_cms.get('isCashOutTabEnabled')
        if not is_cashout_tab_enabled:
            raise CmsClientException('CashOut tab is not enabled in CMS')

        self.__class__.created_events = self.create_several_autotest_premier_league_football_events(number_of_events=2)
        self.site.login()
        self.open_betslip_with_selections(selection_ids=[event_info.selection_ids[event_info.team1] for event_info in
                                                         self.created_events])
        self.place_bet_on_all_available_stakes()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_002_navigate_to_cash_out_tab(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab
        EXPECTED: 'Cash out' tab is opened
        """
        self.site.open_my_bets_cashout()

    def test_003_check_event_id_on_cashout_page_for_single(self):
        """
        DESCRIPTION: Check event id attribute is present for Single bet
        EXPECTED: Event id is present for placed bets on Cashout page
        """
        single_bet_name, single_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            event_names=[self.created_events[0].event_name], bet_type='SINGLE', number_of_bets=3)
        betlegs = single_bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg=f'No betlegs found for "{single_bet_name}"')
        bet_leg_name, bet_leg = list(betlegs.items())[0]

        outcome_name = bet_leg.outcome_name
        expected_event_id = next((event.event_id for event in self.created_events if event.team1 == outcome_name), None)
        self.assertTrue(expected_event_id, msg=f'Cannot find related event id for selection '
                                               f'"{outcome_name}" in "{self.created_events}"')
        actual_event_id = bet_leg.event_id
        self._logger.info(f'*** Verifying event id for bet leg "{bet_leg_name}", event id is: "{actual_event_id}"')
        self.assertEqual(actual_event_id, expected_event_id)

    def test_004_check_event_id_on_cashout_page_for_multiple(self):
        """
        DESCRIPTION: Check event id attribute is present for Multiple bet
        EXPECTED: Event id is present for placed bets on Cashout page
        """
        double_bet_name, double_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            event_names=[event.event_name for event in self.created_events], bet_type='DOUBLE', number_of_bets=3)
        betlegs = double_bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg=f'No betlegs found for "{double_bet_name}"')
        for bet_leg_name, bet_leg in betlegs.items():
            outcome_name = bet_leg.outcome_name
            expected_event_id = next((event.event_id for event in self.created_events if event.team1 == outcome_name),
                                     None)
            self.assertTrue(expected_event_id, msg=f'Cannot find related event id for selection '
                                                   f'"{outcome_name}" in "{self.created_events}"')
            actual_event_id = bet_leg.event_id
            self._logger.info(f'*** Verifying event id for bet leg "{bet_leg_name}", event id is: "{actual_event_id}"')
            self.assertEqual(actual_event_id, expected_event_id,
                             msg=f'Actual event ID: "{actual_event_id}" is not equal to expected: "{expected_event_id}"')
