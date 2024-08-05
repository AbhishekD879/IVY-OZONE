import pytest
import tests
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
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65305100_Verify_GA_tracking_for_users_action_onSports_ribbon_fanzone_entry_pointwhen_clicked(BaseDataLayerTest):
    """
    TR_ID: C65305100
    NAME: Verify GA tracking for user's action onÂ Sports ribbon fanzone entry point(when clicked)
    DESCRIPTION: This test case is to verify GA tracking for user's action on Sports ribbon fanzone entry point(when clicked)
    PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC Entry points in front end
    PRECONDITIONS: 2) User has subscribed to Fanzone
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
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.chelsea.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.chelsea.title())
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=self.username)
        self.site.open_sport(name='Football', fanzone=True)
        self.__class__.dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        self.dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Fanzones are displayed',
                        timeout=5)
        fanzone = self.site.show_your_colors.items_as_ordered_dict
        fanzone[vec.fanzone.TEAMS_LIST.chelsea.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
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
            self.site.header.sport_menu.items_as_ordered_dict[vec.sb.HOME].click()
        self.site.wait_content_state(state_name='HomePage')

    def test_002_click_on_fanzone_entry_point_and_check_ga_tracking(self):
        """
        DESCRIPTION: Click on Fanzone entry point and check GA tracking
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "main",
        EXPECTED: "eventCategory": "navigation",
        EXPECTED: "eventLabel": "Fanzone", //e.g.
        EXPECTED: "position": &lt;Position&gt; //e.g. "1", "2" or "3"
        EXPECTED: })
        """
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict[vec.sb.FANZONE].click()
        else:
            self.site.header.sport_menu.items_as_ordered_dict[vec.sb.FANZONE.upper()].click()
        sleep(3)
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value="main")
        if self.device_type != 'mobile':
            expected_response = {'event': "trackEvent",
                                 'eventAction': "main",
                                 'eventCategory': "navigation",
                                 'eventDetails': "a-z betting",
                                 'eventLabel': "Fanzone"
                                 }
        else:
            if tests.settings.backend_env == 'prod':
                expected_response = {"event": "trackEvent",
                                     "eventCategory": "navigation",
                                     "eventAction": "main",
                                     "eventLabel": "Fanzone",
                                     }

            else:
                expected_response = {"event": "trackEvent",
                                     "eventCategory": "navigation",
                                     "eventAction": "main",
                                     "eventLabel": "Fanzone",
                                     "dimension94": 4
                                     }
        self.assertEqual(expected_response.get("event"), actual_response.get("event"),
                         msg=f'Expected event value "{expected_response.get("event")}" is not '
                             f'same as actual event value "{actual_response.get("event")}"')
        self.assertEqual(expected_response.get("eventCategory"), actual_response.get("eventCategory"),
                         msg=f'Expected eventCategory value "{expected_response.get("eventCategory")}" is not '
                             f'same as actual eventCategory value "{actual_response.get("eventCategory")}"')
        self.assertEqual(expected_response.get("eventAction"), actual_response.get("eventAction"),
                         msg=f'Expected eventAction value "{expected_response.get("eventAction")}" is not '
                             f'same as actual eventAction value "{actual_response.get("eventAction")}"')
        self.assertEqual(expected_response.get("eventLabel"), actual_response.get("eventLabel"),
                         msg=f'Expected eventLabel value "{expected_response.get("eventLabel")}" is not '
                             f'same as actual eventLabel value "{actual_response.get("eventLabel")}"')
        if self.device_type != 'mobile':
            self.assertEqual(expected_response.get("eventDetails"), actual_response.get("eventDetails"),
                             msg=f'Expected eventDetails value "{expected_response.get("eventDetails")}" is not '
                                 f'same as actual eventDetails value "{actual_response.get("eventDetails")}"')
