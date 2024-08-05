import pytest
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305220_To_verify_CTA_buttons_CONFIRM_and_SELECT_DIFFERENT_TEAM_in_confirmation_popup(Common):
    """
    TR_ID: C65305220
    NAME: To verify CTA buttons CONFIRM and SELECT DIFFERENT TEAM in confirmation popup
    DESCRIPTION: To Verify CTA buttons CONFIRM and SELECT DIFFERENT TEAM in confirmation popup
    PRECONDITIONS: 1) User is in logged in state
    PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
    PRECONDITIONS: 3) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
    PRECONDITIONS: 4) User is in SYC- team selection page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User is in logged in state
        PRECONDITIONS: User has Not subscribed for Fanzone Previously
        PRECONDITIONS: In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
        PRECONDITIONS: User is in SYC- team selection page
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)

        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        sleep(5)
        self.site.wait_content_state("football", timeout=30)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        sleep(5)

    def test_001_select_any_team(self):
        """
        DESCRIPTION: Select any team
        EXPECTED: User will see his team selection in a highlighted box and gets a popup
        """
        teams = self.site.show_your_colors.items_as_ordered_dict
        list(teams.values())[1].scroll_to_we()
        list(teams.values())[1].click()
        self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)

    def test_002_click_on_select_different_team_cta_button(self):
        """
        DESCRIPTION: Click on SELECT DIFFERENT TEAM CTA button
        EXPECTED: user should be navigated back to the SYC screenÂ to choose a differentÂ team
        """
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.select_different_button.click()

    def test_003_select_any_team(self):
        """
        DESCRIPTION: Select any team
        EXPECTED: User will see his team selection in a highlighted box
        """
        self.test_001_select_any_team()

    def test_004_click_on_confirm_cta_button(self):
        """
        DESCRIPTION: Click on CONFIRM CTA button
        EXPECTED: Desktop:
        EXPECTED: User selection will store in BE and User navigate to Football Landing Page
        EXPECTED: Mobile:
        EXPECTED: User selection will store in BE and User navigate to preference center screen
        """
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()
