import pytest
import tests
from crlat_siteserve_client.utils.exceptions import SiteServeException
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
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65304885_To_verify_if_any_surface_bet_is_marked_as_disabled_from_CMS_then_those_surface_bets_should_not_be_displayed_in_Fanzone_page(Common):
    """
    TR_ID: C65304885
    NAME: To verify if any surface bet is marked as disabled from CMS then those surface bets should not be displayed in Fanzone page
    DESCRIPTION: To verify is any surface bet is marked as disabled from CMS then those surface bets should not be displayed in Fanzone page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)Surface bets are created with with below data:
    PRECONDITIONS: 1)Offer content 2)Dynamic price button 3)was price, making it fanzone inclusion in CMS- for eg:Everton team
    PRECONDITIONS: 4)User has logged into application and navigated to Fanzone page
    """
    keep_browser_open = True

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3)Surface bets are created with with below data:
        PRECONDITIONS: 1)Offer content 2)Dynamic price button 3)was price, making it fanzone inclusion in CMS- for eg:Everton team
        PRECONDITIONS: 4)User has logged into application and navigated to Fanzone page
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if tests.settings.backend_env == 'prod':
            if not fanzone_status.get('enabled'):
                if 'beta' in tests.HOSTNAME:
                    self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                          field_name='enabled',
                                                                          field_value=True)
                else:
                    raise SiteServeException(f'Fanzone is not enabled for "{tests.HOSTNAME}"')
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        in_play_event=False,
                                                        all_available_events=True)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(event_selection.values())[0]
        else:
            if not fanzone_status.get('enabled'):
                self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                      field_name='enabled',
                                                                      field_value=True)
            event = self.ob_config.add_autotest_premier_league_football_event()
            selection_id = event.selection_ids[event.team1]

        self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())

        self.__class__.surface_bet = self.cms_config.add_fanzone_surface_bet(selection_id=selection_id,
                                                                             priceNum=1,
                                                                             priceDen=2)

        self.__class__.surface_bet_name = self.surface_bet['title'].upper()
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport('football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I Am In Button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_verify_user_is_able_to_see_now_and_next_tab_in_fanzone_page(self):
        """
        DESCRIPTION: Verify user is able to see Now and Next tab in Fanzone page
        EXPECTED: User should be able to see Now and Next Tab in Fanzone page
        """
        # banner = self.site.home.fanzone_banner()
        # banner.let_me_see.click()    as per the new change, after subscription, we will be in fanzone page only
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)

    def test_002_verify_if_the_surface_bets_are_shown_in_now_and_next_tab(self):
        """
        DESCRIPTION: verify if the surface bets are shown in Now and Next tab
        EXPECTED: User should be able to see surface bets in Now and Next tab
        """
        self.assertTrue(self.site.fanzone.tab_content.has_surface_bets(),
                        msg=f'Surface Bets are not shown on Fanzone page')
        surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
        self.assertIn(self.surface_bet_name, surface_bets,
                      msg=f'Created surface bet "{self.surface_bet_name}" is not present in "{surface_bets}"')

    def test_003_now_login_to_cms_and_disable_some_of_the_surface_bets_created_for_fanzone_page_for_the_particular_team(
            self):
        """
        DESCRIPTION: Now login to CMS and disable some of the surface bets created for Fanzone page for the particular team
        EXPECTED: User should be able to disable/inactive some of the surface bets from CMS
        """
        surface_bet_id = self.surface_bet.get('id')
        self.cms_config.update_surface_bet(surface_bet_id=surface_bet_id, disabled=True)
        sleep(20)
        self.device.refresh_page()

    def test_004_navigate_to_fanzone_fe_and_verify_the_surface_bets_created(self):
        """
        DESCRIPTION: Navigate to Fanzone fe and verify the surface bets
        EXPECTED: Disabled/Inactive surface bets should not be shown in Fanzone fe under Now and Next tab
        """
        sleep(3)
        if self.site.fanzone.tab_content.has_surface_bets():
            self.assertTrue(self.site.fanzone.tab_content.has_surface_bets(),
                            msg=f'Surface Bets are not shown on Fanzone page')
            surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
            self.assertNotIn(self.surface_bet_name, surface_bets,
                             msg=f'Created surface bet "{self.surface_bet_name}" is present in "{surface_bets}"')
        else:
            self.assertFalse(self.site.fanzone.tab_content.has_surface_bets(), msg='Surface bets are displayed')
