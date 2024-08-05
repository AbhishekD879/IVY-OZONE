import pytest
from time import sleep
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305095_Verify_GA_tracking_for_users_actions_on_Free_text_input_pop_up_2_CTAs(BaseDataLayerTest):
    """
    TR_ID: C65305095
    NAME: Verify GA tracking for user's actions on Free text input pop-up (2 CTA's)
    DESCRIPTION: This test case is to verify GA tracking for user's actions on Free text input pop-up (2 CTA's)
    PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
    PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
    PRECONDITIONS: 3) User is in logged in state
    PRECONDITIONS: 4) User should be on team selection page and open console
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
        PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
        PRECONDITIONS: 3) User is in logged in state
        PRECONDITIONS: 4) User should be on team selection page and open console
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport('FOOTBALL', fanzone=True, timeout=10)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              verify_name=False)
        dialog_fb.imin_button.click()
        self.site.wait_content_state_changed(timeout=20)
        self.__class__.i_dont_support_any_teams = self.site.show_your_colors.i_dont_support_any_teams
        self.assertTrue(self.i_dont_support_any_teams, msg='"I dont support any teams" is not displayed')

    def test_001_select_i_dont_support_any_of_the_team(self):
        """
        DESCRIPTION: Select I DON'T SUPPORT ANY OF THE TEAM
        EXPECTED: User selected tile should highlighted and gets free text popup
        """
        wait_for_result(lambda: self.site.show_your_colors.scroll_to_we(self.i_dont_support_any_teams), timeout=10)
        sleep(5)
        self.i_dont_support_any_teams.click()
        sleep(3)
        self.__class__.dialog = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_DONT_SUPPORT_ANY_OF_THESE_TEAMS,
            verify_name=False)

    def test_002_enter_user_choice_tea_name_abc_in_free_text__click_on_exit_cta_button_and_check_ga_tracking(self):
        """
        DESCRIPTION: Enter user choice tea name ABC in free text , click on EXIT CTA button and check GA tracking
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "free text input",
        EXPECTED: "eventCategory": "show your colors",
        EXPECTED: "eventLabel": "Exit"
        EXPECTED: "eventDetails": "ABC"
        EXPECTED: })
        """
        self.dialog.select_custom_team_name_input = 'ABC'
        self.assertTrue(self.dialog.select_custom_team_name_input,
                        msg='Choice name has not entered')
        self.dialog.exit_button.click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='EXIT')
        expected_response = {"event": "trackEvent",
                             "eventAction": "free text input",
                             "eventCategory": "show your colors",
                             "eventLabel": "EXIT",
                             "eventDetails": 'ABC'}
        sleep(3)
        self.compare_json_response(actual_response, expected_response)

    def test_003_repeat_step_1_and_click_on_exit_button_without_entering_user_choice_team_namecheck_ga_tracking(self):
        """
        DESCRIPTION: Repeat step 1 and click on EXIT button without entering user choice team name
        DESCRIPTION: Check GA tracking
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "free text input",
        EXPECTED: "eventCategory": "show your colors",
        EXPECTED: "eventLabel": "Exit"
        EXPECTED: "eventDetails": ""
        EXPECTED: })
        """
        self.test_001_select_i_dont_support_any_of_the_team()
        self.dialog.exit_button.click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='EXIT')
        expected_response = {"event": "trackEvent",
                             "eventAction": "free text input",
                             "eventCategory": "show your colors",
                             "eventLabel": "EXIT",
                             "eventDetails": None
                             }
        sleep(3)
        self.compare_json_response(actual_response, expected_response)

    def test_004_repeat_step_1enter_user_choice_tea_name_abc_in_free_text__click_on_confirm_cta_button_and_check_ga_tracking(self):
        """
        DESCRIPTION: Repeat step 1
        DESCRIPTION: Enter user choice tea name ABC in free text , click on CONFIRM CTA button and check GA tracking
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "free text input",
        EXPECTED: "eventCategory": "show your colors",
        EXPECTED: "eventLabel": "CONFIRM"
        EXPECTED: "eventDetails": "ABC"
        EXPECTED: })
        """
        self.test_001_select_i_dont_support_any_of_the_team()
        self.dialog.select_custom_team_name_input = 'ABC'
        self.assertTrue(self.dialog.select_custom_team_name_input,
                        msg='Choice name has not entered')
        self.dialog.confirm_button.click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='CONFIRM')
        expected_response = {"event": "trackEvent",
                             "eventAction": "free text input",
                             "eventCategory": "show your colors",
                             "eventLabel": "CONFIRM",
                             "eventDetails": "ABC"}
        sleep(3)
        self.compare_json_response(actual_response, expected_response)
