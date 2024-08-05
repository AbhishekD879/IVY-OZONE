import pytest
import tests
from voltron.utils.helpers import do_request
from json import JSONDecodeError
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_prod  # Ladbrokes Only
# @pytest.mark.lad_stg2
# @pytest.mark.lad_tst2 # cannot get banach events in qa environments
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.five_a_side
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C49345818_Verify_the_logic_of___buttons_on_Player_Card(BaseFiveASide, BaseSportTest, BaseCashOutTest):
    """
    TR_ID: C49345818
    NAME: Verify the logic of buttons on Player Card
    DESCRIPTION: This test case verifies the logic of +/ - buttons on Player Card
    PRECONDITIONS: Feature epic: https://jira.egalacoral.com/browse/BMA-49261
    PRECONDITIONS: Feature invision: https://projects.invisionapp.com/share/ASHWPQ0DB8K#/screens/397567275
    PRECONDITIONS: Designs: https://app.zeplin.io/project/5e0a3b413cbeb61b6eb8f5c9/dashboard
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - User is on Football event EDP:
    PRECONDITIONS: - '5 A Side' sub tab (event type described above):
    PRECONDITIONS: - 'Build a team' button ->
    PRECONDITIONS: - click on '+' button near the player on the overlay ->
    PRECONDITIONS: - in the list of players select one specific.
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    proxy = None
    headers = {'Content-Type': 'application/json'}

    def get_response_url(self, url):
        """
        :param url: Required URl
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Event has configured 5-A-Side and BYB markets.
        PRECONDITIONS: 2. 5-A-Side config
        PRECONDITIONS: Navigate to Football event details page that has 5-A-Side data configured.
        PRECONDITIONS: Click/Tap on '5-A-Side' tab.
        PRECONDITIONS: Click/Tap on 'Build' button
        """
        cms_formations = self.cms_config.get_five_a_side_formations()
        if not cms_formations:
            raise CmsClientException('5-A-Side formations list from CMS is empty')
        event_id = self.get_ob_event_with_byb_market(five_a_side=True)
        self.navigate_to_edp(event_id=event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails')
        tab = self.site.sport_event_details.markets_tabs_list.items_names.__contains__('5-A-SIDE')
        self.assertTrue(tab,
                        msg=f'5-A-Side is tab is not present, active tabs are "{self.site.sport_event_details.markets_tabs_list.items_names}"')
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.five_a_side)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, self.expected_market_tabs.five_a_side,
                         msg=f'5-A-Side is not active tab after click, active tab is "{current_tab}"')
        self.site.sport_event_details.tab_content.team_launcher.build_button.click()
        if tests.settings.backend_env == 'prod':
            wait_for_result(
                lambda: self.site.sport_event_details.tab_content.pitch_overlay.journey_panel.close_button.is_displayed(
                    timeout=10) is True,
                timeout=60)
            self.site.sport_event_details.tab_content.pitch_overlay.journey_panel.close_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(),
                        msg='Pitch overlay is not shown')
        self.__class__.pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.items_as_ordered_dict
        self.assertTrue(self.pitch_overlay, msg='Players are not displayed on the Pitch View')
        if "Shots" in list(self.pitch_overlay.keys()):
            self.pitch_overlay.get("Shots").icon.click()
        elif "Passes" in list(self.pitch_overlay.keys()):
            self.pitch_overlay.get("Passes").icon.click()
        player_name = self.site.sport_event_details.tab_content.players_overlay.players_list.player_names
        self.assertTrue(player_name, msg='Players name is not present in playerListContent')
        self.assertTrue(len(player_name) > 2, msg='Player name list is empty')

        self.site.sport_event_details.tab_content.players_overlay.players_list.items[0].click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_players_card(),
                        msg='Player Card is not shown')

    def test_001_verify_the_default_value_when_entering_player_card(self):
        """
        DESCRIPTION: Verify the default value when entering player card
        EXPECTED: - default value is displayed as median/average stat value
        EXPECTED: - values are received in response (Network tab: 'statistic-value-range?obEventId=773006&playerId=28&statId=5' request, minValue: /maxValue: /average:)
        EXPECTED: and correspond to values on UI
        EXPECTED: - '+/-' buttons are clickable (if more than 1 step available)
        EXPECTED: ![](index.php?/attachments/get/59204748)
        """
        url = tests.settings.banach_api_hostname + "api/v1/statistic-value-range?"
        response_url = self.get_response_url(url=url)
        req = do_request(method='GET', url=response_url, headers=self.headers)['data']
        self.__class__.average_value = req['average']
        self.__class__.max_value = req['maxValue']
        self.__class__.min_value = req['minValue']
        self.__class__.actual_average_value = self.site.sport_event_details.tab_content.player_card.step_value
        self.assertEqual(self.actual_average_value, str(self.average_value))
        self.assertTrue(self.site.sport_event_details.tab_content.player_card.minus_button.is_enabled())
        self.assertTrue(self.site.sport_event_details.tab_content.player_card.plus_button.is_enabled())
        self.__class__.player_odds = self.site.sport_event_details.tab_content.player_card.player_odds.text
        self.__class__.market_value = self.site.sport_event_details.tab_content.player_card.stat_value.text

    def test_002_click_on_plus_button_on_player_card_overlay(self):
        """
        DESCRIPTION: Click on '+' button on player card overlay
        EXPECTED: - step value increases
        EXPECTED: - price odds button value is recalculated as well on 'Add Player' button ('price' request is sent with latest odds value)
        EXPECTED: - market value (e.g. T.Krul to Concede < 1 Goals) is updated
        EXPECTED: ![](index.php?/attachments/get/59681304)
        """
        self.site.sport_event_details.tab_content.player_card.plus_button.click()
        self.__class__.increased_step_value = self.site.sport_event_details.tab_content.player_card.step_value
        self.assertGreater(self.increased_step_value, self.actual_average_value)
        self.__class__.updated_price_odds = self.site.sport_event_details.tab_content.player_card.player_odds.text
        self.assertNotEqual(self.updated_price_odds, self.player_odds)
        self.__class__.changed_market_value = self.site.sport_event_details.tab_content.player_card.stat_value.text
        self.assertGreater(self.changed_market_value, self.market_value)

    def test_003_click_on_plus_button_several_times(self):
        """
        DESCRIPTION: Click on '+' button several times
        EXPECTED: All places stated above are updated
        """
        if self.max_value > 2:
            self.__class__.plus_button_disabled = self.site.sport_event_details.tab_content.player_card.plus_button_is_enabled
            while not self.plus_button_disabled:
                self.__class__.plus_button_disabled = self.site.sport_event_details.tab_content.player_card.plus_button_is_enabled
                if not self.plus_button_disabled:
                    self.site.sport_event_details.tab_content.player_card.plus_button.click()
                if self.plus_button_disabled is True:
                    self._logger.info(msg="Plus Button becomes greyed out and not clickable")
                    break

            self.__class__.increased_step_value_2 = self.site.sport_event_details.tab_content.player_card.step_value
            self.assertGreater(self.increased_step_value_2, self.increased_step_value)
            self.__class__.updated_price_odds_2 = self.site.sport_event_details.tab_content.player_card.player_odds.text
            self.assertNotEqual(self.updated_price_odds, self.updated_price_odds_2)
            self.__class__.changed_market_value_2 = self.site.sport_event_details.tab_content.player_card.stat_value.text
            self.assertGreater(self.changed_market_value_2, self.changed_market_value)

    def test_004_reach_the_max_value_by_clicking_plus_button(self):
        """
        DESCRIPTION: Reach the max value (by clicking '+' button)
        EXPECTED: Button becomes greyed out and not clickable
        EXPECTED: (max value is received in 'statistic-value-range?obEventId=773006&playerId=28&statId=5' request, maxValue:)
        """
        # Covered in step 3

    def test_005_click_on___button(self):
        """
        DESCRIPTION: Click on '-' button
        EXPECTED: - step value decreases
        EXPECTED: - price odds button value is recalculated as well on 'Add Player' button ('price' request is sent with latest odds value)
        EXPECTED: - market value (e.g. T.Krul to Concede < 1 Goals) is updated
        """
        self.site.sport_event_details.tab_content.player_card.minus_button.click()
        self.__class__.decreased_step_value = self.site.sport_event_details.tab_content.player_card.step_value
        self.assertNotEqual(self.decreased_step_value, self.increased_step_value_2)
        self.__class__.updated_price_odds = self.site.sport_event_details.tab_content.player_card.player_odds.text
        self.assertNotEqual(self.updated_price_odds, self.updated_price_odds_2)
        self.__class__.updated_market_value = self.site.sport_event_details.tab_content.player_card.stat_value.text
        self.assertGreater(self.changed_market_value_2, self.updated_market_value)

    def test_006_reach_the_min_value_by_clicking___button(self):
        """
        DESCRIPTION: Reach the min value (by clicking '-' button)
        EXPECTED: Button becomes greyed out and not clickable
        EXPECTED: (min value is received in 'statistic-value-range?obEventId=773006&playerId=28&statId=5' request, minValue:)
        """
        if self.max_value > 2:
            self.__class__.minus_button_disabled = self.site.sport_event_details.tab_content.player_card.minus_button_is_enabled
            while not self.minus_button_disabled:
                self.site.sport_event_details.tab_content.player_card.minus_button.click()
                self.minus_button_disabled = self.site.sport_event_details.tab_content.player_card.minus_button_is_enabled
                if self.minus_button_disabled is True:
                    self._logger.info(msg="Minus Button becomes greyed out and not clickable")
                    break

            minimum_step_value = self.site.sport_event_details.tab_content.player_card.step_value
            self.assertEqual(str(self.min_value), minimum_step_value)

    def test_007_verify_edge_case_if_happensclick_on_plus__buttons(self):
        """
        DESCRIPTION: Verify edge case (if happens):
        DESCRIPTION: click on '+/-' buttons
        EXPECTED: - step value increases/decreases
        EXPECTED: - market value (e.g. T.Krul to Concede < 1 Goals) is updated
        EXPECTED: - price odds button value stays the same because in 'price' request we receive priceNum: 0, priceDen: 0
        EXPECTED: - 'Add Player' button is active and clickable
        EXPECTED: ![](index.php?/attachments/get/62318401)
        """
        # Cannot automate this step because we dont know when Edge Case will triggered.
