import pytest
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_h1
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65305094_Verify_GA_tracking_for_users_actions_on_the_Team_confirmation_pop_up_2_CTAs(BaseDataLayerTest):
    """
    TR_ID: C65305094
    NAME: Verify GA tracking for user's actions on the Team confirmation pop-up (2 CTA's)
    DESCRIPTION: This test case is to verify GA tracking for user's actions on the Team confirmation pop-up (2 CTA's)
    PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
    PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
    PRECONDITIONS: 3) User is in logged in state
    PRECONDITIONS: 4) User should be on team selection page and open console
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: In CMS-Fanzone SYC- data should be created, which will trigger SYC Entry points in front end
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        arsenal_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.arsenal.title())
        if arsenal_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.arsenal.title())
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_001_select_a_team_ex_arsenal(self):
        """
        DESCRIPTION: Select a team (Ex: Arsenal)
        EXPECTED: User selected tea should highlighted and gets a popup
        """
        self.site.open_sport(name='Football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Fanzone Teams to be displayed',
                        timeout=5)
        fanzone = self.site.show_your_colors.items_as_ordered_dict
        self.__class__.team1 = fanzone[vec.fanzone.TEAMS_LIST.arsenal.title()]
        self.team1.click()
        self.__class__.dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)

    def test_002_click_on_select_different_team_and_check_ga_tracking(self):
        """
        DESCRIPTION: Click on "SELECT DIFFERENT TEAM" and check GA tracking
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "confirmation screen",
        EXPECTED: "eventCategory": "show your colors",
        EXPECTED: "eventLabel": "Select Different Team"
        EXPECTED: "eventDetails": "Arsenal"
        EXPECTED: )
        """
        self.dialog_confirm.select_different_button.click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value="SELECT DIFFERENT TEAM")
        expected_response = {'event': "trackEvent",
                             'eventAction': "confirmation screen",
                             'eventCategory': "show your colors",
                             'eventDetails': self.team1.name,
                             'eventLabel': "SELECT DIFFERENT TEAM"
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_003_select_other_team_on_team_selection_page_ex_chelsea(self):
        """
        DESCRIPTION: Select other team on team selection page (ex: Chelsea)
        EXPECTED: User selected tea should highlighted and gets a popup
        """
        fanzone = self.site.show_your_colors.items_as_ordered_dict
        self.__class__.team2 = fanzone[vec.fanzone.TEAMS_LIST.aston_villa.title()]
        self.team2.click()
        self.__class__.dialog_confirm = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)

    def test_004_click_on_confirm_button_and_check_ga_tracking(self):
        """
        DESCRIPTION: Click on CONFIRM Button and check GA tracking
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "confirmation screen",
        EXPECTED: "eventCategory": "confirm",
        EXPECTED: "eventLabel": "Select Different Team"
        EXPECTED: "eventDetails": "Chelsea"
        EXPECTED: )
        """
        self.dialog_confirm.confirm_button.click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel',
                                                              object_value="CONFIRM")
        expected_response = {'event': "trackEvent",
                             'eventAction': "confirmation screen",
                             'eventCategory': "show your colors",
                             'eventDetails': self.team2.name,
                             'eventLabel': "CONFIRM"
                             }
        self.compare_json_response(actual_response, expected_response)
