import pytest
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from tests.Common import Common
from time import sleep


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305086_Verify_clicking_on_back_button_from_edp_page_user_will_be_navigated_back_to_Fanzone_page_again(Common):
    """
    TR_ID: C65305086
    NAME: Verify clicking on back button from edp page user will be navigated back to Fanzone page again
    DESCRIPTION: To verify if user clicks on back button from edp page then user should be navigated to Fanzone page again
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
    PRECONDITIONS: 3)User has FE url and Valid credentials to Login Lads FE
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
        PRECONDITIONS: 3)User has FE url and Valid credentials to Login Lads FE
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(),
                                           typeId=self.football_config.autotest_class.autotest_premier_league.type_id)

        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state(state_name='Football')
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='OK button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()
        self.site.wait_content_state_changed(timeout=10)
        wait_for_result(lambda: self.site.fanzone.tabs_menu.current,
                        name='Fanzone page not displayed',
                        timeout=5)

    def test_001_verify_user_is_able_to_see_now_and_next_tab_in_fanzone_page(self):
        """
        DESCRIPTION: Verify user is able to see Now and Next tab in Fanzone page
        EXPECTED: user should be able to see Now and Next Tab in Fanzone page
        """
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_002_now_verify_if_next_events_are_shown_in_now_and_next_tab(self):
        """
        DESCRIPTION: Now verify if Next events are shown in Now and Next tab
        EXPECTED: User should be able to see preplay events in Next events section
        """
        self.__class__.next_games = self.site.fanzone.tab_content.highlight_carousels
        self.assertIn('VILLA NEXT GAMES', self.next_games)

    def test_003_now_click_on_any_preplay_events_from_the_section(self):
        """
        DESCRIPTION: Now click on any preplay events from the section
        EXPECTED: User should be navigated to edp page
        """
        events = list(self.next_games.get('VILLA NEXT GAMES').items_as_ordered_dict.values())
        self.assertTrue(events, msg="Events are not found in Next Games")
        events[0].click()
        self.site.wait_content_state(state_name='EventDetails')

    def test_004_click_on_back_button_from_edp_page(self):
        """
        DESCRIPTION: Click on back button from Edp page
        EXPECTED: user should be navigated back to Fanzone page
        """
        self.site.back_button.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu.current,
                        name='Fanzone page not displayed',
                        timeout=5)
