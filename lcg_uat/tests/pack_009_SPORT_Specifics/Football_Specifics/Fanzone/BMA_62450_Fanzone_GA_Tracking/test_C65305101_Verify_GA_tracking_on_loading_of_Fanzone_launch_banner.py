import pytest
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from time import sleep


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_h1
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.other
@pytest.mark.fanzone
@vtest
class Test_C65305101_Verify_GA_tracking_on_loading_of_Fanzone_launch_banner(BaseDataLayerTest):
    """
    TR_ID: C65305101
    NAME: Verify GA tracking on loading of Fanzone launch banner
    DESCRIPTION: This test case is to verify GA tracking on loading of Fanzone launch banner
    PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC banner in front end
    PRECONDITIONS: 2) User has subscribed to Fanzone (ex: Man United)
    PRECONDITIONS: 3) User should be logged in state
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC Entry points in front end
        PRECONDITIONS: 2) User has subscribed to Fanzone
        PRECONDITIONS: 3) User should be logged in state
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(),
                                           typeId=str(self.football_config.autotest_class.autotest_premier_league.type_id))
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=self.username)
        self.site.open_sport(name='Football', fanzone=True)
        self.__class__.dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        self.dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Fanzones are displayed',
                        timeout=5)
        fanzone = self.site.show_your_colors.items_as_ordered_dict
        for fanzoneteam in fanzone.values():
            if fanzoneteam.name == vec.fanzone.TEAMS_LIST.aston_villa.title():
                sleep(2)
                fanzoneteam.click()
                break
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_teamalert.exit_button.click()

    def test_001_user_launches_application(self):
        """
        DESCRIPTION: User launches application
        EXPECTED: User should be in home page
        """
        if self.device_type == 'mobile':
            self.site.navigation_menu.click_item(vec.sb.HOME)
        else:
            self.site.header.sport_menu.items_as_ordered_dict['HOME'].click()
        sleep(5)
        self.site.wait_content_state(state_name='HomePage')

    def test_002_check_ga_tracking_after_loading_syc_banner(self):
        """
        DESCRIPTION: Check GA tracking after loading SYC banner
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "entry banner",
        EXPECTED: "eventCategory": "fanzone",
        EXPECTED: "eventLabel": "render"
        EXPECTED: "eventDetails": "Man United"
        EXPECTED: })
        """
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict['Fanzone'].click()
        else:
            self.site.header.sport_menu.items_as_ordered_dict['FANZONE'].click()
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value="entry banner")
        expected_response = {'event': "trackEvent",
                             'eventAction': "entry banner",
                             'eventCategory': "fanzone",
                             'eventDetails': vec.fanzone.TEAMS_LIST.aston_villa.title(),
                             'eventLabel': "render"
                             }
        self.compare_json_response(actual_response, expected_response)
