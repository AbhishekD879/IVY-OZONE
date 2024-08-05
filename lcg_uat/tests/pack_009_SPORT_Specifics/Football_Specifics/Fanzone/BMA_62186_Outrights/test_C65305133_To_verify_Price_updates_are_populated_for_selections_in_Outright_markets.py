import pytest

from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_prod     # not configured in prod and Beta
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305133_To_verify_Price_updates_are_populated_for_selections_in_Outright_markets(Common):
    """
    TR_ID: C65305133
    NAME: To verify Price updates are populated for selections in Outright markets
    DESCRIPTION: To verify Price updates are populated for selections in Outright markets
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)Outright markets are created with Premier league participating teams as selections for Various type such 442,438 etc.
    PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
    PRECONDITIONS: 5) User has subscribed to Fanzone
    PRECONDITIONS: 6) User is navigated to Fanzone page
    """
    keep_browser_open = True
    teamname = vec.fanzone.TEAMS_LIST.aston_villa.title()
    new_price = '7/6'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3) Top Goal Scorer market is created in OB for that type or competition
        PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
        """
        self.site.wait_content_state('Homepage')
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)

        typeId = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        self.cms_config.update_fanzone(self.teamname.title(), str(typeId))
        outright_event = self.ob_config.add_autotest_premier_league_football_outright_event()
        self.__class__.event_name = outright_event.ss_response['event']['name'].upper()
        self.__class__.market_template_id = outright_event.ss_response['event']['children'][0]['market'][
            'templateMarketId']
        self.__class__.selection_name, self.__class__.selection_id = list(outright_event.selection_ids.items())[0]
        self.ob_config.map_fanzone_event_selection_id(selection_id=self.selection_id,
                                                      fanzone_team=self.teamname,
                                                      team_external_id=self.ob_config.football_config.fanzone_external_id.aston_villa)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.navigate_to_page(name='sport/football', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30)

        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Teams to be displayed',
                        timeout=5)
        team = self.site.show_your_colors.items_as_ordered_dict.get(self.teamname.title())
        team.click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(6)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_verify_if_user_is_able_to_see_outright_market_of_his_subscribed_team_alone_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify if user is able to see Outright Market of his subscribed team alone in Now and next Tab
        EXPECTED: User should be able to able to see single outright market of his subscribed team with one odd value in &lt;team&gt; Bets section in Now and Next tab
        """
        fanzone_banner = self.site.home.fanzone_banner()
        fanzone_banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')
        league = self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.get(self.event_name)
        market = list(league.accordions_list.items_as_ordered_dict.values())[0]
        events = market.items_as_ordered_dict
        self.assertTrue(events.keys(), msg='No outright market found')
        bet_button = list(events.values())[0].bet_button
        self.assertTrue(bet_button.name, msg='No odd/price found')

    def test_002_login_to_open_bet__outrights_markets_and_change_the_price_of_one_of_the_selection_of_outright_market(self):
        """
        DESCRIPTION: Login to Open Bet--Outrights markets and change the price of one of the selection of Outright market
        EXPECTED: Should be able to update the price of selection
        """
        self.ob_config.change_price(selection_id=self.selection_id, price=self.new_price)

    def test_003_navigate_to_fanzone_page_in_front_end_and_verify_updated_prices_of_selections_are_populated_in_the_outright_market(self):
        """
        DESCRIPTION: Navigate to Fanzone page in front end and verify updated prices of selections are populated in the outright market
        EXPECTED: Updated prices should be populated
        """
        self.device.refresh_page()
        league = self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.get(self.event_name)
        market = list(league.accordions_list.items_as_ordered_dict.values())[0]
        events = market.items_as_ordered_dict
        self.assertTrue(events.keys(), msg='No outright market found')
        bet_button = list(events.values())[0].bet_button
        self.assertEqual(bet_button.name, self.new_price, msg=f'Actual price "{bet_button.name}" is not '
                                                              f'same as Expected price "{self.new_price}"')
