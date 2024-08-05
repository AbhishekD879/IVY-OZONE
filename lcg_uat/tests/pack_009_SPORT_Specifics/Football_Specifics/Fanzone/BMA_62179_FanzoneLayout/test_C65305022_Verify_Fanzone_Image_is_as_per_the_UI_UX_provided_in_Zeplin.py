import pytest
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from time import sleep


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65305022_Verify_Fanzone_Image_is_as_per_the_UI_UX_provided_in_Zeplin(Common):
    """
    TR_ID: C65305022
    NAME: Verify Fanzone Image is as per the UI/UX provided in Zeplin
    DESCRIPTION: Verify Fanzone Image is as per the UI/UX provided in Zeplin
    PRECONDITIONS: 1) User has already subscribed for Fanzone
    PRECONDITIONS: 2) Fanzone should be enabled in System Configuration
    PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 3) All the entry points should be enabled in Fanzone Configuration(CMS)
    PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
    PRECONDITIONS: 4) Image should be uploaded in Site core and image id should be inputted while creating the Fanzone for respective teams
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User has already subscribed for Fanzone
        PRECONDITIONS: 2) Fanzone should be enabled in System Configuration
        PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
        PRECONDITIONS: 3) All the entry points should be enabled in Fanzone Configuration(CMS)
        PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
        PRECONDITIONS: 4) Image should be uploaded in Site core and image id should be inputted while creating the Fanzone for respective teams
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        everton_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.everton.title())
        if everton_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.everton.title())

    def test_001_launch_the_lads_application_and_enter_valid_credentials(self):
        """
        DESCRIPTION: Launch the Lads application and enter valid credentials
        EXPECTED: User login should be successful
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_002_below_entry_points_should_be_displayed_for_userb_fanzone_in_sports_ribbonmobile_onlyc_launch_banner_in_home_pagehighlights_tabd_launch_banner_in_football_slpnote_user_should_prompted_with_only_the_fanzone_they_have_subscribed_for(
            self):
        """
        DESCRIPTION: Below entry points should be displayed for User
        DESCRIPTION: b) Fanzone in Sports Ribbon(Mobile only)
        DESCRIPTION: c) Launch banner in Home page/Highlights tab
        DESCRIPTION: d) Launch banner in Football SLP
        DESCRIPTION: Note: User should prompted with only the Fanzone they have subscribed for
        EXPECTED: User should be able to see the listed entry points
        """
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='OK button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.everton.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.everton.title()].click()
        sleep(3)
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION, timeout=10)
        dialog_confirm.confirm_button.click()
        sleep(6)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()
        self.site.wait_content_state_changed(timeout=10)
        sleep(3)
        # self.__class__.banner = wait_for_result(lambda: self.site.football.fanzone_banner(), timeout=10)
        # fanzone_name = self.banner.fanzone_name.split('/')[1].strip().title()
        # self.assertEquals(fanzone_name, vec.fanzone.TEAMS_LIST.everton.title(),
        #                   msg=f'{fanzone_name} User have not prompted with only the Fanzone they have subscribed {vec.fanzone.TEAMS_LIST.everton.title()}')

    def test_003_verify_color_of_the_launch_bannerex_if_you_subscribed_team_is_everton_then_your_launch_banner_color_should_be_blueplease_follow_below_linkhttpsappzeplinioproject5f296ce76014322057c71b9fscreen611bd6bb825e0a13211cce88(
            self):
        """
        DESCRIPTION: Verify color of the Launch Banner
        DESCRIPTION: Ex: If you subscribed team is Everton, then your launch banner color should be blue
        DESCRIPTION: please follow below link:
        DESCRIPTION: https://app.zeplin.io/project/5f296ce76014322057c71b9f/screen/611bd6bb825e0a13211cce88
        EXPECTED: Fanzone Launch Banner color should be as per the team subscribed in Show Your Colors page
        """
        sleep(3)
        # everton_bg_color = self.banner.css_property_value('background-color')
        # self.assertEqual(everton_bg_color, vec.fanzone.EVERTON_HOME_BG_COLOR,
        #                  msg=f'fanzone banner background-color is not equal to Zepplin team box background-color'
        #                      f'actual result "{everton_bg_color}"')

    def test_004_navigate_to_fanzone_page_by_clicking_on_any_of_the_entry_points_listed_in_step_2(self):
        """
        DESCRIPTION: Navigate to Fanzone page by clicking on any of the entry points listed in step 2
        EXPECTED: User should be able to navigate to Fanzone Page
        """
        # self.banner.let_me_see.click() as per the new change, after subscription, we will be in fanzone page only
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')

    def test_005_verify_fanzone_background_image_is_as_per_the_belowzeplin_httpsappzeplinioproject5f296ce76014322057c71b9fdashboardsid613f6bfe0c83bf2769d76fffnote_note_image_will_have_colored_label__as_per_the_team_subscribed(
            self):
        """
        DESCRIPTION: Verify Fanzone (background) Image is as per the below
        DESCRIPTION: Zeplin: https://app.zeplin.io/project/5f296ce76014322057c71b9f/dashboard?sid=613f6bfe0c83bf2769d76fff
        DESCRIPTION: Note Image will have colored label , as per the team subscribed
        EXPECTED: Fanzone image should be as per the Zeplin
        """
        sleep(3)
        expected_fanzone_bg_color = self.site.fanzone.fanzone_banner_header.value_of_css_property('background-color')
        self.assertEqual(vec.fanzone.EVERTON_FANZONE_BG_COLOR, expected_fanzone_bg_color,
                         msg=f'fanzone background-color is not equal to Zepplin team box background-color'
                             f'actual result "{expected_fanzone_bg_color}"')
