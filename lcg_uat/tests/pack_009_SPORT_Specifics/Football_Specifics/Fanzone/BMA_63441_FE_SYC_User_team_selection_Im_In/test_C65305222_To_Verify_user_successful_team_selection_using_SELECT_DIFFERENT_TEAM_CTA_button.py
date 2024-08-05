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
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305222_To_Verify_user_successful_team_selection_using_SELECT_DIFFERENT_TEAM_CTA_button(Common):
    """
    TR_ID: C65305222
    NAME: To Verify user successful team selection using SELECT DIFFERENT TEAM CTA button
    DESCRIPTION: This test case is to verify user successful team selection using SELECT DIFFERENT TEAM CTA button
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
        brentford_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.brentford.title())
        if brentford_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.brentford.title())
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())

        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport('FOOTBALL', fanzone=True, timeout=5)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              verify_name=False)
        dialog_fb.imin_button.click()
        sleep(5)

    def test_001_select_any_team(self, team=vec.fanzone.TEAMS_LIST.brentford.title()):
        """
        DESCRIPTION: Select any team
        EXPECTED: User will see his team selection in a highlighted box and gets a popup
        """
        fanzone = self.site.show_your_colors.items_as_ordered_dict
        fanzone[team].scroll_to()
        fanzone[team].click()
        self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)

    def test_002_click_on_select_different_team_cta_button(self):
        """
        DESCRIPTION: Click on SELECT DIFFERENT TEAM CTA button
        EXPECTED: user should be navigated back to the SYC- team selection screenÂ to choose a differentÂ team
        """
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.select_different_button.click()

    def test_003_select_any_team(self):
        """
        DESCRIPTION: Select any team
        EXPECTED: User will see his team selection in a highlighted box and gets a popup
        """
        self.test_001_select_any_team(team=vec.fanzone.TEAMS_LIST.aston_villa.title())

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
        self.site.wait_content_state('fanzoneevents')
