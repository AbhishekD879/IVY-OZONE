import tests
import pytest
from voltron.environments import constants as vec
from tests.base_test import vtest
from time import sleep
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.hl # not configured in prod and Beta
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65305230_To_verify_SYC_popup_in_football_landing_page_when_user_kills_the_app_without_completing_team_selection_from_SYC_page_and_get_back_to_football_SPL(Common):
    """
    TR_ID: C65305230
    NAME: To verify SYC popup in football landing page when user kills the app without completing team selection from SYC page and get back to football SPL
    DESCRIPTION: To verify SYC popup in football landing page when user kills the app without completing team selection from SYC page and get back to football SPL
    PRECONDITIONS: 1) User is in logged in state
    PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
    PRECONDITIONS: 3) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
    PRECONDITIONS: 4) User is in SYC- team selection page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User is in logged in state
        PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
        PRECONDITIONS: 3) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
        PRECONDITIONS: 4) User is in SYC- team selection page
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport('FOOTBALL', fanzone=True, timeout=5)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              verify_name=False)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I am in button is displayed',
                        timeout=5)

    def test_001_select_any_team(self):
        """
        DESCRIPTION: Select any team
        EXPECTED: User will see his team selection in a highlighted box and gets confirmation popup
        """
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        sleep(2)
        teams = self.site.show_your_colors.items_as_ordered_dict
        team_ui_box_border = teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].css_property_value('border').split()[0]
        self.assertTrue(team_ui_box_border == vec.fanzone.SYC_SELECTED_TEAM_BORDER,
                        msg=f'"{teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].name}" '
                            f' Previously subscribed team selection is not in highlighted box ')
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        self.assertTrue(dialog_confirm, msg='Did not get Confirmation dialog')

    def test_002_exit_from_the_application_or_kill_the_app(self):
        """
        DESCRIPTION: Exit from the application or kill the app
        EXPECTED: User should be able to exit from application
        """
        self.device.open_new_tab()
        self.device.open_tab(tab_index=0)
        self.device.close_current_tab()
        self.device.switch_to_new_tab()

    def test_003_login_to_lads_application_and_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Login to lads application and navigate to Football landing page
        EXPECTED: SYC popup should be displayed
        """
        self.device.navigate_to(tests.HOSTNAME)
        self.site.open_sport('FOOTBALL', fanzone=True, timeout=5)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              verify_name=False)
        self.assertTrue(dialog_fb, msg='SYC popup is not displayed')
