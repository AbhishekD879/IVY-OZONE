import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from time import sleep


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.fanzone
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C65305025_Verify_user_is_populated_with_Fanzone_as_per_the_team_selection_made_in_SYC_page(Common):
    """
    TR_ID: C65305025
    NAME: Verify user is populated with Fanzone as per the team selection made in SYC page
    DESCRIPTION: Verify user is populated with Fanzone as per the team selection made in SYC page
    PRECONDITIONS: 1) User login should be successful
    PRECONDITIONS: 2) User has already subscribed for Fanzone
    PRECONDITIONS: 3) Fanzone should be enabled in System Configuration
    PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 4) All the entry points should be enabled in Fanzone Configuration(CMS)
    PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
    PRECONDITIONS: 5) Image should be uploaded in Site core and image id should be inputted while creating the Fanzone for respective teams
    PRECONDITIONS: 6) Fanzone should be enabled in A-Z menu and Sports Ribbon
    PRECONDITIONS: CMS-->Sports Pages-->Sport Categories-->Fanzone-->General Sport Configuration
    """
    keep_browser_open = True

    def test_000_precondition(self):
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        self.__class__.aston_villa = vec.fanzone.TEAMS_LIST.aston_villa.title()
        astonVilla_fanzone = self.cms_config.get_fanzone(self.aston_villa)
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state('Homepage')
        self.site.login(username=username)
        self.site.open_sport('football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Teams to be displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams.get(self.aston_villa).scroll_to_we()
        teams.get(self.aston_villa).click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(6)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_navigate_promotions_page(self):
        """
        DESCRIPTION: Navigate Promotions page
        EXPECTED: User should be able to navigate to Promotions Page
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state('Promotions')

    def test_002_search_for_show_your_colors_promo_and_click_on_see_more(self):
        """
        DESCRIPTION: Search for Show Your Colors Promo and click on see more
        EXPECTED: Should be able to navigate to Show Your colors page
        """
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        promo = promotions[vec.fanzone.PROMOTION_TITLE]
        promo.more_info_button.click()
        # self.site.wait_content_state(state_name='PromotionDetails')
        promotion_details = self.site.promotion_details.tab_content.promotion
        fz_syc_button = promotion_details.detail_description.fanzone_syc_button
        fz_syc_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')

    def test_003_check_for_the_fanzoneteam_which_user_has_already_subscribed(self):
        """
        DESCRIPTION: Check for the Fanzone(Team) which user has already subscribed
        EXPECTED: User should be displayed with already subscribed team
        """
        aston_villa = self.site.show_your_colors.items_as_ordered_dict.get(self.aston_villa)
        self.assertTrue(aston_villa.is_highlighted(), msg=f'previously subscribed team {aston_villa} is not highlighted')

    def test_004_navigate_to_fanzone_page_by_clicking_on_any_of_the_entry_points(self):
        """
        DESCRIPTION: Navigate to Fanzone page by clicking on any of the entry points
        EXPECTED: User should be navigated to Fanzone Page
        """
        self.navigate_to_page('homepage')
        banner = self.site.home.fanzone_banner()
        banner.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')

    def test_005_user_is_displayed_with_the_fanzone_he_has_opted_for(self):
        """
        DESCRIPTION: User is displayed with the Fanzone he has opted for
        EXPECTED: User should be displayed with the Fanzone he has opted through SYC
        """
        team_name = self.site.fanzone.fanzone_heading
        self.assertIn(self.aston_villa, team_name, msg=f'Actual team name "{team_name}" is not same as expected'
                                                       f'team name "{self.aston_villa}"')
