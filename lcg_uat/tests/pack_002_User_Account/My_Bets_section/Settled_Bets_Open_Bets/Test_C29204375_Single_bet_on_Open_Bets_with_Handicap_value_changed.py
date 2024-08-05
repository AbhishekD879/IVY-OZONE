import voltron.environments.constants as vec
import pytest
import tests
from tests.base_test import vtest
from voltron.utils.helpers import generate_name
from voltron.utils.waiters import wait_for_result
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #can not create OB event in PROD
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@vtest
class Test_C29204375_Single_bet_on_Open_Bets_with_Handicap_value_changed(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C29204375
    NAME: Single bet on Open Bets with Handicap value changed
    DESCRIPTION: This test case verifies single in-play bet on Open Bets tab when handicap value has changed.
    DESCRIPTION: Prod Incident: https://jira.egalacoral.com/browse/BMA-47150
    PRECONDITIONS: - user is logged in
    PRECONDITIONS: - user has navigated to Football In-Play page
    PRECONDITIONS: - event with handicap market should be available
    PRECONDITIONS: NOTE: For new cashout (CMS -> Cashout'isV4Enabled') use 'bet-details' response to check the bet error.
    """
    keep_browser_open = True
    old_handicap_value = "1.2"

    def test_000_create_test_event(self):
        """
        DESCRIPTION: Create test event
        """
        event = self.ob_config.add_autotest_premier_league_football_event(team1=generate_name(),
                                                                          team2=generate_name(),
                                                                          markets=[('handicap_match_result', {'cashout': True})],
                                                                          is_live=True)
        self.__class__.eventID = event.event_id
        self.__class__.selection_ids = list(event.ss_response.values())[0]["name"]

    def test_001_place_single_in_play_bet_which_contains_handicap_value(self):
        """
        DESCRIPTION: Place single in-play bet which contains HANDICAP value
        EXPECTED: Bet is placed successfully
        """
        self.site.login()
        self.navigate_to_edp(event_id=self.eventID)
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        handicap = markets_list.get(self.expected_market_sections.handicap_results)
        self.assertTrue(handicap, msg='*** Can not find Handicap market section')

        outcome_groups = handicap.outcomes.items_as_ordered_dict
        self.assertTrue(outcome_groups, msg='Outcome groups is empty')
        outcome_group_name, outcome_group = list(outcome_groups.items())[0]
        outcomes = outcome_group.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No one outcome was found in section: "%s"' % outcome_group_name)
        outcome_name, outcome = list(outcomes.items())[0]
        outcome.click()
        if self.device_type == 'mobile':
            quick_bet = self.site.quick_bet_panel
            self.assertEqual(quick_bet.header.title, vec.quickbet.QUICKBET_TITLE,
                             msg=f'Actual title "{quick_bet.header.title}" does not match expected "{vec.quickbet.QUICKBET_TITLE}"')
            quick_bet_panel = self.site.quick_bet_panel
            quick_bet = quick_bet_panel.selection.content
            quick_bet.amount_form.input.value = self.bet_amount

            amount = float(quick_bet.amount_form.input.value)
            self.assertEqual(amount, self.bet_amount,
                             msg=f'Entered amount "{amount}" is not equal to expected "{self.bet_amount}"')
            if self.site.wait_for_quick_bet_panel(timeout=2):
                self.site.quick_bet_panel.add_to_betslip_button.click()
                self.site.wait_for_quick_bet_panel(expected_result=False)
                self.site.wait_quick_bet_overlay_to_hide()
                self.site.open_betslip()
                betslip_content = self.get_betslip_content()
                self.assertTrue(betslip_content.header.has_user_balance,
                                msg='Balance is not displayed at the top right corner')
        self.__class__.single_bet_name = 'SINGLE - [%s]' % self.selection_ids
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_002_navigate_to_open_bets_tab(self):
        """
        DESCRIPTION: Navigate to Open Bets tab
        EXPECTED: - tab is opened
        EXPECTED: - Placed bet is displayed
        """
        self.site.open_my_bets_open_bets()
        result = wait_for_result(
            lambda: self.site.open_bets.tab_content.grouping_buttons.current == self.expected_active_btn_open_bets,
            name=f'to became active"{self.expected_active_btn_open_bets}"',
            timeout=2)
        self.assertTrue(result, msg=f'sorting type is not selected by default:"{self.expected_active_btn_open_bets}"')

    def test_003_trigger_cashout_unavailable_for_the_bet_eg_change_handicap_value_from_22___122(self):
        """
        DESCRIPTION: Trigger cashout unavailable for the bet (eg. change handicap value from: 2.2 -> 12.2)
        EXPECTED: - Bet is still displayed on Open Bets tab and does not disappear even when cashout for bet is unavailable (cashout button is disabled)
        EXPECTED: - Error is received in Network: 'getBetDetail' response:
        EXPECTED: cashoutStatus: "Cashout unavailable: Selections are not available for cashout"
        EXPECTED: cashoutValue: "CASHOUT_SELN_NO_CASHOUT"
        EXPECTED: - Bet does not disappear after few seconds
        """
        self.ob_config.change_event_cashout_status(event_id=self.eventID, cashout_available=False)
        self.device.refresh_page()
        self.site.open_my_bets_open_bets()
        bet_sections = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bet_sections, msg='No one bet section found for event with id: %s' % self.eventID)
        self.assertIn(self.single_bet_name, bet_sections.keys())
        single_bet_section = bet_sections[self.single_bet_name]
        self.assertFalse(single_bet_section.buttons_panel.has_full_cashout_button(),
                         msg='"FULL CASH OUT" button  found in bet section: "%s"' % self.single_bet_name)
