import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65305235_To_validate_successful_fanzone_subscription_through_SYC_popup_from_Football_landing_page_for_newly_signed_up_Ladbrokes_user(Common):
    """
    TR_ID: C65305235
    NAME: To validate successful fanzone subscription through SYC popup from Football landing page, for newly signed up Ladbrokes user
    DESCRIPTION: To validate successful fanzone subscription through SYC popup from Football landing page, for newly signed up Ladbrokes user
    PRECONDITIONS: 1) New User is signed up and is in logged in state
    PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
    PRECONDITIONS: 3) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
    """
    keep_browser_open = True
    team_name = vec.fanzone.TEAMS_LIST.aston_villa.title()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) New User is signed up and is in logged in state
        PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
        PRECONDITIONS: 3) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        burnley_fanzone = self.cms_config.get_fanzone(self.team_name)
        if burnley_fanzone['active'] is not True:
            self.cms_config.update_fanzone(self.team_name)
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_001_launch_the_application_and_navigate_football_slp(self):
        """
        DESCRIPTION: Launch the application and navigate Football SLP
        EXPECTED: User should get SYC popup
        """
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        self.__class__.dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              verify_name=False)
        self.assertTrue(self.dialog_fb, msg='"SYC overlay"is not displayed on Football landing page')

    def test_002_select_any_team(self):
        """
        DESCRIPTION: Select any team
        EXPECTED: User will see his team selection in a highlighted box and user is presented with Team Confirmation popup
        """
        self.dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I am in button is displayed',
                        timeout=5)
        self.assertTrue(self.site.show_your_colors, msg='"SYC selection page"is not displayed after click')
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[self.team_name].click()
        self.__class__.dialog_confirm = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        self.assertTrue(self.dialog_confirm, msg='Team confirmation pop-up is not appeared')
        self.assertEqual(vec.fanzone.TEAMS_LIST.aston_villa, self.dialog_confirm.card_dialog_text,
                         msg=f'"{self.team_name} is not same in pop-up "{self.dialog_confirm.card_dialog_text}""')

    def test_003_click_on_confirm_cta_button(self):
        """
        DESCRIPTION: Click on Confirm CTA button
        EXPECTED: Desktop:
        EXPECTED: User selection will store in BE and User navigate to Football Landing Page
        EXPECTED: Mobile:
        EXPECTED: User selection will store in BE and User navigate to preference center screen
        """
        self.dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS,
                                                 timeout=15)
        wait_for_result(lambda: dialog_alert.exit_button.is_displayed(), timeout=5,
                        name='"EXIT" button to be displayed.')
        self.assertTrue(dialog_alert, msg='Failed to load dailog alert pop-up ')
        dialog_alert.exit_button.click()
        self.assertTrue(self.site.fanzone.setting_link, msg='Fanzone setting link is not shown')
