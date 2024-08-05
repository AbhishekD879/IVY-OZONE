import tests
import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from time import sleep
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_h1
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65304927_Verify_SYC_popup_should_not_display_for_unsubscribed_user_until_user_completes_30days_from_previous_subscribe_to_fanzone(Common):
    """
    TR_ID: C65304927
    NAME: Verify SYC popup should not display for unsubscribed user until user completes 30days from previous subscribe to fanzone
    DESCRIPTION: Verify SYC popup should not display for unsubscribed user until user completes 30days from previous subscribe to fanzone
    PRECONDITIONS: 1) User has logged into lads application
    PRECONDITIONS: 2) User has Unsubscribed to Fanzone less than 30 days ago
    PRECONDITIONS: 3) Configure fanzone data in CMS
    PRECONDITIONS: CMS-->Fanzone-->Fanzones
    PRECONDITIONS: 4) In System Config Fanzone should be enabled
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User has logged into lads application
        PRECONDITIONS: 2) User has Unsubscribed to Fanzone less than 30 days ago
        PRECONDITIONS: 3) Configure fanzone data in CMS
        PRECONDITIONS: CMS-->Fanzone-->Fanzones
        PRECONDITIONS: 4) In System Config Fanzone should be enabled
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state(state_name='HomePage')
        sleep(3)
        self.site.login(username=username)
        self.site.open_sport(name='Football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Fanzones are displayed',
                        timeout=5)
        fanzone = self.site.show_your_colors.items_as_ordered_dict
        fanzone[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_teamalert.exit_button.click()
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")
        if tests.settings.device_type == "mobile":
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.get(vec.racing.RACING_HIGHLIGHTS_TAB_NAME).click()
        self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")
        fanzone_banner = self.site.home.fanzone_banner()
        fanzone_banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')
        self.site.fanzone.setting_link.click()
        dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_teamalert.toggle_switch.click()
        dialog_unsubscribe_fanzone = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_UNSUBSCRIBE_FROM_FANZONE)
        dialog_unsubscribe_fanzone.confirm_button.click()

    def test_001_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football landing page
        EXPECTED: User should be navigated to Football landing page
        """
        self.site.open_sport(name='FOOTBALL', fanzone=True)

    def test_002_verify_syc_popup_is_not_displayed_in_football_landing_page(self):
        """
        DESCRIPTION: Verify SYC popup is not displayed in Football landing page
        EXPECTED: SYC popup shouldn't be displayed
        """
        dialog_fb = self.site.football.has_syc_popup(expected_result=False)
        self.assertFalse(dialog_fb, msg='Syc popup is displayed even after unsubscribed')
