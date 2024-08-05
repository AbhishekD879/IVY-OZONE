import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_prod     # not configured in prod and Beta
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65304889_To_Verify_Special_Surface_Bets_in_Fanzone_page(Common):
    """
    TR_ID: C65304889
    NAME: To Verify Special Surface Bets in Fanzone page
    DESCRIPTION: To Verify Special Surface Bets in Fanzone page
    PRECONDITIONS: 1) Evens should be created and Special Marktes should be configured in Open Bet
    PRECONDITIONS: Event Creation-->Market Creation page--> Flags section-> Enable FANZONE checkbox
    PRECONDITIONS: 2) User should be Logged into applicaion
    PRECONDITIONS: 3) User should be navigated to Fanzone
    PRECONDITIONS: 4) Fanzone should be enabled in CMS-->System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 5) User should be in Fanzone page
    PRECONDITIONS: 6) Special Market selections should be configured as Surface bet via Sports Categeries-->Fanzone-->Surface Bets
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
        PRECONDITIONS: 5) User should be in Fanzone page
        PRECONDITIONS: 6) Special Market selections should be configured as Surface bet via Sports Categeries-->Fanzone-->Surface Bets
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
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

        self.__class__.surface_bet = self.cms_config.add_fanzone_surface_bet(selection_id=selection_id,
                                                                             priceNum=self.price_num,
                                                                             priceDen=self.price_den)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username, timeout=30)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30)
        dialog_fb.imin_button.click()
        results = wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict, timeout=30,
                                  name='All Teams to be displayed')
        self.assertTrue(results, msg='Teams are not displayed')
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_verify_special_bets_are_populated_in_fanzone_page(self):
        """
        DESCRIPTION: Verify Special Bets are populated in Fanzone page
        EXPECTED: Special bets should be populated in Fanzone page
        """
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)
        self.assertTrue(self.site.fanzone.tab_content.has_surface_bets(),
                        msg=f'Surface Bets are not shown on Fanzone page')

    def test_002_position_of_special_bets_are_same_surface_bets(self):
        """
        DESCRIPTION: Position of Special Bets are same surface Bets
        EXPECTED: Position of Special Bets should be same as Surface Bets
        """
        surface_bet_name = self.surface_bet['title'].upper()
        surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
        self.assertIn(surface_bet_name, surface_bets,
                      msg=f'Created surface bet "{surface_bet_name}" is not present in "{surface_bets}"')
