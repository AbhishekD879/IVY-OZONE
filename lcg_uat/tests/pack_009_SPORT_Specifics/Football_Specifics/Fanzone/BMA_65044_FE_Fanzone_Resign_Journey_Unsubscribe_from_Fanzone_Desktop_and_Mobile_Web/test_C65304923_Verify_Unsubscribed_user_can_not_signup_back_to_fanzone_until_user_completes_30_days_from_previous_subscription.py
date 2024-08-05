import tests
import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from time import sleep
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_prod # Cannot create leagues on prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65304923_Verify_Unsubscribed_user_can_not_signup_back_to_fanzone_until_user_completes_30_days_from_previous_subscription(Common):
    """
    TR_ID: C65304923
    NAME: Verify Unsubscribed user can not signup back to fanzone until user completes 30 days from previous subscription
    DESCRIPTION: Verify Unsubscribed user can not signup back to fanzone until user completes 30 days from previous subscription
    PRECONDITIONS: 1) User has logged into lads application
    PRECONDITIONS: 2) User has Unsubscribed to Fanzone less than 30 days ago
    PRECONDITIONS: 3) Configure fanzone data in CMS
    PRECONDITIONS: CMS-->Fanzone-->Fanzones
    PRECONDITIONS: 4) In System Config Fanzone should be enabled
    PRECONDITIONS: 5) User is in SYC page.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User has logged into lads application
        PRECONDITIONS: 2) User has subscribed to Fanzone Previously
        PRECONDITIONS: 3) Configure fanzone data in CMS
        PRECONDITIONS: CMS-->Fanzone-->Fanzones
        PRECONDITIONS: 4) In System Config Fanzone should be enabled
        PRECONDITIONS: 5) All entry points for each and every Fanzone team should be enabled
        PRECONDITIONS: 6) User is in Fanzone Page
        PRECONDITIONS: Note: User could navigate to Fanzone page through any of the 4 entry points
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state(state_name='HomePage')
        sleep(3)
        self.site.login(username=username)
        self.site.open_sport(name='Football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Fanzones are displayed',
                        timeout=5)
        fanzone = self.site.show_your_colors.items_as_ordered_dict
        fanzone[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        sleep(3)
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_teamalert.exit_button.click()
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")
        if tests.settings.device_type == "mobile":
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.get(vec.racing.RACING_HIGHLIGHTS_TAB_NAME).click()
        self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")
        fanzone_banner = self.site.home.fanzone_banner()
        fanzone_banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')
        self.site.fanzone.setting_link.click()
        sleep(4)
        self.dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        self.dialog_teamalert.toggle_switch.click()
        sleep(3)
        dialog_unsubscribe_fanzone = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_UNSUBSCRIBE_FROM_FANZONE)
        dialog_unsubscribe_fanzone.confirm_button.click()
        self.site.wait_content_state("homepage")
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        promo = promotions[vec.fanzone.PROMOTION_TITLE]
        promo.more_info_button.click()
        self.site.wait_content_state(state_name='PromotionDetails')
        promotion_details = self.site.promotion_details.tab_content.promotion
        fz_syc_button = promotion_details.detail_description.fanzone_syc_button
        fz_syc_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')

    def test_001_verify_no_team_is_highlighted_as_user_is_unsubscribed_from_fanzone(self):
        """
        DESCRIPTION: Verify no team is highlighted, as user is unsubscribed from Fanzone
        EXPECTED: No team should be highlighted
        """
        self.__class__.teams = list(self.site.show_your_colors.items_as_ordered_dict.values())
        self.assertFalse(self.teams[1].is_highlighted(), msg='Subscribed team is highlighted')

    def test_002_select_any_team(self):
        """
        DESCRIPTION: Select any team
        EXPECTED: CHANGE TEAM popup should display
        """
        self.teams[2].scroll_to_we()
        self.teams[2].click()
        self.__class__.dialog_change_team = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_CHANGE_TEAM, timeout=5)
        self.assertTrue(self.dialog_change_team, msg='Change team popup not appeared')

    def test_003_verify_below_details_in_change_team_popuptitle_change_teampopup_text__you_signed_up_less_than_30_days_ago_you_will_need_to_wait_until_the_30_days_expire_to_change_your_teamselected_team_jersey_and_team_name_underneath_thatcta_exit(self):
        """
        DESCRIPTION: Verify below details in CHANGE TEAM popup
        DESCRIPTION: Title: CHANGE TEAM
        DESCRIPTION: Popup text : You signed upâ€‹ less than 30 days ago you will need toâ€‹ wait until the 30 days expire to change your team.
        DESCRIPTION: Selected team jersey and team name underneath that
        DESCRIPTION: CTA: EXIT
        EXPECTED: All the listed information should display
        """
        self.assertTrue(self.dialog_change_team,
                        msg=f'"{vec.dialogs.DIALOG_MANAGER_CHANGE_TEAM}" dialog is not displayed')
        self.assertEqual(self.dialog_change_team.description, vec.fanzone.CHANGE_TEAM_MESSAGE,
                         msg=f'Actual change team message "{self.dialog_change_team.description}" is not same as Expected change team message "{vec.fanzone.CHANGE_TEAM_MESSAGE}"')
        self.assertTrue(self.dialog_change_team.exit_button, msg=" EXIT button is not displayed")

    def test_004_click_on_exit_cta(self):
        """
        DESCRIPTION: Click on EXIT CTA
        EXPECTED: Pop Up will Disappear
        """
        self.dialog_change_team.exit_button.click()
        dialog_closed = self.dialog_change_team.wait_dialog_closed(timeout=20)
        self.assertTrue(dialog_closed, msg='Change Team dialog was not closed')
