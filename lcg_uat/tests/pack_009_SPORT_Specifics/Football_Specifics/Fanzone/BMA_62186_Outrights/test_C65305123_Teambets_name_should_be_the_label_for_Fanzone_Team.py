import pytest
import tests
from crlat_ob_client.create_event import CreateSportEvent
from voltron.environments import constants as vec
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_prod     # not configured in prod and Beta
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305123_Teambets_name_should_be_the_label_for_Fanzone_Team(Common):
    """
    TR_ID: C65305123
    NAME: <Team>bets name should be the label for Fanzone Team
    DESCRIPTION: Verify <Team>bets name will be updated the Fanzone team user has selected in SYC
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)Outright markets are created with Premier league participating teams as selections for Various type such 442,438 etc.
    PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
    PRECONDITIONS: 5) User has subscribed to Fanzone
    """
    keep_browser_open = True

    def create_market_to_event(self, market_name, selection_name, external_id):
        market_id = self.event.create_market(market_name=market_name,
                                             market_template_id=self.ob_config.football_config.autotest_class.autotest_premier_league.outright_market_template_id,
                                             class_id=self.class_id, event_id=self.outright_event.event_id,
                                             bet_in_run='Y')
        selections_number = 1
        selection_types = ['A'] * selections_number  # actually, selection_types is not needed at all, but otherwise add_selections will fail
        prices = ['%s/%s' % (i + 1, i + 2) for i in range(0, 2)]
        selections = self.event.add_selections(prices=prices,
                                               marketID=market_id,
                                               selection_names=[selection_name],
                                               selection_types=selection_types)
        self.ob_config.map_fanzone_event_selection_id(selection_id=list(selections.values())[0],
                                                      fanzone_team=selection_name,
                                                      team_external_id=external_id)

    def login_select_fanzone(self, fanzone_team):
        if fanzone_team in "burnley":
            fanzone_team = vec.fanzone.TEAMS_LIST.burnley.title()
        elif fanzone_team in "aston_villa":
            fanzone_team = vec.fanzone.TEAMS_LIST.aston_villa.title()
        self.cms_config.update_fanzone(fanzone_team, typeId=str(self.typeId))
        username = self.gvc_wallet_user_client.register_new_user().username
        sleep(3)
        self.site.login(username=username)
        self.navigate_to_page(name='sport/football', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Teams to be displayed',
                        timeout=5)
        team = self.site.show_your_colors.items_as_ordered_dict.get(fanzone_team)
        team.click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3)Outright markets are created with Premier league participating teams as selections for Various type such 442,438 etc.
        PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
        PRECONDITIONS: 5) User has subscribed to Fanzone
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        self.__class__.typeId = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        self.__class__.class_id = self.ob_config.football_config.autotest_class.class_id
        self.__class__.outright_event = self.ob_config.add_autotest_premier_league_football_outright_event()
        self.__class__.event_name = self.outright_event.ss_response['event']['name'].upper()
        self.__class__.event = CreateSportEvent(env=tests.settings.backend_env, brand=self.brand,
                                                category_id=self.ob_config.football_config.category_id,
                                                class_id=self.class_id, type_id=self.typeId)

        self.create_market_to_event(market_name="outright_Team_Bets0",
                                    selection_name=vec.fanzone.TEAMS_LIST.burnley.title(),
                                    external_id=self.ob_config.football_config.fanzone_external_id.burnley)

        self.create_market_to_event(market_name="outright_Team_Bets1",
                                    selection_name=vec.fanzone.TEAMS_LIST.aston_villa.title(),
                                    external_id=self.ob_config.football_config.fanzone_external_id.aston_villa)
        sleep(3)
        self.login_select_fanzone(fanzone_team="burnley")

    def test_001_navigate_to_fanzone_page(self):
        """
        DESCRIPTION: Navigate to Fanzone page
        EXPECTED: User should be navigated to Fanzone page
        """
        fanzone_banner = self.site.home.fanzone_banner()
        fanzone_banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_002_verify_if_user_is_able_to_see_outright_market_of_his_subscribed_team_alone_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify if user is able to see Outright Market of his subscribed team alone in Now and next Tab
        EXPECTED: User should be able to able to see single outright market of his subscribed team with one odd value in &lt;team&gt; Bets section in Now and Next tab
        """
        outright = self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.get(self.event_name)
        market = outright.accordions_list.items_as_ordered_dict.get('outright_Team_Bets0')
        events = market.items_as_ordered_dict
        self.assertIn(vec.fanzone.TEAMS_LIST.burnley.title(), list(events),
                      msg=f'Expected event "{vec.fanzone.TEAMS_LIST.burnley.title()}" is not found in actual events "{list(events)}"')

    def test_003_verify_the_outright_market_section_name(self):
        """
        DESCRIPTION: Verify the Outright market section name
        EXPECTED: The label name &lt;team&gt; bets, Team should be on the name user has selected Fanzone team , eg- Everton Bets, Liverpool bets
        """
        # covered in step 2

    def test_004_logout_from_application_and_login_with_user_having_any_other_fanzone_team_with_outright_market_created(
            self):
        """
        DESCRIPTION: Logout from application and login with user having Any other Fanzone team with Outright market created
        EXPECTED: User should be able to login to application successfully
        """
        self.site.logout()

    def test_005_navigate_to_fanzone_page(self):
        """
        DESCRIPTION: Navigate to Fanzone page
        EXPECTED: User should be navigated to Fanzone page
        """
        self.login_select_fanzone(fanzone_team="aston_villa")
        self.test_001_navigate_to_fanzone_page()

    def test_006_verify_if_outright_markets_are_shown_in_mobile_view_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify if Outright markets are shown in mobile view in Now and Next tab
        EXPECTED: The label name &lt;team&gt; bets, Team should be on the name user has selected Fanzone team , eg- Everton Bets, Liverpool bets
        """
        outright = self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.get(self.event_name)
        market = outright.accordions_list.items_as_ordered_dict.get('outright_Team_Bets1')
        events = market.items_as_ordered_dict
        self.assertIn(vec.fanzone.TEAMS_LIST.aston_villa.title(), list(events),
                      msg=f'Expected event "{vec.fanzone.TEAMS_LIST.aston_villa.title()}" is not found in actual events "{list(events)}"')
