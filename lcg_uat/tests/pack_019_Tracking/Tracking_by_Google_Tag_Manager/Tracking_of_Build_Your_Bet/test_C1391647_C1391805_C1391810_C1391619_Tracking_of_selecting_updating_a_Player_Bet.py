import pytest

from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseYourCallTrackingTest


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.google_analytics
@pytest.mark.banach
@pytest.mark.build_your_bet
@pytest.mark.mocked_data
@pytest.mark.cms
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C1391647_C1391805_C1391810_C1391619_Tracking_of_selecting_updating_a_Player_Bet(BaseYourCallTrackingTest, BaseBanachTest):
    """
    TR_ID: C1391647
    TR_ID: C1391805
    TR_ID: C1391810
    TR_ID: C1391619
    VOL_ID: C9698061
    NAME: Tracking of selecting/updating a Player Bet
    PRECONDITIONS: 1. Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: 2. Browser console should be opened
    """
    keep_browser_open = True

    def expand_collapse_market(self, market_name, collapse=False):
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg='Can not find market list "%s"' % markets_list)
        market = markets_list.get(market_name)
        self.assertTrue(market, msg='Can not get market "%s"' % market_name)
        if collapse:
            if not market.is_expanded(expected_result=False, timeout=0.5):
                market.expand()
                market.is_expanded()
            market.collapse()
            self.assertFalse(market.is_expanded(expected_result=False), msg='%s section is not expanded' % market_name)
        else:
            if market.is_expanded():
                market.collapse()
                market.is_expanded(expected_result=False)
            market.expand()
            self.assertTrue(market.is_expanded(), msg='%s section is not expanded' % market_name)

    def verify_tracking_of_player_actions(self, event_label, player_name, player_stat, player_stat_value):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'build bet',
        EXPECTED: 'eventLabel' : 'select player bet',
        EXPECTED: 'playerName' : '<< PLAYER NAME >>'
        EXPECTED: 'playerStat' : '<< STATISTIC NAME >>',
        EXPECTED: 'playerStatNum' : '<< STATISTIC NUMBER >>' })
        """
        actual_response = self.get_data_layer_specific_object(object_key='playerName', object_value=player_name)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'your call',
                             'eventAction': 'build bet',
                             'eventLabel': event_label,
                             'playerName': player_name,
                             'playerStat': player_stat,
                             'playerStatNum': int(player_stat_value),
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_000_check_ob_event_is_active_to_use_in_mock(self):
        """
        DESCRIPTION: Get OB event to use in mock service
        """
        self.__class__.eventID = self.create_ob_event_for_mock()
        self._logger.info('*** Created BYB event id "%s"' % self.eventID)

    def test_001_turned_on_required_yourcall_league_in_cms(self):
        """
        DESCRIPTION: Check if required #YourCall league enabled in CMS and turn it on if not
        """
        self.cms_config.your_call_league_switcher()

    def test_002_navigate_to_yourcall_detail_page(self):
        """
        DESCRIPTION: Click on 'Go to Event' link within the #YourCall accordions
        EXPECTED: - Event details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet, timeout=5),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

    def test_003_track_expand_collapse_choose_a_player_statistic_and_statistic_number_from_the_player_bets_accordion(self):
        """
        DESCRIPTION: Track Expand/collapse
        DESCRIPTION: Choose a player, statistic and statistic number from the 'Player Bets' accordion
        EXPECTED: Player and statistic are chosen
        """
        # track expand selection
        player_bets = self.expected_market_sections.player_bets
        self.expand_collapse_market(market_name=player_bets, collapse=True)
        self.verify_tracking_of_expanding_collapsing_market_accordion(accordion_action='collapse market accordion')

        # track collapse selection
        self.expand_collapse_market(market_name=player_bets)
        self.verify_tracking_of_expanding_collapsing_market_accordion(accordion_action='expand market accordion')

        self.__class__.selection_params = self.add_player_bet_selection_to_dashboard(player_index=1,
                                                                                     statistic_index=1,
                                                                                     statistic_value_index=1)

    def test_004_click_on_add_to_bet_button(self):
        """
        DESCRIPTION: Click on 'Add to Bet' button
        EXPECTED: The selections are added to #YC Dashboard
        """
        self.__class__.dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        self.assertTrue(self.dashboard_panel.byb_summary.has_place_bet_button(),
                        msg='"Place bet" button not displayed on Dashboard')
        self.assertTrue(self.dashboard_panel.byb_summary.place_bet.has_price,
                        msg='"Place bet" button price not displayed')

    def test_005_track_of_added_selection(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'build bet',
        EXPECTED: 'eventLabel' : 'select player bet',
        EXPECTED: 'playerName' : '<< PLAYER NAME >>'
        EXPECTED: 'playerStat' : '<< STATISTIC NAME >>',
        EXPECTED: 'playerStatNum' : '<< STATISTIC NUMBER >>' })
        """
        self.verify_tracking_of_player_actions(event_label='select player bet',
                                               player_name=self.selection_params.player_name,
                                               player_stat=self.selection_params.player_statistic,
                                               player_stat_value=self.selection_params.statistic_value)

    def test_006_edit_added_player_bet_change_player_name_or_statistic_within_the_bet_dashboard_click_on_done_button(self):
        """
        DESCRIPTION: Edit added Player Bet (change player name or statistic) within the Bet Dashboard > Click on Done button
        EXPECTED: Player name and Statistic are changed
        """
        outcomes = self.dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'List of outcomes does not exist')
        edit_player_bets_button = list(outcomes.values())[0]
        edit_player_bets_button.edit_button.click()

        edit_section = self.dashboard_panel.outcomes_section.edit_selection.edit
        self.assertTrue(edit_section.is_displayed(), msg='Edit Selection section is not displayed')

        edit_section.select_player_drop_down.select_value_by_index(3)
        edit_section = self.dashboard_panel.outcomes_section.edit_selection.edit
        self.__class__.player_name = edit_section.select_player_drop_down.selected_item

        edit_section.select_statistic_drop_down.select_value_by_index(1)
        edit_section = self.dashboard_panel.outcomes_section.edit_selection.edit
        self.__class__.statistic_name = edit_section.select_statistic_drop_down.selected_item

        edit_section.select_statistic_value_drop_down.value = '2'
        edit_section = self.dashboard_panel.outcomes_section.edit_selection.edit
        self.__class__.statistic_value = edit_section.select_statistic_value_drop_down.selected_item

        edit_selection = self.dashboard_panel.outcomes_section.edit_selection
        edit_selection.header.done_button.click()

    def test_007_verify_updated_statistic_in_datalayer(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: he following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'build bet',
        EXPECTED: 'eventLabel' : 'update statistic',
        EXPECTED: 'playerName' : '<< PLAYER NAME >>'
        EXPECTED: 'playerStat' : '<< STATISTIC NAME >>',
        EXPECTED: 'playerStatNum' : '<< STATISTIC NUMBER >>' })
        """
        self.verify_tracking_of_player_actions(event_label='update statistic', player_name=self.player_name, player_stat=self.statistic_name,
                                               player_stat_value=self.statistic_value)

    def test_008_verify_converted_odds_in_datalayer(self, event_action='display odds'):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: {  'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'display odds',
        EXPECTED: 'eventLabel' : '(display the actual odds i.e 3.00)'
        EXPECTED: >> All odds are converted to decimal for tracking
        """
        price = self.dashboard_panel.byb_summary.place_bet.value_text
        event_price = self.convert_fraction_price_to_decimal(initial_price=price, round_to=2) + 1
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value=event_action)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'your call',
                             'eventAction': event_action,
                             'eventLabel': event_price,
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_009_click_on_the_final_priceodds_to_place_bet_within_the_yc_dashboard(self):
        """
        DESCRIPTION: Click on the final price/odds to place bet within the #YC Dashboard
        """
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary
        dashboard_panel.place_bet.click()

    def test_010_verify_event_action_click_odds_in_datalayer(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: {  'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'click odds',
        EXPECTED: 'eventLabel' : '(display the actual odds i.e 3.00)'
        EXPECTED: >> All adds are converted to decimal format
        """
        self.test_008_verify_converted_odds_in_datalayer(event_action='click odds')
