import pytest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # As bets needs to be settled, cannot script it on prod.
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C9618066_Verify_displaying_of_edited_ACCA_in_Settled_Bet(BaseBetSlipTest):
    """
    TR_ID: C9618066
    NAME: Verify displaying of edited ACCA in Settled Bet
    DESCRIPTION: This test case verifies the view of an edited ACCA on My Bets>Settled Bets
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: 1. Login with User1
    PRECONDITIONS: 2. Place Single line Multiple Bet (e.g. ACCA5)
    PRECONDITIONS: 3. Go to By Bets> Open Bets tap 'EDIT MY ACCA' for placed bet
    PRECONDITIONS: 4. Remove few selections from the bet and save changes
    PRECONDITIONS: Note: all data in Step1 is based on received data from BPP in Network -> accountHistory?detailLevel=DETAILED&fromDate=<DateFrom>%2000%3A00%3A00&toDate=<DateTo> Request
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Enable My ACCA feature toggle in CMS
        PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
        PRECONDITIONS: 1. Login
        PRECONDITIONS: 2. Place Single line Multiple Bet (e.g. ACCA5)
        PRECONDITIONS: 3. Go to By Bets> Open Bets tap 'EDIT MY ACCA' for placed bet
        PRECONDITIONS: 4. Remove few selections from the bet and save changes
        """
        if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
            self.cms_config.set_my_acca_section_cms_status(ema_status=True)

        event = self.ob_config.add_autotest_premier_league_football_event()
        event2 = self.ob_config.add_autotest_premier_league_football_event()
        event3 = self.ob_config.add_autotest_premier_league_football_event()
        event4 = self.ob_config.add_autotest_premier_league_football_event()
        event5 = self.ob_config.add_autotest_premier_league_football_event()
        self.selection_ids = [event.selection_ids[event.team1],
                              event2.selection_ids[event2.team1],
                              event3.selection_ids[event3.team1],
                              event4.selection_ids[event4.team1],
                              event5.selection_ids[event5.team1]]

        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()

        self.__class__.event_id = event.event_id
        self.__class__.event_name = '%s v %s' % (event.team1, event.team2)
        self.__class__.market_id = self.ob_config.market_ids[event.event_id][market_short_name]
        self.__class__.selection_id = event.selection_ids[event.team1]

        self.__class__.event2_id = event2.event_id
        self.__class__.market2_id = self.ob_config.market_ids[event2.event_id][market_short_name]
        self.__class__.selection2_id = event2.selection_ids[event2.team1]

        self.__class__.event3_id = event3.event_id
        self.__class__.market3_id = self.ob_config.market_ids[event3.event_id][market_short_name]
        self.__class__.selection3_id = event3.selection_ids[event3.team1]

        self.__class__.event4_id = event4.event_id
        self.__class__.market4_id = self.ob_config.market_ids[event4.event_id][market_short_name]
        self.__class__.selection4_id = event4.selection_ids[event4.team1]

        self.__class__.event5_id = event5.event_id
        self.__class__.market5_id = self.ob_config.market_ids[event5.event_id][market_short_name]
        self.__class__.selection5_id = event5.selection_ids[event5.team1]

        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_open_bets()
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='"Bet types are not displayed"')
        self.__class__.bet_before_EMA = list(bets.values())[0]
        self.assertTrue(self.bet_before_EMA.edit_my_acca_button.is_displayed(),
                        msg=f'"{vec.ema.EDIT_MY_BET}" Button is not displayed')
        self.__class__.bet_type_before_EMA = self.bet_before_EMA.bet_type
        self.__class__.actual_potential_returns = self.bet_before_EMA.est_returns.value
        self.bet_before_EMA.edit_my_acca_button.click()
        sleep(1)
        selection = list(self.bet_before_EMA.items_as_ordered_dict.values())[0]
        selection.edit_my_acca_remove_icon.click()
        sleep(2)
        self.assertTrue(wait_for_result(lambda: selection.edit_my_acca_undo_icon.is_displayed(), timeout=3),
                        msg=f'"{vec.ema.UNDO_LEG_REMOVE}" Button" not displayed')

        self.bet_before_EMA.confirm_button.click()
        self.site.wait_content_state_changed()

    def test_001_go_to_my_betsopen_betsverify_that_the_edited_acca_is_shown_with_all_appropriate_elements(self, open_bets=True):
        """
        DESCRIPTION: Go to My Bets>Open Bets
        DESCRIPTION: Verify that the edited ACCA is shown with all appropriate elements
        EXPECTED: The edited ACCA is shown with appropriate elements:
        EXPECTED: - Updated ACCA Bet Type
        EXPECTED: - Bet Result for ACCA bet
        EXPECTED: - Total stake which was used for the edited ACCA
        EXPECTED: - Returns value
        EXPECTED: - Event name is displayed for all remaining selections
        EXPECTED: - Event Date and Time
        EXPECTED: - Market names for all remaining selections
        EXPECTED: - Selection name for all remaining selections
        EXPECTED: - Prices accepted for the new ACCA for all selections
        EXPECTED: - Scores result (if available)
        EXPECTED: - Status for each selection
        EXPECTED: - 'SHOW EDIT HISTORY' button is shown
        """
        self.device.refresh_page()
        if open_bets:
            self.site.open_my_bets_open_bets()
            new_bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        else:
            self.site.open_my_bets_settled_bets()
            new_bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(new_bets, msg='"New bet" types are not displayed')
        self.__class__.bet_after_EMA = list(new_bets.values())[0]
        self.assertTrue(self.bet_after_EMA.show_edit_history_button.is_displayed(),
                        msg=f'"{vec.ema.HISTORY.show_history}" is not displayed')
        bet_type_after_EMA = self.bet_after_EMA.bet_type
        self.assertNotEqual(bet_type_after_EMA, self.bet_type_before_EMA,
                            msg='"New bet type" is  not changed')
        stake_after_EMA = self.bet_after_EMA.stake.value
        self.assertTrue(stake_after_EMA, msg='stake is not displayed')
        new_potential_returns = self.bet_after_EMA.est_returns.value
        self.assertNotEqual(self.actual_potential_returns, new_potential_returns,
                            msg=f'Actual potential returns:"{self.actual_potential_returns}" is same as New potential returns:"{new_potential_returns}".')
        selections = self.bet_before_EMA.items_as_ordered_dict.values()
        for selection in list(selections):
            self.assertTrue(selection.event_name, msg=f'"{selection.event_name}" is not displayed')
            self.assertTrue(selection.market_name, msg=f'"{selection.market_name}" is not displayed')
            self.assertTrue(selection.outcome_name, msg=f'"{selection.outcome_name}" is not displayed')
            self.assertTrue(selection.odds_value, msg=f'"{selection.odds_value}" is not displayed')
            self.assertTrue(selection.event_time, msg=f'"{selection.event_time}" is not displayed')

    def test_002_make_a_placed_bet_edited_bet_settled_add_and_settle_the_result_for_each_event_in_the_edited_betverify_that_the_new_bet_is_resulted_and_shown_on_by_betsbet_historysettled_bets(self):
        """
        DESCRIPTION: Make a placed bet (edited bet) SETTLED (add and settle the result for each event in the edited bet)
        DESCRIPTION: Verify that the new bet is resulted and shown on By Bets>(Bet History)Settled Bets
        EXPECTED: - Edited Bet is resulted
        EXPECTED: - Edited Bet is shown on By Bets>(Bet History)Settled Bets
        """
        self.ob_config.update_selection_result(event_id=self.event2_id, market_id=self.market2_id,
                                               selection_id=self.selection_id, result='L')
        self.ob_config.update_selection_result(event_id=self.event3_id, market_id=self.market3_id,
                                               selection_id=self.selection3_id, result='v')
        self.ob_config.update_selection_result(event_id=self.event4_id, market_id=self.market4_id,
                                               selection_id=self.selection4_id, result='W')
        self.ob_config.update_selection_result(event_id=self.event5_id, market_id=self.market5_id,
                                               selection_id=self.selection5_id, result='L')
        self.site.open_my_bets_settled_bets()
        self.__class__.bet = list(self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict.values())[1]
        self.site.wait_splash_to_hide(5)
        selection = list(self.bet.items_as_ordered_dict.values())[0]
        self.assertFalse(selection.has_edit_my_acca_remove_icon(),
                         msg='"Selection removal icon(X)" is displayed')

    def test_003_go_to_by_betsbet_historysettled_betsverify_that_the_edited_acca_is_shown_with_all_appropriate_elements(self):
        """
        DESCRIPTION: Go to By Bets>(Bet History)Settled Bets
        DESCRIPTION: Verify that the edited ACCA is shown with all appropriate elements
        EXPECTED: The edited ACCA is shown with appropriate elements:
        EXPECTED: - Updated ACCA Bet Type
        EXPECTED: - Bet Result for ACCA bet
        EXPECTED: - Date and time of when the bet was placed
        EXPECTED: - Total stake which was used for the edited ACCA
        EXPECTED: - Returns value
        EXPECTED: - New Bet Receipt ID
        EXPECTED: - Event name is displayed for all remaining selections
        EXPECTED: - Event Date and Time
        EXPECTED: - Market names for all remaining selections
        EXPECTED: - Selection name for all remaining selections
        EXPECTED: - Prices accepted for the new ACCA for all selections
        EXPECTED: - Scores result (if available)
        EXPECTED: - Status for each selection
        EXPECTED: - 'SHOW EDIT HISTORY' button is shown
        """
        self.test_001_go_to_my_betsopen_betsverify_that_the_edited_acca_is_shown_with_all_appropriate_elements(open_bets=False)
