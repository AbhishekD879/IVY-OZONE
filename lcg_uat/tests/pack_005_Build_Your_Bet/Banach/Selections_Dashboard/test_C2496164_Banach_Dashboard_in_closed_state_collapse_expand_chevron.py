import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest


# @pytest.mark.tst2  # cannot get banach events in qa environments
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.build_your_bet
@pytest.mark.desktop
@vtest
class Test_C2496164_Banach_Dashboard_in_closed_state_collapse_expand_chevron(BaseBanachTest):
    """
    TR_ID: C2496164
    NAME: Banach. Dashboard in closed state, collapse/expand chevron
    DESCRIPTION: Test case verifies collapse/expand chevron and Banach selections dashboard in closed state
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **Banach selections are added to the dashboard**
    PRECONDITIONS: **Dashboard is expanded**
    """
    keep_browser_open = True
    proxy = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login as user that has freebets
        DESCRIPTION: Find event with Banach markets
        DESCRIPTION: Add two combinable selections to BYB Dashboard
        EXPECTED: Dashboard is expanded
        """
        self.__class__.event_id = self.get_ob_event_with_byb_market()
        self.navigate_to_edp(event_id=self.event_id, timeout=50)
        self.site.wait_content_state(state_name='EventDetails')
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

        # Match betting selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.assertTrue(match_betting, msg=f'Can not get market "{self.expected_market_sections.match_result}"')

        match_betting_selection_names = match_betting.set_market_selection(selection_index=1, time=True)
        self.assertTrue(match_betting_selection_names, msg='No one selection added to Dashboard')
        match_betting.add_to_betslip_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(),
                        msg='BYB Dashboard panel is not shown')
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)

        self.__class__.initial_counter += 1

        # Double Chance selection
        double_chance_market = self.get_market(market_name=self.expected_market_sections.double_chance)
        double_chance_market.scroll_to()
        double_chance_market_names = double_chance_market.set_market_selection(selection_index=1)[0]
        self.assertTrue(double_chance_market_names, msg='No one selection added to Dashboard')
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        self.__class__.initial_counter += 1
        is_expanded = self.site.sport_event_details.tab_content.dashboard_panel.is_expanded(timeout=13)
        self.assertTrue(is_expanded, msg='Dashboard is not expanded by default')

    def test_001_tap_on_close_chevron_button_on_dashboard_header(self):
        """
        DESCRIPTION: Tap on Close chevron button on dashboard header
        EXPECTED: Dashboard is closed and contains:
        EXPECTED: - Dashboard header
        EXPECTED: - Odds area
        """
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.open_close_toggle_button.click()
        is_expanded = self.site.sport_event_details.tab_content.dashboard_panel.is_expanded(timeout=13)
        self.assertFalse(is_expanded, msg='Dashboard is expanded even after click')
        self.__class__.dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        dashboard_summary_markets = self.dashboard_panel.byb_summary.summary_description.dashboard_market_text
        self.assertTrue(dashboard_summary_markets,
                        msg=f'Dashboard summary markets text is empty "{dashboard_summary_markets}"')
        odds = self.dashboard_panel.byb_summary.place_bet.value_text
        self.assertTrue(odds, msg='Odds area is blank')

    def test_002_verify_dashboard_header_in_closed_dashboard_state(self):
        """
        DESCRIPTION: Verify dashboard header in closed dashboard state
        EXPECTED: The following information is displayed:
        EXPECTED: - icon with number of selections
        EXPECTED: - BUILD YOUR BET **Coral**/BET BUILDER **Ladbrokes** text
        EXPECTED: - name of the first selections (separated by comma)
        EXPECTED: - "Open" chevron
        """
        summary_block = self.dashboard_panel.byb_summary
        self.assertTrue(summary_block.summary_counter.icon, msg='Dashboard icon is not visible')

        self.assertEqual(int(summary_block.summary_counter.value), self.initial_counter,
                         msg=f'Dashboard counter "{summary_block.summary_counter.value}" '
                             f'is not the same as expected "{self.initial_counter}"')
        self.assertEquals(summary_block.summary_description.dashboard_title,
                          vec.yourcall.DASHBOARD_TITLE,
                          msg=f'Dashboard title "{summary_block.summary_description.dashboard_title}" '
                              f'is not the same as expected "{vec.yourcall.DASHBOARD_TITLE}"')

        label = summary_block.open_close_toggle_button.name
        expected_label = 'Open' if self.brand == 'bma' else 'OPEN'
        self.assertEqual(label, expected_label,
                         msg=f'Button name "{label}" is not the same as expected "Close"')
        self.assertTrue(summary_block.open_close_toggle_button.has_up_down_arrow(),
                        msg='There\'s no up/down arrow near button')

    def test_003_tap_open_chevron_button(self):
        """
        DESCRIPTION: Tap Open chevron button
        EXPECTED: Dashboard is expanded and contains selections from pre-conditions
        """
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.open_close_toggle_button.click()
        is_expanded = self.site.sport_event_details.tab_content.dashboard_panel.is_expanded(timeout=13)
        self.assertTrue(is_expanded, msg='Dashboard is not expanded after click')

        selections = self.dashboard_panel.outcomes_section.items_as_ordered_dict
        dashboard_selections = list(selections.keys())
        self.assertTrue(dashboard_selections, msg=f'Dashboard does not contain the selections added before')
