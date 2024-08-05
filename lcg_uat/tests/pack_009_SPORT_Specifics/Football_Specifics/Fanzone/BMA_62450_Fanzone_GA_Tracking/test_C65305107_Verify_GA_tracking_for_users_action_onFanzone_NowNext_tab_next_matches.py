import pytest
from time import sleep
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_prod # can't create events in prod and Beta
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305107_Verify_GA_tracking_for_users_action_onFanzone_NowNext_tab_next_matches(BaseDataLayerTest):
    """
    TR_ID: C65305107
    NAME: Verify GA tracking for user's action on A Fanzone Now&Next tab - next matches
    DESCRIPTION: This test case is to verify GA tracking for user's action on Fanzone Now&Next tab: next matches
    PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC Entry points in front end
    PRECONDITIONS: 2) Create fanzone tabs: now&next, stats and clubs
    PRECONDITIONS: 3) Create surface bets, HC and outrights data for fanzone
    PRECONDITIONS: 4) User has subscribed to Fanzone
    PRECONDITIONS: 5) User should be logged in state
    """
    keep_browser_open = True

    def fanzone_subscription(self):
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username, timeout=30)
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
        sleep(7)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        wait_for_result(lambda: dialog_alert.exit_button.is_displayed(), timeout=5,
                        name='"EXIT" button to be displayed.')
        dialog_alert.exit_button.click()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC Entry points in front end
        PRECONDITIONS: 2) Create fanzone tabs: now&next, stats and clubs
        PRECONDITIONS: 3) Create surface bets, HC and outrights data for fanzone
        PRECONDITIONS: 4) User has subscribed to Fanzone
        PRECONDITIONS: 5) User should be logged in state
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        home_team = vec.fanzone.TEAMS_LIST.aston_villa.title()
        away_team = vec.fanzone.TEAMS_LIST.brentford.title()
        astonVilla_fanzone = self.cms_config.get_fanzone(home_team)
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(home_team)
        self.ob_config.create_fanzone_league_event_id(
            league_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
            home_team=home_team,
            away_team=away_team,
            home_team_external_id=self.ob_config.football_config.fanzone_external_id.aston_villa,
            away_team_external_id=self.ob_config.football_config.fanzone_external_id.brentford)
        self.fanzone_subscription()

    def test_001_launch_application_and_click_on_any_fanzone_entry_point(self):
        """
        DESCRIPTION: Launch application and click on any fanzone entry point
        EXPECTED: User should be navigated to fanzone now&next tab
        """
        self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")
        fanzone_banner = self.site.home.fanzone_banner()
        fanzone_banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=30,
                        name='"Fanzone tab menus" to be displayed.')
        sleep(5)
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_002_navigate_to_next_matcheshighlight_carousel_and_add_any_selection_to_quick_bet_or_betslipand_check_ga_tracking(self):
        """
        DESCRIPTION: Navigate to Next matches(Highlight carousel) and add any selection to quick bet or betslip
        DESCRIPTION: and check GA tracking
        EXPECTED: The tag should be contain
        """
        sleep(3)
        self.device.refresh_page()
        self.site.fanzone.tabs_menu.click_button(button_name='NOW & NEXT')
        carousel = list(self.site.fanzone.tab_content.highlight_carousels.values())[0]
        events = carousel.items_as_ordered_dict
        self.assertTrue(events, msg="Events are not found under Now and Next tab")
        event = list(events.values())[0]
        bet_button = list(event.items_as_ordered_dict.values())[0]
        bet_button.click()

        if self.device_type == 'mobile':
            sleep(5)
            actual_response = self.get_data_layer_specific_object(object_key='eventAction',
                                                                  object_value="add to quickbet")
        else:
            actual_response = self.get_data_layer_specific_object(object_key='eventAction',
                                                                  object_value="add to betslip")
        response = actual_response[u'ecommerce']['add']['products'][0]['dimension64']
        self.assertEqual(response, 'Fanzone',
                         msg=f'{actual_response} is not same as '
                             f'"Dimension64" tag should contain "Fanzone"')
