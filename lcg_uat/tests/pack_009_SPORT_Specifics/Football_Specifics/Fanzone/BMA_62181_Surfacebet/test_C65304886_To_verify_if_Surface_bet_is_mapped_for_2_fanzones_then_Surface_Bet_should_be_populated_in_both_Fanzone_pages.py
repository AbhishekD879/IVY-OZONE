import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from time import sleep


@pytest.mark.lad_stg2
# @pytest.mark.lad_tst2     # Not configured in tst2
# @pytest.mark.lad_prod     # not configured in prod and Beta
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65304886_To_verify_if_Surface_bet_is_mapped_for_2_fanzones_then_Surface_Bet_should_be_populated_in_both_Fanzone_pages(Common):
    """
    TR_ID: C65304886
    NAME: To verify if Surface bet is mapped for 2 fanzone's, then Surface Bet should be populated in both Fanzone pages
    DESCRIPTION: To verify if Surface bet is mapped for 2 fanzone's, then Surface Bet should be populated in both Fanzone pages
    """
    keep_browser_open = True

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3)Surface bets are created with below data:
        PRECONDITIONS: 1)Offer content 2)Dynamic price button 3)was price, making it fanzone inclusion in cms-2 teams for eg:Everton team and Liverpool
        PRECONDITIONS: 4)User has logged into application and navigated to Fanzone page
        """
        if tests.settings.backend_env != 'prod':
            fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
            if not fanzone_status.get('enabled'):
                self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                      field_name='enabled',
                                                                      field_value=True)
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.selection_id = event.selection_ids[event.team1]
            self.__class__.surface_bet = self.cms_config.add_fanzone_surface_bet(selection_id=self.selection_id,
                                                                                 priceNum=1,
                                                                                 priceDen=2)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.__class__.user_2 = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport('football', fanzone=True)
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
        sleep(2)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_verify_user_is_able_to_see_now_and_next_tab_in_fanzone_page(self):
        """
        DESCRIPTION: Verify user is able to see Now and Next tab in Fanzone page
        EXPECTED: User should be able to see Now and Next Tab in Fanzone page
        """
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu, msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)

    def test_002_verify_if_the_surface_bets_are_shown_in_now_and_next_tab_for_everton_team(self):
        """
        DESCRIPTION: verify if the surface bets are shown in Now and Next tab For Everton team
        EXPECTED: User should be able to see surface bets in Now and Next tab
        """
        self.assertTrue(self.site.fanzone.tab_content.has_surface_bets(),
                        msg=f'Surface Bets are not shown on Fanzone page')
        surface_bet_name = self.surface_bet['title'].upper()
        self.surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
        self.assertIn(surface_bet_name, self.surface_bets, msg=f'Created surface bet "{surface_bet_name}" is not present in "{self.surface_bets}"')

    def test_003_now_logout_and_login_with_a_user_having_liverpool_team_selected_in_syc(self):
        """
        DESCRIPTION: Now logout and login with a user having Liverpool team selected in SYC
        EXPECTED: User should be able to login with Liverpool credentials
        """
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(),
                        msg='User has not logged out!')
        self.site.login(username=self.user_2)
        self.site.open_sport('football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I Am In Button is displayed',
                        timeout=5)
        teams = list(self.site.show_your_colors.items_as_ordered_dict.values())
        teams[2].scroll_to_we()
        teams[2].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(2)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_004_navigate_fanzone_page_and_verify_if_surface_bets_are_shown_in_now_and_next_tab(self):
        """
        DESCRIPTION: Navigate Fanzone page and verify if surface bets are shown in now and next tab
        EXPECTED: User should be able to see surface bets in Now and Next tab
        """
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu, msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)
        self.assertTrue(self.site.fanzone.tab_content.has_surface_bets(),
                        msg=f'Surface Bets are not shown on Fanzone page')
        surface_bet_name = self.surface_bet['title'].upper()
        self.surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
        self.assertIn(surface_bet_name, self.surface_bets, msg=f'Created surface bet "{surface_bet_name}" is not present in "{self.surface_bets}"')
