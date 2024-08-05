from time import sleep

import pytest
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.user_journey_football_multiple
@pytest.mark.event_details
@pytest.mark.liveserv_updates
@pytest.mark.bet_placement
@pytest.mark.my_bets
@pytest.mark.cash_out
@pytest.mark.slow
@pytest.mark.safari
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C238033_C237389_Cash_Out_bet_lines_with_errors_filtered_by_proxy_and_UI(BaseCashOutTest, BaseUserAccountTest):
    """
    TR_ID: C238033
    TR_ID: C237389
    VOL_ID: C9698422
    NAME: Cash Out bet lines with errors filtered by proxy and UI
    """
    keep_browser_open = True
    bet_amount = 1
    number_of_events = 2
    expected_status = 'susp'

    def get_bet_sections(self):
        try:
            wait_for_result(lambda: self.site.sport_event_details.my_bets.accordions_list.items_as_ordered_dict,
                            name='Bet sections to appear',
                            bypass_exceptions=(NoSuchElementException, ),
                            timeout=5)
        except (StaleElementReferenceException, VoltronException):
            wait_for_result(lambda: self.site.sport_event_details.my_bets.accordions_list.items_as_ordered_dict,
                            name='Bet sections to appear',
                            bypass_exceptions=(NoSuchElementException,),
                            timeout=1)
        bet_sections = self.site.sport_event_details.my_bets.accordions_list.items_as_ordered_dict
        self.assertTrue(bet_sections, msg='No one bet section found for event with id: %s' % self.eventID)
        self.assertIn(self.single_bet_name, bet_sections.keys())
        self.assertIn(self.multiple_bet_name, bet_sections.keys())
        self.__class__.single_bet_section = bet_sections[self.single_bet_name]
        self.__class__.multiple_bet_section = bet_sections[self.multiple_bet_name]

    def get_bet_status_from_cashout(self, bet):
        betlegs = bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg=f'No bet leg was found for bet "{bet.name}"')
        betleg_name, betleg = list(betlegs.items())[0]
        return betleg.icon.status if betleg.has_icon_status() else False

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events, place Single and Multiple cashout available bets
        EXPECTED: Created football test events
        """
        self.__class__.events_info = self.create_several_autotest_premier_league_football_events(
            number_of_events=self.number_of_events)
        self.site.login(username=tests.settings.betplacement_user)

        for event_info in self.events_info:
            self.__class__.selection_ids[event_info.team1] = event_info.selection_ids[event_info.team1]
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values()))

        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiples_section = sections.Singles, sections.Multiples

        for stake in self.zip_available_stakes(section=singles_section, number_of_stakes=1).items():
            self.enter_stake_amount(stake=stake)

        for stake in self.zip_available_stakes(section=multiples_section, number_of_stakes=1).items():
            self.enter_stake_amount(stake=stake)

        betnow_section = self.get_betslip_content().betnow_section
        betnow_section.bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        self.site.has_betslip_opened(expected_result=False)
        list_of_keys = list(self.selection_ids.keys())
        self.__class__.single_bet_name = 'SINGLE - [%s]' % list_of_keys[0]
        self.__class__.multiple_bet_name = 'DOUBLE - [%s]' % ', '.join(list_of_keys)
        self.__class__.eventID = self.events_info[0].event_id

    def test_001_navigate_to_event_details_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets from preconditions
        """
        self.navigate_to_edp(self.eventID)
        self.site.sport_event_details.event_user_tabs_list.open_tab(tab_name=self.my_bets_tab_name)

    def test_002_verify_single_and_multiple_cash_out_bet_lines(self):
        """
        DESCRIPTION: Verify Single and Multiple Cash Out bet lines
        EXPECTED: Single and Multiple bets are shown with 'FULL CASH OUT' and 'PARTIAL CASH OUT' buttons:
        """
        # ToDo: fails here because of VOL-2535, passes in debug mode
        self.get_bet_sections()
        self.assertTrue(self.single_bet_section.buttons_panel.has_full_cashout_button(),
                        msg='"FULL CASH OUT" button was not found in bet section: "%s"' % self.single_bet_name)
        self.assertTrue(self.multiple_bet_section.buttons_panel.has_full_cashout_button(),
                        msg='"FULL CASH OUT" button was not found in bet section: "%s"' % self.multiple_bet_name)

        # We shouldn't verify partial CashOut on non-prod envs
        # self.assertTrue(self.single_bet_section.buttons_panel.has_partial_cashout_button(),
        #                 msg='"PARTIAL CASH OUT" button was not found in bet section: "%s"' % self.single_bet_name)
        # self.assertTrue(self.multiple_bet_section.buttons_panel.has_partial_cashout_button(),
        #                 msg='"PARTIAL CASH OUT" button was not found in bet section: "%s"' % self.multiple_bet_name)

    def test_003_trigger_cash_out_status_that_is_not_filtered_by_the_proxy(self):
        """
        DESCRIPTION: In OB Backoffice trigger cashOutStatus that is not filtered by the proxy for event with placed
        DESCRIPTION: Single bet (i.e. 'CASHOUT_SELN_NO_CASHOUT' cashOutStatus via disabling 'Cashout Available' option and undisplaying event/market/selection)
        """
        # need to trigger OB changes with some delay to make test run more stable
        sleep(2)
        self.ob_config.change_event_cashout_status(event_id=self.eventID, cashout_available=False)
        sleep(2)
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=True)
        # need back event displaying state to be able get EDP
        sleep(2)

    def test_004_verify_single_and_multiple_bet_lines_with_modified_event(self):
        """
        DESCRIPTION: Verify Single and Multiple bet lines with modified event
        EXPECTED: Bet is displayed on 'Cash Out' tab
        EXPECTED: 'FULL CASH OUT' and 'PARTIAL CASH OUT' buttons are not shown
        """
        self.get_bet_sections()

        self.assertFalse(self.single_bet_section.buttons_panel.has_full_cashout_button(expected_result=False, timeout=10),
                         msg=f'"FULL CASH OUT" button was found in bet section: "{self.single_bet_name}"')
        self.assertFalse(self.multiple_bet_section.buttons_panel.has_full_cashout_button(expected_result=False),
                         msg=f'"FULL CASH OUT" button was found in bet section: "{self.multiple_bet_name}"')

        # We shouldn't verify partial CashOut on non-prod envs
        # self.assertFalse(self.multiple_bet_section.buttons_panel.has_partial_cashout_button(expected_result=False),
        #                  msg='"PARTIAL CASH OUT" button was found in bet section: "%s"' % self.multiple_bet_name)
        # self.assertFalse(self.single_bet_section.buttons_panel.has_partial_cashout_button(expected_result=False),
        #                  msg='"PARTIAL CASH OUT" button was found in bet section: "%s"' % self.single_bet_name)

    def test_005_verify_bet_is_displayed_as_a_normal_non_cash_out_bet(self):
        """
        DESCRIPTION: Wait 5 seconds
        EXPECTED: Error message disappears
        EXPECTED: Bet is displayed as a normal non-Cash Out bet
        EXPECTED: 'FULL CASH OUT' and 'PARTIAL CASH OUT' buttons are not shown
        """
        self.get_bet_sections()
        self.assertFalse(self.single_bet_section.buttons_panel.has_full_cashout_button(expected_result=False),
                         msg=f'"FULL CASH OUT" button was found in bet section: "{self.single_bet_name}"')
        self.assertFalse(self.multiple_bet_section.buttons_panel.has_full_cashout_button(expected_result=False),
                         msg=f'"FULL CASH OUT" button was found in bet section: "{self.multiple_bet_name}"')
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        sleep(2)  # so the event state got changed

    def test_006_refresh_page(self):
        """
        DESCRIPTION: Refresh page
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state(state_name='EventDetails', timeout=10)
        self.site.sport_event_details.event_user_tabs_list.open_tab(tab_name=self.my_bets_tab_name, timeout=5)

    def test_007_verify_single_and_multiple_bet_lines_with_modified_event(self):
        """
        DESCRIPTION: Verify Single and Multiple bet lines with modified event
        EXPECTED: Bet is displayed as a normal non-Cash Out bet without error
        """
        self.test_005_verify_bet_is_displayed_as_a_normal_non_cash_out_bet()

    def test_008_revert_cashout_status_for_event(self):
        """
        DESCRIPTION: Revert Cash Out status for event
        EXPECTED: 'CASH OUT' and 'Partial CashOut' buttons are shown under bet details instead of error message
        """
        self.ob_config.change_event_cashout_status(event_id=self.eventID, cashout_available=True)

    def test_009_verify_single_and_multiple_cash_out_bet_lines(self):
        """
        DESCRIPTION: Verify Single and Multiple Cash Out bet lines
        EXPECTED: 'CASH OUT' and 'Partial CashOut' buttons are shown under bet details instead of error message
        """
        self.test_006_refresh_page()
        self.test_002_verify_single_and_multiple_cash_out_bet_lines()

    def test_010_trigger_selection_suspended(self):
        """
        DESCRIPTION: Trigger selections suspended situation
        EXPECTED: Single and Multiple bet lines are shown with 2 error messages instead of 'CASH OUT' button
        """
        self.ob_config.change_selection_state(selection_id=list(list(self.selection_ids.values()))[0], displayed=True,
                                              active=False)
        self.ob_config.change_event_cashout_status(event_id=self.eventID, cashout_available=False)
        self.test_006_refresh_page()
        self.test_004_verify_single_and_multiple_bet_lines_with_modified_event()

        actual_status = self.get_bet_status_from_cashout(self.single_bet_section)
        self.assertEqual(self.expected_status, actual_status,
                         msg=f'Actual status "{actual_status}" does not equal to expected "{self.expected_status}"')
        actual_status = self.get_bet_status_from_cashout(self.multiple_bet_section)
        self.assertEqual(self.expected_status, actual_status,
                         msg=f'Actual status "{actual_status}" does not equal to expected "{self.expected_status}"')

    def test_011_repeat_steps_6_7(self):
        """
        DESCRIPTION: Repeat steps 6-7
        """
        self.test_006_refresh_page()
        self.test_007_verify_single_and_multiple_bet_lines_with_modified_event()

    def test_012_revert_selection_statuses(self):
        """
        DESCRIPTION: Revert selections status
        EXPECTED: 'CASH OUT' and 'Partial CashOut' buttons are shown under bet details instead of error message
        """
        self.ob_config.change_selection_state(selection_id=list(list(self.selection_ids.values()))[0], displayed=True,
                                              active=True)
        self.ob_config.change_event_cashout_status(event_id=self.eventID, cashout_available=True)
        self.test_006_refresh_page()
        self.test_002_verify_single_and_multiple_cash_out_bet_lines()
