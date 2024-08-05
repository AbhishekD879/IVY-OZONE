import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from time import sleep
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_h1
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65305280_To_verify_UI_of_TEAM_ALERTS_Popup(Common):
    """
    TR_ID: C65305280
    NAME: To verify UI of TEAM ALERTS Popup
    DESCRIPTION: To verify UI of TEAM ALERTS Popup
    PRECONDITIONS: 1) Fanzone should be enabled in System Configuration
    PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 2) Fanzones(Team's) should be created from Create  Fanzone page
    PRECONDITIONS: CMS-->Fanzone-->Fanzones-->Create Fanzone
    PRECONDITIONS: 3) All he 4 entry points should be enabled
    PRECONDITIONS: 4) User has selected Team in SYC page , User has clicked the Confirm Button in Team confirmation popup
    PRECONDITIONS: Note: User could navigate to SYC page via promotions or by selecting IM IN in SYC popup from Football landing page.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User has logged into lads application
        PRECONDITIONS: 2) User has Unsubscribed to Fanzone less than 30 days ago
        PRECONDITIONS: 3) Configure fanzone data in CMS
        PRECONDITIONS: CMS-->Fanzone-->Fanzones
        PRECONDITIONS: 4) In System Config Fanzone should be enabled
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
        self.site.wait_content_state(state_name='HomePage')
        self.site.login(username=username)
        self.site.open_sport(name='Football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Fanzones are displayed',
                        timeout=5)
        fanzone = self.site.show_your_colors.items_as_ordered_dict
        fanzone[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)

    def test_001_verify_notification_popup_is_triggered_to_user(self):
        """
        DESCRIPTION: Verify Notification Popup is triggered to User
        EXPECTED: Notification Popup should be triggered to User
        """
        self.__class__.dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)

    def test_002_verify_ui_of_team_alerts_popup_should_be_as_mockup_attached_to_story_bma_63809(self):
        """
        DESCRIPTION: Verify UI of TEAM ALERTS Popup should be as mockup attached to story BMA-63809
        EXPECTED: UI should be as per the mockup attached to BMA-63809
        """
        # covered in step 003

    def test_003_verify_the_details_of_popup_messageatitle_team_alertbtext_message_dont_miss_a_thing_go_to_the_ladbrokes_app_and_set_your_push_notification_preferences_to_receive_team_news_in_play_match_updates_and_more_these_are_for_the_app_platform_only_they_are_notsent_on_desktop_or_mobile_web_platformsccta_exit(self):
        """
        DESCRIPTION: Verify the details of Popup message
        DESCRIPTION: a.Title: Team Alert
        DESCRIPTION: b.Text message: Donâ€™t miss a thing! Go to the Ladbrokes app and set your push notification preferences to receive team news, in-play match updates and more. These are for the app platform only; they are notsent on desktop or mobile web platforms.
        DESCRIPTION: c.CTA :EXIT
        EXPECTED: All the listed details should display in popup
        """
        self.assertTrue(self.dialog_teamalert.header_object.title_text, msg='Team alerts title is not displayed')
        self.assertEquals(self.dialog_teamalert.description, vec.FANZONE.TEAM_ALERTS_MSG,
                          msg=f"Actual message '{self.dialog_teamalert.description}' is not same as expected message '{vec.FANZONE.TEAM_ALERTS_MSG}'")
        self.assertTrue(self.dialog_teamalert.exit_button, msg='Team alerts exit button is not displayed')
