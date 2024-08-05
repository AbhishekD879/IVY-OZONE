import pytest

import tests
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest


# @pytest.mark.tst2  # cannot get banach events in qa environments
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.build_your_bet
@pytest.mark.desktop
@vtest
class Test_C2553331_Banach_Format_of_Player_Markets_selection_on_dashboard(BaseBanachTest):
    """
    TR_ID: C2553331
    NAME: Banach. Format of Player Markets selection on dashboard
    DESCRIPTION: Test case verifies selection format of Banach Player Markets
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **Player Markets examples**
    PRECONDITIONS: Player Markets: First Goalscorer, Anytime Goalscorer, Player to score 2+ goals, To be shown a card, Player to get first booking
    PRECONDITIONS: **Build Your bet (for Coral) / Bet Builder (for Ladbrokes) tab is opened**
    """
    keep_browser_open = True
    proxy = None
    device_name = 'Desktop Chrome' if not tests.use_browser_stack else tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find event with Banach markets
        """
        self.__class__.event_id = self.get_ob_event_with_byb_market(
            market_name=self.expected_market_sections.double_chance.title())
        self.navigate_to_edp(event_id=self.event_id, timeout=50)
        self.site.wait_content_state(state_name='EventDetails')
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

    def test_001_add_selections_from_available_player_markets_to_dashboardverify_selections_name_format(self):
        """
        DESCRIPTION: Add selections from available Player Markets to dashboard
        DESCRIPTION: Verify selections name format
        EXPECTED: Selections names have the following format in dashboard
        EXPECTED: [Market name SELECTION] - for Coral
        EXPECTED: ![](index.php?/attachments/get/114303312)
        EXPECTED: [Market name - Selection] - for Ladbrokes
        EXPECTED: ![](index.php?/attachments/get/114303313)
        """
        double_chance_market = self.get_market(market_name=self.expected_market_sections.double_chance)
        double_chance_default_switcher = double_chance_market.grouping_buttons.current
        double_chance_selection_names = double_chance_market.set_market_selection(count=1)
        self.assertTrue(double_chance_selection_names, msg='No one selection added to Dashboard')
        if self.brand == 'bma':
            expected_selection_name = f'{self.expected_market_sections.double_chance.title()} ' \
                                      f'{double_chance_default_switcher.lower()} ' \
                                      f'{double_chance_selection_names[0].upper()}'
        else:
            expected_selection_name = f'{self.expected_market_sections.double_chance.title()} ' \
                                      f'{double_chance_default_switcher.lower()} - ' \
                                      f'{double_chance_selection_names[0]}'

        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        outcomes = dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'List of outcomes is empty: "{outcomes}"')
        actual_selection_name = list(outcomes.keys())[0]
        self.assertEqual(expected_selection_name, actual_selection_name,
                         msg=f'Actual "{actual_selection_name}" Expected "{expected_selection_name}"')
