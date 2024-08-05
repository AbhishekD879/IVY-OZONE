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
class Test_C65304882_To_verify_user_should_be_able_to_see_surface_bets_related_to_respective_team_selected_in_syc(Common):
    """
    TR_ID: C65304882
    NAME: To verify user should be able to see surface bets related to respective team selected in syc
    DESCRIPTION: To verify user should be able to see surface bets related to respective team selected in syc
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)Surface bets are created with with below data:
    PRECONDITIONS: 1)Offer content 2)Dynamic price button 3)was price, making it fanzone inclusion in CMS- for eg:Everton team
    PRECONDITIONS: 4)User has logged into application and navigated to Fanzone page
    """
    keep_browser_open = True
    price_num = 1
    price_den = 2

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3)Surface bets are created with with below data:
        PRECONDITIONS: 1)Offer content 2)Dynamic price button 3)was price, making it fanzone inclusion in CMS- for eg:Everton team
        PRECONDITIONS: 4)User has logged into application and navigated to Fanzone page
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
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
            event_type_id = event['event']['typeId']
            if astonVilla_fanzone['active'] is not True:
                if 'beta' in tests.HOSTNAME:
                    self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(),
                                                   typeId=event_type_id)
                else:
                    raise SiteServeException(f'Fanzone is not active for Aston Villa on Prod')
        else:
            if not fanzone_status.get('enabled'):
                self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                      field_name='enabled',
                                                                      field_value=True)
            event = self.ob_config.add_autotest_premier_league_football_event()
            selection_id = event.selection_ids[event.team1]
            event_type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
            if astonVilla_fanzone['active'] is not True:
                self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(),
                                               typeId=event_type_id)

        self.__class__.surface_bet = self.cms_config.add_fanzone_surface_bet(selection_id=selection_id,
                                                                             priceNum=1,
                                                                             priceDen=2)

        username = self.gvc_wallet_user_client.register_new_user().username
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
        # banner = self.site.home.fanzone_banner()
        # banner.let_me_see.click()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)

    def test_002_verify_if_user_is_able_to_see_surface_bet_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify if user is able to see Surface bet in Now and Next tab
        EXPECTED: User should be able to see Surface bets in Now and Next tab only for the Team user has selected in SYC , not for another team
        """
        self.assertTrue(self.site.fanzone.tab_content.has_surface_bets(),
                        msg=f'Surface Bets are not shown on Fanzone page')
        surface_bet_name = self.surface_bet['title'].upper()
        surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
        self.assertIn(surface_bet_name, surface_bets,
                      msg=f'Created surface bet "{surface_bet_name}" is not present in "{surface_bets}"')
