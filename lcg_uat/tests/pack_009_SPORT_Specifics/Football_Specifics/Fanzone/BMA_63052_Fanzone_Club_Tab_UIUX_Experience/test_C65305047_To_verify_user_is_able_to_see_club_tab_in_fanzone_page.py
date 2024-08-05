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
class Test_C65305047_To_verify_user_is_able_to_see_club_tab_in_fanzone_page(Common):
    """
    TR_ID: C65305047
    NAME: To verify user is able to see club tab in fanzone page
    DESCRIPTION: To verify user is able to see club tab in fanzone page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)User has enabled Club toggle in Fanzone page
    PRECONDITIONS: 4)Promotion banners are created in Sitecore
    PRECONDITIONS: 5)User has created promotion in club subsection in Fanzone
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
        PRECONDITIONS: 5)User has FE url and Valid credentials to Login Lads FE
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)

        fanzone_clubs = self.cms_config.get_fanzone_club()
        fanzoneclub = []
        for fanzone_club in fanzone_clubs:
            if (fanzone_club['validityPeriodStart'] <= datetime.datetime.utcnow().isoformat() <= fanzone_club['validityPeriodEnd']) and fanzone_club['active'] is True:
                fanzoneclub.append(fanzone_club)
        if len(fanzoneclub) is 0:
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
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_teamalert.exit_button.click()
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")
        if tests.settings.device_type == "mobile":
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.get(
                vec.racing.RACING_HIGHLIGHTS_TAB_NAME).click()
        fanzone_banner = self.site.home.fanzone_banner()
        self.assertTrue(fanzone_banner, msg="Fanzone banner is not displayed")
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
