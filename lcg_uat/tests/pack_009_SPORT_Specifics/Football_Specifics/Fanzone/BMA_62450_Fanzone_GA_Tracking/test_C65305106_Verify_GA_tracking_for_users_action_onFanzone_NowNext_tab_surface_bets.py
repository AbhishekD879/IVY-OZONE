import pytest
import tests
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
# @pytest.mark.lad_tst2 # Not configured in tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305106_Verify_GA_tracking_for_users_action_onFanzone_NowNext_tab_surface_bets(BaseDataLayerTest):
    """
    TR_ID: C65305106
    NAME: Verify GA tracking for user's action onÂ Fanzone Now&Next tab: surface bets
    DESCRIPTION: This test case is to verify GA tracking for user's action on Fanzone Now&Next tab: surface bets
    PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC Entry points in front end
    PRECONDITIONS: 2) Create fanzone tabs: now&next, stats and clubs
    PRECONDITIONS: 3) Create surface bets, HC and outrights data for fanzone
    PRECONDITIONS: 4) User has subscribed to Fanzone
    PRECONDITIONS: 5) User should be logged in state
    """
    keep_browser_open = True
    price_num = 1
    price_den = 2
    selection_price = '4/5'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User has access to CMS
        PRECONDITIONS: Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
        PRECONDITIONS: User has FE url and Valid credentials to Login Lads FE
        PRECONDITIONS: User has completed the Fanzone Syc successfully in FE
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(event_selection.values())[0]
            event_type_id = event['event']['typeId']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            selection_id = event.selection_ids[event.team1]
            event_type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id

        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(),
                                           typeId=event_type_id)
        self.__class__.surface_bet = self.cms_config.add_fanzone_surface_bet(selection_id=selection_id,
                                                                             priceNum=self.price_num,
                                                                             priceDen=self.price_den)
        self.__class__.surface_bet_name = self.surface_bet['title'].upper()
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        results = wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict, timeout=30,
                                  name='All Teams to be displayed')
        self.assertTrue(results, msg='Teams are not displayed')
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        wait_for_result(lambda: dialog_confirm.confirm_button.is_displayed(), timeout=10,
                        name='"CONFIRM" button to be displayed.')
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        wait_for_result(lambda: dialog_alert.exit_button.is_displayed(), timeout=5,
                        name='"EXIT" button to be displayed.')
        dialog_alert.exit_button.click()

    def test_001_launch_application_and_click_on_any_fanzone_entry_point(self):
        """
        DESCRIPTION: Launch application and click on any fanzone entry point
        EXPECTED: User should be navigated to fanzone now&next tab
        """
        fanzone_banner = self.site.home.fanzone_banner()
        fanzone_banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_002_navigate_to_surface_bet_and_add_any_selection_to_quick_bet_or_betslipand_check_ga_tracking(self):
        """
        DESCRIPTION: Navigate to surface bet and add any selection to quick bet or betslip
        DESCRIPTION: and check GA tracking
        EXPECTED: The tag should be contain "Dimension64":<bet-location>,eg://fanzone
        """
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.fanzone.tab_content.has_surface_bets(),
                        msg=f'Surface Bets are not shown on Fanzone page')
        surface_bet_name = self.surface_bet['title'].upper()
        surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
        self.assertIn(surface_bet_name, surface_bets,
                      msg=f'Created surface bet "{surface_bet_name}" is not present in "{surface_bets}"')
        surface_bet = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict[self.surface_bet_name]
        surface_bet.bet_button.click()
        sleep(2)
        if self.device_type == 'mobile':
            actual_response = self.get_data_layer_specific_object(object_key='eventAction',
                                                                  object_value="add to quickbet")
        else:
            actual_response = self.get_data_layer_specific_object(object_key='eventAction',
                                                                  object_value="add to betslip")
        actual_response = actual_response[u'ecommerce']['add']['products'][0]['dimension64']
        self.assertEqual(actual_response, "Fanzone",
                         msg=f'{actual_response} is not same as '
                             f'"Dimension64" tag should contain "fanzone"')
