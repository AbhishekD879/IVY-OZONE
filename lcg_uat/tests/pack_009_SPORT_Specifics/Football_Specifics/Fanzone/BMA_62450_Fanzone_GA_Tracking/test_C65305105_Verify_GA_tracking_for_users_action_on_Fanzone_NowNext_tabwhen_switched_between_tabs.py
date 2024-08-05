import pytest
from tests.base_test import vtest
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result, wait_for_haul
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_h1
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone_reg_tests
@pytest.mark.desktop
@vtest
class Test_C65305105_Verify_GA_tracking_for_users_action_on_Fanzone_NowNext_tabwhen_switched_between_tabs(BaseDataLayerTest):
    """
    TR_ID: C65305105
    NAME: Verify GA tracking for users action on Fanzone NowNext tab when switched between tabs
    DESCRIPTION: This test case is to verify GA tracking for user's action on Fanzone Now&Next tab when switched between tabs
    PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC Entry points in front end
    PRECONDITIONS: 2) Create fanzone tabs: now&next, stats and clubs
    PRECONDITIONS: 3) User has subscribed to Fanzone
    PRECONDITIONS: 4) User should be logged in state
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC Entry points in front end
        PRECONDITIONS: 2) Create fanzone tabs: now&next, stats and clubs
        PRECONDITIONS: 3) User has subscribed to Fanzone
        PRECONDITIONS: 4) User should be logged in state
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
        results = wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict, timeout=30,
                                  name='All Teams to be displayed')
        self.assertTrue(results, msg='Teams are not displayed')
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        wait_for_result(lambda: dialog_confirm.confirm_button.is_displayed(), timeout=10,
                        name='"CONFIRM" button to be displayed.')
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        wait_for_result(lambda: dialog_alert.exit_button.is_displayed(), timeout=5,
                        name='"EXIT" button to be displayed.')
        dialog_alert.exit_button.click()

    def test_001_launch_application_and_click_on_any_fanzone_entry_point(self):
        """
        DESCRIPTION: Launch application and click on any fanzone entry point
        EXPECTED: User should be navigated to fanzone now&next tab
        """
        # fanzone_banner = self.site.home.fanzone_banner() as per the new change, after subscription, we will be in fanzone page only
        # fanzone_banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_002_check_ga_tracking(self):
        """
        DESCRIPTION: Check GA tracking
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "tab",
        EXPECTED: "eventCategory": "fanzone",
        EXPECTED: "eventLabel": "now & next"
        EXPECTED: })
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "content-view",
        EXPECTED: "screen_name": &lt;Page URI&gt;, //e.g. "/sport/football/fanzone/{TeamName}/now & next"
        EXPECTED: })
        """
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value='fanzone')
        expected_response = {"event": "trackEvent",
                             "eventAction": "tab",
                             "eventCategory": "fanzone",
                             "eventLabel": "NOW & NEXT"
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_003_click_stats_tab_and_check_ga_tracking(self):
        """
        DESCRIPTION: Click STATS tab and check GA tracking
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "tab",
        EXPECTED: "eventCategory": "fanzone",
        EXPECTED: "eventLabel": "stats"
        EXPECTED: })
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "content-view",
        EXPECTED: "screen_name": &lt;Page URI&gt;, //e.g. "/sport/football/fanzone/{TeamName}/stats"
        EXPECTED: })
        """
        # Right Now, Stats Tab is in disabled due to no data available for stats.
        # In future,If we get data for stats we can uncomment it.
        # tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        # self.assertIn(vec.fanzone.STATS, tabs_menu,
        #               msg=f'"{vec.fanzone.STATS}" tab is not present in tabs menu')
        # self.site.fanzone.tabs_menu.click_button(button_name='STATS')
        #
        # actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='tab')
        # expected_response = {"event": "trackEvent",
        #                      "eventAction": "tab",
        #                      "eventCategory": "fanzone",
        #                      "eventLabel": "STATS"
        #                      }
        # self.compare_json_response(actual_response, expected_response)

    def test_004_click_on_clubs_tab_and_check_ga_tracking(self):
        """
        DESCRIPTION: Click on CLUBS tab and check GA tracking
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "tab",
        EXPECTED: "eventCategory": "fanzone",
        EXPECTED: "eventLabel": "club"
        EXPECTED: })
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "content-view",
        EXPECTED: "screen_name": &lt;Page URI&gt;, //e.g. "/sport/football/fanzone/{TeamName}/club"
        EXPECTED: })
        """
        dialog_alert_email = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_EMAIL_OPT_IN)
        if dialog_alert_email:
            dialog_alert_email.remind_me_later.click()
            wait_for_haul(3)

        dialog_alert_fanzone_game = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES)
        if dialog_alert_fanzone_game:
            dialog_alert_fanzone_game.close_btn.click()

        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.CLUB, tabs_menu,
                      msg=f'"{vec.fanzone.CLUB}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name='CLUB')

        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='tab')
        expected_response = {"event": "trackEvent",
                             "eventAction": "tab",
                             "eventCategory": "fanzone",
                             "eventLabel": "CLUB"
                             }
        self.compare_json_response(actual_response, expected_response)
