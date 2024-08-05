import pytest
import voltron.environments.constants as vec
from selenium.webdriver import ActionChains
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.pages.shared import get_driver


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65305233_To_Verify_I_dont_support_any_of_these_teams_popup_is_disappeared_in_SYC_page_when_clicks_on_other_area_in_the_page(Common):
    """
    TR_ID: C65305233
    NAME: To Verify I don't support any of these teams' popup is disappeared in SYC page when clicks on other area in the page
    DESCRIPTION: To Verify I don't support any of these teams' popup is disappeared in SYC page when clicks on other area in the page
    PRECONDITIONS: 1) User is in logged in state
    PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
    PRECONDITIONS: 3) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')

    def test_001_launch_the_application_and_navigate_football_slp(self):
        """
        DESCRIPTION: Launch the application and navigate Football SLP
        EXPECTED: User should get SYC popup
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport('FOOTBALL', fanzone=True, timeout=5)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              verify_name=False)
        dialog_fb.imin_button.click()
        self.site.wait_content_state_changed()
        self.__class__.i_dont_support_any_teams = self.site.show_your_colors.i_dont_support_any_teams
        self.assertTrue(self.i_dont_support_any_teams, msg='"I dont support any teams" is not displayed')

    def test_002_select_21st_tile__i_dont_support_any_of_these_teams(self):
        """
        DESCRIPTION: Select 21st tile ' I don't Support any of these Teams'
        EXPECTED: User will see his team selection in a highlighted box
        """
        self.site.show_your_colors.scroll_to_we(self.site.show_your_colors.i_dont_support_any_teams)
        self.site.show_your_colors.i_dont_support_any_teams.click()
        self.__class__.dialog = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_DONT_SUPPORT_ANY_OF_THESE_TEAMS,
            verify_name=False)

    def test_003_user_should_get_i_dont_support_any_of_the_team_popup(self):
        """
        DESCRIPTION: user should get I don't support any of the team popup
        EXPECTED: Should be able to see the popup with text message and 2 CTA buttons
        """
        self.dialog.select_custom_team_name_input = vec.fanzone.TEAMS_LIST.arsenal
        self.assertTrue(self.dialog.select_custom_team_name_input,
                        msg='Choice name has not entered')
        self.assertTrue(self.dialog.confirm_button.is_displayed(), msg="Confirm button is not displayed")

    def test_004_click_on_any_part_of_the_page_other_than_popup_layout(self):
        """
        DESCRIPTION: Click on any part of the page, other than popup layout
        EXPECTED: Team Confirmation Popup should be disappeared
        """
        ActionChains(get_driver()).move_by_offset(30, 30).click().perform()
        sleep(1)
        self.assertFalse(self.dialog.select_custom_team_name_input, msg='Choice name has not entered')
        self.site.show_your_colors.scroll_to_we(self.site.show_your_colors.i_dont_support_any_teams)
        self.assertTrue(self.i_dont_support_any_teams, msg='"I dont support any teams" is not displayed')
