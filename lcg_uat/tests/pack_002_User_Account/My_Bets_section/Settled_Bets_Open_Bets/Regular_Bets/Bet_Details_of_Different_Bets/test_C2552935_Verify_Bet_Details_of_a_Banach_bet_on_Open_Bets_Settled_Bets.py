import pytest
from crlat_ob_client.utils.date_time import validate_time

from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.banach
@pytest.mark.build_your_bet
@pytest.mark.my_bets
@pytest.mark.bet_history
@pytest.mark.open_bets
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@pytest.mark.login
@vtest
class Test_C2552935_Verify_Bet_Details_of_a_Banach_bet_on_Open_Bets_Settled_Bets(BaseBanachTest):
    """
    TR_ID: C2552935
    NAME: Verify Bet Details of a Banach bet on Open Bets/Settled Bets
    DESCRIPTION: Test case verifies Banach bet display on Settled Bets and Open Bets
    PRECONDITIONS: Build Your Bet CMS configuration
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To check Open Bet data for event on Settled Bets tabs:
    PRECONDITIONS: in Dev tools > Network find **accountHistory** request
    PRECONDITIONS: **User has placed Banach bet(s)**
    PRECONDITIONS: 'Open Bets' and 'Settled Bets' can be found on 'My Bets' page on mobile and on 'Bet Slip' widget for Tablet/Desktop
    """
    keep_browser_open = True
    proxy = None
    single_byb_section = None
    bet_type = None
    detailed_event_name = event_name = None
    all_selection_names = []
    stake_value = 1
    odds = stake = est_returns = None
    total_stake_currency = total_estimate_returns_currency = None
    event_start_time_local = None
    byb_bet_receipt_id = None
    date_pattern_today = '%H:%M, Today'

    def verify_banach_bet_details(self, bet_name):
        """
        This method verifies bet details of banach bet
        :param bet_name: name (type) of the bet (e.g., 'SINGLE - BUILD YOUR BET')
        """
        bet_legs = self.single_byb_section.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'"{bet_name}" bet has no bet legs')
        betleg_name, betleg = list(bet_legs.items())[0]

        outcome_name = list(betleg.byb_selections.items_as_ordered_dict.keys())
        self.assertEqual(outcome_name, self.all_selection_names,
                         msg=f'Outcome name "{outcome_name}" is not the same as expected '
                             f'"{self.all_selection_names}"')

        self.assertEqual(betleg.market_name.upper(), vec.yourcall.DASHBOARD_TITLE,
                         msg=f'Market name "{betleg.market_name.upper()}" is not the same '
                             f'as expected "{vec.yourcall.DASHBOARD_TITLE}"')

        self.assertEqual(betleg.event_name, self.event_name,
                         msg=f'Event name "{betleg.event_name}" is not the same as expected "{self.event_name}"')

        self.assertEqual(betleg.event_time, self.event_start_time_local,
                         msg=f'Event time "{betleg.event_time}" is not the same '
                             f'as expected "{self.event_start_time_local}"')
        validate_time(betleg.event_time, self.date_pattern_today) if 'Today' in betleg.event_time else \
            validate_time(betleg.event_time, self.event_card_future_time_format_pattern)

        # 'Bet Receipt' info removed from bet details on 'Open Bets' tab
        # cannot settle Banach bets
        # bet_receipt_info = self.single_byb_section.bet_receipt_info
        # date_of_bet_placement = datetime.now().strftime('%m/%d/%Y')
        # self.assertEqual(bet_receipt_info.date.name, date_of_bet_placement,
        #                  msg='Date of bet placement "%s" is not the same as expected "%s"' %
        #                      (bet_receipt_info.date.name, date_of_bet_placement))
        #
        # self.assertEqual(bet_receipt_info.bet_receipt.value, self.byb_bet_receipt_id,
        #                  msg='Bet Receipt Id "%s" is not the same as expected "%s"' %
        #                      (bet_receipt_info.bet_receipt.value, self.byb_bet_receipt_id))

        self.assertEqual(self.single_byb_section.stake.currency, self.total_stake_currency,
                         msg=f'Stake currency "{self.single_byb_section.stake.currency}" is not the same '
                             f'as expected "{self.total_stake_currency}"')

        self.assertEqual(self.single_byb_section.stake.stake_value, self.stake,
                         msg=f'Stake amount value "{self.single_byb_section.stake.stake_value}" is not the same '
                             f'as expected "{self.stake}"')

        self.assertEqual(betleg.odds_value, self.odds, msg=f'Odds value "{betleg.odds_value}" is not the same '
                                                           f'as expected "{self.odds}"')

        self.assertEqual(self.single_byb_section.est_returns.currency, self.total_estimate_returns_currency,
                         msg=f'Est. Returns currency "{self.single_byb_section.est_returns.currency}" is not the same '
                             f'as expected "{self.total_estimate_returns_currency}"')

        actual_est_returns = self.single_byb_section.est_returns.stake_value
        self.assertAlmostEqual(float(actual_est_returns), float(self.est_returns), delta=0.02,
                               msg=f'Est. Returns amount value "{actual_est_returns}" is not the same '
                                   f'as expected "{self.est_returns}" with delta 0.02')

        betleg.click_event_name()
        self.site.wait_content_state(state_name='EventDetails')
        self.assertIn(str(self.eventID), self.device.get_current_url(),
                      msg='User redirected to the incorrect Event Details Page')

    def test_000_preconditions(self):
        """
        DESCRIPTION: User has placed Banach bet(s)
        """
        self.site.login()
        self.site.wait_content_state('homepage')
        self.__class__.eventID = self.get_ob_event_with_byb_market()

        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                  query_builder=self.ss_query_builder)
        event_start_time = event_details[0]['event']['startTime']
        self.__class__.event_start_time_local = self.convert_time_to_local(
            date_time_str=event_start_time,
            ob_format_pattern=self.ob_format_pattern,
            future_datetime_format=self.event_card_future_time_format_pattern,
            ss_data=True)

        self.__class__.event_name = normalize_name(event_details[0]['event']['name'])
        self.__class__.detailed_event_name = f'{self.event_name} {self.event_start_time_local}'

        self.__class__.bet_type = vec.bet_history.MY_BETS_SINGLE_BET_BUILDER_STAKE_TITLE

        self.navigate_to_edp(event_id=self.eventID)

        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

        # Match betting selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.assertTrue(match_betting, msg=f'"{self.expected_market_sections.match_betting}" market does not exist')
        match_betting_selection_name = match_betting.set_market_selection(selection_index=1)
        match_betting.set_market_selection(selection_index=1, time=True)
        self.assertTrue(match_betting_selection_name, msg='Match betting selection is not added to Dashboard')
        match_betting.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        self.__class__.initial_counter += 1
        team1 = ''.join(match_betting_selection_name)
        match_betting_market_and_selection_name = f'{self.expected_market_sections.match_betting.title()} ' \
                                                  f'{team1}'.replace('  ', ' ')
        self.__class__.all_selection_names.append(match_betting_market_and_selection_name)

        # Double chance selection
        double_chance_selection_name = self.add_byb_selection_to_dashboard(
            market_name=self.expected_market_sections.double_chance, switcher_name='90 MINS', selection_index=1)
        self.assertTrue(double_chance_selection_name, msg='Double chance selection is not added to Dashboard')
        double_chance_selection_name = ''.join(double_chance_selection_name)
        double_chance_market_and_selection_name = f'{self.expected_market_sections.double_chance.title()} ' \
                                                  f'{double_chance_selection_name}'.replace('  ', ' ')
        self.__class__.all_selection_names.append(double_chance_market_and_selection_name)
        self.__class__.initial_counter += 1
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)

        if self.site.sport_event_details.tab_content.dashboard_panel.has_price_not_available_message():
            self.assertFalse(
                self.site.sport_event_details.tab_content.dashboard_panel.price_not_available_message.is_displayed(
                    expected_result=False),
                msg=f'Message: "{vec.yourcall.PRICE_NOT_AVAILABLE}" displayed')

        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.place_bet.click()

        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='BYB Betslip has not appeared')
        byb_betslip_panel = self.site.byb_betslip_panel
        self.assertTrue(byb_betslip_panel.is_displayed(), msg='BYB BetSlip is not shown')
        byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.stake_value)

        self.__class__.odds = byb_betslip_panel.selection.content.odds
        self.assertTrue(self.odds, msg='Odds/price are not shown')

        self.__class__.total_stake_currency = self.site.byb_betslip_panel.selection.bet_summary.total_stake_currency
        self.assertTrue(self.total_stake_currency, msg='Stake currency is not shown')
        self.__class__.stake = self.site.byb_betslip_panel.selection.bet_summary.total_stake
        self.assertTrue(self.stake, msg='Stake is not shown')

        self.__class__.total_estimate_returns_currency = \
            byb_betslip_panel.selection.bet_summary.total_estimate_returns_currency
        self.assertTrue(self.total_estimate_returns_currency, msg='Est. Returns currency is not shown')
        self.__class__.est_returns = byb_betslip_panel.selection.bet_summary.total_estimate_returns
        self.assertTrue(self.est_returns, msg='Est. Returns is not shown')
        try:
            byb_betslip_panel.place_bet.click()
            self.assertTrue(self.site.wait_for_byb_bet_receipt_panel(timeout=25),
                            msg='Build Your Bet Receipt is not displayed')
        except VoltronException:
            byb_betslip_panel.place_bet.click()
            self.assertTrue(self.site.wait_for_byb_bet_receipt_panel(timeout=25),
                            msg='Build Your Bet Receipt is not displayed')

        byb_bet_receipt_panel = self.site.byb_bet_receipt_panel
        self.__class__.byb_bet_receipt_id = byb_bet_receipt_panel.selection.content.bet_id_value
        byb_bet_receipt_panel.header.close_button.click()

    def test_001_navigate_to_open_bets_tab(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' tab
        EXPECTED: 'Open Bets' tab is opened
        """
        self.site.open_my_bets_open_bets()

    def test_002_verify_display_of_banach_bet(self):
        """
        DESCRIPTION: Verify display of Banach bet
        EXPECTED: The following bet details are shown for Banach bet:
        EXPECTED: - Bet type BUILD YOUR BET (for Coral) / BET BUILDER (for Ladbrokes)
        EXPECTED: - Selection names user has bet on, separated by comma, truncated into a few lines
        EXPECTED: - **Build Your Bet** text
        EXPECTED: - Corresponding Event name which is redirecting users to corresponding Event Details Page
        EXPECTED: - Event start date in DD MMM, hh:mm AM/PM (time only displayed for Today's events)
        EXPECTED: - Date of bet placement and bet receipt ID are shown below bet details
        EXPECTED: - Date of bet placement is shown in a format MM/DD/YYYY (e.g. 11/06/2008)
        EXPECTED: - 'Bet Receipt' label and its ID (e.g. O/15242822/0000017) are shown to the right of bet placement date
        EXPECTED: - Stake <currency symbol> <value> (e.g., £10.00)
        EXPECTED: - Odds
        EXPECTED: - Est. Returns <currency symbol> <value> (e.g., £30.00)
        EXPECTED: All the details correspond to the placed Banach bet
        """
        bet_name, self.__class__.single_byb_section = \
            self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=self.bet_type,
                                                                    event_names=self.detailed_event_name,
                                                                    number_of_bets=1)
        self.verify_banach_bet_details(bet_name=bet_name)

    # cannot settle Banach bets
    # def test_003_navigate_to_bet_history_tab(self):
    #     """
    #     DESCRIPTION: Navigate to 'Settled Bets' tab
    #     EXPECTED: 'Settled Bets' tab is opened
    #     """
    #     self.site.open_my_bets_cashout()
    #     self.site.cashout.tabs_menu.open_tab(tab_name=vec.bet_history.SETTLED_BETS_TAB_NAME)
    #
    # def test_004_repeat_step_2(self):
    #     """
    #     DESCRIPTION: Repeat step 2
    #     """
    #     bet_name, self.__class__.single_byb_section = \
    #         self.site.bet_history.tab_content.accordions_list.get_bet(bet_type=self.bet_type,
    #                                                                   event_names=self.detailed_event_name)
    #     self.verify_banach_bet_details(bet_name=bet_name)
