import pytest
import tests
from tests.base_test import vtest
from time import sleep
from tests.Common import Common
from datetime import datetime
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305052_To_verify_user_should_be_able_to_see_only_Active_banners_with_data_in_Fanzone_page(Common):
    """
    TR_ID: C65305052
    NAME: To verify user should be able to see only Active banners with data in Fanzone page
    DESCRIPTION: To verify user should be able to see only Active banners with data in Fanzone page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)Promotion banners are created in Sitecore
    PRECONDITIONS: 4)User has enabled Club toggle in Fanzone page
    PRECONDITIONS: 5)User has created promotion in club subsection in Fanzone with below data:
    PRECONDITIONS: a)Promotion Title
    PRECONDITIONS: b)Promotion details
    PRECONDITIONS: c)CTA button
    PRECONDITIONS: d)Promotion title
    PRECONDITIONS: 6)Make some of the promotions as expired in CMS
    PRECONDITIONS: 7)User has FE url and Valid credentials to Login Lads FE
    PRECONDITIONS: 8) User has logged into the application successfully
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3)Promotion banners are created in Sitecore
        PRECONDITIONS: 4)User has enabled Club toggle in Fanzone page
        PRECONDITIONS: 5)User has created promotion in club subsection in Fanzone
        PRECONDITIONS: 5)User has FE url and Valid credentials to Login Lads FE
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(),
                                           typeId=str(self.ob_config.football_config.autotest_class.autotest_premier_league.type_id))

        fanzone_clubs = self.cms_config.get_fanzone_club()
        self.__class__.fanzoneclub = []
        for fanzone_club in fanzone_clubs:
            if (fanzone_club['validityPeriodStart'] <= datetime.utcnow().isoformat() <= fanzone_club['validityPeriodEnd']) and fanzone_club['active'] is True:
                self.fanzoneclub.append(fanzone_club)
        if self.fanzoneclub is None:
            raise CmsClientException('fanzone promotions are not available')
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['fanzoneConfiguration']['showClubs'] is not True:
            raise CmsClientException('showClubs is not enabled')
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state('Homepage')
        self.site.login(username=username)
        self.navigate_to_page(name='sport/football', fanzone=True)
        self.site.wait_content_state(state_name='Football')
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
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.get(
                vec.racing.RACING_HIGHLIGHTS_TAB_NAME).click()
        self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")
        fanzone_banner = self.site.home.fanzone_banner()
        fanzone_banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=10,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_001_navigate_to_fanzone_page(self):
        """
        DESCRIPTION: Navigate to Fanzone page
        EXPECTED: User should be navigated to Fanzone page
        """
        # covered in above step

    def test_002_verify_user_is_able_to_see_club_tab_in_fanzone_page(self):
        """
        DESCRIPTION: Verify user is able to see Club Tab in Fanzone page
        EXPECTED: User should be able to see Club Tab in Fanzone page
        """
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.CLUB, tabs_menu,
                      msg=f'"{vec.fanzone.CLUB}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.CLUB)

    def test_003_verify_the_promotion_in_club_page(self):
        """
        DESCRIPTION: Verify the promotion in Club page
        EXPECTED: User should be able to see the created promotions in FE under club tab with below data:
        EXPECTED: 1)Promotion Banner
        EXPECTED: 2)Promotion Title
        EXPECTED: 3)Promotion details
        EXPECTED: 4)CTA button
        """
        fanzone_banners = self.site.fanzone.tab_content.club_container
        for i in range(len(self.fanzoneclub)):
            self.assertTrue(fanzone_banners.get(self.fanzoneclub[i]['title']).name,
                            msg=f'banner name is not displayed in promotions')
            self.assertTrue(fanzone_banners.get(self.fanzoneclub[i]['title']).banner,
                            msg='banner link is not displayed')

    def test_004_login_to_cms_and_navigate_to_fanzonegtgtclub_page_and_make_1_2_promotions_active_and_save_the_changes(self):
        """
        DESCRIPTION: Login to CMS and navigate to Fanzone&gt;&gt;Club page and make 1-2 promotions active and save the changes
        EXPECTED: User should be able to login successfully and is able to make some of the promotions inactive in CMS
        """
        # Cannot automate as we don't have access to sitecore to get the banner id's

    def test_005_login_to_fe_and_navigate_to_fanzone_page(self):
        """
        DESCRIPTION: Login to FE and navigate to Fanzone page
        EXPECTED: User should be able to login to FE successfully
        """
        # Cannot automate

    def test_006_verify_only_active_promotions_are_displayed_in_fanzone_page(self):
        """
        DESCRIPTION: Verify only active promotions are displayed in Fanzone page
        EXPECTED: User should be able to see only active promotions in FE, the promotions which are inactive will not be shown in FE
        """
        # Cannot automate