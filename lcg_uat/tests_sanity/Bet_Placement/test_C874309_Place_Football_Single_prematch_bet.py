from random import choice
import pytest
import tests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.sports
@pytest.mark.football
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.critical
@pytest.mark.login
@pytest.mark.safari
@pytest.mark.hotfix
@pytest.mark.sanity
@pytest.mark.soc
@vtest
class Test_C874309_Place_Football_Single_prematch_bet(BaseBetSlipTest):
    """
    TR_ID: C874309
    NAME: Place Football Single prematch bet
    DESCRIPTION: Bet Placement - Verify that the customer can place a Single bet on pre-match Football events
    DESCRIPTION: *Pre-match events:
    DESCRIPTION: Event should not be started (isStarted=false)
    DESCRIPTION: Event should NOT have attribute isMarketBetInRun=true
    PRECONDITIONS: - Login to Oxygen app
    """
    keep_browser_open = True
    sport_name = vec.sb.FOOTBALL

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login to Oxygen app
        DESCRIPTION: Find / create event for test
        EXPECTED: User is logged in
        EXPECTED: Event is found / created
        """
        if tests.settings.backend_env == 'prod':
            additional_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)
            event = self.get_active_events_for_category(
                category_id=self.ob_config.football_config.category_id, additional_filters=additional_filter)[0]
            self.__class__.event_name = normalize_name(event['event']['name'])
            self.__class__.event_id = event['event']['id']
            self.__class__.league = self.get_accordion_name_for_event_from_ss(event=event)
            self._logger.info(f'*** Found Football event "{self.event_name}" with ID "{self.event_id}"')
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_name = f'{event.team1} v {event.team2}'
            self.__class__.event_id = event.event_id
            self.__class__.league = tests.settings.football_autotest_league
            self._logger.info(f'*** Created Football event "{self.event_name}" with ID "{self.event_id}"')

        self.site.login(username=tests.settings.betplacement_user)

    def test_001_navigate_to_football_page_from_the_menu(self):
        """
        DESCRIPTION: Navigate to Football page from the menu
        EXPECTED: Football landing page is loaded
        """
        self.site.open_sport(name=self.sport_name)
        self.site.wait_content_state(state_name=self.sport_name)

    def test_002_add_1_selection_to_bet_slip_from_pre_match_events(self):
        """
        DESCRIPTION: Add 1 selection to bet slip from pre-match events
        EXPECTED: Selection is added to bet slip
        """
        event = self.get_event_from_league(event_id=self.event_id,
                                           section_name=self.league)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for event "{self.event_name}"')

        self.__class__.selection = choice(list(output_prices.keys()))
        bet_button = output_prices.get(self.selection)
        self.assertTrue(bet_button, msg=f'Bet button for "{self.selection}" was not found')

        bet_button.click()

        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip(timeout=3)

        self.assertTrue(bet_button.is_selected(timeout=3), msg=f'Bet button is not active after selection')

    def test_003_navigate_to_betslip(self):
        """
        DESCRIPTION: Navigate to betslip
        EXPECTED: Betslip is loaded
        """
        self.site.open_betslip()

    def test_004_add_a_stake_in_the_single_stake_box_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add a stake in the Single Stake box and click on "Place Bet" button
        EXPECTED: The bet is successfully placed and bet confirmation is displayed.
        EXPECTED: The currency is in £ (or another due to customer currency set while registration).
        """
        self.__class__.bet_info = self.place_and_validate_single_bet()

    def test_005_verify_the_bet_receipt(self):
        """
        DESCRIPTION: Verify the Bet Receipt
        EXPECTED: ** The currency is in £ (or another due to customer currency set while registration)
        EXPECTED: ** The bet type is displayed: (e.g: single);
        EXPECTED: ** Odds are exactly the same as when bet has been placed;
        EXPECTED: ** Same Selection and Market is displayed where the bet was placed;
        EXPECTED: ** Correct Event is displayed;
        EXPECTED: * 'Cashout' label between the bet and Bet stake info area (if cashout is available for this event)
        EXPECTED: ** Unique Bet ID is displayed;
        EXPECTED: ** The balance is correctly updated;
        EXPECTED: ** Stake is correctly displayed;
        EXPECTED: ** Total Stake is correctly displayed;
        EXPECTED: ** Estimated Returns are exactly the same as on Bet Slip;
        EXPECTED: ** "Reuse Selection" and "Go Betting" buttons are displayed.
        """
        bet_receipt = self.site.bet_receipt.footer
        self.assertTrue(bet_receipt.has_reuse_selections_button(),
                        msg=f'"{bet_receipt.reuse_selection_button.name}" is not displayed')
        self.assertTrue(bet_receipt.has_done_button(),
                        msg=f'"{bet_receipt.done_button.name}" is not displayed')

    def test_006_click_on_go_betting_button(self):
        """
        DESCRIPTION: Click on "Go Betting" button
        EXPECTED: - Betslip is closed
        EXPECTED: - The customer is on Football page
        """
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state(state_name=self.sport_name)

    def test_007_click_on_my_bets_button_from_the_header_and_select_open_bets_tab(self):
        """
        DESCRIPTION: Click on My Bets button from the header and select "Open Bets" tab
        EXPECTED: Open Bets page is opened
        """
        self.site.open_my_bets_open_bets()

    def test_008_go_to_the_bet_that_was_just_placed_and_verify_event_card(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify event card
        EXPECTED: ** The currency is in £ (or another due to customer currency set while registration)
        EXPECTED: ** The bet type, Selection Name and odds are displayed
        EXPECTED: ** Event Name is displayed
        EXPECTED: ** Market where the bet has been placed
        EXPECTED: ** Time and Date - 24 hours format:
        EXPECTED: **HH:MM, Today** (e.g. "14:00 or 05:00, Today")
        EXPECTED: **HH:MM, DD MMM** (e.g. 14:00 or 05:00, 24 Nov or 02 Nov) - future dates
        EXPECTED: ** Correct Stake is correctly displayed
        """
        bet_name, single_bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name)

        bet_info = self.bet_info.get(self.selection)
        self.assertTrue(bet_info, msg=f'Selection "{self.selection}" info is not found')
        self.assertEqual(single_bet.bet_type, vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                         msg=f'Bet type: "{single_bet.bet_type}" '
                             f'is not as expected: "{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE}"')
        self.assertEqual(single_bet.selection_name, bet_info.get('outcome_name'),
                         msg=f'Selection Name: "{single_bet.selection_name}" '
                             f'is not as expected: "{bet_info.get("outcome_name")}"')
        self.assertEqual(single_bet.odds_value, bet_info.get('odds'),
                         msg=f'Selection Name: "{single_bet.bet_type}" '
                             f'is not as expected: "{bet_info.get("odds")}"')
        self.assertEqual(single_bet.event_name, bet_info.get('event_name'),
                         msg=f'Selection Name: "{single_bet.bet_type}" '
                             f'is not as expected: "{bet_info.get("event_name")}"')
        self.assertEqual(single_bet.market_name, bet_info.get('market_name'),
                         msg=f'Bet market name: "{single_bet.market_name}" '
                             f'is not as expected: "{bet_info.get("market_name")}"')
        expected_stake = f'£{self.bet_amount:.2f}'
        self.assertEqual(single_bet.stake.value, expected_stake,
                         msg=f'Bet Stake value: "{single_bet.stake.value}" '
                             f'is not as expected: "{expected_stake}"')
