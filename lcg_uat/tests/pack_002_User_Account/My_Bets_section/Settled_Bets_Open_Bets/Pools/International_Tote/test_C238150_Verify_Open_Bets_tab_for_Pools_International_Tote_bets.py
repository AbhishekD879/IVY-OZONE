import tests
from tests.pack_010_RACES_General.BaseRacingTest import BaseTote


# @pytest.mark.crl_prod
# @pytest.mark.crl_tst2
# @pytest.mark.crl_stg2
# @pytest.mark.tote
# @pytest.mark.quarantine
# @pytest.mark.bet_placement
# @pytest.mark.open_bets
# @pytest.mark.login
# @vtest
class Test_C238150_Verify_Open_Bets_tab_for_Pools_International_Tote_bets(BaseTote):
    """
    TR_ID: C238150
    VOL_ID: C528022
    NAME: Verify Open Bets tab for Pools International Tote bets
    """
    keep_browser_open = True
    meeting_name = None
    active_pool_type = None
    expected_active_btn = 'REGULAR'
    total_stake_betreceipt = 3.00
    unit_stake = 3.00
    outcome_bet_receipt_selection_name = None
    outcome_bet_receipt_bet_leg = None
    outcome_bet_receipt_bet_id = None
    section = None
    expected_market_name = 'Tote Win Pool'

    def test_000_login_and_go_to_the_event_details(self):
        """
        DESCRIPTION: Login with valid credentials
        EXPECTED: User is logged in successfully
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_001_go_to_event_details_page(self):
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
                         msg='Incorrect default grouping: current "{0}", while expected "{1}"'.
                         format(self.active_pool_type, expected_active_tab))
        self.place_single_pool_bet()
        self._logger.info('Total stake: "%s"' % self.total_stake)
        converted_value = self.site.tote_event_details.tab_content.event_markets_list.betslip_bet_container.total_stake.converted_value
        if converted_value:
            self.__class__.converted_value = self.total_stake_converted
            self._logger.info('Total stake converted: "%s"' % self.converted_value)
        self.site.tote_event_details.tab_content.event_markets_list.betslip_bet_container.bet_now_button.click()

    def test_003_verify_bet_receipt_view(self):
        """
        DESCRIPTION: Verify Bet Receipt view and get all parameters
        EXPECTED: Events are expected to be expanded
        """
        self.verify_tote_betreceipt_success_message()
        sections = self.site.tote_event_details.tab_content.bet_receipt_section_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found on page')
        first_section_name, first_section = list(sections.items())[0]
        outcomes = first_section.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No one outcome was found in section: "%s"' % first_section_name)
        outcome_name, self.__class__.outcome = list(outcomes.items())[0]
        self._logger.info('Outcome bet receipt title is "%s"' % self.outcome.bet_receipt_title)
        self._logger.info('Outcome stake value is "%s"' % self.outcome.stake.value)
        self.assertFalse(self.outcome.is_expanded(), msg='Bet Receipt is expected to be collapsed by default')
        self.outcome.expand()
        self.assertTrue(self.outcome.is_expanded(), msg='Events are expected to be expanded')

    def test_004_check_correctness_of_full_bet_info(self):
        """
        DESCRIPTION: Verify correctness of full bet info
        EXPECTED:<Selection name>
        EXPECTED:"Leg:" <Leg Event details>
        EXPECTED:"Bet ID:" <Bet Reference ID>
        """
        if self.outcome.is_expanded():
            self._logger.info('*** Selection name is: "%s" ' % self.outcome.outcome_name)
            self._logger.info('*** Leg: "%s"' % self.outcome.bet_leg)
            self._logger.info('*** Bet ID: "%s"' % self.outcome.bet_id)
            self._logger.info('*** Outcome stake value: "%s" ' % self.outcome.stake.value)
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

    def test_006_tap_open_bets_tab(self):
        """
        DESCRIPTION: Tap 'Open Bets' tab
        EXPECTED: *  'Regular', 'Player Bets', 'Lotto' and 'Pools' sort filters are shown
        EXPECTED: *  'Regular' sort filter is selected by default
        """
        self.site.cashout.tabs_menu.open_tab(tab_name='OPEN BETS')
        active_btn = self.site.open_bets.grouping_buttons.current
        self.assertEqual(active_btn, self.expected_active_btn,
                         msg='"%s" sorting type is not selected by default' % self.expected_active_btn)

    def test_007_navigate_to_pools_and_check_content_within(self):
        """
        DESCRIPTION: Navigate to 'Pools' and check content within
        EXPECTED: 1. All '**Pending bets**' sections are displayed chronologically (**'settled=N'** attribute is set for all displayed bets (from response select 'Network' tab-> 'All' filter -> choose the request described in 2 point in preconditions->'Preview' tab))
        EXPECTED: 2. All sections are collapsed by default
        EXPECTED: 3. If there are more than 20 events, they should be loaded after scrolling by portions (20 events by portion)
        """
        self.__class__.expected_active_btn = 'POOLS'
        self.site.open_bets.grouping_buttons.click_button('POOLS')
        active_btn = self.site.open_bets.grouping_buttons.current
        self.assertEqual(active_btn, self.expected_active_btn,
                         msg='"%s" sorting type is not selected' % self.expected_active_btn)
        sections = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertLessEqual(len(sections), 20,
                             msg='Default number of my bets items should be not more than 20 but found "%s" items'
                                 % len(sections))
        self.site.open_bets.scroll_to_bottom()
        self.site.open_bets.tab_content.accordions_list.wait_for_sections()

    def test_008_verify_view(self):
        """
        EXPECTED: Must Display:
        EXPECTED: - date and time the bet was placed
        EXPECTED: - Selection name
        EXPECTED: - Event name
        EXPECTED: - Pool Type
        EXPECTED: - Unit and Total Stake
        """
        bet_name, self.__class__.tote_win_pool = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type='SINGLE', event_names=self.event_name, number_of_bets=1)
        bet_legs = self.tote_win_pool.items_as_ordered_dict
        self.assertTrue(bet_legs, msg='No one bet leg was found for bet: "%s"' % bet_name)

        betleg_name, betleg = list(bet_legs.items())[0]
        self.assertEqual(betleg.market_name, self.expected_market_name)
        self.assertFalse(betleg.event_time, msg='Event time is present on page')
        self.assertFalse(betleg.has_link, msg='Event is hyperlinked')

        self.assertEqual(float(self.tote_win_pool.stake.value.strip('£')), self.converted_value,
                         msg='Stake amount "%s" is not equal to expected "%s" for bet "%s"' %
                             (float(self.tote_win_pool.stake.value.strip('£')), self.converted_value,
                              self.tote_win_pool.name))

        self.assertEqual(self.tote_win_pool.est_returns.value, '£0.00',
                         msg='Estimated returns: "%s" does not match with required: "%s"'
                             % (self.tote_win_pool.est_returns.value, '£0.00'))

        self.assertEqual(self.tote_win_pool.bet_receipt_info.bet_receipt.value, self.outcome_bet_receipt_bet_id,
                         msg='Open Bet section: "%s" bet receipt ID "%s" not found' %
                             (self.tote_win_pool.name, self.outcome_bet_receipt_bet_id))
