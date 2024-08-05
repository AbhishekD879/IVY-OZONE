import pytest
import voltron.environments.constants as vec
import tests
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
@pytest.mark.desktop
@vtest
class Test_C169131_Verify_Market_selector_drop_down_on_Competitions_page(BaseBetSlipTest):
    """
    TR_ID: C169131
    NAME: Verify Market selector drop down on Competitions page
    DESCRIPTION: This test case verifies Market selector drop down on Competitions page and also verify Bet placement for Single and Quick Bet
    PRECONDITIONS: 1. Load Oxygen application
    PRECONDITIONS: 2. Go to Football Landing page
    PRECONDITIONS: 3. Click/Tap on Competition Module header
    PRECONDITIONS: 4. Click/Tap on sub-category (Class ID) with Type ID's
    PRECONDITIONS: 5. Choose Competition (Type ID)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following templateMarketNames:
    PRECONDITIONS: * |Match Betting| - "Match Result"
    PRECONDITIONS: * |To Qualify| - "To Qualify"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 2.5"
    PRECONDITIONS: * |Both Teams to Score| - "Both Teams to Score"
    PRECONDITIONS: * |To Win Not to Nil| - "To Win and Both Teams to Score" **Ladbrokes removed from OX 100.3/Coral from OX 101.1**
    PRECONDITIONS: * |Match Result and Both Teams To Score| - "Match Result & Both Teams To Score" **Ladbrokes added from OX 100.3/Coral from OX 101.1**
    PRECONDITIONS: * |Draw No Bet| - "Draw No Bet"
    PRECONDITIONS: * |First-Half Result| - "1st Half Result"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    is_clicked = False
    markets = [('to_qualify', ),
               ('over_under_total_goals', {'over_under': 2.5}),
               ('both_teams_to_score', ),
               ('draw_no_bet', ),
               ('first_half_result', ),
               ('match_result_and_both_teams_to_score', ),
               ('next_team_to_score', ),
               ('extra_time_result', ),
               ('to_win_not_to_nil', )]

    def place_bet_and_verify(self):
        sections = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(sections,
                        msg='"Sections" are not available')
        for section in sections:
            events = list(section.items_as_ordered_dict.values())
            self.assertTrue(' "Events" are not available')
            for event in events:
                selections = list(event.template.items_as_ordered_dict.values())
                self.assertTrue(' "Selections" are not available')
                for selection in selections:
                    if selection.is_enabled():
                        selection.click()
                        self.__class__.is_clicked = True
                        break
                if self.is_clicked:
                    break
            if self.is_clicked:
                break

        self.__class__.is_clicked = False
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(timeout=10), msg='Quick Bet panel is not opened')
            self.site.quick_bet_panel.selection.content.amount_form.input.value = self.bet_amount
            self.site.quick_bet_panel.place_bet.click()
            self.assertTrue(self.site.quick_bet_panel.wait_for_bet_receipt_displayed(), msg='Bet Receipt is not displayed')
            self.site.quick_bet_panel.header.close_button.click()
        else:
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1, header3, header2=None):
        self.site.wait_content_state_changed()
        items = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())[-1]
        events = items.items_as_ordered_dict.values()
        self.assertTrue(events, msg='"Events" are not available')
        event = items.fixture_header
        self.assertEqual(event.header1, header1,
                         msg=f'Actual fixture header "{event.header1}" does not equal to'
                             f'Expected "{header1}"')
        if header2:
            self.assertEqual(event.header2, header2,
                             msg=f'Actual fixture header "{event.header2}" does not equal to'
                                 f'Expected "{header2}"')
        self.assertEqual(event.header3, header3,
                         msg=f'Actual fixture header "{event.header3}" does not equal to'
                             f'Expected "{header3}"')
        bet_buttons = len(list(events)[-1].template.get_available_prices())
        self.assertEqual(bet_buttons, bet_button_qty,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "{bet_button_qty}".')

    def market_switcher_is_sticky(self):
        is_sticky = self.site.contents.tab_content.is_market_selector_sticky
        if self.device_type == 'desktop':
            self.assertFalse(is_sticky, msg='"Market Selector" is sticky in Football league')
        else:
            self.assertTrue(is_sticky, msg='"Market Selector" is not sticky in Football league')
        self.drop_down_functionality()

    def drop_down_functionality(self):
        dropdown = self.site.competition_league.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown arrow" is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                dropdown.click()
                sleep(2)
                self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')

    def check_empty_strings(self, list):
        """
        DESCRIPTION:  This condition ensures that the list itself is not empty
                      and also checks if all items in the list, after stripping any whitespace,
                      are non-empty strings.
        """
        return list if all(list) and all(item.strip() for item in list) else False

    def test_000_pre_conditions(self):
        """
        DESCRIPTION: User should be logged in
        """
        if tests.settings.backend_env != 'prod':
            competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
            if not competitions_countries:
                competitions_countries = self.cms_config.get_system_configuration_item('CompetitionsFootball')
            if str(self.ob_config.football_config.autotest_class.class_id) not in competitions_countries.get(
                    'A-ZClassIDs').split(','):
                raise CmsClientException(f'{tests.settings.football_autotest_competition} class '
                                         f'is not configured on Competitions tab')

            all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
            self.assertTrue(all_sports_status, msg='"All Sports" market switcher status is disabled')
            market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='football', status=True)
            self.assertTrue(market_switcher_status, msg='Market switcher is disabled for football sport')

            self.ob_config.add_autotest_premier_league_football_event(markets=self.markets)

        self.site.login()
        self.site.open_sport(name='FOOTBALL')
        self.site.wait_content_state('football')
        expected_sport_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                     self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(expected_sport_tab)
        self.site.wait_content_state_changed()
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'Competition tab is not active, active is "{active_tab}"')

        if self.device_type == 'desktop':
            self.site.football.tab_content.grouping_buttons.items_as_ordered_dict[vec.sb_desktop.COMPETITIONS_SPORTS].click()
            competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        else:
            competitions = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict
        self.assertTrue(competitions, msg='No competitions are present on page')

        if tests.settings.backend_env == 'prod':
            competition_league = vec.siteserve.PREMIER_LEAGUE_NAME
            if tests.settings.brand == 'ladbrokes' and self.device_type == 'desktop':
                league = vec.siteserve.ENGLAND.title()
            else:
                league = vec.siteserve.ENGLAND
        else:
            if tests.settings.brand == 'ladbrokes' and self.device_type == 'desktop':
                league = 'Auto Test'
            else:
                league = 'AUTO TEST'
            competition_league = vec.siteserve.AUTO_TEST_PREMIER_LEAGUE_NAME

        competition = competitions[league]
        competition.expand()
        leagues = wait_for_result(lambda: self.check_empty_strings(competition.items_as_ordered_dict),
                                  name='Leagues list is loaded',
                                  timeout=5)
        self.assertTrue(leagues, msg='No leagues are present on page')
        self.assertIn(competition_league, leagues.keys(),
                      msg=f'League "{competition_league}" is not found in "{list(leagues.keys())}"')
        league = leagues[competition_league]
        league.click()
        self.site.wait_content_state('CompetitionLeaguePage')

    def test_001_verify_displaying_of_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify displaying of the 'Market selector' drop down
        EXPECTED: **For tablet/mobile:**
        EXPECTED: * ‘Market Selector’ is displayed below Competitions sub-tabs (Matches/Outrights/Results)
        EXPECTED: * 'Match Result' is selected by default in 'Market selector' drop down
        EXPECTED: * "Market:" is shown in front of <market name>
        EXPECTED: **For desktop:**
        EXPECTED: * ‘Market Selector’ is displayed next to Matches/Outrights Selector on the right side
        EXPECTED: * 'Match Result' is selected by default in 'Market Selector' drop down
        EXPECTED: * Up and down arrows (chevrons) are shown next to 'Match result' in 'Market Selector'
        """
        has_market_selector = self.site.competition_league.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Football Leauge')
        self.drop_down_functionality()
        selected_value = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(),
                         msg=f'Actual selected value: "{selected_value}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper()}"')

    def test_002_scroll_the_page_down(self):
        """
        DESCRIPTION: Scroll the page down
        EXPECTED: **For tablet/mobile:**
        EXPECTED: * Market selector remains at the top of the scrolling page
        EXPECTED: * Market selector functionality remains the same
        EXPECTED: **For desktop:**
        EXPECTED: * Market selector is NOT sticky. It becomes hidden when scrolling the page down
        """
        self.site.contents.scroll_to_bottom()
        self.market_switcher_is_sticky()

    def test_003_scroll_the_page_up(self):
        """
        DESCRIPTION: Scroll the page up
        EXPECTED: **For tablet/mobile:**
        EXPECTED: * Market selector remains at the top of the scrolling page
        EXPECTED: * Market selector functionality remains the same
        EXPECTED: **For desktop:**
        EXPECTED: * Market selector is NOT sticky. It becomes visible when scrolling the page up
        """
        self.site.contents.scroll_to_top()
        self.market_switcher_is_sticky()

    def test_004_verify_options_available_for_football_in_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify options available for Football in the Market selector drop down:
        EXPECTED: *The following markets are shown in the Market selector drop down in the order listed below:*
        EXPECTED: * Match Result
        EXPECTED: * To Qualify
        EXPECTED: * Next Team to Score
        EXPECTED: * Extra Time Result
        EXPECTED: * Total Goals Over/Under 2.5
        EXPECTED: * Both Teams to Score
        EXPECTED: * To Win Not to Nil **Ladbrokes removed from OX 100.3/Coral from OX 101.1**
        EXPECTED: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3/Coral from OX 101.1**
        EXPECTED: * Draw No Bet
        EXPECTED: * 1st Half Result
        EXPECTED: *If any Market is not available it is skipped in the Market selector drop down list*
        """
        self.__class__.expected_market_list = vec.siteserve.EXPECTED_MARKETS_NAMES
        self.__class__.actual_market_list = list(self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())

        if tests.settings.backend_env == "prod":
            # Checking if all markets are available in FE as configured in the CMS
            expected_markets = self.cms_config \
                .get_sports_tab_data(sport_id=self.ob_config.football_config.category_id,
                                     tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,)['marketsNames']
            expected_market_list_cms = [market['title'] for market in expected_markets]
            # If events are not available for any market then skip the validation
            for market in self.actual_market_list:
                self.assertIn(market, expected_market_list_cms,
                                msg=f'Actual market: {market} is not present in '
                                    f'the Expected list: {expected_market_list_cms}')
        else:
            for market in self.actual_market_list:
                self.assertIn(market, self.expected_market_list,
                              msg=f'Market "{market}" is not in expected market list')

    def test_005_select_match_results_in_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Select 'Match Results' in the Market selector drop down
        EXPECTED: * The events for selected market are shown
        EXPECTED: * Values on Fixture header are changed for each event according to selected market
        EXPECTED: * Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        if self.expected_market_list.match_result_default in self.actual_market_list:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_market_list.match_result_default).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1=vec.sb.HOME, header2=vec.sb.DRAW, header3=vec.sb.AWAY)
            self.place_bet_and_verify()
        else:
            self._logger.info(msg=f'Market {self.expected_market_list.match_result_default} is not in the actual market list')

    def test_006_select_both_teams_to_score_in_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Select 'Both Teams to Score' in the Market selector drop down
        EXPECTED: * The events for selected market are shown
        EXPECTED: * Values on Fixture header are changed for each event according to selected market
        EXPECTED: * Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        if self.expected_market_list.both_teams_to_score in self.actual_market_list:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_market_list.both_teams_to_score).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1=vec.sb.FIXTURE_HEADER.yes, header3=vec.sb.FIXTURE_HEADER.no)
            self.place_bet_and_verify()
        else:
            self._logger.info(msg=f'Market {self.expected_market_list.both_teams_to_score} is not in the actual market list')

    def test_007_repeat_step_6_for_to_qualify_next_team_to_score_extra_time_result_overunder_total_goals_25_to_win_not_to_nil_ladbrokes_removed_from_ox_1003_match_result_and_both_teams_to_score_ladbrokes_added_from_ox_1003_draw_no_bet_1st_half_result(self):
        """
        DESCRIPTION: Repeat step 6 for:
        DESCRIPTION: * To Qualify
        DESCRIPTION: * Next Team to Score
        DESCRIPTION: * Extra Time Result
        DESCRIPTION: * Over/Under Total Goals 2.5
        DESCRIPTION: * To Win Not to Nil **Ladbrokes removed from OX 100.3**
        DESCRIPTION: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3**
        DESCRIPTION: * Draw No Bet
        DESCRIPTION: * 1st Half Result
        EXPECTED:Verify the messages displayed for user in Bet Slip and My Bets section when Logged Out/Logged in.
        """
        if self.expected_market_list.to_qualify in self.actual_market_list:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_market_list.to_qualify).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1=vec.sb.HOME, header3=vec.sb.AWAY)
            self.place_bet_and_verify()
        else:
            self._logger.info(msg=f'Market {self.expected_market_list.to_qualify} is not in the actual market list')

        if self.expected_market_list.next_team_to_score in self.actual_market_list:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_market_list.next_team_to_score).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1=vec.sb.HOME, header2=vec.sb.AWAY, header3=vec.sb.NO_GOAL)
            self.place_bet_and_verify()
        else:
            self._logger.info(msg=f'Market {self.expected_market_list.next_team_to_score} is not in the actual market list')

        if self.expected_market_list.extra_time_result in self.actual_market_list:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_market_list.extra_time_result).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1=vec.sb.HOME, header2=vec.sb.DRAW, header3=vec.sb.AWAY)
            self.place_bet_and_verify()
        else:
            self._logger.info(msg=f'Market {self.expected_market_list.extra_time_result} is not in the actual market list')

        if self.expected_market_list.total_goals_over_under_2_5 in self.actual_market_list:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_market_list.total_goals_over_under_2_5).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1=vec.sb.OVER.upper(), header3=vec.sb.UNDER.upper())
            self.place_bet_and_verify()
        else:
            self._logger.info(msg=f'Market {self.expected_market_list.total_goals_over_under_2_5} is not in the actual market list')

        if self.expected_market_list.match_result_and_both_teams_to_score in self.actual_market_list:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_market_list.match_result_and_both_teams_to_score).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1=vec.sb.HOME, header2=vec.sb.DRAW, header3=vec.sb.AWAY)
            self.place_bet_and_verify()
        else:
            self._logger.info(msg=f'Market {self.expected_market_list.match_result_and_both_teams_to_score} is not in the actual market list')

        if self.expected_market_list.draw_no_bet in self.actual_market_list:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_market_list.draw_no_bet).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1=vec.sb.HOME, header3=vec.sb.AWAY)
            self.place_bet_and_verify()
        else:
            self._logger.info(msg=f'Market {self.expected_market_list.draw_no_bet} is not in the actual market list')

        if self.expected_market_list.first_half_result in self.actual_market_list:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_market_list.first_half_result).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1=vec.sb.HOME, header2=vec.sb.DRAW, header3=vec.sb.AWAY)
            self.place_bet_and_verify()
        else:
            self._logger.info(msg=f'Market {self.expected_market_list.first_half_result} is not in the actual market list')

    def test_008_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_match_result_to_qualify_next_team_to_score_extra_time_result_total_goals_overunder_25_both_teams_to_score_to_win_not_to_nil_ladbrokes_removed_from_ox_1003coral_from_ox_1011_match_result_and_both_teams_to_score_ladbrokes_added_from_ox_1003coral_from_ox_1011_draw_no_bet_1st_half_result(self):
        """
        DESCRIPTION: Verify Bet Placement for Single and Quick Bet for the below markets
        DESCRIPTION: * Match Result
        DESCRIPTION: * To Qualify
        DESCRIPTION: * Next Team to Score
        DESCRIPTION: * Extra Time Result
        DESCRIPTION: * Total Goals Over/Under 2.5
        DESCRIPTION: * Both Teams to Score
        DESCRIPTION: * To Win Not to Nil **Ladbrokes removed from OX 100.3/Coral from OX 101.1**
        DESCRIPTION: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3/Coral from OX 101.1**
        DESCRIPTION: * Draw No Bet
        DESCRIPTION: * 1st Half Result
        EXPECTED: Bet should be placed successfully
        """
        # Covered in step 6 and 7
