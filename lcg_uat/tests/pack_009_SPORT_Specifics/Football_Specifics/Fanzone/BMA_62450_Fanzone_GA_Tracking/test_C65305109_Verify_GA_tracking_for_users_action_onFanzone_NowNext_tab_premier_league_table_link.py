import pytest
import tests
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result, wait_for_haul
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_tst2
# @pytest.mark.lad_hl   # not configured in prod and Beta
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone_reg_tests
@vtest
class Test_C65305109_Verify_GA_tracking_for_users_action_onFanzone_NowNext_tab_premier_league_table_link(BaseDataLayerTest):
    """
    TR_ID: C65305109
    NAME: Verify GA tracking for user's action on Fanzone Now&Next tab premier league table link
    DESCRIPTION: This test case is to verify GA tracking for user's action on Fanzone Now&Next tab: premier league table link
    PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC Entry points in front end
    PRECONDITIONS: 2) Create fanzone tabs: now&next, stats and clubs
    PRECONDITIONS: 3) Create surface bets, HC and outrights data for fanzone
    PRECONDITIONS: 4) User has subscribed to Fanzone
    PRECONDITIONS: 5) User should be logged in state
    """
    keep_browser_open = True

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC Entry points in front end
        PRECONDITIONS: 2) Create fanzone tabs: now&next, stats and clubs
        PRECONDITIONS: 3) Create surface bets, HC and outrights data for fanzone
        PRECONDITIONS: 4) User has subscribed to Fanzone
        PRECONDITIONS: 5) User should be logged in state
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
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
        wait_for_haul(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()
        wait_for_haul(3)
        dialog_alert_email = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_EMAIL_OPT_IN)
        if dialog_alert_email:
            dialog_alert_email.remind_me_later.click()
        wait_for_haul(3)

        dialog_alert_fanzone_game = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES)
        if dialog_alert_fanzone_game:
            dialog_alert_fanzone_game.close_btn.click()

    def test_001_launch_application_and_click_on_any_fanzone_entry_point(self):
        """
        DESCRIPTION: Launch application and click on any fanzone entry point
        EXPECTED: User should be navigated to fanzone now&next tab
        """
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")
        if tests.settings.device_type == "mobile":
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.get('HIGHLIGHTS').click()
        self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")
        fanzone_banner = self.site.home.fanzone_banner()
        fanzone_banner.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu.current,
                        name='Fanzone page not displayed',
                        timeout=5)
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_002_navigate_to_premier_league_table_link_and_click_on_itand_check_ga_tracking(self):
        """
        DESCRIPTION: Navigate to Premier League Table Link and click on it
        DESCRIPTION: and check GA tracking
        EXPECTED: The tag should be contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "league table",
        EXPECTED: "eventCategory": "in-line stats",
        EXPECTED: "eventLabel": "Premier League"
        EXPECTED: "categoryID": "16"
        EXPECTED: "typeID": "442"
        EXPECTED: })
        """
        click(self.site.fanzone.premier_leauge_link)
        wait_for_haul(5)
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel',
                                                              object_value='Premier League')
        expected_response = {
            "event": "trackEvent",
            "eventAction": "league table",
            "eventCategory": "in-line stats",
            "eventLabel": "Premier League",
            "categoryID": "16",
            "typeID": "442"
        }
        self.compare_json_response(actual_response, expected_response)


