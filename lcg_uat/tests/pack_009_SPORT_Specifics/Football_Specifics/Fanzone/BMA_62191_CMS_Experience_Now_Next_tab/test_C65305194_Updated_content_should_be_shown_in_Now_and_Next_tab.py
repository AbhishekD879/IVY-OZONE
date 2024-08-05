import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305194_Updated_content_should_be_shown_in_Now_and_Next_tab(Common):
    """
    TR_ID: C65305194
    NAME: Updated content should be shown in Now and Next tab
    DESCRIPTION: To verify when user updates the Label in Now and next tab in cms then updated data should be shown in FE
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)User has valid credentials to login to cms
    PRECONDITIONS: 3)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
    PRECONDITIONS: 4)User has logged into Lads FE and is on Fanzone page
    PRECONDITIONS: 5) User is on NOW and NEXT tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)User has valid credentials to login to cms
        PRECONDITIONS: 3)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
        PRECONDITIONS: 4)User has logged into Lads FE and is on Fanzone page
        PRECONDITIONS: 5) User is on NOW and NEXT tab
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        self.__class__.astonvilla_premierLeagueLbl = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())['premierLeagueLbl']
        if self.astonvilla_premierLeagueLbl:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(), premierLeagueLbl=False)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='OK button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION, timeout=10)
        dialog_confirm.confirm_button.click()
        sleep(6)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()
        self.site.wait_content_state_changed(timeout=10)

    def test_001_verify_now_and_next_tab_label_in_fe(self):
        """
        DESCRIPTION: Verify NOW and Next tab Label in FE
        EXPECTED: User should be able to labels in Now and Next tab as entered in CMS
        """
        # as per the new change, after subscription, we will be in fanzone page only
        # banner = self.site.home.fanzone_banner()
        # banner.let_me_see.click()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)

    def test_002_hit_the_cms_url_and_login_to_cms(self):
        """
        DESCRIPTION: Hit the cms url and Login to CMS
        EXPECTED: User should be able to login to cms
        """
        # Can't automate CMS

    def test_003_now_click_on_fanzone_label_from_left_menu_in_cms(self):
        """
        DESCRIPTION: Now click on Fanzone label from Left menu in cms
        EXPECTED: User should be able to see Fanzone page
        """
        # Can't automate CMS

    def test_004_click_on_now_and_next_tab(self):
        """
        DESCRIPTION: Click on Now and Next tab
        EXPECTED: User should be navigated to NOW and Next tab and is able to see the available fields
        """
        # Can't automate CMS

    def test_005_now_update_the_label_data_for_the_fields_and_save_the_changes(self):
        """
        DESCRIPTION: Now update the Label data for the fields and save the changes
        EXPECTED: User should be able to update the Label data in cms and save the changes
        """
        # Covered in preconditions

    def test_006_login_to_fe_and_navigate_to_fanzone_page(self):
        """
        DESCRIPTION: Login to FE and navigate to Fanzone page,
        EXPECTED: User should be able to login to FE successfully and should be navigate to Fanzone FE
        """
        # Covered in preconditions

    def test_007_verify_if_now_and_next_tab__if_updated_labels_data_is_shown(self):
        """
        DESCRIPTION: Verify if NOW and Next Tab , if updated labels data is shown
        EXPECTED: User should be able to see updated label names in NOW and Next tab
        """
        self.assertEqual("FALSE", self.site.fanzone.premier_leauge_link.text, msg="Premier League Table is displayed")

    def tearDown(self):
        # Reverting the premier league label fanzone configuration
        self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(), premierLeagueLbl=self.astonvilla_premierLeagueLbl)
