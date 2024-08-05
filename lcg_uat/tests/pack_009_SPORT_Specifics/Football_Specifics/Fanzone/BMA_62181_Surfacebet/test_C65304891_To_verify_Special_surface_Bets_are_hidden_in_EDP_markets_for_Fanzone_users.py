import voltron.environments.constants as vec
import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from time import sleep


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_prod     # not configured in prod and Beta
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65304891_To_verify_Special_surface_Bets_are_hidden_in_EDP_markets_for_Fanzone_users(Common):
    """
    TR_ID: C65304891
    NAME: To verify Special surface Bets are hidden in EDP markets for Fanzone users
    DESCRIPTION: To verify Special surface Bets are hidden in EDP markets for Fanzone users
    PRECONDITIONS: 1) Evens should be created and Special Marktes should be configured in Open Bet
    PRECONDITIONS: Event Creation-->Market Creation page--> Flags section-> Enable FANZONE checkbox
    PRECONDITIONS: 2) User should be Logged into applicaion
    PRECONDITIONS: 3) User should be navigated to Fanzone
    PRECONDITIONS: 4) Fanzone should be enabled in CMS-->System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 5) Surface Bets should be configured using selections from Special Markets
    PRECONDITIONS: CMS--> Sports Pages--> Sports Categeories--> Fanzone-->Surface Bets
    PRECONDITIONS: 6) User should be in Fanzone page
    """
    keep_browser_open = True
    price_num = 4
    price_den = 9

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1) Evens should be created and Special Marktes should be configured in Open Bet
        PRECONDITIONS: Event Creation-->Market Creation page--> Flags section-> Enable FANZONE checkbox
        PRECONDITIONS: 2) User should be Logged into applicaion
        PRECONDITIONS: 3) User should be navigated to Fanzone
        PRECONDITIONS: 4) Fanzone should be enabled in CMS-->System Configuration--> Structure-->Fanzone
        PRECONDITIONS: 5) Surface Bets should be configured using selections from Special Markets
        PRECONDITIONS: CMS--> Sports Pages--> Sports Categeories--> Fanzone-->Surface Bets
        PRECONDITIONS: 6) User should be in Fanzone page
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score
        event_params = self.ob_config.add_autotest_premier_league_football_event(special=True, default_market_name=market_name)
        self.__class__.event_id = event_params.event_id
        actual_market_name, market_id = \
            next(iter(self.ob_config.market_ids.get(self.event_id).items()))
        selection_id = event_params.selection_ids[event_params.team1]
        market_template_id = next(iter(self.ob_config.football_config.autotest_class.
                                       autotest_premier_league.markets.get(actual_market_name).values()))
        self.ob_config.make_market_special(
            market_id=market_id,
            market_template_id=market_template_id,
            event_id=self.event_id,
            flags='FZ')

        surface_bet = self.cms_config.add_fanzone_surface_bet(selection_id=selection_id,
                                                              priceNum=self.price_num,
                                                              priceDen=self.price_den)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL')
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I Am In Button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        list(teams.values())[1].scroll_to_we()
        list(teams.values())[1].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name='NOW & NEXT')

        self.assertTrue(self.site.fanzone.tab_content.has_surface_bets(),
                        msg=f'Surface Bets are not shown on Fanzone page')
        surface_bet_name = surface_bet['title'].upper()
        surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
        self.assertIn(surface_bet_name, surface_bets,
                      msg=f'Created surface bet "{surface_bet_name}" is not present in "{surface_bets}"')

    def test_001_navigate_to_event_details_page_for_which_special_markets_are_configured(self):
        """
        DESCRIPTION: Navigate to Event details page for which Special Markets are configured
        EXPECTED: User should be navigated to EDP
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails', timeout=20)

    def test_002_verify_special_markets_are_not_displayed_for_fanzone_subscribed_users(self):
        """
        DESCRIPTION: Verify Special Markets are not displayed for Fanzone subscribed users
        EXPECTED: Special Markets are not displayed for Fanzone subscribed users
        """
        markets = self.site.sport_event_details.tab_content.has_no_events_label()
        self.assertTrue(markets, msg='Special markets are displayed')
