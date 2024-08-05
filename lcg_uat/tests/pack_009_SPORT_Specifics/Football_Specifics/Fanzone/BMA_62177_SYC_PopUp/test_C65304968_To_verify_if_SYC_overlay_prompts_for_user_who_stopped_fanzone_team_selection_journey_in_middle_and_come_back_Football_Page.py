import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_tst2
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone_reg_tests
@vtest
class Test_C65304968_To_verify_if_SYC_overlay_prompts_for_user_who_stopped_fanzone_team_selection_journey_in_middle_and_come_back_Football_Page(Common):
    """
    TR_ID: C65304968
    NAME: To verify if SYC overlay prompts for user who stopped fanzone team selection journey in middle and come back Football Page
    DESCRIPTION: To verify if SYC overlay prompts for user who stopped fanzone team selection journey in middle and come back Football Page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
    PRECONDITIONS: 3)Featured events are present to be displayed for competition for the particular team in OB
    PRECONDITIONS: 4)SYC page is created in cms with all required data in Fanzone SYC section
    PRECONDITIONS: 5)User has not performed any action on SYC overlay
    PRECONDITIONS: 6)User has FE url and Valid credentials to Login Lads FE and user has successfully logged into application
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Active the fanzone team and register a new user
        EXPECTED: Fanzone team is activated in cms and logged into the application
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
        self.site.login(username=username, timeout=10)
        self.site.wait_content_state('Homepage')

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: User should be navigated to Football page
        """
        self.site.open_sport(name='Football', fanzone=True)
        self.site.wait_content_state("football", timeout=30)

    def test_002_verify_if_syc_overlay_is_shown_in_football_page(self):
        """
        DESCRIPTION: Verify if SYC overlay is shown in Football page
        EXPECTED: SYC overlay is shown to the user in Football Landing page
        """
        self.__class__.dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        self.assertTrue(self.dialog_fb, msg=f'{vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS} is not displayed.')

    def test_003_click_on_im_in_button_in_the_overlay(self):
        """
        DESCRIPTION: Click on "I'M IN" BUTTON in the overlay
        EXPECTED: user should be navigated to SYC selection page
        """
        self.dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='SYC is displayed',
                        timeout=5)

    def test_004_select_a_team(self):
        """
        DESCRIPTION: Select a team
        EXPECTED: User should get confiramtion popup
        """
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        self.assertTrue(dialog_confirm, msg=f'Team Confirmation popup is not displayed.')

    def test_005_click_on_home_page_button(self):
        """
        DESCRIPTION: click on home page button
        EXPECTED: User should be redirected to home page
        """
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('Homepage', timeout=30)

    def test_006_navigate_to_football_page_and_check_syc_overlay(self):
        """
        DESCRIPTION: navigate to football page and check SYC Overlay
        EXPECTED: User should get SYC Overlay
        """
        self.test_001_navigate_to_football_page()
        self.test_002_verify_if_syc_overlay_is_shown_in_football_page()

    def test_007_repeat_the_above_process_by_redirecting_to_other_page_closing_the_app_disconnecting_network(self):
        """
        DESCRIPTION: Repeat the above process by redirecting to other page, closing the app, disconnecting network....
        EXPECTED:
        """
        # cannot automate with closing the app and disconnecting the network
        self.navigate_to_page(name='home/in-play')
        self.site.wait_content_state('Homepage')
        self.test_006_navigate_to_football_page_and_check_syc_overlay()
