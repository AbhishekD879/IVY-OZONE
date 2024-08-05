import voltron.environments.constants as vec
import pytest
from time import sleep
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_tst2
# @pytest.mark.hl # not configured in prod and Beta
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65305225_To_verify_exit_button_in_free_text_popup(Common):
    """
    TR_ID: C65305225
    NAME: To verify exit button in free text popup
    DESCRIPTION: This test case is to verify the exit button navigating back to SYC-Team selection page without entering text and after entering text
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
        self.site.wait_content_state_changed()
        self.__class__.i_dont_support_any_teams = self.site.show_your_colors.i_dont_support_any_teams
        self.assertTrue(self.i_dont_support_any_teams, msg='"I dont support any teams" is not displayed')

    def test_001_select__i_dont_support_any_of_these_teams(self):
        """
        DESCRIPTION: Select ' I don't support any of these teams'
        EXPECTED: A Free text popup should display, to tell us whom do they support
        """
        self.site.show_your_colors.scroll_to_we(self.i_dont_support_any_teams)
        self.i_dont_support_any_teams.click()
        self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_DONT_SUPPORT_ANY_OF_THESE_TEAMS,
                                                          verify_name=False)

    def test_002_click_on_exit_button(self):
        """
        DESCRIPTION: Click on exit button
        EXPECTED: user should be navigated back to Team selection page.
        """
        self.dialog.exit_button.click()
        self.assertTrue(self.site.show_your_colors,
                        msg='User not redirected to show us your colors page')

    def test_003_select__i_dont_support_any_of_these_teams(self):
        """
        DESCRIPTION: Select ' I don't support any of these teams'
        EXPECTED: A Free text popup should display, to tell us whom do they support
        """
        sleep(5)
        self.site.show_your_colors.scroll_to_we(self.site.show_your_colors.i_dont_support_any_teams)
        self.site.show_your_colors.i_dont_support_any_teams.click()
        self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_DONT_SUPPORT_ANY_OF_THESE_TEAMS,
                                                          verify_name=False)

    def test_004_enter_any_team_of_user_choice_name_in_the_text_popup(self):
        """
        DESCRIPTION: enter any team of user choice name in the text popup
        EXPECTED: User should be able to input the team of their of choice successfully
        """
        self.dialog.select_custom_team_name_input = vec.fanzone.TEAMS_LIST.arsenal
        self.assertTrue(self.dialog.select_custom_team_name_input,
                        msg='Choice name has not entered')

    def test_005_click_on_exit_button(self):
        """
        DESCRIPTION: Click on exit button
        EXPECTED: user should be navigated back to Team selection page.
        """
        self.dialog.exit_button.click()
        self.assertTrue(self.site.show_your_colors,
                        msg='User not redirected to show us your colors page')
