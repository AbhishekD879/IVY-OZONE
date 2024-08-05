import tests
import pytest
from crlat_ob_client.create_event import CreateSportEvent
from voltron.environments import constants as vec
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from crlat_ob_client.utils.helpers import generate_name


@pytest.mark.lad_stg2
# @pytest.mark.lad_tst2 # Not configured in tst2
# @pytest.mark.lad_prod # we cannot create events in prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305113_To_verify_UI_of_outright_markets_in_Now_and_Next_tab_under_Team_Bets_section_in_Fanzone_page(Common):
    """
    TR_ID: C65305113
    NAME: To verify UI of outright markets in Now and Next tab under <Team> Bets section in Fanzone page
    DESCRIPTION: To verify UI of outright markets in Now and Next tab under <Team> Bets section in Fanzone page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)Outright markets are created with Premier league participating teams as selections for Various type such 442,438 etc.
    PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
    PRECONDITIONS: 5) User has subscribed to Fanzone
    """
    keep_browser_open = True

    def create_market_to_event(self, market_name):

        market_id = self.event.create_market(market_name=market_name,
                                             market_template_id=self.ob_config.football_config.autotest_class.autotest_premier_league.outright_market_template_id,
                                             class_id=self.class_id, event_id=self.outright_event.event_id,
                                             bet_in_run='Y')
        selections_number = 1
        selection_types = ['A'] * selections_number  # actually, selection_types is not needed at all, but otherwise add_selections will fail
        selection_names = ['|Auto test %s|' % generate_name() for _ in range(0, selections_number)]
        prices = ['%s/%s' % (i + 1, i + 2) for i in range(0, 2)]
        selections = self.event.add_selections(prices=prices,
                                               marketID=market_id,
                                               selection_names=selection_names,
                                               selection_types=selection_types)
        self.ob_config.map_fanzone_event_selection_id(selection_id=list(selections.values())[0],
                                                      fanzone_team=vec.fanzone.TEAMS_LIST.burnley.title(),
                                                      team_external_id=self.ob_config.football_config.fanzone_external_id.burnley)

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
        self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.burnley.title(), str(self.typeId))
        self.__class__.class_id = self.ob_config.football_config.autotest_class.class_id
        self.__class__.outright_event = self.ob_config.add_autotest_premier_league_football_outright_event()
        self.__class__.event_name = self.outright_event.ss_response['event']['name'].upper()
        self.__class__.event = CreateSportEvent(env=tests.settings.backend_env, brand=self.brand,
                                                category_id=self.ob_config.football_config.category_id,
                                                class_id=self.class_id, type_id=self.typeId)
        for i in range(0, 2):
            self.create_market_to_event(market_name="outright_burnley_" + str(i))

        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username)
        self.site.wait_content_state('Homepage')
        self.site.open_sport('football', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Teams to be displayed',
                        timeout=5)
        team = self.site.show_your_colors.items_as_ordered_dict.get(vec.fanzone.TEAMS_LIST.burnley.title())
        team.click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_hit_the_fe_url_and_login_to_lads_fe(self):
        """
        DESCRIPTION: Hit the FE url and login to Lads FE
        EXPECTED: User should be able to access the url and is logged into Lads application
        """
        # covered in above step

    def test_002_navigate_to_fanzone_page_via_below_entry_pointsa_launch_banner_in_home_pageb_fanzone_in_sports_ribbonc_fanzone_in_a_zall_sports_menud_launch_banner_in_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Fanzone page via below entry points
        DESCRIPTION: a. Launch Banner in home page
        DESCRIPTION: b. Fanzone in Sports Ribbon
        DESCRIPTION: c. Fanzone in A-Z(All sports) menu
        DESCRIPTION: d. Launch Banner in Football landing page
        EXPECTED: User should be able to navigate Fanzone page
        """
        self.assertTrue(self.site.football.fanzone_banner(), msg="Fanzone banner is not displayed")
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")
        if tests.settings.device_type == "mobile":
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.get(
                vec.racing.RACING_HIGHLIGHTS_TAB_NAME).click()
        self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")
        fanzone_banner = self.site.home.fanzone_banner()
        fanzone_banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_003_verify_is_user_is_able_to_see_outright_market_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify is user is able to see Outright Market in Now and next Tab
        EXPECTED: User should be able to see Outright market under &lt;Team&gt; Bets section in Now and Next tab
        """
        outrights = self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.get(self.event_name)
        for i in range(0, 2):
            market = outrights.accordions_list.items_as_ordered_dict.get("outright_burnley_" + str(i))
            market_ui_box_font_family = market.css_property_value('font-family')
            self.assertIn(vec.fanzone.MARKET_TEAM_FONT_FAMILY, market_ui_box_font_family,
                          msg=f'Team UI box font family is not equal to Zepplin team box font family'
                              f'actual result "{market_ui_box_font_family}"')
            market_ui_box_color = market.css_property_value('color')
            self.assertEqual(market_ui_box_color, vec.fanzone.MARKET_TEAM_COLOR,
                             msg=f'Team UI box color is not equal to Zepplin team box color'
                                 f'actual result "{market_ui_box_color}"')
            market_ui_box_bgcolor = market.css_property_value('background-color')
            self.assertEqual(market_ui_box_bgcolor, vec.fanzone.MARKET_TEAM_BG_COLOR,
                             msg=f'Team UI box background-color is not equal to Zepplin team box background-color'
                                 f'actual result "{market_ui_box_bgcolor}"')
            market_ui_box_border = market.css_property_value('border-radius')
            self.assertEqual(market_ui_box_border, vec.fanzone.MARKET_TEAM_BORDER_RADIUS,
                             msg=f'Team UI box border is not equal to Zepplin team box border'
                                 f'actual result "{market_ui_box_border}"')
            market_ui_box_font_size = market.css_property_value('font-size')
            self.assertEqual(market_ui_box_font_size, vec.fanzone.MARKET_TEAM_FONT_SIZE,
                             msg=f'Team UI box font-size is not equal to Zepplin team box font-size'
                                 f'actual result "{market_ui_box_font_size}"')
            selections = market.items_as_ordered_dict
            self.assertTrue(selections, "selections are not displayed for outrights")

    def test_004_verify_ui_of_outright_markets(self):
        """
        DESCRIPTION: Verify UI of outright markets
        EXPECTED: Outright UI should be similar to sample provided in Jira BMA-62186 or Zeplin attached to the story
        """
        # covered in above step

    def test_005_verify_content_for_outrights_markets_in_below_listed_orderltteamgt_bets__configurable_on_cmsleague_namemarket_name1selectionyour_subscribed_fanzonemarket_name2selectionnote_same_order_applies_if_we_have_data_for_more_than_1_leaguetype(
            self):
        """
        DESCRIPTION: Verify content for Outrights Markets in below listed order
        DESCRIPTION: &lt;Team&gt; Bets--Configurable on CMS
        DESCRIPTION: League Name
        DESCRIPTION: Market Name1
        DESCRIPTION: Selection(Your subscribed Fanzone)
        DESCRIPTION: Market Name2
        DESCRIPTION: Selection
        DESCRIPTION: Note: Same order applies if we have data for more than 1 league/Type.
        EXPECTED: Outright market content should be as per the order mentioned
        """
        # covered in step 3
