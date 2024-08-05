import pytest
from crlat_siteserve_client.utils.date_time import get_date_time_as_string
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.sports
@pytest.mark.football
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.critical
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.safari
@pytest.mark.hotfix
@pytest.mark.sanity
@vtest
class Test_C874311_Place_Football_Double_bet(BaseBetSlipTest):
    """
    TR_ID: C874311
    NAME: Place Football Double bet
    DESCRIPTION: Bet Placement - Verify that the customer can place a Double bet on pre-match Football events
    PRECONDITIONS: Login to Oxygen app with user that has currency in £
    """
    keep_browser_open = True
    sport_name = vec.sb.FOOTBALL
    end_date = f'{get_date_time_as_string(days=1)}T00:00:00.000Z'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login to Oxygen app
        DESCRIPTION: Find / create event for test
        EXPECTED: User is logged in
        EXPECTED: Event is found / created
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(
                category_id=self.ob_config.football_config.category_id, number_of_events=2)
            self.__class__.event_name1 = normalize_name(event[0]['event']['name'])
            self.__class__.event_name2 = normalize_name(event[1]['event']['name'])

            self.__class__.team1 = self.event_name1.split(' v ')[0]
            self.__class__.team2 = self.event_name2.split(' v ')[0]

            self.__class__.event_id1 = event[0]['event']['id']
            self.__class__.event_id2 = event[1]['event']['id']

            self.__class__.league1 = self.get_accordion_name_for_event_from_ss(event=event[0])
            self.__class__.league2 = self.get_accordion_name_for_event_from_ss(event=event[1])

            self._logger.info(f'*** Found Football event #1 "{self.event_name1}" with ID "{self.event_id1}"')
            self._logger.info(f'*** Found Football event #2 "{self.event_name2}" with ID "{self.event_id2}"')
        else:
            event1 = self.ob_config.add_autotest_premier_league_football_event()
            event2 = self.ob_config.add_autotest_premier_league_football_event()

            self.__class__.event_name1 = f'{event1.team1} v {event1.team2}'
            self.__class__.event_name2 = f'{event2.team1} v {event2.team2}'

            self.__class__.team1 = event1.team1
            self.__class__.team2 = event2.team1

            self.__class__.event_id1 = event1.event_id
            self.__class__.event_id2 = event2.event_id

            self.__class__.league1 = self.__class__.league2 = tests.settings.football_autotest_league

            self._logger.info(f'*** Created Football event #1 "{self.event_name1}" with ID "{self.event_id1}"')
            self._logger.info(f'*** Created Football event #2 "{self.event_name2}" with ID "{self.event_id2}"')

        self.site.login(username=tests.settings.betplacement_user)

    def test_001_navigate_to_football_page_from_the_menu(self):
        """
        DESCRIPTION: Navigate to Football page from the menu
        EXPECTED: Football page is loaded
        """
        self.site.open_sport(name=self.sport_name)
        self.site.wait_content_state(state_name=self.sport_name)

    def test_002_add_2_selections_to_bet_slip_from_2_different_pre_match_events_not_live_eg_from_matches_tab(self):
        """
        DESCRIPTION: Add 2 selections to bet slip from 2 different pre-match events (not live) e.g. from Matches tab
        EXPECTED: Selections are added to bet slip
        """
        # [DESKTOP]pre-match events may comes under today tab or tomorrow tab, So it will check in today tab in desktop(try block)
        # if not available it will check in tomorrow tab(except block).
        try:
            event = self.get_event_from_league(event_id=self.event_id1,
                                               section_name=self.league1)
        except VoltronException:
            if self.device_type=='desktop':
                self.site.football.tab_content.grouping_buttons.items_as_ordered_dict.get(vec.sb.SPORT_DAY_TABS.tomorrow).click()
            event = self.get_event_from_league(event_id=self.event_id1,
                                               section_name=self.league1)
        output_prices1 = event.get_active_prices()
        self.assertTrue(output_prices1, msg=f'Could not find output prices for event "{self.event_name1}"')

        name, bet_button_1 = list(output_prices1.items())[0]
        bet_button_1.click()
        self.assertTrue(bet_button_1, msg=f'Bet button for "{self.team1}" was not found')

        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip(timeout=3)
        result = bet_button_1.is_selected(timeout=2)
        self.assertTrue(result, msg=f'Bet button "{self.team1}" is not active after selection')
        # [DESKTOP]pre-match events may comes under today tab or tomorrow tab, So it will check in tomorrow tab in desktop(try block)
        # if not available it will check in today tab(except block).
        try:
            event2 = self.get_event_from_league(event_id=self.event_id2,
                                                section_name=self.league2)
        except VoltronException:
            if self.device_type == 'desktop':
                if self.site.football.tab_content.grouping_buttons.current == vec.sb.SPORT_DAY_TABS.today:
                    self.site.football.tab_content.grouping_buttons.items_as_ordered_dict.get(vec.sb.SPORT_DAY_TABS.tomorrow).click()
                else:
                    self.site.football.tab_content.grouping_buttons.items_as_ordered_dict.get(vec.sb.SPORT_DAY_TABS.today).click()
            event2 = self.get_event_from_league(event_id=self.event_id2,
                                                section_name=self.league2)
        output_prices2 = event2.get_active_prices()
        self.assertTrue(output_prices2,
                        msg=f'Could not find output prices for event "{self.event_name2}"')

        name, bet_button_2 = list(output_prices2.items())[0]
        self.assertTrue(bet_button_2, msg=f'Bet button for "{self.team2}" was not found')

        bet_button_2.click()

        result = bet_button_2.is_selected(timeout=2)
        self.assertTrue(result, msg=f'Bet button "{self.team2}" is not active after selection')

    def test_003_navigate_to_betslip(self):
        """
        DESCRIPTION: Navigate to betslip
        EXPECTED: Betslip is loaded
        """
        self.site.open_betslip()

    def test_004_add_a_stake_in_the_double_stake_box_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add a stake in the Double Stake box and click on "Place Bet" button
        EXPECTED: - The bet is successfully placed and bet confirmation is displayed.
        EXPECTED: - The currency is in £ (or other currency set during user registration)
        """
        self.__class__.bet_info = self.place_and_validate_multiple_bet(number_of_stakes=1)

    def test_005_verify_the_bet_confirmation(self):
        """
        DESCRIPTION: Verify the Bet Confirmation
        EXPECTED: - The currency is in £ (or other currency set during user registration)
        EXPECTED: - The bet type is displayed: DOUBLE;
        EXPECTED: - Same Selection and Market is displayed where the bet was placed;
        EXPECTED: - Event name is displayed;
        EXPECTED: - 'Cashout' label between last bet and stake info area (if cashout is available for both selections)
        EXPECTED: - Unique Bet ID is displayed;
        EXPECTED: - The balance is correctly updated;
        EXPECTED: - Odds are exactly the same as when bet has been placed;
        EXPECTED: - Stake is correctly displayed;
        EXPECTED: - Total Stake is correctly displayed;
        EXPECTED: - Estimated Returns is exactly the same as when bet has been placed;
        EXPECTED: - "Reuse Selection" and "Go betting" buttons are displayed at the bottom
        """
        self.__class__.bet_receipt = self.site.bet_receipt.footer
        self.assertTrue(self.bet_receipt.has_reuse_selections_button(),
                        msg=f'"{self.bet_receipt.reuse_selection_button.name}" is not displayed')
        self.assertTrue(self.bet_receipt.has_done_button(),
                        msg=f'"{self.bet_receipt.done_button.name}" is not displayed')

    def test_006_tap_on_go_betting_button(self):
        """
        DESCRIPTION: Tap on 'Go betting' button
        EXPECTED: The customer is redirected back to Football page
        """
        self.bet_receipt.click_done()
        self.site.wait_content_state(state_name=self.sport_name)

    def test_007_tap_on_my_bets_open_bets_button_from_the_header(self):
        """
        DESCRIPTION: Tap on My Bets -> Open Bets button from the header
        EXPECTED: My Bets page is opened
        """
        self.site.open_my_bets_open_bets()

    def test_008_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify that the Bet Receipt fields are correct
        EXPECTED: The currency is in £ (or other user currency)
        EXPECTED: - The bet type: DOUBLE
        EXPECTED: - Selection Names correspond to the placed outcome name
        EXPECTED: - Odds (for 2 selections) are displayed
        EXPECTED: - Event Name is displayed
        EXPECTED: - Market where the bet has been placed
        EXPECTED: - Time and Date - 24 hours format:
        EXPECTED: **HH:MM, Today**  (e.g. "14:00 or 05:00, Today")
        EXPECTED: **HH:MM, DD MMM** (e.g. 14:00 or 05:00, 24 Nov or 02 Nov) - future dates
        EXPECTED: - E/W Terms: (None for bets where E/W is not valid)
        EXPECTED: - Stake is correctly displayed;
        """
        _, double_bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=[self.event_name1, self.event_name2])

        for _, betleg in double_bet.items_as_ordered_dict.items():
            market_name = self.bet_info[betleg.outcome_name.replace('(','').replace(')','')]['market_name']
            self.assertEqual(betleg.market_name, market_name,
                             msg=f'Market name: "{betleg.market_name}" '
                                 f'is not as expected: "{market_name}"')
            self.assertEqual(betleg.odds_value, self.bet_info[betleg.outcome_name.replace('(','').replace(')','')]['odds'],
                             msg=f'Actual Odds value: "{betleg.odds_value}" '
                                 f'is not as expected: "{self.bet_info[betleg.outcome_name.replace("(","").replace(")","")]["odds"]}"')
        actual_stake = double_bet.stake.value
        expected_stake = f'£{self.bet_info["total_stake"]:.2f}'
        self.assertEqual(actual_stake, expected_stake,
                         msg=f'Actual stake: "{actual_stake} '
                             f'is not as expected: "{expected_stake}"')
