import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.hl # not configured in prod and Beta
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65305012_To_verify_user_will_not_be_able_change_the_team_in_SYC_page_when_user_log_in_from_different_device_for_user30_days(BaseUserAccountTest):
    """
    TR_ID: C65305012
    NAME: To verify user will not be able change the team in SYC page when user log in from different device for user(<30 days)
    DESCRIPTION: This test case is to to verify user will not be able change the team in SYC page when user log in from different device for user(<30 days)
    PRECONDITIONS: 1) User is in logged in state(Lads app)
    PRECONDITIONS: 2) User has already subscribed for Fanzone and has not completed 30 days form subscription
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User is in logged in state(Lads app)
        PRECONDITIONS: 2) User has already subscribed for Fanzone and has not completed 30 days form subscription
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=self.username)
        self.site.open_sport('football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Teams to be displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_launch_the_application_in_different_deviceother_device_form_which_fanzone_team_wasnt_opted(self):
        """
        DESCRIPTION: Launch the application in different device(other device form which Fanzone team wasn't opted)
        EXPECTED: Application should be launched successfully
        """
        self.device.driver.quit()
        self.__class__._device = self.__class__._site = None
        if self.device_type == 'mobile':
            self.__class__.device_name = tests.desktop_default
        else:
            self.__class__.device_name = tests.mobile_default
        self.site.login(username=self.username)

    def test_002_click_on_promotions(self):
        """
        DESCRIPTION: Click on Promotions
        EXPECTED: User should be navigated to Promotions page
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        self.__class__.promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(self.promotions, msg='No promotions found on page')

    def test_003_verify_show_your_colors_promotion_is_displayed(self):
        """
        DESCRIPTION: Verify Show Your Colors Promotion is displayed
        EXPECTED: SYC promotion should be displayed
        """
        promo = self.promotions[vec.fanzone.PROMOTION_TITLE]
        self.assertTrue(promo, msg='SYC promotion is not shown')
        promo.more_info_button.click()
        # self.site.wait_content_state(state_name='PromotionDetails')
        promotion_details = self.site.promotion_details.tab_content.promotion
        fz_syc_button = promotion_details.detail_description.fanzone_syc_button
        fz_syc_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')
        sleep(3)

    def test_004_click_on_cta_button(self):
        """
        DESCRIPTION: click on cTA button
        EXPECTED: User should be navigated to SYC team selection page
        """
        # covered in above step

    def test_005_verify_your_selected_team_is_highlighted(self):
        """
        DESCRIPTION: Verify your selected Team is highlighted
        EXPECTED: Previously subscribed team should be highlighted
        """
        self.__class__.teams = self.site.show_your_colors.items_as_ordered_dict
        aston_villa = self.teams[vec.fanzone.TEAMS_LIST.aston_villa.title()]
        self.assertTrue(aston_villa.is_highlighted(),
                        msg=f'previously subscribed team {aston_villa} is not highlighted')

    def test_006_select_any_team(self):
        """
        DESCRIPTION: Select any team
        EXPECTED: User should get a change team popup
        EXPECTED: Popup should have below:
        EXPECTED: 1. Tittle : "Change Team"
        EXPECTED: 2. Message: " You signed upâ€‹less than 30 days ago you will need toâ€‹ wait until the 30 days expire to change your team.â€‹"
        EXPECTED: 3. CTA button:  "EXIT"
        """
        self.teams[vec.fanzone.TEAMS_LIST.manchester_united.title()].click()
        dialog_change_team = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_CHANGE_TEAM)
        self.assertTrue(dialog_change_team, msg=" Change team pop is not displayed")
        self.assertEqual(dialog_change_team.name, vec.dialogs.DIALOG_MANAGER_CHANGE_TEAM,
                         msg=f'Actual title "{dialog_change_team.name}" is not same as Expected title "{vec.dialogs.DIALOG_MANAGER_CHANGE_TEAM}"')
        self.assertEqual(dialog_change_team.description, vec.fanzone.CHANGE_TEAM_MESSAGE,
                         msg=f'Actual change team message "{dialog_change_team.description}" is not same as Expected change team message "{vec.fanzone.CHANGE_TEAM_MESSAGE}"')
        self.assertTrue(dialog_change_team.exit_button, msg=" EXIT button is not displayed")
