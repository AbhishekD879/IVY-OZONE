import tests
import pytest
from time import sleep
from voltron.utils.waiters import wait_for_result
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
class Test_C65305221_To_Verify_user_successful_team_selection(Common):
    """
    TR_ID: C65305221
    NAME: To Verify user successful team selection
    DESCRIPTION: This test case to Verify user successful team selection
    PRECONDITIONS: 1) User is in logged in state
    PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
    PRECONDITIONS: 3) In CMS-Fanzone SYCx- data should be created, which will trigger SYC popup in front end
    PRECONDITIONS: 4) User is in SYC- team selection page
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: To Verify Team selection confirmation popup is disappeared in SYC page when clicks on other area in the page
        PRECONDITIONS: 1) User is in logged in state
        PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
        PRECONDITIONS: 3) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        self.__class__.astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if self.astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())

        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')

    def test_001_select_any_team(self):
        """
        DESCRIPTION: Select any team
        EXPECTED: User will see his team selection in a highlighted box and gets a popup
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
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        sleep(5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        team_ui_box_border = teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].css_property_value('border').split()[0]
        self.assertTrue(team_ui_box_border == vec.fanzone.SYC_SELECTED_TEAM_BORDER,
                        msg=f'"{teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].name}" '
                            f' Previously subscribed team selection is not in highlighted box ')

    def test_002_click_on_confirm_cta_button(self):
        """
        DESCRIPTION: Click on CONFIRM CTA button
        EXPECTED: Desktop:
        EXPECTED: User selection will store in BE and User navigate to Football Landing Page
        EXPECTED: User get entry points to fanzone page
        EXPECTED: Mobile:
        EXPECTED: User selection will store in BE and User navigate to preference center screen
        """
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)

        self.assertEqual(dialog_confirm.description, vec.FANZONE.TEAMS_CONFIRMATION_MESSAGE_DESKTOP.format(team_name=vec.fanzone.TEAMS_LIST.aston_villa.title(), duration=1),
                         msg=f'"Actual text message " {dialog_confirm.description} is not same as'
                         f' "Expected text message "{vec.FANZONE.TEAMS_CONFIRMATION_MESSAGE_DESKTOP.format(team_name=vec.fanzone.TEAMS_LIST.aston_villa.title(), duration=1)}')
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        wait_for_result(lambda: dialog_alert.exit_button.is_displayed(), timeout=5,
                        name='"EXIT" button to be displayed.')
        dialog_alert.exit_button.click()
        # self.site.wait_content_state("football")  # as per the new change, after subscription, we will be in
        # fanzone page only
