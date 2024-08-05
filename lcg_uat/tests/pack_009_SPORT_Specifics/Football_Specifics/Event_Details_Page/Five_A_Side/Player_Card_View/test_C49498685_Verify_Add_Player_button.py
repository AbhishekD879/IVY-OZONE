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
class Test_C49498685_Verify_Add_Player_button(BaseFiveASide, BaseSportTest, BaseCashOutTest):
    """
    TR_ID: C49498685
    NAME: Verify 'Add Player' button
    DESCRIPTION: This test case verifies 'Add Player' button on player card overlay
    PRECONDITIONS: Feature epic: https://jira.egalacoral.com/browse/BMA-49261
    PRECONDITIONS: Feature invision: https://projects.invisionapp.com/share/ASHWPQ0DB8K#/screens/397567275
    PRECONDITIONS: Designs: https://app.zeplin.io/project/5e0a3b413cbeb61b6eb8f5c9/dashboard
    PRECONDITIONS: OX 103 design changes:
    PRECONDITIONS: https://zpl.io/V4xq3W0
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - User is on Football event EDP: Player Card view
    PRECONDITIONS: - '5 A Side' sub tab (event type described above):
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

    def test_001_clicktap_build_a_team_button___clicktap_plus_button_near_the_player_on_the_overlay___in_the_list_of_players_select_one_specific(self):
        """
        DESCRIPTION: Click/tap 'Build a team' button -> click/tap '+' button near the player on the overlay -> in the list of players select one specific
        EXPECTED: User is on Player Card View
        """
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
        list(self.pitch_overlay.values())[0].icon.click()
        player_name = self.site.sport_event_details.tab_content.players_overlay.players_list.player_names
        self.assertTrue(player_name, msg='Players name is not present in playerListContent')
        self.assertTrue(len(player_name) > 2, msg='Player name list is empty')

        self.site.sport_event_details.tab_content.players_overlay.players_list.items[0].click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_players_card(),
                        msg='Player Card is not shown')

    def test_002_verify_the_button_state_before_user_changes_the_stats_value(self):
        """
        DESCRIPTION: Verify the button state before user changes the stats value
        EXPECTED: - 'Add Player' button is active and clickable
        EXPECTED: - 'Add Player' button is visually separated from odds with lighter color
        EXPECTED: - 'ODDS' label is changed to 'Team Odds'
        EXPECTED: ![](index.php?/attachments/get/114764009)
        """
        add_player_button = self.site.sport_event_details.tab_content.player_card.add_player_button
        self.assertTrue(add_player_button.is_enabled(), msg='"Add Player" button is not active and not clickable')
        self.assertIn('Team Odds', add_player_button.name.split('\n'))
        self.__class__.output_price = add_player_button.output_price

    def test_003_click_on_plus__functional_buttons_at_the_right_upper_corner_of_the_overlay(self):
        """
        DESCRIPTION: Click on '+/-' functional buttons at the right upper corner of the overlay
        EXPECTED: - Request 'price' is triggered to Banach
        EXPECTED: - Odds change accordingly and are displayed on the button
        EXPECTED: - 'Add Player' button is active
        """
        url = tests.settings.banach_api_hostname + 'api/v1/price'
        self.site.sport_event_details.tab_content.player_card.plus_button.click()
        self.__class__.add_player_button = self.site.sport_event_details.tab_content.player_card.add_player_button
        self.assertTrue(self.add_player_button.is_enabled(), msg='"Add Player" button is not active and not clickable')
        odds_change = self.add_player_button.output_price
        self.assertNotEqual(odds_change, self.output_price,
                            msg=f'Actual odds "{odds_change}" is same as'
                                f'Expected Odds "{self.output_price}".')
        response_url = self.get_web_socket_response_by_url(url=url)
        self.assertTrue(response_url, msg=f'URL "{url}" is not triggered')

    def test_004_press_add_player_button(self):
        """
        DESCRIPTION: Press 'Add Player' button
        EXPECTED: - User is redirected to pitch view
        EXPECTED: - Player is added and displayed on the corresponding position on pitch view
        """
        self.add_player_button.click()
        actual_selected_player = list(self.pitch_overlay.values())[0].icon.get_attribute('class')
        self.assertIn(actual_selected_player, 'player-icon no-box-shadow', msg='Selected player is not appearing in pitch view')

    def test_005_return_to_player_card_view_and_press_plus_functional_button_till_user_reaches_max_value_limit(self):
        """
        DESCRIPTION: Return to player card view and press '+' functional button till user reaches max value limit
        EXPECTED: - 'Add Player' button is active and clickable
        EXPECTED: - Odds are recalculated and displayed (spinner is displayed when user clicks several times the functional +/- buttons)
        """
        url = tests.settings.banach_api_hostname + "api/v1/statistic-value-range?"
        response_url = self.get_response_url(url=url)
        req = do_request(method='GET', url=response_url, headers=self.headers)['data']
        self.__class__.max_value = req['maxValue']
        list(self.pitch_overlay.values())[0].icon.click()
        if self.max_value > 2:
            plus_button_disabled = self.site.sport_event_details.tab_content.player_card.plus_button_is_enabled
            while not plus_button_disabled:
                plus_button_disabled = self.site.sport_event_details.tab_content.player_card.plus_button_is_enabled
                if not plus_button_disabled:
                    self.site.sport_event_details.tab_content.player_card.plus_button.click()
                if plus_button_disabled is True:
                    self._logger.info(msg="Plus Button becomes greyed out and not clickable")
                    break
        add_player_button = self.site.sport_event_details.tab_content.player_card.add_player_button
        self.assertTrue(add_player_button.is_enabled(), msg='"Add Player" button is not active and not clickable')
        odds_change = add_player_button.output_price
        self.assertNotEqual(odds_change, self.output_price,
                            msg=f'Actual odds "{odds_change}" is same as'
                                f'Expected Odds "{self.output_price}"')

    def test_006_press___functional_button_till_user_reaches_min_value_limit(self):
        """
        DESCRIPTION: Press '-' functional button till user reaches min value limit
        EXPECTED: - 'Add Player' button is active and clickable
        EXPECTED: - Odds are recalculated and displayed
        """
        if self.max_value > 2:
            minus_button_disabled = self.site.sport_event_details.tab_content.player_card.minus_button_is_enabled
            while not minus_button_disabled:
                self.site.sport_event_details.tab_content.player_card.minus_button.click()
                minus_button_disabled = self.site.sport_event_details.tab_content.player_card.minus_button_is_enabled
                if minus_button_disabled is True:
                    self._logger.info(msg="Minus Button becomes greyed out and not clickable")
                    break
        add_player_button = self.site.sport_event_details.tab_content.player_card.add_player_button
        self.assertTrue(add_player_button.is_enabled(), msg='"Add Player" button is not active and not clickable')
        odds_change = add_player_button.output_price
        self.assertNotEqual(odds_change, self.output_price,
                            msg=f'Actual odds "{odds_change}" is same as'
                                f'Expected Odds "{self.output_price}"')
