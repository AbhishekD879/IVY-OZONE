import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_fixed
from voltron.utils.exceptions.voltron_exception import VoltronException
from selenium.common.exceptions import StaleElementReferenceException


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod    #cannot create special markets in beta/prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65599831_To_Verify_Special_markets_are_displayed_in_EDP_if_Fanzone_flag_is_unchecked_from_OB(Common):
    """
    TR_ID: C65599831
    NAME: To verify special markets are displayed in EDP if Fanzone flag is unchecked from OB
    DESCRIPTION: To Verify Special Surface Bets in Fanzone page
    PRECONDITION:1)User has access to CMS
    PRECONDITION:2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITION:3)Fanzone should be unchecked to respective market.
    PRECONDITION:3)Surface bets are created with with below data:
    PRECONDITION:1)Offer content 2)Dynamic price button 3)was price, marking fanzone inclusion in CMS
    PRECONDITION:4)User has logged into application and navigated to Fanzone page
    """
    keep_browser_open = True
    price_num = 4
    price_den = 7

    def test_000_precondition(self):
        """
        PRECONDITION:1)User has access to CMS
        PRECONDITION:2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
        PRECONDITION:3)Fanzone should be unchecked to respective market.
        PRECONDITION:3)Surface bets are created with with below data:
        PRECONDITION:1)Offer content 2)Dynamic price button 3)was price, marking fanzone inclusion in CMS
        PRECONDITION:4)User has logged into application and navigated to Fanzone page
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score
        event_params = self.ob_config.add_autotest_premier_league_football_event(special=True,
                                                                                 default_market_name=market_name)
        self.__class__.event_id = event_params.event_id
        actual_market_name, market_id = \
            next(iter(self.ob_config.market_ids.get(self.event_id).items()))
        selection_id = event_params.selection_ids[event_params.team1]
        market_template_id = next(iter(self.ob_config.football_config.autotest_class.
                                       autotest_premier_league.markets.get(actual_market_name).values()))
        self.ob_config.make_market_special(
            market_id=market_id,
            market_template_id=market_template_id,
            event_id=self.event_id)

        surface_bet = self.cms_config.add_fanzone_surface_bet(selection_id=selection_id,
                                                              eventIDs=[self.event_id],
                                                              priceNum=self.price_num,
                                                              priceDen=self.price_den, edpOn=True,
                                                              displayOnDesktop=True)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True, timeout=30)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Teams to be displayed')
        teams = self.site.show_your_colors.items_as_ordered_dict
        list(teams.values())[1].scroll_to_we()
        list(teams.values())[1].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION, timeout=30)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS, timeout=30)
        dialog_alert.exit_button.click()

        banner = self.site.home.fanzone_banner(timeout=30)
        banner.let_me_see.click()
        sleep(5)
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name='NOW & NEXT')

        self.assertTrue(self.site.fanzone.tab_content.has_surface_bets(),
                        msg=f'Surface Bets are not shown on Fanzone page')
        self.__class__.surface_bet_name = surface_bet['title'].upper()
        surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
        self.assertIn(self.surface_bet_name, surface_bets,
                      msg=f'Created surface bet "{self.surface_bet_name}" is not present in "{surface_bets}"')

    def test_001_navigate_to_event_details_page_for_which_special_markets_are_configured(self):
        """
        DESCRIPTION: Navigate to Event details page for which Special Markets are configured
        EXPECTED: User should be navigated to EDP
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails', timeout=30)

    @retry(stop=stop_after_attempt(4), wait=wait_fixed(wait=40),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def test_002_verify_special_markets_are_displayed_EDP(self):
        """
        DESCRIPTION: Verify Special Markets are displayed in EDP.
        EXPECTED: Special markets should be displayed in EDP.
        """
        self.device.refresh_page()
        sleep(10)  # CMS changes are taking time to reflect on UI
        self.site.wait_content_state(state_name='EventDetails', timeout=30)
        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='There are no surface bet in the container')
        surface_bet = surface_bets.get(self.surface_bet_name)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_name}" is not found in "{list(surface_bets.keys())}"')
