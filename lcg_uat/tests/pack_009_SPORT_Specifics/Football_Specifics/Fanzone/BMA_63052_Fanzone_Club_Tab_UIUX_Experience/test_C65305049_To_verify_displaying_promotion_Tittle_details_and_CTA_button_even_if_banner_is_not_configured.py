import datetime
import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from time import sleep


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305049_To_verify_displaying_promotion_Tittle_details_and_CTA_button_even_if_banner_is_not_configured(Common):
    """
    TR_ID: C65305049
    NAME: To verify displaying promotion Tittle, details and CTA button even if banner is not configured
    DESCRIPTION: To verify displaying promotion Tittle, details and CTA button even if banner is not configured
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)Promotion banners are created in Sitecore
    PRECONDITIONS: 4)User has enabled Club toggle in Fanzone page
    PRECONDITIONS: 5)User has created promotion in club subsection in Fanzone
    PRECONDITIONS: Promotion Banner(From Sitecore) Is not configured , other fields are configured:
    PRECONDITIONS: a)Promotion Title
    PRECONDITIONS: b)Promotion details
    PRECONDITIONS: c)CTA button
    PRECONDITIONS: 6)User has FE url and Valid credentials to Login Lads FE
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3)Promotion banners are created in Sitecore
        PRECONDITIONS: 4)User has enabled Club toggle in Fanzone page
        PRECONDITIONS: 5)User has created promotion in club subsection in Fanzone
        PRECONDITIONS: Promotion Banner(From Sitecore) Is not configured , other fields are configured:
        PRECONDITIONS: a)Promotion Title
        PRECONDITIONS: b)Promotion details
        PRECONDITIONS: c)CTA button
        PRECONDITIONS: 6)User has FE url and Valid credentials to Login Lads FE
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)

        fanzone_clubs = self.cms_config.get_fanzone_club()
        self.__class__.fanzoneclub = []
        for fanzone_club in fanzone_clubs:
            if (fanzone_club['validityPeriodStart'] <= datetime.datetime.utcnow().isoformat() <= fanzone_club[
                'validityPeriodEnd']) and fanzone_club['active'] is True:
                self.fanzoneclub.append(fanzone_club)
        if len(self.fanzoneclub) is 0:
            raise CmsClientException('fanzone promotions are not available')
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['fanzoneConfiguration']['showClubs'] is not True:
            raise CmsClientException('showClubs is not enabled')
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='Football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Fanzones are displayed',
                        timeout=5)
        fanzone = self.site.show_your_colors.items_as_ordered_dict
        fanzone[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        sleep(5)
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

    def test_001_navigate_to_fanzone_page(self):
        """
        DESCRIPTION: Navigate to Fanzone page
        EXPECTED: User should be navigated to Fanzone page
        """
        self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")
        fanzone_banner = self.site.home.fanzone_banner()
        fanzone_banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=10,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_002_verify_user_is_able_to_see_club_tab_in_fanzone_page(self):
        """
        DESCRIPTION: Verify user is able to see Club Tab in Fanzone page
        EXPECTED: User should be able to see Club Tab in Fanzone page
        """
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.CLUB, tabs_menu,
                      msg=f'"{vec.fanzone.CLUB}" tab is not present in tabs menu')

    def test_003_verify_the_promotion_in_club_page(self):
        """
        DESCRIPTION: Verify the promotion in Club page
        EXPECTED: User should be able to see the created promotions in FE under club tab with below data:
        EXPECTED: 1)Promotion Title
        EXPECTED: 2)Promotion details
        EXPECTED: 3)CTA button
        """
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.CLUB)
        fanzone_banners = self.site.fanzone.tab_content.club_container
        for i in range(len(self.fanzoneclub)):
            self.assertTrue(fanzone_banners.get(self.fanzoneclub[i]['title']).name,
                            msg=f'banner name is not displayed in promotions')
            self.assertTrue(fanzone_banners.get(self.fanzoneclub[i]['title']).banner,
                            msg='banner link is not displayed')
