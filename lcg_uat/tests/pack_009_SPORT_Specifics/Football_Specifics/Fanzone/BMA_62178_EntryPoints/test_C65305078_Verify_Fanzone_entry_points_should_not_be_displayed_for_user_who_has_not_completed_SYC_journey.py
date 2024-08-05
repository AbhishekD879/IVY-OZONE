import pytest
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.fanzone
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C65305078_Verify_Fanzone_entry_points_should_not_be_displayed_for_user_who_has_not_completed_SYC_journey(Common):
    """
    TR_ID: C65305078
    NAME: Verify Fanzone entry points should not be displayed for user who has not completed SYC journey
    DESCRIPTION: To verify if user has not completed the SYC journey then Fanzone Banner/option should not be displayed to the user after login irrespective of any entry points
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

        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_001_hit_the_fe_url_and_login_to_lads_fe(self):
        """
        DESCRIPTION: Hit the FE url and login to Lads FE
        EXPECTED: User should be able to access the url and is logged into Lads application, User is on Homepage
        """
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football", timeout=10)

    def test_002_click_on_the_im_in_option(self):
        """
        DESCRIPTION: Click on the "Im In" option
        EXPECTED: User should be navigated to Syc page
        """
        dialog_fb = wait_for_result(
            lambda: self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=10))
        sleep(3)
        dialog_fb.imin_button.click()

    def test_003_select_the_team_and_close_the_syc_page__abruptly(self):
        """
        DESCRIPTION: Select the team and close the syc page  abruptly
        EXPECTED: User should be able to close syc page abruptly
        """
        teams = wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict, timeout=40,
                                name='All Teams to be displayed')
        self.assertTrue(teams, msg='Teams are not displayed')

        list(teams.values())[1].scroll_to_we()
        list(teams.values())[1].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION, timeout=20)
        sleep(3)
        dialog_confirm.select_different_button.click()

    def test_004_now_navigate_homepage(self):
        """
        DESCRIPTION: Now navigate Homepage
        EXPECTED: User should be navigated to homepage
        """
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")

    def test_005_verify_if_fanzone_entry_points_are_visible_to_the_user(self):
        """
        DESCRIPTION: Verify if Fanzone entry points are visible to the user
        EXPECTED: User should not be able to see any entry points in FE as Syc journey is not completed for the logged in user
        """
        if self.device_type == 'mobile':
            sports_ribbon = self.site.home.menu_carousel.items_as_ordered_dict
        else:
            sports_ribbon = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict.keys()
        self.assertNotIn('Fanzone', sports_ribbon, msg='user able to see entry points in FE')
