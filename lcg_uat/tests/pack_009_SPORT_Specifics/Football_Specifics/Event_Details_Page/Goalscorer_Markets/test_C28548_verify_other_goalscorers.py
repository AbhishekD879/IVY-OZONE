import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.markets
@pytest.mark.goalscorer
@pytest.mark.sports
@pytest.mark.medium
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-36215')
@vtest
class Test_C28548_Verify_Other_Goalscorers(BaseSportTest):
    """
    TR_ID: C28548
    VOL_ID: C9698484
    NAME: Verify Other Goalscorer Markets section on Football Event Details pages
    """
    sport_name = 'Football'
    keep_browser_open = True
    section = None
    market = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add 'Football' event
        """
        event_params = self.ob_config.add_football_event_to_autotest_league2(
            markets=[('hat_trick', {'cashout': True}), ('last_goalscorer', {'cashout': True})])
        self.__class__.team1, self.__class__.team2, self.__class__.selection_ids =\
            event_params.team1, event_params.team2, event_params.selection_ids
        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.created_event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.created_event_name}"')

        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

    def test_001_tap_sport(self):
        """
        DESCRIPTION: Tap '<Sport>' icon on the Sports Menu Ribbon
        """
        self.site.open_sport(name=self.sport_name)

    def test_002_click_event(self):
        """
        DESCRIPTION: Tap Event name on the event section, Football Event Details page is opened
        """
        event = self.get_event_from_league(section_name=self.section_name, event_id=self.eventID)
        event.click()

    def test_003_navigating_other_goalscorers(self):
        """
        DESCRIPTION: Go to 'Other Goalscorer Markets' section
        EXPECTED: Verify It is possible to collapse/expand section
        """
        self.site.sport_event_details.markets_tabs_list.open_tab(vec.siteserve.EXPECTED_MARKET_TABS.all_markets)
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg='Markets list is not present')
        self.assertTrue(self.expected_market_sections.other_goalscorer_markets in markets_list,
                        msg='"OTHER GOALSCORER MARKETS" section is not present')
        self.__class__.section = markets_list.get(self.expected_market_sections.other_goalscorer_markets)
        self.assertTrue(self.section, msg='OTHER GOALSCORER MARKETS section is not found')

        self.section.collapse()
        self.assertFalse(self.section.is_expanded(), msg='"OTHER GOALSCORER MARKETS" is not collapsible')
        self.section.expand()
        self.assertTrue(self.section.is_expanded(), msg='"OTHER GOALSCORER MARKETS" is not expandable')

    def test_004_verify_cash_out_indicator(self):
        """
        DESCRIPTION: Verify Cash out label next to Goalscorer Market section name
        EXPECTED: Verify "Other Goalscorer" table
        """
        self.assertTrue(self.section.market_section_header.has_cash_out_mark(),
                        msg='Market %s have no cashout indicator' % self.section)

        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets are shown')
        self.assertIn(self.expected_market_sections.other_goalscorer_markets, markets,
                      msg='OTHER GOALSCORER MARKETS market was not found in %s' % markets)
        self.__class__.market = markets.get(self.expected_market_sections.other_goalscorer_markets)
        self.assertTrue(self.market, msg='OTHER GOALSCORER MARKETS section is not found')

        actual_columns = self.market.outcome_table.columns
        self.assertEqual(actual_columns, vec.sb.EXPECTED_OTHER_GOALSCORER_COLUMNS,
                         msg=f'Incorrect table columns. Actual: "{actual_columns}", Expected:"{vec.sb.EXPECTED_OTHER_GOALSCORER_COLUMNS}"')
        if self.market.has_show_all_button:
            self.market.show_all_button.click()
        actual_players = sorted(self.market.outcome_table.players)
        expected_home_players = sorted(self.selection_ids['last_goalscorer'].keys())[1::2]
        self.assertListEqual(actual_players, expected_home_players,
                             msg='Incorrect players. Actual: "%s", Expected:"%s"'
                             % (actual_players, expected_home_players))

        self.__class__.market_grouping_buttons = self.market.grouping_buttons.items_as_ordered_dict
        # BMA-36215
        self.assertIn(self.team2.upper(), self.market_grouping_buttons,
                      msg=f'Tab name "{self.team2.upper()}" is not available, one of "{list(self.market_grouping_buttons.keys())}" expected')
        self.market.grouping_buttons.click_button(self.team2.upper())
        if self.market.has_show_all_button:
            self.market.show_all_button.click()
        actual_players = sorted(self.market.outcome_table.players)
        expected_away_players = sorted(self.selection_ids['last_goalscorer'].keys())[0::2]
        self.assertListEqual(actual_players, expected_away_players,
                             msg='Incorrect players. Actual: "%s", Expected:"%s"' %
                                 (actual_players, expected_away_players))

    def test_005_verify_players_column_content(self):
        """
        DESCRIPTION: Verify ‘Players’ column content
        """
        self.assertTrue(self.market.has_grouping_buttons,
                        msg='Market %s have no grouping buttons' % self.section)
        team1_selector = self.market_grouping_buttons.get(self.team1.upper())
        team2_selector = self.market_grouping_buttons.get(self.team2.upper())
        self.assertEqual(team1_selector.name, self.team1.upper(),
                         msg='Incorrect text for team 1 selector. Actual: "%s", Expected:"%s"'
                             % (team1_selector.name, self.team1.upper()))
        self.assertEqual(team2_selector.name, self.team2.upper(),
                         msg='Incorrect text for team 2 selector. Actual: "%s", Expected:"%s"'
                             % (team2_selector.name, self.team2.upper()))
        team1_selector.click()
        self.assertTrue(team1_selector.is_selected(),
                        msg='Team1 "%s" selector is not active' % self.team1.upper())
