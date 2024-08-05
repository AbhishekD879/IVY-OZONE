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
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305219_To_verify_confirmation_pop_up_UI_after_user_selecting_a_team(Common):
    """
    TR_ID: C65305219
    NAME: To verify confirmation pop-up UI after user selecting a team
    DESCRIPTION: This test case is to verify confirmation pop-up UI after user selecting a team
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
        EXPECTED: User will see his team selection in a highlighted box
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

    def test_002_user_should_be_prompted_with_pop_up(self):
        """
        DESCRIPTION: User should be prompted with pop-up
        EXPECTED: Verify below in popup on desktop/Mobile
        EXPECTED: Mobile:
        EXPECTED: 1. Team Confirmation 'By CONFIRMING that you are a supporter of < TEAM > you will not be able to change
        EXPECTED: your team for another 30 days.
        EXPECTED: On the next screen you can tell us which FANZONE notifications you want to receive 2. CTA buttons 'SELECT DIFFERENT TEAM' and ' CONFIRM '
        EXPECTED: Desktop:
        EXPECTED: 1. Are you sure? By CONFIRMING that
        EXPECTED: you are a supporter of < TEAM > you will not be able to change your team for another 30 days.
        EXPECTED: FANZONE notifications are unavailable on desktop; head over to our app to receive notifications of offers, team news and live
        EXPECTED: updates. '
        EXPECTED: 2. CTA buttons 'SELECT DIFFERENT TEAM' and ' CONFIRM '
        """
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        sleep(5)
        if self.device_type == "mobile":
            expected_msg = vec.fanzone.TEAMS_CONFIRMATION_MESSAGE_MOBILE.format(team_name=self.aston_villa, duration="1")
        else:
            expected_msg = vec.fanzone.TEAMS_CONFIRMATION_MESSAGE_DESKTOP.format(team_name=self.aston_villa, duration="1")
        self.assertEqual(dialog.description, expected_msg, msg=f'Actual msg "{dialog.description}"is not same as expected msg"{expected_msg}"')
        self.assertTrue(dialog.select_different_button.is_displayed(), msg="Select different team button is not displayed")
        self.assertTrue(dialog.confirm_button.is_displayed(), msg="Confirm button is not displayed")

    def test_003_verify_ui_of_the_pop_up(self):
        """
        DESCRIPTION: Verify UI of the pop-up
        EXPECTED: UI of the pop-up should be similar to Zeplin screen
        EXPECTED: Zeplin link:
        EXPECTED: https://app.zeplin.io/project/609b99f3e39d17baed699db1/screen/61a7a6d33d4c9c8dcd82ad57
        """
        # Cannot verify zeplin screen
