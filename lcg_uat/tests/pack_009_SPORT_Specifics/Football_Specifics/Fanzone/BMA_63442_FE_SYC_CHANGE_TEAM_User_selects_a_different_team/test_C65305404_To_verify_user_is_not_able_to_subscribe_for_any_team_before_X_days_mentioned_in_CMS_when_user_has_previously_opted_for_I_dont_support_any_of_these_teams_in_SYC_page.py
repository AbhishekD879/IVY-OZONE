import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.hl # not configured in prod and Beta
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone_reg_tests
@pytest.mark.desktop
@vtest
class Test_C65305404_To_verify_user_is_not_able_to_subscribe_for_any_team_before_X_days_mentioned_in_CMS_when_user_has_previously_opted_for_I_dont_support_any_of_these_teams_in_SYC_page(Common):
    """
    TR_ID: C65305404
    NAME: To verify user is not able to subscribe for any team before X days mentioned in CMS when user has previously opted for ' I don't support any of these teams' in SYC page
    DESCRIPTION: This test case is to verify user is not able to subscribe for any team  before X days mentioned in CMS when user has previously opted for ' I don't support any of these teams' in SYC page
    PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
    PRECONDITIONS: 2) User should be logged into ladbroks
    PRECONDITIONS: 3) User should subscribe to I DONT SUPPORT ANY OF THE TEAM and should not completed X  days as configured for REMIND ME LATER
    PRECONDITIONS: 4) User should be  in SYC promotion page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
        PRECONDITIONS: 2) User should be logged into ladbroks
        PRECONDITIONS: 3) User should subscribe to I DONT SUPPORT ANY OF THE TEAM and should not completed X  days as configured for REMIND ME LATER
        PRECONDITIONS: 4) User should be  in SYC promotion page
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
        self.site.open_sport('FOOTBALL', fanzone=True, timeout=10)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              verify_name=False)
        dialog_fb.imin_button.click()
        self.site.wait_content_state_changed(timeout=20)
        self.__class__.i_dont_support_any_teams = self.site.show_your_colors.i_dont_support_any_teams
        wait_for_result(lambda: self.site.show_your_colors.scroll_to_we(self.i_dont_support_any_teams), timeout=15)
        sleep(5)
        self.i_dont_support_any_teams.click()
        self.__class__.dialog = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_DONT_SUPPORT_ANY_OF_THESE_TEAMS,
            verify_name=False)
        self.dialog.select_custom_team_name_input = vec.fanzone.TEAMS_LIST.aston_villa
        self.assertTrue(self.dialog.select_custom_team_name_input,
                        msg='Choice name has not entered')
        self.dialog.confirm_button.click()
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')
        self.navigate_to_page('promotions', test_automation=False)
        self.site.wait_content_state(state_name='Promotions')
        self.__class__.promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(self.promotions, msg='No promotions found on page')

    def test_001_click_on_cta_button_in_promotion(self):
        """
        DESCRIPTION: Click on CTA button in promotion
        EXPECTED: User should  be navigated to SYC team selection page
        """
        promo = self.promotions[vec.fanzone.PROMOTION_TITLE]
        promo.more_info_button.click()
        # self.site.wait_content_state(state_name='PromotionDetails')
        promotion_details = self.site.promotion_details.tab_content.promotion
        fz_syc_button = promotion_details.detail_description.fanzone_syc_button
        fz_syc_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')
        sleep(3)

    def test_002_select_any__team_tile(self):
        """
        DESCRIPTION: Select any  team tile
        EXPECTED: Change Team popup should display
        """
        self.__class__.team = vec.fanzone.TEAMS_LIST.manchester_city.title()
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[self.team].scroll_to_we()
        teams[self.team].click()

    def test_003_verify_popup(self):
        """
        DESCRIPTION: Verify popup
        EXPECTED: Below content should display in popup
        EXPECTED: Title: Team confirmation
        EXPECTED: Popup text: By CONFIRMING that you are a supporter of​ < TEAM >  you will not be able to change​ your team for another 30 days.On the next screen you can tell us which​ FANZONE notifications you want to receive
        EXPECTED: CTA:  select different team & confirm
        """
        cms_syc_details = self.cms_config.get_fanzone_syc()
        days_to_change_team = cms_syc_details['daysToChangeTeam']
        dialog_confirm = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        self.assertTrue(dialog_confirm, msg='Team confirmation pop-up is not appeared')
        if self.device_type == "mobile":
            expected_msg = vec.fanzone.TEAMS_CONFIRMATION_MESSAGE_MOBILE.format(team_name=self.team,
                                                                                duration=days_to_change_team)
        else:
            expected_msg = vec.fanzone.TEAMS_CONFIRMATION_MESSAGE_DESKTOP.format(team_name=self.team,
                                                                                 duration=days_to_change_team)
        self.assertEqual(dialog_confirm.description, expected_msg,
                         msg=f'Actual msg "{dialog_confirm.description}"is not same as expected msg"{expected_msg}"')
        self.assertTrue(dialog_confirm.select_different_button, msg='select different team CTA is not displayed')
        self.assertTrue(dialog_confirm.confirm_button, msg='select different team CTA is not displayed')
