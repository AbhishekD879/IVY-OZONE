import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import get_inplay_event_initial_data, normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.in_play
@pytest.mark.safari
@pytest.mark.hotfix
@pytest.mark.sanity
@pytest.mark.soc
@vtest
class Test_C874310_Place_In_Play_single_bet(BaseBetSlipTest):
    """
    TR_ID: C874310
    NAME: Place In Play single bet
    DESCRIPTION: Bet Placement - Verify that the customer can place a Single bet on "In Play" selections
    DESCRIPTION: AUTOTEST [C9690003] - tst2/stg2 endpoints only
    """
    keep_browser_open = True
    enable_bs_performance_log = True

    def find_or_create_event(self):
        """
        Find live event on PROD/ Create Live event on TST2/STG2
        """
        if tests.settings.backend_env == 'prod':
            self.navigate_to_page(name='in-play/football')
            self.site.wait_content_state(state_name='InPlay', timeout=2)
            events = get_inplay_event_initial_data(category_id=str(self.ob_config.football_config.category_id))
            self.__class__.sport_name="football"
            if len(events) == 0:
                self.navigate_to_page(name='in-play/tennis')
                self.site.wait_content_state(state_name='InPlay', timeout=2)
                events = get_inplay_event_initial_data(category_id=str(self.ob_config.tennis_config.category_id))
                self.__class__.sport_name="Tennis"
            if len(events)== 0:
                raise SiteServeException(f'No Live events found for Football and tennis')
            resp, event = None, None
            for event in reversed(events):
                events_outcomes_filter = self.basic_active_events_filter() \
                    .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
                    .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A'))
                resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event['id'],
                                                                 query_builder=events_outcomes_filter,
                                                                 raise_exceptions=False)
                if resp:
                    break
            if not resp:
                raise SiteServeException('No live events with active prices found for Football or tennis' )
            self.__class__.event_name = normalize_name(event['name'])
            self.__class__.team1, self.__class__.team2 = self.event_name.split(' v ')
            self.__class__.event_id = event['id']
            self.__class__.league = self.get_accordion_name_for_event_from_ss(event=resp[0], in_play_tab_home_page=True)
            self._logger.info(f'*** Found Football event "{self.event_name}" with ID "{self.event_id}"')
        else:
            event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            self.__class__.event_name = f'{event.team1} v {event.team2}'
            self.__class__.team1, self.__class__.team2 = event.team1, event.team2
            self.__class__.event_id = event.event_id
            self.__class__.league = tests.settings.football_autotest_competition_league \
                if self.device_type == 'mobile' else tests.settings.football_autotest_league
            self._logger.info(f'*** Created Football event "{self.event_name}" with ID "{self.event_id}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login to Oxygen app
        EXPECTED: User is logged in
        """
        self.find_or_create_event()
        self.site.login()

    def test_001_navigate_to_in_play_page_from_the_menu(self):
        """
        DESCRIPTION: Navigate to In Play page from the menu
        EXPECTED: The In Play page is opened
        """
        self.navigate_to_page(name='in-play')
        self.site.wait_content_state(state_name='InPlay')
        if self.sport_name=="football":
            sport_name = vec.sb.FOOTBALL if self.brand == 'ladbrokes' else vec.sb.FOOTBALL.upper()
        else:
            sport_name=vec.sb.TENNIS if self.brand =="ladbrokes" else vec.sb.TENNIS.upper()
        self.site.inplay.inplay_sport_menu.click_item(item_name=sport_name)

    def test_002_add_a_selection_to_bet_slip_from_an_in_play_event(self):
        """
        DESCRIPTION: Add a selection to bet slip from an in Play event
        EXPECTED: Selection is added to betslip
        """
        event = self.get_event_from_league(event_id=self.event_id,
                                           section_name=self.league)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for event "{self.event_name}"')

        bet_button = output_prices.get(self.team1)
        if not bet_button:
            self._logger.warning(f'*** Bet button for "{self.team1}" was not found, looking for the next live event.')
            self.find_or_create_event()
            event = self.get_event_from_league(event_id=self.event_id,
                                               section_name=self.league)
            output_prices = event.get_active_prices()
            self.assertTrue(output_prices,
                            msg=f'Could not find output prices for event "{self.event_name}"')

            bet_button = output_prices.get(self.team1)

        self.assertTrue(bet_button, msg=f'Bet button for "{self.team1}" was not found')

        bet_button.click()
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip(timeout=2)
        is_selected = bet_button.is_selected(timeout=2)
        self.assertTrue(is_selected, msg=f'Bet button "{self.team1}" is not active after selection')

    def test_003_navigate_to_betslip(self):
        """
        DESCRIPTION: Navigate to betslip
        EXPECTED: Betslip is loaded
        """
        self.site.open_betslip()

    def test_004_add_a_stake_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add a stake and click on "Place Bet" button
        EXPECTED: * The bet is successfully placed and bet receipt is displayed.
        EXPECTED: * The currency is in £ (or another due to customer currency set while registration)
        """
        self.__class__.bet_info = self.place_and_validate_single_bet()

    def test_005_verify_the_bet_receipt(self):
        """
        DESCRIPTION: Verify the Bet Receipt
        EXPECTED: - The currency is in £  (or another due to customer currency set while registration)
        EXPECTED: - The bet type is displayed: (e.g: single);
        EXPECTED: - Same Selection and Market is displayed where the bet was placed;
        EXPECTED: - Correct Time (of bet placement) and Event is displayed;
        EXPECTED: - 'Cashout' label between the bet and stake info area (if cashout is available for this event)
        EXPECTED: - Unique Bet ID is displayed;
        EXPECTED: - The balance is correctly updated;
        EXPECTED: - Odds are exactly the same as when bet has been placed;
        EXPECTED: - 'Stake' is correctly displayed;
        EXPECTED: - 'Total Stake' is correctly displayed;
        EXPECTED: - 'Estimated Returns' is exactly the same as when bet has been placed;
        EXPECTED: - "Reuse Selection" and "Go Betting" buttons are displayed at the bottom of Bet receipt
        """
        self.check_bet_receipt(betslip_info=self.bet_info)
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        if self.brand == 'ladbrokes':
            self.assertTrue(self.site.bet_receipt.receipt_header.bet_datetime,
                            msg='Date and Time of event not displayed on the bet receipt')
        for section_name, section in betreceipt_sections.items():
            receipts = section.items_as_ordered_dict
            for receipt_name, receipt in receipts.items():
                receipt_type = receipt.__class__.__name__
                if receipt_type == 'ReceiptSingles':
                    if receipt.has_cash_out_label():
                        self.assertTrue(receipt.has_cash_out_label(), msg=f'"Cashout" label is not displayed')
                    self.assertEqual(receipt.event_name, self.event_name, msg=f'Event name is not displayed'
                                                                              f' Actual: "{receipt.event_name}"'
                                                                              f' Expected: "{self.event_name}"')
                    self.assertIn(receipt.estimate_returns_currency, receipt.currencies,
                                  msg=f'Currency symbol "{receipt.estimate_returns_currency}" is not valid')
        bet_receipt = self.site.bet_receipt.footer
        self.assertTrue(bet_receipt.has_reuse_selections_button(),
                        msg=f'"{bet_receipt.reuse_selection_button.name}" is not displayed')
        self.assertTrue(bet_receipt.has_done_button(),
                        msg=f'"{bet_receipt.done_button.name}" is not displayed')

    def test_006_click_on_go_betting_button(self):
        """
        DESCRIPTION: Click on 'Go betting' button
        EXPECTED: In Play page loads
        """
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state(state_name='InPlay')

    def test_007_click_on_my_bets(self):
        """
        DESCRIPTION: Click on 'My Bets' button from the header (mobile)
        DESCRIPTION: Click on 'My Bets' tab (Betslip element - desktop)
        EXPECTED: Cashout/Open Bets page is opened
        """
        self.site.open_my_bets_open_bets()

    def test_008_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify that the Bet fields are correct.
        EXPECTED: - The currency is in £ (or another due to customer currency set while registration)
        EXPECTED: - The bet type (eg. Single)
        EXPECTED: - Selection Name where the bet has been placed
        EXPECTED: - Odds are the same as while placing the bet
        EXPECTED: - Market where the bet has been placed
        EXPECTED: - Event Name is displayed
        EXPECTED: - Time and Date (except live events)
        EXPECTED: - Correct Stake is correctly displayed;
        """
        bet_name, single_bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name, number_of_bets=3)

        bet_info = self.bet_info.get(self.team1.replace('(','').replace(')',''))
        self.assertTrue(bet_info, msg=f'"{self.team1}" not found in "{self.bet_info.keys()}"')
        self.assertIn(single_bet.est_returns.currency, single_bet.currencies,
                      msg=f'Currency "{single_bet.est_returns}" is not valid')
        self.assertEqual(single_bet.bet_type, vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                         msg=f'Bet type: "{single_bet.bet_type}" '
                             f'is not as expected: "{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE}"')
        self.assertEqual(single_bet.selection_name, bet_info.get('outcome_name'),
                         msg=f'Selection Name: "{single_bet.selection_name}" '
                             f'is not as expected: "{bet_info.get("outcome_name")}"')
        self.assertEqual(single_bet.odds_value, bet_info.get('odds'),
                         msg=f'Odds "{single_bet.odds_value}" '
                             f'is not as expected: "{bet_info.get("odds")}"')
        self.assertEqual(single_bet.event_name, bet_info.get('event_name'),
                         msg=f'Event name: "{single_bet.event_name}" '
                             f'is not as expected: "{bet_info.get("event_name")}"')
        self.assertEqual(single_bet.market_name, bet_info.get('market_name'),
                         msg=f'Bet market name: "{single_bet.market_name}" '
                             f'is not as expected: "{bet_info.get("market_name")}"')
        expected_stake = f'£{self.bet_amount:.2f}'
        self.assertEqual(single_bet.stake.value, expected_stake,
                         msg=f'Bet Stake value: "{single_bet.stake.value}" '
                             f'is not as expected: "{expected_stake}"')
