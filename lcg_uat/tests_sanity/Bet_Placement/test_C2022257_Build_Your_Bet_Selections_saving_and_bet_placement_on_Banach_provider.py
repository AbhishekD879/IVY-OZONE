import pytest
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@pytest.mark.build_your_bet_dashboard
@pytest.mark.banach
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.other
@pytest.mark.safari
@vtest
class Test_C2022257_Build_Your_Bet__Selections_saving_on_Banach_event(BaseBanachTest):
    """
    TR_ID: C2022257
    NAME: Build Your Bet - Selections saving on Banach event
    DESCRIPTION: Test case describes Remember selections feature
    DESCRIPTION: AUTOTEST [C48912786], [C48921973]
    PRECONDITIONS: Guide for Banach CMS configuration: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: HL requests:
    PRECONDITIONS: Request for Banach leagues: https://buildyourbet-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v1/leagueshttps://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues
    PRECONDITIONS: Request for Banach market groups: https://buildyourbet-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v2/markets-grouped?obEventId=xxxxx
    PRECONDITIONS: Request for Banach selections: https://buildyourbet-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v1/selections?marketIds=[ids]&obEventId=xxxxx
    PRECONDITIONS: - Open the app (site)
    PRECONDITIONS: - Navigate to Event details page (EDP) with Banach markets available from:
    PRECONDITIONS: Module Ribbon Tab on the Home page ( 'BUILD YOUR BET' tab name for **CORAL** / 'BET BUILDER' tab name for **LADBROKES** )
    PRECONDITIONS: or
    PRECONDITIONS: Football Sport Landing page
    PRECONDITIONS: or
    PRECONDITIONS: 'BUILD YOUR BET' module **CORAL** / 'BET BUILDER' module **LADBROKES** on the Home page ( **DESKTOP** )
    """
    keep_browser_open = True
    proxy = None
    bet_amount = 1
    blocked_hosts = ['*spark-br.*']

    def verify_selections_on_dashboard(self):
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(), msg='BYB Dashboard panel is not shown')
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        result = wait_for_result(lambda: '' != list(dashboard_panel.outcomes_section.items_as_ordered_dict.keys())[0],
                                 timeout=2,
                                 name='No empty name on dashboard')
        self.assertTrue(result, msg='Empty name on dashboard')
        outcomes = dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'List of outcomes is empty: "{outcomes}"')
        dashboard_selections = list(outcomes.keys())
        if self.brand == 'ladbrokes':
            match_betting_market_and_selection_name = f'{self.expected_market_sections.match_betting.title()} ' \
                                                      f'{self.match_betting_default_switcher.lower()} - {self.team1.title()}'

            both_teams_to_score_market_and_selection_name = f'{self.expected_market_sections.both_teams_to_score.title()} - '\
                                                            f'{self.both_teams_to_score_names.title()}'
        else:
            match_betting_market_and_selection_name = f'{self.expected_market_sections.match_betting.title()} ' \
                f'{self.match_betting_default_switcher.lower()} {self.team1.upper()}'

            both_teams_to_score_market_and_selection_name = f'{self.expected_market_sections.both_teams_to_score.title()} '\
                                                            f'{self.both_teams_to_score_names.upper()}'

        expected_added_selections = [match_betting_market_and_selection_name, both_teams_to_score_market_and_selection_name]

        self.assertListEqual(sorted(dashboard_selections), sorted(expected_added_selections),
                             msg=f'Lists with outcomes "{sorted(dashboard_selections)}" are not equal \n'
                                 f'to list of added selections "{sorted(expected_added_selections)}"')

    def test_001_tap_on_the_build_your_bet_coral__bet_builder_ladbrokes_edp_market_nameif_we_navigate_from_module_ribbon_tab_or_module__desktop__it_will_redirect_to_build_your_bet_coral__bet_builder_ladbrokes_edp_market_by_default(self):
        """
        DESCRIPTION: Tap on the 'BUILD YOUR BET' **CORAL** / 'BET BUILDER' **LADBROKES** edp market name
        DESCRIPTION: (if we navigate from Module ribbon tab or module ( **Desktop** ) it will redirect to 'BUILD YOUR BET' **CORAL** / 'BET BUILDER' **LADBROKES** edp market by default)
        EXPECTED: 'BUILD YOUR BET' **CORAL** / 'BET BUILDER' **LADBROKES** edp market is opened
        EXPECTED: **CORAL**
        EXPECTED: ![](index.php?/attachments/get/59007988)
        EXPECTED: **LADBROKES**
        EXPECTED: ![](index.php?/attachments/get/59007989)
        """
        self.__class__.initial_counter = 0
        self.__class__.eventID = self.get_ob_event_with_byb_market()
        self.site.login(async_close_dialogs=False)
        self.navigate_to_edp(event_id=self.eventID)
        self.site.wait_content_state(state_name='EventDetails')
        self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict[self.expected_market_tabs.build_your_bet].click()
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict[self.expected_market_tabs.build_your_bet].is_selected(),
                        msg=f'tab "{self.expected_market_tabs.build_your_bet}" is not selected')

    def test_002_add_few_combinable_selections_to_bybbet_builder_dashboard_from_different_markets_accordionsmatch_betting_or_both_teams_to_scoreoverunder_marketscorrect_score_etc(self):
        """
        DESCRIPTION: Add few combinable selections to BYB/Bet Builder Dashboard from different markets accordions:
        DESCRIPTION: Match Betting or Both teams to score
        DESCRIPTION: Over/Under markets
        DESCRIPTION: Correct Score etc
        EXPECTED: - Selected selections are highlighted within accordions
        EXPECTED: - 'Build Your Bet' (for **Coral** )/ 'Bet Builder' (for **Ladbrokes** ) Dashboard appears with slide animation and is displayed in an expanded state (only when the page is accessed and selections are added for the first time): on mobile in the bottom of the screen over footer menu on tablet/desktop in the bottom of the market area and above footer menu (if market area is too long to be shown within screen)
        """
        # Match betting selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.__class__.match_betting_default_switcher = match_betting.grouping_buttons.current
        self.assertTrue(match_betting, msg=f'Can not get market "{self.expected_market_sections.match_result}"')

        match_betting_selection_names = match_betting.set_market_selection(count=1)
        self.assertTrue(match_betting_selection_names, msg='No one selection added to Dashboard')
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        self.initial_counter += 1

        self.__class__.team1 = ''.join(match_betting_selection_names)

        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(),
                        msg='BYB Dashboard panel is not shown')
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)

        # Both Teams To Score selection
        both_teams_to_score_market = self.get_market(market_name=self.expected_market_sections.both_teams_to_score)
        self.__class__.both_teams_to_score_names = both_teams_to_score_market.set_market_selection(count=1)[0]
        self.assertTrue(self.both_teams_to_score_names, msg='No one selection added to Dashboard')

        self.initial_counter += 1
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)
        self.verify_selections_on_dashboard()

    def test_003_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: - Selections stay highlighted after page refresh
        EXPECTED: - 'Build Your Bet' (for **Coral** ) / 'Bet Builder' (for **Ladbrokes** ) Dashboard is displayed after page refresh
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state(state_name='EventDetails')
        self.verify_selections_on_dashboard()

    def test_004_navigate_between_tabs_of_event_details_page_and_app_modules_and_then_return_back_to_the_same_banach_event(self):
        """
        DESCRIPTION: Navigate between tabs of Event Details page and app modules and then return back to the same Banach event
        EXPECTED: - Selections stay highlighted after navigation
        EXPECTED: - 'Build Your Bet' (for **Coral** ) / 'Bet Builder' (for **Ladbrokes** ) Dashboard is displayed after navigation
        """
        wait_for_result(lambda: self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict[self.expected_market_tabs.all_markets].is_enabled(), timeout=20)
        self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict[self.expected_market_tabs.all_markets].click()
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict[self.expected_market_tabs.all_markets].is_selected(),
                        msg=f'tab "{self.expected_market_tabs.all_markets}" is not selected')
        wait_for_result(lambda: self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict[self.expected_market_tabs.build_your_bet].is_enabled(), timeout=20)
        self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict[self.expected_market_tabs.build_your_bet].click()
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict[self.expected_market_tabs.build_your_bet].is_selected(),
                        msg=f'tab "{self.expected_market_tabs.build_your_bet}" is not selected')
        self.verify_selections_on_dashboard()

    def test_005_close_the_browser_tab_kill_the_app_then_open_tab_app_again_and_navigate_to_the_same_banach_event(self):
        """
        DESCRIPTION: Close the browser tab (kill the app), then open tab (app) again and navigate to the same Banach event
        EXPECTED: - Selections stay highlighted after tab (app) was closed and restored
        EXPECTED: - 'Build Your Bet' (for **Coral** ) / 'Bet Builder' (for **Ladbrokes** ) Dashboard is displayed tab (app) was closed and restored
        """
        self._logger.warning("*** Skipping Step can't be automated. "
                             "Selection are not restored for browser that is started via automation. "
                             "No issue in real browser")
        self.verify_selections_on_dashboard()
        summary_block = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary
        self.assertTrue(summary_block.is_displayed(), msg='Dashboard is not displayed')
