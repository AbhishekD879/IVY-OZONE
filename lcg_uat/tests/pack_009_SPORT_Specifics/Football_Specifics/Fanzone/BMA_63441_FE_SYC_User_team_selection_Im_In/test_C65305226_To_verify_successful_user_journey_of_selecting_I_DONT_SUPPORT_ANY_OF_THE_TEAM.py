import voltron.environments.constants as vec
import pytest
from tests.base_test import vtest
from time import sleep
from tests.Common import Common


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.hl # not configured in prod and Beta
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65305226_To_verify_successful_user_journey_of_selecting_I_DONT_SUPPORT_ANY_OF_THE_TEAM(Common):
    """
    TR_ID: C65305226
    NAME: To verify successful user journey of selecting I DONT SUPPORT ANY OF THE TEAM
    DESCRIPTION: This test case is to verify successful user journey of selecting I DONT SUPPORT ANY OF THE TEAM
    PRECONDITIONS: 1) User is in logged in state
    PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
    PRECONDITIONS: 3) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
    PRECONDITIONS: 4) User is in SYC- team selection page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User is in logged in state
        PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
        PRECONDITIONS: 3) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
        PRECONDITIONS: 4) User is in SYC- team selection page
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
        self.site.open_sport('FOOTBALL',fanzone=True, timeout=5)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              verify_name=False)
        dialog_fb.imin_button.click()
        self.site.wait_content_state_changed()
        self.__class__.i_dont_support_any_teams = self.site.show_your_colors.i_dont_support_any_teams
        self.assertTrue(self.i_dont_support_any_teams, msg='"I dont support any teams" is not displayed')

    def test_001_select_any_21st_box__i_dont_support_any_of_these_teams(self):
        """
        DESCRIPTION: Select any 21st box ' I don't support any of these teams'
        EXPECTED: A Free text popup should display, to tell us whom do they support
        """
        self.site.show_your_colors.scroll_to_we(self.site.show_your_colors.i_dont_support_any_teams)
        self.site.show_your_colors.i_dont_support_any_teams.click()
        self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_DONT_SUPPORT_ANY_OF_THESE_TEAMS,
                                                          verify_name=False)

    def test_002_enter_any_team_of_user_choice_name_in_the_text_popup(self):
        """
        DESCRIPTION: enter any team of user choice name in the text popup
        EXPECTED: User should be able to input the team of their of choice successfully
        """
        self.dialog.select_custom_team_name_input = vec.fanzone.TEAMS_LIST.arsenal
        self.assertTrue(self.dialog.select_custom_team_name_input,
                        msg='Choice name has not entered')

    def test_003_click_on_confirm_button_(self):
        """
        DESCRIPTION: Click on confirm button .
        EXPECTED: User should get thankyou message popup
        """
        self.dialog.confirm_button.click()

    def test_004_verify_thank_you_message__popup(self):
        """
        DESCRIPTION: Verify 'Thank You Message ' popup
        EXPECTED: The popup should have below
        EXPECTED: 1. Thank you message as " Thank you for telling us which team you support. Weâ€™ll hopefully have a FANZONE for your team soon."
        EXPECTED: 2. "EXIT" CTA Button
        EXPECTED: Zeplin Link:
        EXPECTED: https://app.zeplin.io/project/609b99f3e39d17baed699db1/screen/61a7a6d2806c6aa4f0a50861
        """
        self.__class__.msg_dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_THANK_YOU,
                                                              verify_name=False)
        self.assertTrue(self.msg_dialog, msg="Thank you message pop up is not displayed")
        sleep(5)
        self.assertEqual(self.msg_dialog.description, vec.FANZONE.THANK_YOU_MESSAGE, msg=f"Actual message '{self.msg_dialog.description}' is not same as expected message '{vec.FANZONE.THANK_YOU_MESSAGE}'")
        self.assertTrue(self.msg_dialog.exit_button, msg='"EXIT" CTA Button is not displayed')

    def test_005_click_on_exit_button(self):
        """
        DESCRIPTION: Click on EXIT button
        EXPECTED: User should be navigate to Football landing page
        """
        self.msg_dialog.exit_button.click()
        self.site.wait_content_state(state_name="football")
