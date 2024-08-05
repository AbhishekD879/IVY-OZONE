import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305224_To_verify_Free_text_popup_UI_and_free_text_box(Common):
    """
    TR_ID: C65305224
    NAME: To verify Free text popup UI and free text box
    DESCRIPTION: This test case is to verify the UI of the popup which populate after selecting i don't support any if the team
    DESCRIPTION: and free text box.
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
        self.site.open_sport('FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              verify_name=False)
        dialog_fb.imin_button.click()
        self.site.wait_content_state_changed(timeout=20)
        self.__class__.i_dont_support_any_teams = self.site.show_your_colors.i_dont_support_any_teams
        self.assertTrue(self.i_dont_support_any_teams, msg='"I dont support any teams" is not displayed')

    def test_001_select__i_dont_support_any_of_these_teams(self):
        """
        DESCRIPTION: Select ' I don't support any of these teams'
        EXPECTED: A Free text popup should display, to tell us whom do they support
        """
        wait_for_result(lambda: self.site.show_your_colors.scroll_to_we(self.i_dont_support_any_teams), timeout=10)
        sleep(5)
        self.i_dont_support_any_teams.click()
        self.__class__.dialog = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_DONT_SUPPORT_ANY_OF_THESE_TEAMS,
            verify_name=False)

    def test_002_verify_ui_of_popup(self):
        """
        DESCRIPTION: Verify UI of popup
        EXPECTED: Popup should display below
        EXPECTED: 1. message "Sorry your team is not listed yet. Tell us which team you do support by typing in the box below and we will hopefully have a FANZONE for your team in future. ''
        EXPECTED: 2. A text box
        EXPECTED: 3. Two CTA buttons 'Exit and Confirm' should display
        EXPECTED: Zeplin link:
        EXPECTED: https://app.zeplin.io/project/609b99f3e39d17baed699db1/screen/61b8c263c6a16a61a0d1856d
        """
        self.assertEqual(self.dialog.description, vec.fanzone.I_DONT_SUPPORT_ANY_OF_THE_TEAM_MSG, msg=f"Actual "
                                                                                                      f"message is '{self.dialog.description}', is not same as expected '{vec.fanzone.I_DONT_SUPPORT_ANY_OF_THE_TEAM_MSG}'")

    def test_003_click_on_confirm_button_without_entering_text(self):
        """
        DESCRIPTION: Click on confirm button without entering text
        EXPECTED: the free text box should be highlight in red color.
        """
        self.dialog.confirm_button.click()
        self.assertTrue(self.dialog.is_underscored_red(), msg='free text box is not highlight in red color')

    def test_004_enter_any_team_of_user_choice_name_in_the_text_popup(self):
        """
        DESCRIPTION: enter any team of user choice name in the text popup
        EXPECTED: User should be able to input the team of their of choice successfully
        """
        self.dialog.select_custom_team_name_input = vec.fanzone.TEAMS_LIST.arsenal
        self.assertTrue(self.dialog.select_custom_team_name_input,
                        msg='Choice name has not entered')
        self.dialog.confirm_button.click()
