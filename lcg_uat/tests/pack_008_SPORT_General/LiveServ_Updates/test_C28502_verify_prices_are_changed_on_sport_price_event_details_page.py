import pytest

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.safari
@vtest
class Test_C28502_Verify_Prices_Are_Changed(BaseSportTest):
    """
    TR_ID: C28502
    NAME: Prices are changed on <Sport> Event Details page
    """
    keep_browser_open = True

    markets = [
        ('to_win_not_to_nil', {'cashout': True}),
        ('over_under_total_goals', {'cashout': True}),
        ('handicap', {'cashout': True})
    ]
    new_price = '13/17'
    new_price_2 = '11/19'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add event with markets
        """
        event = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets)
        self.__class__.team1 = event.team1
        self.__class__.selection_ids = event.selection_ids
        self.__class__.eventID = event.event_id

    def test_001_trigger_price_change_for_different_markets(self):
        """
        DESCRIPTION: Trigger price change for a few selections from different markets
        EXPECTED: Corresponding 'Price/Odds' buttons should immediately display new prices
        """
        self.navigate_to_edp(event_id=self.eventID)
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()

        self.ob_config.change_price(selection_id=self.selection_ids[market_short_name][self.team1],
                                    price=self.new_price)
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets, msg='No items found on market selection list')

        self.assertIn(self.expected_market_sections.match_result, markets, msg='Match Result market is not in markets')

        markets[self.expected_market_sections.match_result].expand()

        outcomes = markets[self.expected_market_sections.match_result].outcomes.items_as_ordered_dict
        self.assertTrue(outcomes,
                        msg=f'No items found on {self.expected_market_sections.match_result} market outcomes')
        self.__class__.outcome_name = self.team1 if self.brand != 'ladbrokes' else self.team1.upper()
        self.assertIn(self.outcome_name, outcomes, msg=f'{self.outcome_name} is not in outcomes "{outcomes.keys()}"')

        self.assertTrue(outcomes[self.outcome_name].bet_button.is_price_changed(expected_price=self.new_price, timeout=40),
                        msg=f'Price for Bet Button in Match Result market did not change. '
                            f'Actual price: {outcomes[self.outcome_name].bet_button.name}. Expected price: {self.new_price}')
        markets[self.expected_market_sections.match_result].collapse()

        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No items found on market selection list')
        self.assertIn(self.expected_market_sections.to_win_not_to_nil, markets,
                      msg='To Win Not To Nil market is not in markets')

        markets[self.expected_market_sections.to_win_not_to_nil].expand()
        self.ob_config.change_price(selection_id=self.selection_ids['to_win_not_to_nil'][self.team1],
                                    price=self.new_price)

        outcomes = markets[self.expected_market_sections.to_win_not_to_nil].outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No items found on {self.expected_market_sections.to_win_not_to_nil} '
                                      f'market outcomes')
        self.assertIn(self.outcome_name, outcomes, msg=f'{self.outcome_name} is not in outcomes "{outcomes.keys()}"')

        self.assertTrue(outcomes[self.outcome_name].bet_button.is_price_changed(expected_price=self.new_price, timeout=40),
                        msg=f'Price for Bet Button in To Win To Nil market did not change. '
                            f'Actual price: {outcomes[self.outcome_name].bet_button.name}. Expected price: {self.new_price}')
        markets[self.expected_market_sections.to_win_not_to_nil].collapse()

    def test_002_trigger_price_change_from_combined_market(self):
        """
        DESCRIPTION: Trigger price change for a few selections from combined market
        EXPECTED: Corresponding 'Price/Odds' buttons should immediately display new prices
        """
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No items found on market selection list')
        self.assertIn(self.expected_market_sections.over_under_total_goals, markets,
                      msg='OverUnder Total Goals market is not in markets')

        markets[self.expected_market_sections.over_under_total_goals].expand()
        self.ob_config.change_price(selection_id=self.selection_ids['over_under_total_goals']['Over'],
                                    price=self.new_price)
        options = markets[self.expected_market_sections.over_under_total_goals].outcomes.items_as_ordered_dict
        self.assertTrue(options, msg=f'No total goals items found '
                                     f'on {self.expected_market_sections.over_under_total_goals} market')
        self.assertIn('1.5', options, msg=f'"1.5" option is not in options '
                                          f'for {self.expected_market_sections.over_under_total_goals} market')
        outcomes = options['1.5'].items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No outcome items found for "1.5" option '
                                      f'of {self.expected_market_sections.over_under_total_goals} market')
        self.assertIn('Over', outcomes, msg='"Over" is not in outcomes')

        self.assertTrue(outcomes['Over'].is_price_changed(expected_price=self.new_price, timeout=40),
                        msg=f'Price for "OVER" Bet Button in Over/Under Total Goals market did not change. '
                            f'Actual price: {outcomes["Over"].name}, Expected price: {self.new_price}')

        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No items found on market selection list')
        self.assertIn(self.expected_market_sections.over_under_total_goals, markets,
                      msg='OverUnder Total Goals market is not in markets')

        self.ob_config.change_price(selection_id=self.selection_ids['over_under_total_goals']['Under'],
                                    price=self.new_price)
        options = markets[self.expected_market_sections.over_under_total_goals].outcomes.items_as_ordered_dict
        self.assertTrue(options, msg=f'No total goals items found '
                                     f'on {self.expected_market_sections.over_under_total_goals} market')
        self.assertIn('1.5', options, msg=f'"1.5" option is not in options '
                                          f'for {self.expected_market_sections.over_under_total_goals} market')
        outcomes = options['1.5'].items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No outcome items found for "1.5" option '
                                      f'of {self.expected_market_sections.over_under_total_goals} market')
        self.assertIn('Under', outcomes, msg='"Under" is not in outcomes')

        self.assertTrue(outcomes['Under'].is_price_changed(expected_price=self.new_price, timeout=40),
                        msg=f'Price for "UNDER" Bet Button in Over/Under Total Goals market did not change. '
                            f'Actual price: {outcomes["Under"].name}, Expected price: {self.new_price}')
        markets[self.expected_market_sections.over_under_total_goals].collapse()

    def test_003_trigger_price_change_for_market_in_a_collapsed_state(self):
        """
        DESCRIPTION: Trigger prices changes for markets sections in a collapsed state
        EXPECTED: If market section is collapsed and price was changed, after expanding the section -
        updated price will be shown there
        """
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No items found on market selection list')
        self.assertIn(self.expected_market_sections.match_result, markets, msg='Match Result market is not in markets')

        markets[self.expected_market_sections.match_result].collapse()
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.ob_config.change_price(selection_id=self.selection_ids[market_short_name][self.team1], price=self.new_price_2)
        markets[self.expected_market_sections.match_result].expand()
        outcomes = markets[self.expected_market_sections.match_result].outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No items found on {self.expected_market_sections.match_result} market outcomes')
        self.assertIn(self.outcome_name, outcomes, msg=f'{self.outcome_name} is not in outcomes "{outcomes.keys()}"')
        self.assertTrue(outcomes[self.outcome_name].bet_button.is_price_changed(expected_price=self.new_price_2, timeout=40),
                        msg=f'Price for Bet Button in Match Result market did not change. '
                            f'Actual price: {outcomes[self.outcome_name].bet_button}, Expected price: {self.new_price_2}')
        markets[self.expected_market_sections.match_result].collapse()

    def test_004_trigger_prices_for_not_opened_market_collection_tabs(self):
        """
        DESCRIPTION: Trigger prices changes for not opened markets collection tabs within one event
        EXPECTED: If tab with markets is not opened and price was changed, after navigating to the tab -
        updated price will be shown there
        """
        self.ob_config.change_price(selection_id=self.selection_ids['handicap_match_result +2.0'][self.team1],
                                    price=self.new_price)

        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No items found on market selection list')
        self.assertIn(self.expected_market_sections.handicap_results, markets,
                      msg='Handicap Results market is not in markets')

        markets[self.expected_market_sections.handicap_results].expand()

        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No items found on market selection list')
        self.assertIn(self.expected_market_sections.handicap_results, markets,
                      msg='Handicap Results market is not in markets')

        outcomes = markets[self.expected_market_sections.handicap_results].outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No items found on {self.expected_market_sections.handicap_results} '
                                      f'market outcomes')
        self.assertIn('+2', outcomes, msg=f'"+2" option is not in options '
                                          f'of {self.expected_market_sections.handicap_results} market')
        bet_buttons = outcomes['+2'].items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No bet buttons found for "+2" option '
                                      f'of {self.expected_market_sections.handicap_results} market')
        self.assertIn('Home', bet_buttons, msg=f'"Home" button is not present for "+2" option '
                                               f'of {self.expected_market_sections.handicap_results} market')

        self.assertTrue(bet_buttons['Home'].is_price_changed(expected_price=self.new_price, timeout=40),
                        msg=f'Price for Bet Button in Handicap Result 1st half market did not change. '
                            f'Actual price: {bet_buttons["Home"].name}, Expected price: {self.new_price}')
