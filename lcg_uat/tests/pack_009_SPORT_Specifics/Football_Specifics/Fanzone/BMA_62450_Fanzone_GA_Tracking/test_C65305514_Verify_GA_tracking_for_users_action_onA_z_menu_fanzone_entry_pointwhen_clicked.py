import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305514_Verify_GA_tracking_for_users_action_onA_z_menu_fanzone_entry_pointwhen_clicked(BaseDataLayerTest):
    """
    TR_ID: C65305514
    NAME: Verify GA tracking for user's action onÂ A-z menu fanzone entry point(when clicked)
    DESCRIPTION: This test case is to verify GA tracking for user's action on A-z menu fanzone entry point(when clicked)
    PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC Entry points in front end
    PRECONDITIONS: 2) User has subscribed to Fanzone
    PRECONDITIONS: 3) User should be logged in state
    """
    keep_browser_open = True

    expected_response_featured_menu = {"event": "trackEvent",
                                       "eventAction": "a-z sports",
                                       "eventCategory": "navigation",
                                       "eventLabel": "Fanzone",
                                       "eventDetails": "featured"
                                       }
    expected_response_a_z_menu = {"event": "trackEvent",
                                  "eventAction": "a-z sports",
                                  "eventCategory": "navigation",
                                  "eventLabel": "Fanzone",
                                  "eventDetails": "a-z betting"
                                  }

    def test_000_preconditions(self):
        """
        DESCRIPTION: Active the fanzone team and register a new user
        EXPECTED: Fanzone team is activated in cms and logged into the application
        """
        fanzone_status = self.get_initial_data_system_configuration().get(vec.sb.FANZONE)
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.manchester_city.title())
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football", timeout=30)
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

    def test_001_user_launches_application_and_navigate_to_a_z_sports(self):
        """
        DESCRIPTION: User launches application and navigate to a-z sports
        EXPECTED: A-z menu should be displayed
        """
        self.navigate_to_page(name=tests.HOSTNAME)
        self.site.wait_content_state(state_name='HomePage')
        if self.device_type == 'mobile':
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertTrue(all_items, msg='No items on MenuCarousel found')
        else:
            az_links = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertTrue(az_links, msg='No one item found in "A-Z Menu" section')

    def test_002_click_on_fanzone_entry_point_from_featured_menu(self):
        """
        DESCRIPTION: Click on Fanzone entry point from featured menu
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "a-z sports",
        EXPECTED: "eventCategory": "navigation",
        EXPECTED: "eventLabel": "Fanzone"
        EXPECTED: "eventDetails": "featuredâ€�
        EXPECTED: })
        """
        if self.device_type == 'mobile':
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertTrue(all_items, msg='No items on MenuCarousel found')
            all_items.get(vec.SB.ALL_SPORTS).click()
            self.site.wait_content_state(state_name='AllSports')
            top_sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
            self.assertTrue(top_sports, msg='No sports found in "Top Sports" section')
            top_sports.get(vec.sb.FANZONE).click()
        else:
            self.site.sport_menu.click_item(vec.sb.FANZONE)
        self.site.wait_content_state_changed(timeout=15)

        sleep(3)
        actual_response = self.get_data_layer_specific_object(object_key='eventDetails', object_value='featured')
        self.compare_json_response(actual_response, self.expected_response_featured_menu)

    def test_003_navigate_back_to_home_page_and_click_on_fanzone_entry_point_in_a_z_menu(self):
        """
        DESCRIPTION: Navigate back to home page and click on fanzone entry point in a-z menu
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "a-z sports",
        EXPECTED: "eventCategory": "navigation",
        EXPECTED: "eventLabel": "Fanzone"
        EXPECTED: "eventDetails": "a-z betting"
        EXPECTED: })
        """
        if self.device_type == 'mobile':
            self.navigate_to_page(name='Home')
            self.site.wait_content_state('HomePage')
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertTrue(all_items, msg='No items on MenuCarousel found')
            all_items.get(vec.SB.ALL_SPORTS).click()
            self.site.wait_content_state(state_name='AllSports')

            az_sports_name = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
            self.assertTrue(az_sports_name, msg='No items on MenuCarousel found')
            az_sports_name.get(vec.sb.FANZONE).click()
            self.site.wait_content_state_changed(timeout=15)
            sleep(3)
            actual_response = self.get_data_layer_specific_object(object_key='eventDetails', object_value='a-z betting')
            self.compare_json_response(actual_response, self.expected_response_a_z_menu)
