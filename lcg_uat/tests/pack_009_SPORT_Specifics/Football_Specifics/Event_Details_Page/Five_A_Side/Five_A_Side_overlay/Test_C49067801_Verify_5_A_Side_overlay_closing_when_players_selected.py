import pytest
import tests
import voltron.environments.constants as vec
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
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.five_a_side
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C49067801_Verify_5_A_Side_overlay_closing_when_players_selected(BaseFiveASide, BaseSportTest,
                                                                           BaseCashOutTest):
    """
    TR_ID: C49067801
    NAME: Verify '5-A-Side' overlay closing when players selected
    DESCRIPTION: This test case verifies '5-A-Side' overlay closing when players are selected
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

    def five_a_side_overlay_close_verification(self):
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

    def five_a_side_pop_up_content_verification(self):

        self.site.sport_event_details.tab_content.pitch_overlay.header.close_button.click()
        self.__class__.five_a_side_dailog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FIVE_A_SIDE,
                                                                      timeout=20)
        self.assertTrue(self.five_a_side_dailog,
                        msg='Five a Side dailog is not shown, after clicking on close icon in pitch view')
        self.assertEqual(self.five_a_side_dailog.pop_up_title, vec.yourcall.FIVE_A_SIDE_DRAWER_TITLE.split()[1],
                         msg=f'Pop-up title is not matching, actual text is "{self.five_a_side_dailog.pop_up_title}, '
                             f' & expected text is "{vec.yourcall.FIVE_A_SIDE_DRAWER_TITLE.split()[1]}"')
        self.assertEqual(self.five_a_side_dailog.pop_up_text, vec.five_a_side.POP_UP_TEXT,
                         msg=f'Pop-up text is not correct, actual text is "{self.five_a_side_dailog.pop_up_text}, '
                             f'& exepcted text is "{vec.five_a_side.POP_UP_TEXT}')
        self.assertTrue(self.five_a_side_dailog.leave, msg='Leave button is not present on 5-A-Side pop-up')
        self.assertTrue(self.five_a_side_dailog.stay, msg='Stay button is not present on 5-A-Side pop-up')

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

    def test_001_clicktap_plus_add_button__select_any_player__click_add_player(self):
        """
        DESCRIPTION: Click/Tap '+' (add) button > Select any player > Click 'Add player'
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

    def test_002_clicktap_on_x_close_button(self):
        """
        DESCRIPTION: Click/Tap on 'X' (close) button
        EXPECTED: Pop-up is displayed with the following content:
        EXPECTED: * '5-A-Side' title
        EXPECTED: * 'If you leave now, your team will not be saved' text
        EXPECTED: * 'Leave' button and 'Stay' button
        """
        self.five_a_side_pop_up_content_verification()

    def test_003_clicktap_on_stay_button(self):
        """
        DESCRIPTION: Click/Tap on 'Stay' button
        EXPECTED: * Pop-up is closed
        EXPECTED: * 'Pitch View' section is displayed with the selected player
        """
        self.five_a_side_dailog.stay.click()
        self.assertFalse(self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FIVE_A_SIDE, timeout=5),
                         msg='Five a Side dailog is not closed upon clicking on stay button on pop-up dailog')
        pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.items_as_ordered_dict
        actual_selected_player = list(pitch_overlay.values())[0].icon.get_attribute('class')
        self.assertEqual(actual_selected_player, 'player-icon', msg='Selected player is not appearing in pitch view')

    def test_004_clicktap_on_x_close_button(self):
        """
        DESCRIPTION: Click/Tap on 'X' (close) button
        EXPECTED: Pop-up is displayed with the same content
        """
        self.five_a_side_pop_up_content_verification()

    def test_005_clicktap_on_leave_button(self):
        """
        DESCRIPTION: Click/Tap on 'Leave' button
        EXPECTED: * '5-A-Side' overlay is closed
        EXPECTED: * Event details page remains displayed with '5-A-Side' tab selected
        EXPECTED: * Content from static block 'five-a-side-launcher' remains displayed
        """
        self.five_a_side_dailog.leave.click()
        self.five_a_side_overlay_close_verification()

    def test_006_clicktap_build_a_team_buttonverify_if_the_previous_state_is_not_saved(self):
        """
        DESCRIPTION: Click/Tap 'Build A Team' button.
        DESCRIPTION: Verify if the previous state is not saved.
        EXPECTED: * '5-A-Side' overlay is opened
        EXPECTED: * There are no added players on the 'Pitch View' section
        """
        self.site.sport_event_details.tab_content.team_launcher.build_button.click()

        pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay
        self.assertTrue(pitch_overlay, msg='Players are not displayed on the Pitch View')

        player_list = pitch_overlay.content.football_field.items_as_ordered_dict
        for players in list(player_list.values()):
            self.assertNotEqual(players.icon.get_attribute('class'), 'player-icon',
                                msg='Player is selected in pitch view, whereas it player should not be selected')
