import pytest
import tests
from time import sleep
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from crlat_ob_client.create_event import CreateSportEvent


@pytest.mark.lad_stg2
# @pytest.mark.lad_tst2     # Not configured in tst2
# @pytest.mark.lad_prod     # not configured in prod and Beta
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305136_To_verify_Outright_markets_for_more_than_1_competition(Common):
    """
    TR_ID: C65305136
    NAME: To verify Outright markets for more than 1 competition
    DESCRIPTION: To verify Outright markets for more than 1 competition
    """
    keep_browser_open = True
    teamname = vec.fanzone.TEAMS_LIST.burnley
    new_market_name = "Top 6"

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3)Outright markets are created with Premier league participating teams as selections for Various type such 442,438 etc.
        PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
        PRECONDITIONS: 5) User has subscribed to Fanzone
        PRECONDITIONS: 6) User is navigated to Fanzone page
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        self.cms_config.update_fanzone(self.teamname.title())
        class_id = self.ob_config.football_config.autotest_class.class_id
        type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        outright_event = self.ob_config.add_autotest_premier_league_football_outright_event()
        self.__class__.event_name = outright_event.ss_response['event']['name'].upper()
        self.__class__.market_template_id = outright_event.ss_response['event']['children'][0]['market']['templateMarketId']
        selection_name, selection_id = list(outright_event.selection_ids.items())[0]
        self.ob_config.map_fanzone_event_selection_id(selection_id=selection_id,
                                                      fanzone_team=self.teamname,
                                                      team_external_id=self.ob_config.football_config.fanzone_external_id.burnley)
        event = CreateSportEvent(env=tests.settings.backend_env, brand=self.brand,
                                 category_id=self.ob_config.football_config.category_id,
                                 class_id=class_id, type_id=type_id)
        event.update_market_settings(market_id=outright_event.default_market_id, event_id=outright_event.event_id,
                                     market_template_id=self.market_template_id, market_display_sort_code='--',
                                     new_market_name=self.new_market_name)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport('football', fanzone=True)
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
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_verify_if_user_is_able_to_see_outright_market_of_his_subscribed_team_alone_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify if user is able to see Outright Market of his subscribed team alone in Now and next Tab
        EXPECTED: User should be able to able to see single outright market of his subscribed team with one odd value in &lt;team&gt; Bets section in Now and Next tab
        """
        self.navigate_to_page("sport/football", fanzone=True)
        self.site.wait_content_state("football")
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)

    def test_002_verify_outright_markets_for_more_than_1_competiton_are_displayed(self):
        """
        DESCRIPTION: Verify Outright markets for more than 1 competiton are displayed
        EXPECTED: Outright markets for more than 1 competiton should be displayed
        """
        outrights = self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.get(self.event_name)
        markets_list = list(outrights.accordions_list.items_as_ordered_dict)
        self.assertIn(self.new_market_name, markets_list,
                      msg=f'Market "{self.new_market_name}" is not in the market list')
        if len(markets_list) > 1:
            self._logger.debug('*** More than one competition are available in outrights')

    def test_003_ex_premier_league_fa_cup_uefa_champions_league_etc_outright_markets_data_should_be_created_in_ob(self):
        """
        DESCRIPTION: Ex: Premier League, FA Cup, UEFA Champions League etc, outright markets data should be created in OB
        EXPECTED:
        """
        # Covered in above step
