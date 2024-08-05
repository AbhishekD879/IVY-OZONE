import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_haul


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone_reg_tests
@vtest
class Test_C65305092_Verify_GA_tracking_for_users_actions_on_SYC_pop_up_3_CTAs(BaseDataLayerTest):
    """
    TR_ID: C65305092
    NAME: Verify GA tracking for user's actions on SYC pop-up (3 CTA's)
    DESCRIPTION: This test case is to verify GA tracking for user's actions on SYC pop-up (3 CTA's)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
        PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
        PRECONDITIONS: 3) User is in logged out state
        PRECONDITIONS: 4) User should be on team selection page through promotion and open console
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)

        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=self.username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football", timeout=30)

    def test_001_check_syc_pop_up(self):
        """
        DESCRIPTION: Check SYC pop-up
        EXPECTED: User should populated with SYC pop-up with 3 CTA buttons
        """
        self.__class__.dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        self.assertTrue(self.dialog_fb, msg='"SYC overlay"is not displayed on Football landing page')

    def test_002_click_on_imin_button_and_check_ga_tracking(self):
        """
        DESCRIPTION: Click on ImIn button and check GA tracking
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "I'm In"
        EXPECTED: "eventCategory": "show your colors",
        EXPECTED: "eventLabel": ""
        EXPECTED: })
        """
        self.dialog_fb.imin_button.click()
        wait_for_haul(5)
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='')
        expected_response = {"event": "trackEvent",
                             "eventAction": "I'M IN",
                             "eventCategory": "show your colours",
                             "eventLabel": ""}
        self.compare_json_response(actual_response, expected_response)

    def test_003_repeat_the_process_by_click_ing_on_remind_me_later(self):
        """
        DESCRIPTION: Repeat the process by click ing on REMIND ME LATER
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "Remind Me Later"
        EXPECTED: "eventCategory": "show your colors",
        EXPECTED: "eventLabel": ""
        EXPECTED: })
        """
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(),
                        msg='User has not logged out!')
        self.site.login(username=self.username)
        self.navigate_to_page("Homepage")
        self.site.wait_content_state("Homepage")
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football", timeout=30)
        self.dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        self.dialog_fb.remind_later_button.click()
        wait_for_haul(5)
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='Remind Me Later')
        expected_response = {"event": "trackEvent",
                             "eventAction": "Remind Me Later",
                             "eventCategory": "show your colours",
                             "eventLabel": ""}
        self.compare_json_response(actual_response, expected_response)

    def test_004_repeat_the_process_by_click_ing_on_dont_show_me_this_again(self):
        """
        DESCRIPTION: Repeat the process by click ing on DON'T SHOW ME THIS AGAIN
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "Remind Me Later"
        EXPECTED: "eventCategory": "Donâ€™t Show Me This Again",
        EXPECTED: "eventLabel": ""
        EXPECTED: })
        """
        self.delete_cookies()
        self.device.driver.execute_script('localStorage.clear();')
        self.navigate_to_page("Homepage")
        self.site.login(username=self.username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football", timeout=30)
        self.dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        self.assertTrue(self.dialog_fb, msg='"SYC overlay"is not displayed on Football landing page')
        self.dialog_fb.dont_show_me_button.click()
        wait_for_haul(5)
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value="Dont show me this again")
        expected_response = {"event": "trackEvent",
                             "eventAction": "Dont show me this again",
                             "eventCategory": "show your colours",
                             "eventLabel": ""}
        self.compare_json_response(actual_response, expected_response)
