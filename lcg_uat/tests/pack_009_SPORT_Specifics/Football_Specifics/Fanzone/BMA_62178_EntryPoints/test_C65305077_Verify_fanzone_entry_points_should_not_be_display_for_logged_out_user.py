import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C65305077_Verify_fanzone_entry_points_should_not_be_display_for_logged_out_user(Common):
    """
    TR_ID: C65305077
    NAME: Verify  fanzone entry points should not be display for logged out user
    DESCRIPTION: To verify if user is logged out (though syc journey is done) still Fanzone entry option should not be displayed to the user in FE
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
    PRECONDITIONS: 3)User has FE url and Valid credentials to Login Lads FE
    PRECONDITIONS: 4)User has completed the Fanzone Syc successfully in FE
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User has access to CMS
        PRECONDITIONS: Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
        PRECONDITIONS: User has FE url and Valid credentials to Login Lads FE
        PRECONDITIONS: User has completed the Fanzone Syc successfully in FE
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
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I am in button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_hit_the_fe_url_and_login_to_lads_fe(self):
        """
        DESCRIPTION: Hit the FE url and login to Lads FE
        EXPECTED: User should be able to access the url and is logged into Lads application, User is on Homepage
        """
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")

    def test_002_now_verify_if_any_of_the_entry_points_for_fanzone_page_is_visible(self):
        """
        DESCRIPTION: Now verify if any of the Entry points for Fanzone page is visible
        EXPECTED: User should be able to see All the Fanzone entry points
        """
        self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")

    def test_003_now_logout_from_the_application(self):
        """
        DESCRIPTION: Now logout from the application
        EXPECTED: User should be logged out from application successfully
        """
        self.site.logout()

    def test_004_now_verify_the_fanzone_entry__if_user_is_able_to_see(self):
        """
        DESCRIPTION: Now Verify the Fanzone entry , if user is able to see
        EXPECTED: User should not be able to see any entry points as user  has not logged in to application
        """
        self.assertFalse(self.site.home.fanzone_banner(timeout=3), msg="Fanzone banner is still displayed after logout")
