import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from time import sleep


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305228_To_verify_the_back_button_in_SYC_page_navigates_to_football_SPL_and_gets_SYC_popup(Common):
    """
    TR_ID: C65305228
    NAME: To verify the back button in SYC page navigates to football SPL and gets SYC popup
    DESCRIPTION: To verify the back button in SYC page navigates to football SPL and gets SYC popup
    PRECONDITIONS: 1) User is in logged in state
    PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
    PRECONDITIONS: 3) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
    PRECONDITIONS: 4) User is in SYC- team selection page
    """
    keep_browser_open = True
    aston_villa = vec.fanzone.TEAMS_LIST.aston_villa.title()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User is in logged in state
        PRECONDITIONS: User has Not subscribed for Fanzone Previously
        PRECONDITIONS: In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
        PRECONDITIONS: User is in SYC- team selection page
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30)
        self.assertTrue(dialog_fb, msg='"SYC Pop Up"is not displayed on Football landing page')
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I am in button is displayed',
                        timeout=5)

    def test_001_select_any_team(self):
        """
        DESCRIPTION: Select any team
        EXPECTED: Selected team should be in highlighted box
        """
        teams = self.site.show_your_colors.items_as_ordered_dict
        self.assertTrue(teams, msg='No teams found')
        teams[self.aston_villa].scroll_to_we()
        selected_team = teams[self.aston_villa]
        selected_team.click()
        sleep(5)
        self.assertTrue(
            selected_team.css_property_value('border').split()[0] == vec.fanzone.SYC_SELECTED_TEAM_BORDER,
            msg=f'"{teams[self.aston_villa].name}" '
                f' team selection is not in highlighted box ')
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.select_different_button.click()

    def test_002_click_on_back_button(self):
        """
        DESCRIPTION: Click on Back button
        EXPECTED: User should be navigated back to Football Landing page
        """
        self.site.back_button.click()

    def test_003_check_popup_is_displayed(self):
        """
        DESCRIPTION: Check popup is displayed
        EXPECTED: User should get SYC popup
        """
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30)
        self.assertTrue(dialog_fb, msg='"SYC Pop Up"is not displayed on Football landing page')
