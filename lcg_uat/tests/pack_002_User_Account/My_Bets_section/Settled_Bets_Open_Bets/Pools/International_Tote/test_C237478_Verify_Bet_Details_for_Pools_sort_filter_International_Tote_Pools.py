import tests
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseTote


# @pytest.mark.crl_prod
# @pytest.mark.crl_tst2
# @pytest.mark.crl_stg2
# @pytest.mark.tote
# @pytest.mark.bet_placement
# @pytest.mark.bet_history
# @pytest.mark.medium
# @pytest.mark.login
# @vtest
# @pytest.mark.issue('https://jira.egalacoral.com/browse/VOL-1712')
class Test_C237478_Verify_Bet_Details_for_Pools_sort_filter_International_Tote_Pools(BaseTote, BaseBetSlipTest):
    """
    TR_ID: C237478
    VOL_ID: C528132
    NAME: Verify Bet Details for Pools sort filter International Tote Pools
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: User should make bets on International Tote Pools with **'Status'**:
    PRECONDITIONS: - Won
    """
    keep_browser_open = True
    outcome_bet_receipt_bet_id = None
    meeting_name = None
    bet_winnings = 2.00
    expected_market_name = 'Tote Win Pool'

    def test_000_login_with_valid_credentials(self):
        """
        DESCRIPTION: Login with valid credentials
        EXPECTED: User is logged in successfully
        """
        self.__class__.user = tests.settings.betplacement_user
        self.site.login(username=self.user)

    def test_001_go_to_event_detail_page(self):
        """
        DESCRIPTION: Go to event detail page
        EXPECTED: Event detail page is loaded
        """
        event_details = self.get_event_details()
        event_id, self.__class__.meeting_name, off_time = event_details.event_id, event_details.meeting_name, event_details.off_time
        self.__class__.event_name = f'{off_time} {self.meeting_name}'
        self.__class__.pool_currency = self.get_pool_currency(event_id=event_id, pool_type='WN')
        self.navigate_to_edp(event_id=event_id, sport_name='tote')

    def test_002_place_a_bet_on_at_least_one_selection(self):
        """
        DESCRIPTION: Place a bet on at least one selection
        EXPECTED: - Bet is placed successfully
        EXPECTED: - Bet Receipt appears at the bottom of the event detail page
        """
        expected_active_tab = 'WIN'
        self.__class__.active_pool_type = self.site.tote_event_details.tab_content.grouping_buttons.current
        self.assertEqual(self.active_pool_type, expected_active_tab,
                         msg='Incorrect default grouping: current "%s", while expected "%s"'
                         % (self.active_pool_type, expected_active_tab))
        self.place_single_pool_bet()
        self.site.tote_event_details.tab_content.event_markets_list.betslip_bet_container.bet_now_button.click()

    def test_003_verify_bet_receipt_view(self):
        """
        DESCRIPTION: Verify Bet Receipt view and get all parameters
        EXPECTED: Events are expected to be expanded
        """
        self.verify_tote_betreceipt_success_message()
        sections = self.site.tote_event_details.tab_content.bet_receipt_section_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Can not find sections')
        first_section_name, first_section = list(sections.items())[0]
        outcomes = first_section.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No one outcome was found in section: "%s"' % first_section_name)
        outcome_name, self.__class__.outcome = list(outcomes.items())[0]
        self._logger.info('Outcome bet receipt title is %s ' % self.outcome.bet_receipt_title)
        self.assertFalse(self.outcome.is_expanded(), msg='Bet Receipt is expected to be collapsed by default')
        self.outcome.expand()
        self.assertTrue(self.outcome.is_expanded(), msg='Events are expected to be expanded')

    def test_004_check_correctness_of_full_bet_info(self):
        """
        DESCRIPTION: Verify correctness of full bet info
        EXPECTED: <Selection name>
        EXPECTED: "Leg:" <Leg Event details>
        EXPECTED: "Bet ID:" <Bet Reference ID>
        """
        if self.outcome.is_expanded():
            self._logger.info('*** Selection name is: {0} '.format(self.outcome.outcome_name))
            self._logger.info('*** Leg: {0} '.format(self.outcome.bet_leg))
            self._logger.info('*** Bet ID: {0} '.format(self.outcome.bet_id))
            self.__class__.outcome_bet_receipt_selection_name = self.outcome.outcome_name
            self.__class__.outcome_bet_receipt_bet_leg = self.outcome.bet_leg
            self.__class__.outcome_bet_receipt_bet_id = self.outcome.bet_id
        else:
            self.assertTrue(self.outcome.outcome_name, msg='No outcome information in full bet info block')

    def test_005_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My Bets' item on Top Menu
        EXPECTED: *  'My Bets' page/'Bet Slip' widget is shown
        EXPECTED: *  'Open Bets' tab is shown next to 'Cash Out' tab
        """
        self.site.open_my_bets_cashout()
        active_tab = self.site.cashout.tabs_menu.current
        self.assertEqual('CASH OUT', active_tab,
                         msg='Current tab is: "%s" not the same as expected: "CASH OUT"' % active_tab)

    def test_006_tap_bet_history_bets_tab(self):
        """
        DESCRIPTION: Tap 'Settled Bets Bets' tab
        EXPECTED: *  'Regular' sort filter is selected by default
        """
        self.site.cashout.tabs_menu.open_tab(tab_name=vec.bet_history.SETTLED_BETS_TAB_NAME)
        active_btn = self.site.bet_history.grouping_buttons.current
        self.assertEqual(active_btn, self.expected_active_btn,
                         msg='%s sorting type is not selected by default' % self.expected_active_btn)

    def test_007_navigate_to_pools_and_check_content_within(self):
        """
        DESCRIPTION: Navigate to 'Pools' and check content within
        """
        self.__class__.expected_active_btn = 'POOLS'
        self.site.bet_history.grouping_buttons.click_button('POOLS')

    def test_008_go_to_pools_sort_filter(self):
        """
        DESCRIPTION: Verify sorting section with four options is present
        """
        self.check_bet_sorting_types(tab=vec.bet_history.SETTLED_BETS_TAB_NAME, expected_active_btn='POOLS')

    def test_009_verify_view_of_tote_pools_bets(self):
        """
        DESCRIPTION: Verify  view of tote Pools bets
        EXPECTED: Must Display:
        EXPECTED: - Selection name
        EXPECTED: - Event name
        EXPECTED: - Pool Type
        EXPECTED: - Unit and Total Stake
        EXPECTED: - Status icon
        """
        bet_name, self.__class__.tote_win_pool = self.site.bet_history.tab_content.accordions_list.get_bet(
            bet_type='SINGLE', event_names=self.event_name, number_of_bets=1)
        outcomes = self.tote_win_pool.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes were found for bet: "%s"' % bet_name)

        event_name, event = list(outcomes.items())[0]
        self.assertEqual(event.market_name, self.expected_market_name)
        self.assertFalse(event.event_time, msg='Event time is present on page')
        self.assertFalse(event.has_link, msg='Event is hyperlinked')

        self.assertEqual(str(self.tote_win_pool.stake.stake_value), str(self.total_stake_converted),
                         msg='Stake amount "%s" is not equal to expected "%s" for bet "%s"' %
                             (str(self.tote_win_pool.stake.stake_value), str(self.total_stake_converted),
                              self.tote_win_pool.name))

        self.assertEqual(self.tote_win_pool.est_returns.stake_value, '0.00',
                         msg='Estimated returns: "%s" does not match with required: "%s"'
                             % (self.tote_win_pool.est_returns.stake_value, '0.00'))

        self.assertEqual(self.tote_win_pool.bet_receipt_info.bet_receipt.value, self.outcome_bet_receipt_bet_id,
                         msg='Open Bet section: "%s" bet receipt ID "%s" not found' %
                             (self.tote_win_pool.name, self.outcome_bet_receipt_bet_id))

    def test_010_trigger_the_situation_of_winning_a_bet_and_verify_bet_with_status_won_in_bet_history(self):
        """
        DESCRIPTION: Trigger the situation of Winning a bet and verify bet with status 'Won' in Settled Bets
        EXPECTED: Bet with status 'Won' should be present in Settled Bets
        EXPECTED: settled:Y
        EXPECTED: Winning !=0
        """
        expected_bet_status = vec.betslip.WON_STAKE
        self.set_status_of_tote_pool(self.user, self.outcome_bet_receipt_bet_id,
                                     bet_winnings=self.bet_winnings, set_status='Won')
        self.device.refresh_page()
        self.site.wait_content_state(state_name='BetHistory')
        self.site.wait_splash_to_hide()
        self.site.bet_history.grouping_buttons.click_button('POOLS')
        active_btn = self.site.bet_history.grouping_buttons.current
        self.assertEqual(active_btn, self.expected_active_btn,
                         msg='%s sorting type is not selected' % self.expected_active_btn)

        sections = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Can not find sections')
        bet_name, self.__class__.tote_win_pool = self.site.bet_history.tab_content.accordions_list.get_bet(
            bet_type='SINGLE', event_names=self.event_name, number_of_bets=1)

        self.assertTrue(self.tote_win_pool.bet_status == expected_bet_status,
                        msg="Bet status %s is not the same as expected %s"
                            % (self.tote_win_pool.bet_status, expected_bet_status))
