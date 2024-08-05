import tests
import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305104_Verify_GA_tracking_on_launching_the_Fanzone_page(BaseDataLayerTest):
    """
    TR_ID: C65305104
    NAME: Verify GA tracking on launching the Fanzone page
    DESCRIPTION: This test case is to verify GA tracking on launching the Fanzone page
    PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC Entry points in front end
    PRECONDITIONS: 2) User has subscribed to Fanzone
    PRECONDITIONS: 3) User should be logged in state
    """
    keep_browser_open = True
    expected_response = {'event': 'content-view', 'screen_name': '/fanzone/sport-football/ManCity/now-next'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Active the fanzone team and register a new user
        EXPECTED: Fanzone team is activated in cms and logged into the application
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        manchesterCity_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.manchester_city.title())
        if manchesterCity_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.manchester_city.title(),
                                           typeId=self.football_config.autotest_class.autotest_premier_league.type_id)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='SYC is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.manchester_city.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.manchester_city.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_launch_application_and_click_on_any_fanzone_entry_point(self):
        """
        DESCRIPTION: Launch application and click on any fanzone entry point
        EXPECTED: User should be navigate to fanzone page
        """
        self.navigate_to_page(name=tests.HOSTNAME)
        self.site.wait_content_state(state_name='HomePage')
        if self.device_type == 'mobile':
            # Top Sports
            self.site.open_sport(name='ALL SPORTS')
            self.__class__.sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
            self.assertIn('Fanzone', self.sports, msg='Fanzone is present in Top Sports')
        else:
            # A - Z Sports
            self.__class__.sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertIn('Fanzone', self.sports, msg='Fanzone is present in A-Z Sports')
        self.sports.get(vec.sb.FANZONE).click()

    def test_002_check_ga_tracking_after_loading_syc_page(self):
        """
        DESCRIPTION: Check GA tracking after loading SYC page
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "content-view",
        EXPECTED: "screen_name": &lt;Page URI&gt;, //e.g. "/sport/football/fanzone/{TeamName}/now-and-next"
        EXPECTED: })
        """
        actual_response = self.get_data_layer_specific_object(object_key='event', object_value='content-view')
        self.compare_json_response(actual_response, self.expected_response)
