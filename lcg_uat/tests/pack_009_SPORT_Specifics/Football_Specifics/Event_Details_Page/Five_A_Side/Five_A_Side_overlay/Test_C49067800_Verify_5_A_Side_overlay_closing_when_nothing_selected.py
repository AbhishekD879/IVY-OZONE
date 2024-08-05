import pytest
import tests
import re
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import cleanhtml, normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_prod  # Ladbrokes Only
@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.five_a_side
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C49067800_Verify_5_A_Side_overlay_closing_when_nothing_selected(BaseFiveASide, BaseSportTest,
                                                                           BaseCashOutTest):
    """
    TR_ID: C49067800
    NAME: Verify '5-A-Side' overlay closing when nothing selected
    DESCRIPTION: This test case verifies '5-A-Side' overlay closing when no players are selected
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Click/Tap on '5-A-Side' tab
    PRECONDITIONS: 4. Click/Tap 'Build A Team' button
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    """
    keep_browser_open = True
    proxy = None

    def tap_on_close(self):
        """
        This method verifies following points:
        * '5-A-Side' overlay is closed
        * Event details page remains displayed with '5-A-Side' tab selected
        * Content from static block 'five-a-side-launcher' remains displayed
        """
        self.site.sport_event_details.tab_content.pitch_overlay.header.close_button.click()
        try:
            self.site.sport_event_details.tab_content.pitch_overlay
            self.assertFalse(self.site.sport_event_details.tab_content.pitch_overlay,
                             msg='5-A-Side overlay is not closed')
        except Exception:
            pass

        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, self.expected_market_tabs.five_a_side,
                         msg=f'5-A-Side is not active tab after click, active tab is "{current_tab}"')

        current_url = self.device.get_current_url()
        self.assertTrue(current_url.endswith(f'{self.event_id}/5-a-side'),
                        msg=f'Current url "{current_url}" not ends with "{self.event_id}/5-a-side"')

        static_block = self.cms_config.get_static_block(uri='five-a-side-launcher')
        cms_title = cleanhtml(static_block['htmlMarkup']).splitlines()[1]
        cms_text = cleanhtml(static_block['htmlMarkup']).splitlines()[2]

        ui_title = self.site.sport_event_details.tab_content.five_a_side_title
        self.assertEquals(cms_title, ui_title,
                          msg=f'Title from UI "{ui_title}" does not match with cms title"{cms_title}"')
        ui_text = self.site.sport_event_details.tab_content.five_a_side_text
        self.assertEquals(cms_text, ui_text, msg=f'Text from UI "{ui_text}" does not match with cms text"{cms_text}"')

    def formation_name_verification(self):

        cms_active_formation = self.cms_formations[0]
        pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay
        formation_carousel = pitch_overlay.content.formation_carousel.items_as_ordered_dict
        self.assertTrue(formation_carousel, msg='Formation toggles carousel is not displayed')
        formation_name, self.__class__.formation_item = next(iter(formation_carousel.items()))
        cms_formation_name = cms_active_formation.get("title").upper()
        self.assertEqual(formation_name, cms_formation_name,
                         msg=f'Formation name "{formation_name}" is not the same as expected '
                             f'from cms "{cms_formation_name}"')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
        PRECONDITIONS: 3. Click/Tap on '5-A-Side' tab
        PRECONDITIONS: 4. Click/Tap 'Build A Team' button
        """
        self.__class__.cms_formations = self.cms_config.get_five_a_side_formations()
        if not self.cms_formations:
            raise CmsClientException('5-A-Side formations list from CMS is empty')
        self.__class__.event_id = self.get_ob_event_with_byb_market(five_a_side=True)

        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.event_id)
        event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'***Found Football 5-A-Side event {event_name} with id "{self.event_id}"')

        self.navigate_to_edp(event_id=self.event_id, sport_name='football')
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

    def test_001_clicktap_on_x_close_button(self):
        """
        DESCRIPTION: Click/Tap on 'X' (close) button
        EXPECTED: * '5-A-Side' overlay is closed
        EXPECTED: * Event details page remains displayed with '5-A-Side' tab selected
        EXPECTED: * Content from static block 'five-a-side-launcher' remains displayed
        """
        self.tap_on_close()

    def test_002_clicktap_build_team_button(self):
        """
        DESCRIPTION: Click/Tap 'Build team' button
        EXPECTED: * '5-A-Side' overlay is opened
        EXPECTED: * First formation is selected
        """
        self.site.sport_event_details.tab_content.team_launcher.build_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(),
                        msg='5-A-Side Pitch overlay is not shown')

        self.formation_name_verification()

        lst = [formation_item for formation_item in self.formation_item.get_attribute('innerHTML').split('class')]
        formation_selected = False
        for attribute in lst:
            if re.search(r"formation-name selected", attribute):
                formation_selected = True
                break
        self.assertTrue(formation_selected, msg='First formation is not selected')

    def test_003_clicktap_plus_add_button__select_any_player__clicktap_add_player(self):
        """
        DESCRIPTION: Click/Tap '+' (add) button > Select any player > Click/Tap 'Add player'
        EXPECTED: * 'Pitch View' section is displayed with the selected player
        """
        pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.items_as_ordered_dict
        self.assertTrue(pitch_overlay, msg='Players are not displayed on the Pitch View')
        list(pitch_overlay.values())[0].icon.click()

        self.site.sport_event_details.tab_content.players_overlay.players_list.items[0].click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_players_card(),
                        msg='Player Card is not shown')
        self.site.sport_event_details.tab_content.player_card.add_player_button.click()
        actual_selected_player = list(pitch_overlay.values())[0].icon.get_attribute('class')
        self.assertEqual(actual_selected_player, 'player-icon', msg='Selected player is not appearing in pitch view')

    def test_004_clicktap_on_formation_2_and_back_on_formation_1(self):
        """
        DESCRIPTION: Click/Tap on formation #2 and back on formation #1
        EXPECTED: * 'Pitch View' section is displayed with NO players selected
        """
        pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay
        self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.items_as_ordered_dict

        formation_carousel = pitch_overlay.content.formation_carousel.items_as_ordered_dict
        self.assertTrue(formation_carousel, msg='Formation toggles carousel is not displayed')

        pitch_overlay.content.formation_carousel.items[1].click()

        pitch_overlay.content.formation_carousel.items[0].click()
        self.formation_name_verification()

        result = wait_for_result(lambda: pitch_overlay.content.football_field.items_as_ordered_dict, timeout=60)
        self.assertTrue(result, msg='Pitch content is not loaded after tab switch')

        player_list = pitch_overlay.content.football_field.items_as_ordered_dict

        for players in list(player_list.values()):
            self.assertNotEqual(players.icon.get_attribute('class'), 'player-icon',
                                msg='Player selected tab-1, is appearing in tab2')

    def test_005_clicktap_on_x_close_button(self):
        """
        DESCRIPTION: Click/Tap on 'X' (close) button
        EXPECTED: * '5-A-Side' overlay is closed
        EXPECTED: * Event details page remains displayed with '5-A-Side' tab selected
        EXPECTED: * Content from static block 'five-a-side-launcher' remains displayed
        """
        self.tap_on_close()
