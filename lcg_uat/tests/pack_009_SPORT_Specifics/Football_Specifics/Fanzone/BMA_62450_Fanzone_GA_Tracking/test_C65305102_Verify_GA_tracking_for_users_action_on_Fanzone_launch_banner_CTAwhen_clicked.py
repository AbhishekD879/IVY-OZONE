import tests
import voltron.environments.constants as vec
import pytest
from crlat_siteserve_client.utils.exceptions import SiteServeException
from time import sleep
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.lad_stg2
# @pytest.mark.lad_h1
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.other
@pytest.mark.fanzone_reg_tests
@vtest
class Test_C65305102_Verify_GA_tracking_for_users_action_on_Fanzone_launch_banner_CTAwhen_clicked(BaseDataLayerTest):
    """
    TR_ID: C65305102
    NAME: Verify GA tracking for user's action on Fanzone launch banner CTA(when clicked)
    DESCRIPTION: This test case is to verify GA tracking for user's action on Fanzone launch banner CTA(when clicked)
    PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC banner in front end
    PRECONDITIONS: 2) User has subscribed to Fanzone (ex: Man United)
    PRECONDITIONS: 3) User should be logged in stateh
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC Entry points in front end
        PRECONDITIONS: 2) User has subscribed to Fanzone
        PRECONDITIONS: 3) User should be logged in state
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if tests.settings.backend_env == 'prod':
            if not fanzone_status.get('enabled'):
                if 'beta' in tests.HOSTNAME:
                    self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                          field_name='enabled',
                                                                          field_value=True)
                else:
                    raise SiteServeException(f'Fanzone is not enabled for "{tests.HOSTNAME}"')
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
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
        fanzone[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        fanzone[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        wait_for_haul(3)
        dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_teamalert.exit_button.click()
        wait_for_haul(3)
        dialog_alert_email = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_EMAIL_OPT_IN)
        if dialog_alert_email:
            dialog_alert_email.remind_me_later.click()
        wait_for_haul(3)

        dialog_alert_fanzone_game = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES)
        if dialog_alert_fanzone_game:
            dialog_alert_fanzone_game.close_btn.click()

    def test_001_user_launches_application(self):
        """
        DESCRIPTION: User launches application
        EXPECTED: User should be in home page and displays SYC banner
        """
        if self.device_type == 'mobile':
            self.site.navigation_menu.click_item(vec.sb.HOME)
        else:
            self.site.header.sport_menu.items_as_ordered_dict['HOME'].click()
        sleep(5)
        self.site.wait_content_state(state_name='HomePage')

    def test_002_click_on_let_me_see_button_in_banner(self):
        """
        DESCRIPTION: Click on LET ME SEE button in banner
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "entry banner",
        EXPECTED: "eventCategory": "fanzone",
        EXPECTED: "eventLabel": "click"
        EXPECTED: "eventDetails": "Man United"
        EXPECTED: })
        """
        if self.device_type == 'mobile' and (not self.site.home.fanzone_banner()):
            tabs = self.site.home.tabs_menu.items_as_ordered_dict
            list(tabs.values())[0].click()
        fanzone_banner = wait_for_result(self.site.home.fanzone_banner, timeout=15, name='SYC banner to be displayed')
        #fanzone_banner.let_me_see.click()
        fanzone_banner.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=10,
                        name='"Fanzone tab menus" to be displayed.')
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value="entry banner")
        expected_response = {'event': "trackEvent",
                             'eventAction': "entry banner",
                             'eventCategory': "fanzone",
                             'eventDetails': vec.fanzone.TEAMS_LIST.aston_villa.title(),
                             'eventLabel': "click"
                             }
        self.compare_json_response(actual_response, expected_response)
