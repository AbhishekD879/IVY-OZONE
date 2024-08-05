import pytest

from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.prod_incident
@pytest.mark.back_button
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.football
@pytest.mark.scorecast
@pytest.mark.bet_placement
@pytest.mark.login
@vtest
class Test_C28544_Placing_Scorecast_bet(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C28544
    NAME: Placing Scorecast bet
    DESCRIPTION: This scenario verifies placing a Scorecast bet for Football event
    PRECONDITIONS: 1) In order to run this test scenario select event with market name "First Goal Scorecast" and/or "Last Goal Scorecast"
    PRECONDITIONS: 2) To get information for an event use the following url
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) User is logged in
    PRECONDITIONS: 4) User should have fractional price type as default
    """
    keep_browser_open = True
    market_value = 'Last Goal Scorecast'
    goal_scorer_name = 'Player 1, Draw 1-1'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event with Scorecast market
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(markets=[('scorecast', {'cashout': True})])
        self.__class__.eventID = event_params.event_id
        self.__class__.event_name_on_sports_page = event_params.team1 + ' v ' + event_params.team2

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application and  Log in.
        EXPECTED: User is successfully logged in.
        """
        self.site.login(async_close_dialogs=False)

    def test_002_tap_football_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu Ribbon
        EXPECTED: Football Landing page is opened
        """
        self.__class__.user_balance = self.site.header.user_balance
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')

    def test_003_open_event_details_page(self):
        """
        DESCRIPTION: Open Event Details Page
        EXPECTED: *   Football Event Details page is opened
        EXPECTED: *   FOR CORAL: 'Main Markets' collection is selected by default
        EXPECTED: *   FOR LADBROKES: 'All Markets' collection is selected by default
        """
        self.navigate_to_edp(self.eventID, timeout=30)
        markets_tabs = self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict
        self.assertTrue(markets_tabs, msg=f'Market tabs are not shown "{markets_tabs.keys()}"')

        cms_market_tabs = self.cms_config.get_market_tabs_order()
        self.assertTrue(cms_market_tabs, msg='EDP market tabs list from CMS is empty')
        if self.expected_market_tabs.main_markets in cms_market_tabs:
            current_tab = self.site.sport_event_details.markets_tabs_list.current
            self.assertEqual(current_tab, self.expected_market_tabs.main_markets,
                             msg=f'Main Markets is not active tab, active tab is "{current_tab}"')

    def test_004_go_to_scorecast_market_section(self):
        """
        DESCRIPTION: Go to Scorecast market section
        EXPECTED: Scorecast market section is present and shown after 'Correct Score' market
        """
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg=f'Markets accordions are not shown "{markets.keys()}"')
        correct_score = markets.get(self.expected_market_sections.correct_score)
        self.assertTrue(correct_score, msg=f'"{self.expected_market_sections.correct_score}" market section is not found in "{markets.keys()}"')
        self.__class__.scorecast = markets.get(self.expected_market_sections.scorecast)
        self.assertTrue(self.scorecast, msg=f'"{self.expected_market_sections.scorecast}" market section is not found in "{markets.keys()}"')

    def test_005_select_first_scorerlast_scorer_and_home_teamaway_team_from_section_1(self):
        """
        DESCRIPTION: Select 'First Scorer'/'Last Scorer' and '<Home Team>'/'<Away Team>' from section 1
        EXPECTED: 'First Scorer'/'Last Scorer' and <Home Team>/<Away Team> options are selected
        """
        self.scorecast.first_scorer_tab.click()
        self.assertTrue(self.scorecast.first_scorer_tab.is_selected(), msg='First scorer tab is not selected')

        self.scorecast.last_scorer_tab.click()
        self.assertTrue(self.scorecast.last_scorer_tab.is_selected(), msg='Last scorer tab is not selected')
        self.scorecast.first_goalscorer_team_button.click()

        first_goalscorer_team_selected = self.scorecast.first_goalscorer_team_button.is_selected()
        self.assertTrue(first_goalscorer_team_selected, msg='First goal scorer team button is not selected')

        self.scorecast.last_goalscorer_team_button.click()

        last_goalscorer_team_selected = self.scorecast.last_goalscorer_team_button.is_selected()
        self.assertTrue(last_goalscorer_team_selected, msg='Last goal scorer team button is not selected')

    def test_006_select_firstplayer_to_scorelast_player_to_score_and_correct_score(self):
        """
        DESCRIPTION: Select '**First Player to Score**'/'**Last Player to Score**' and '**Correct Score**'
        EXPECTED: 'Odds calculation' button becomes enabled when both selections are made
        """
        selected_player = self.scorecast.player_scorers_list.selected_item
        self._logger.debug(f'*** Selected player name is: "{selected_player}"')
        self.assertFalse(self.scorecast.add_to_betslip.is_enabled(expected_result=False),
                         msg='"Odds calculation" button is active')
        self.scorecast.home_team_results_dropdown.select_value('1')
        self.scorecast.away_team_results_dropdown.select_value('1')
        self.assertTrue(self.scorecast.add_to_betslip.is_enabled(timeout=4),
                        msg='"Odds calculation" button is not active')
        result = wait_for_result(lambda: self.scorecast.add_to_betslip.output_price != 'N/A',
                                 name='Odds to recalculate',
                                 timeout=1)
        self.assertTrue(result, msg='Price still shown as N/A')
        self.__class__.odds_price = self.scorecast.add_to_betslip.output_price
        self._logger.debug(f'*** Output price for selection is: "{self.odds_price}"')

    def test_007_tap_odds_calculation_button(self):
        """
        DESCRIPTION: Tap 'Odds calculation' button
        EXPECTED: Bet Slip counter is changed
        """
        self.scorecast.add_to_betslip.click()
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip()
            self.verify_betslip_counter_change(expected_value=1)

    def test_008_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: *  Selection is added to the Betslip
        EXPECTED: *  All information is displayed correctly
        EXPECTED: * Odds within Betslip is the same as on selected 'Odds calculation' button
        """
        if self.device_type == 'mobile':
            self.site.open_betslip()
        self.__class__.singles_section = self.get_betslip_sections().Singles
        self.__class__.section_details = list(self.singles_section.values())[0]
        self.assertEqual(self.singles_section.name, vec.betslip.BETSLIP_SINGLES_NAME,
                         msg=f'Section title "{self.singles_section.name}" is not the same as expected '
                         f'"{vec.betslip.BETSLIP_SINGLES_NAME}"')
        self.assertEqual(self.section_details.odds, self.odds_price,
                         msg=f'Actual: "{self.section_details.odds}" odds '
                             f'are not the same as Expected: "{self.odds_price}"')

    def test_009_verify_selection_name(self):
        """
        DESCRIPTION: Verify Selection Name
        EXPECTED: Selection Name contains two parts:
        EXPECTED: *   Selected Goal Scorer first (name corresponds to **player name **selected in Scorecast market section)
        EXPECTED: *   Selected Correct Score (corresponds to **correct score outcome name** selected in Scorecast market section)
        EXPECTED: in format **<goal scorer name>, <correct score>**
        """
        selections_count = self.get_betslip_content().selections_count
        self.assertEqual(selections_count, '1',
                         msg=f'Singles selection count "{selections_count}" is not the same as expected "1"')
        self.assertEqual(self.section_details.outcome_name, self.goal_scorer_name,
                         msg=f'Actual outcome name "{self.section_details.outcome_name}", '
                             f'expected "{self.goal_scorer_name}"')

    def test_010_verify_market_type(self):
        """
        DESCRIPTION: Verify Market Type
        EXPECTED: **'First Goal Scorecast'/'Last Goal Scorecast' **market name is displayed accordingly to market that user selects in Scorecast market section (**'First Scorer'**/**'Last Scorer' **respectively)
        """
        self.assertEqual(self.section_details.market_name, self.market_value,
                         msg=f'Actual market type "{self.section_details.market_name}" '
                             f'is not matched with expected "{self.market_value}"')

    def test_011_verify_event_start_time_and_event_name(self):
        """
        DESCRIPTION: Verify Event Start Time and Event Name
        EXPECTED: Event Name is shown in format: **Team1 v/vs Team2 **
        EXPECTED: accordingly to SS response
        """
        self.assertEqual(self.section_details.event_name, self.event_name_on_sports_page,
                         msg=f'Actual event title "{self.section_details.event_name}", '
                             f'expected "{self.event_name_on_sports_page}"')

    def test_012_enter_valid_stake_amount_and_place_a_bet_by_tapping_bet_now_button(self):
        """
        DESCRIPTION: Enter valid 'Stake' amount and place a bet by tapping 'Bet Now' button
        EXPECTED: *  Bet is placed successfully
        EXPECTED: *  User's balance is decremented by entered stake
        EXPECTED: * Bet Reciept is displayed
        """
        self.place_single_bet()
        expected_user_balance = self.user_balance - self.bet_amount
        self.verify_user_balance(expected_user_balance=expected_user_balance)
        self.user_balance = expected_user_balance
        self.check_bet_receipt_is_displayed()

    def test_013_change_price_type_format_from_fractional_to_decimal_and_repeat_steps_7_12(self):
        """
        DESCRIPTION: Change price type format from fractional to decimal and repeat steps #7-12
        """
        self.site.close_betreceipt()
        result = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(result, msg='Odds format is not changed to Decimal')
        # To repeat steps 7 to 12 there is dependency from step 4
        self.navigate_to_edp(self.eventID, timeout=30)
        self.test_004_go_to_scorecast_market_section()
        self.test_005_select_first_scorerlast_scorer_and_home_teamaway_team_from_section_1()
        self.test_006_select_firstplayer_to_scorelast_player_to_score_and_correct_score()
        self.test_007_tap_odds_calculation_button()
        self.test_008_open_betslip_page()
        self.test_009_verify_selection_name()
        self.test_010_verify_market_type()
        self.test_011_verify_event_start_time_and_event_name()
        self.test_012_enter_valid_stake_amount_and_place_a_bet_by_tapping_bet_now_button()
