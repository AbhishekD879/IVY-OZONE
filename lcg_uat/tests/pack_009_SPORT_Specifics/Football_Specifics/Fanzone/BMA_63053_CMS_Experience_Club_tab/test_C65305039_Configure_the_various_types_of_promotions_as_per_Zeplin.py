import pytest
import datetime
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C65305039_Configure_the_various_types_of_promotions_as_per_Zeplin(Common):
    """
    TR_ID: C65305039
    NAME: Configure the various types of promotions as per Zeplin
    DESCRIPTION: Configure the various types of promotions as per Zeplin
    PRECONDITIONS: 1) User has logged into CMS
    PRECONDITIONS: 2) Fanzone records should be created
    PRECONDITIONS: 3) User is in Club Page
    PRECONDITIONS: 4) Image Banner should be configured in Sitecore
    PRECONDITIONS: 5) Fanzone should be enabled in System Configuration
    PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 6) Toggle should be On for all the Entry points listed in Fanzone Configuration(CMS)
    PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User has logged into CMS
        PRECONDITIONS: 2) Fanzone records should be created
        PRECONDITIONS: 3) User is in Club Page
        PRECONDITIONS: 4) Image Banner should be configured in Sitecore
        PRECONDITIONS: 5) Fanzone should be enabled in System Configuration
        PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
        PRECONDITIONS: 6) Toggle should be On for all the Entry points listed in Fanzone Configuration(CMS)
        PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)

        fanzone_clubs = self.cms_config.get_fanzone_club()
        self.__class__.fanzoneclub = []
        for fanzone_club in fanzone_clubs:
            if (fanzone_club['validityPeriodStart'] <= datetime.datetime.utcnow().isoformat() <= fanzone_club['validityPeriodEnd']) and fanzone_club['active'] is True:
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
        self.site.wait_content_state(state_name='Football', timeout=20)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Fanzones are displayed',
                        timeout=10)
        fanzone = self.site.show_your_colors.items_as_ordered_dict
        fanzone[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION, verify_name=False)
        dialog_confirm.confirm_button.click()
        sleep(6)
        dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS, verify_name=False)
        dialog_teamalert.exit_button.click()
        sleep(4)
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=10,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_001_click_on_club(self):
        """
        DESCRIPTION: Click on Club
        EXPECTED: Club Page should be opened
        """
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.CLUB, tabs_menu,
                      msg=f'"{vec.fanzone.CLUB}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.CLUB)

    def test_002_click_on_create_promotion_button(self):
        """
        DESCRIPTION: Click on create promotion Button
        EXPECTED: Create promotion page should be displayed
        """
        #  covered in step4

    def test_003_configure_various_types_of_promotions_like_promotion_banner_club_dataexcel_tables_and_dynamic_price_buttons_for_any_bet_ctas(self):
        """
        DESCRIPTION: Configure Various types of promotions like Promotion Banner, Club data(excel tables) and Dynamic price buttons for any bet CTA'S
        EXPECTED: Should be able to configure all the promotion's
        """
        #  covered in step4

    def test_004_validate_the_promotions_in_frontend(self):
        """
        DESCRIPTION: Validate the promotion's in Frontend
        EXPECTED: All the configured promotions should be displayed in Frontend
        """
        fanzone_banners = self.site.fanzone.tab_content.club_container
        for i in range(len(self.fanzoneclub)):
            self.assertTrue(fanzone_banners.get(self.fanzoneclub[i]['title']).name,
                            msg=f'banner name is not displayed in promotions')
            self.assertTrue(fanzone_banners.get(self.fanzoneclub[i]['title']).banner,
                            msg='banner link is not displayed')
