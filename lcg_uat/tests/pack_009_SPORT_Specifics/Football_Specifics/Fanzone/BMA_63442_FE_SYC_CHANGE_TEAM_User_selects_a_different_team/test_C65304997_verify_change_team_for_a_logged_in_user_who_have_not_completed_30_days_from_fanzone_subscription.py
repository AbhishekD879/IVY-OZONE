import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C65304997_verify_change_team_for_a_logged_in_user_who_have_not_completed_30_days_from_fanzone_subscription(Common):
    """
    TR_ID: C65304997
    NAME: verify  change team  for a logged in user who have not completed 30 days from fanzone subscription
    DESCRIPTION: This test case is to verify change team  for a logged in user who have not completed 30 days from fanzone subscription
    PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
    PRECONDITIONS: 2) User should be logged into ladbroks
    PRECONDITIONS: 3) User should subscribe to fanzone and not compled 30 days
    PRECONDITIONS: 4) User should be  in SYC promotion page
    """
    keep_browser_open = True

    def test_000_precondition(self):
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport('Football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I Am In Button is displayed',
                        timeout=5)
        teams = list(self.site.show_your_colors.items_as_ordered_dict.values())
        teams[1].scroll_to_we()
        teams[1].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        promo = promotions[vec.fanzone.PROMOTION_TITLE]
        promo.more_info_button.click()
        # self.site.wait_content_state(state_name='PromotionDetails')

    def test_001_click_on_cta_button_in_promotion(self):
        """
        DESCRIPTION: Click on CTA button in promotion
        EXPECTED: User should  be navigated to SYC team selection page
        """
        promotion_details = self.site.promotion_details.tab_content.promotion
        fz_syc_button = promotion_details.detail_description.fanzone_syc_button
        fz_syc_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')

    def test_002_check_team_selection_page(self):
        """
        DESCRIPTION: Check Team selection page
        EXPECTED: Previously subscribed team should be in highlighted box
        """
        self.__class__.teams = list(self.site.show_your_colors.items_as_ordered_dict.values())
        self.assertTrue(self.teams[1].is_highlighted(), msg='Subscribed team is not highlighted')

    def test_003_click_on_any_other_team_tile(self):
        """
        DESCRIPTION: Click on any other team tile
        EXPECTED: User should get change team popup
        """
        self.teams[2].scroll_to_we()
        self.teams[2].click()
        self.__class__.dialog_change_team = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_CHANGE_TEAM, timeout=5)
        self.assertTrue(self.dialog_change_team, msg='Change team popup not appeared')

    def test_004_click_on_exit__button(self):
        """
        DESCRIPTION: Click on exit  button
        EXPECTED: Popup should be disappeared.
        """
        self.dialog_change_team.exit_button.click()
        self.assertFalse(self.dialog_change_team.has_exit_button(expected_result=False), msg='Change team popup is still displayed with title')
