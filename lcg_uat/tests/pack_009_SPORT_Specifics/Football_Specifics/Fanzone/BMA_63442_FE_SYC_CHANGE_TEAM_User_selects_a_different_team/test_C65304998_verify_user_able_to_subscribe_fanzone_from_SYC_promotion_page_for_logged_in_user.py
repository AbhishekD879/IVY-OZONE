import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
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
class Test_C65304998_verify_user_able_to_subscribe_fanzone_from_SYC_promotion_page_for_logged_in_user(Common):
    """
    TR_ID: C65304998
    NAME: verify user able to subscribe fanzone from SYC promotion page for logged in user
    DESCRIPTION: This test case is to verify  user able to subscribe fanzone from SYC promotion page for logged in user
    PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
    PRECONDITIONS: 2) User should be logged into ladbroks
    PRECONDITIONS: 3) User not  subscribed to fanzone
    PRECONDITIONS: 4) User should be  in SYC promotion page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
        PRECONDITIONS: 2) User should be logged into ladbroks
        PRECONDITIONS: 3) User not  subscribed to fanzone
        PRECONDITIONS: 4) User should be  in SYC promotion page
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)

        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')
        username = self.gvc_wallet_user_client.register_new_user().username
        sleep(3)
        self.site.login(username=username)
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')

    def test_001_click_on_cta_button_in_promotion(self):
        """
        DESCRIPTION: Click on CTA button in promotion
        EXPECTED: User should  be navigated to SYC team selection page
        """
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No promotions found on page')
        promo = promotions[vec.fanzone.PROMOTION_TITLE + '!'] if not tests.settings.backend_env == 'prod' else promotions[vec.fanzone.PROMOTION_TITLE]
        promo.more_info_button.click()
        # self.site.wait_content_state(state_name='PromotionDetails')

    def test_002_check_team_selection_page(self):
        """
        DESCRIPTION: Check Team selection page
        EXPECTED: Team selection page should be diaplyed with all available team tiles
        """
        promotion_details = self.site.promotion_details.tab_content.promotion
        fz_syc_button = promotion_details.detail_description.fanzone_syc_button
        fz_syc_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')
        sleep(3)

    def test_003_select__team_tile(self):
        """
        DESCRIPTION: Select  team tile
        EXPECTED: The selected team tile should be highlighted and gets confiramtion popup
        """
        team = self.site.show_your_colors.items_as_ordered_dict.get(vec.fanzone.TEAMS_LIST.aston_villa.title())
        team.click()
        team_ui_box_border = team.css_property_value('border').split(" ")[0]
        self.assertEqual(team_ui_box_border, vec.fanzone.SYC_SELECTED_TEAM_BORDER,
                         msg=f'Team UI box border is not equal to Zepplin team box border'
                             f'actual result "{team_ui_box_border}"')
        self.__class__.dialog_confirm = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION,
            verify_name=False)
        self.assertTrue(self.dialog_confirm,
                        msg='login popup not appeared')

    def test_004_click_on_confirm_button(self):
        """
        DESCRIPTION: Click on confirm Button
        EXPECTED: Desktop:
        EXPECTED: User selection will store in BE and User navigate to SYC promotion page
        EXPECTED: Mobile:
        EXPECTED: User selection will store in BE and User navigate to preference centre screen
        """
        self.dialog_confirm.confirm_button.click()
        sleep(4)
        dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_teamalert.exit_button.click()
        self.site.wait_content_state(state_name='fanzoneevents')
