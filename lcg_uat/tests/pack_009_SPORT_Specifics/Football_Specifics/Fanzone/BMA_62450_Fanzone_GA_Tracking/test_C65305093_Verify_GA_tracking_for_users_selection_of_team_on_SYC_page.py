import pytest
import tests
from time import sleep
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_h1
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65305093_Verify_GA_tracking_for_users_selection_of_team_on_SYC_page(BaseDataLayerTest):
    """
    TR_ID: C65305093
    NAME: Verify GA tracking for user's selection of team on SYC page
    DESCRIPTION: This test case is to verify GA tracking for user's selection of team on SYC page
    PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
    PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
    PRECONDITIONS: 3) User is in logged in state
    PRECONDITIONS: 4) User should be on football page
    PRECONDITIONS: 5) User should open console page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
        PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
        PRECONDITIONS: 3) User is in logged in state
        PRECONDITIONS: 4) User should be on football page
        PRECONDITIONS: 5) User should open console page
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

    def test_001_click_on_im_in_cta_button_in_the_syc_popup(self):
        """
        DESCRIPTION: Click on I'm In CTA button in the syc popup
        EXPECTED: User should be navigated to Team selection page
        """
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        results = wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict, timeout=30,
                                  name='All Teams to be displayed')
        self.assertTrue(results, msg='Teams are not displayed')

    def test_002_click_on_any_teamex_arsenal_and_check_ga_tracking(self):
        """
        DESCRIPTION: Click on any team(ex: Arsenal) and check GA tracking
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": select
        EXPECTED: "eventCategory": "show your colors",
        EXPECTED: "eventLabel": Arsenal
        EXPECTED: })
        """
        teams = self.site.show_your_colors.items_as_ordered_dict
        for team in teams.items():
            if not team[0] == "":
                team[1].scroll_to_we()
                team[1].click()
                dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION, verify_name=False)
                self.assertTrue(dialog_confirm,msg='Confirmation popup not appeared')

                actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value='show your colors')
                expected_response = {"event": "trackEvent",
                                     "eventAction": "select",
                                     "eventCategory": "show your colors",
                                     "eventLabel": team[0]
                                     }
                self.compare_json_response(actual_response, expected_response)
                dialog_confirm = self.site.wait_for_dialog(
                    dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION,
                    verify_name=False)
                self.assertTrue(dialog_confirm, msg='login popup not appeared')
                dialog_confirm.select_different_button.click()
                sleep(1)

    def test_003_deselect_the_team__exarsenal_and_check_ga_tracking(self):
        """
        DESCRIPTION: Deselect the team ( ex:Arsenal) and check GA tracking
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": deselect
        EXPECTED: "eventCategory": "show your colors",
        EXPECTED: "eventLabel": Arsenal
        EXPECTED: })
        """
        # Deselect eventAction is NA

    def test_004_repeat_above_process_for_all_the_buttons_in_team_selection_page(self):
        """
        DESCRIPTION: Repeat above process for all the buttons in team selection page
        EXPECTED:
        """
        # Covered in Step 2
