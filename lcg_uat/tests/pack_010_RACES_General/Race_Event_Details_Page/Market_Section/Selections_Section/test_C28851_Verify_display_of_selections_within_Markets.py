import pytest
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


# @pytest.mark.tst2
# @pytest.mark.stg2  # Cannot get mapped silks in tst env
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C28851_Verify_display_of_selections_within_Markets(BaseRacing):
    """
    TR_ID: C28851
    NAME: Verify display of selections within Markets
    DESCRIPTION: This test case verifies display of selections within different Markets
    PRECONDITIONS: **JIRA Ticket** : BMA-6584 'Racecard Layout Update - Horse Information'
    PRECONDITIONS: BMA-18626'Replace Generic Silks with Race Card Number Design (Racing)'
    PRECONDITIONS: NOTE : all information about <Race> and Runner is displayed only if it is mapped
    PRECONDITIONS: NOTE 2: Timeform will be not used for Ladbrokes. Racing post data will be displayed instead. This is from comment in BMA-44480
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id)[0]
        self.__class__.event_id = event['event']['id']

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('homepage')

    def test_002_tap_race_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon on the Sports Menu Ribbon
        EXPECTED: <Race> Landing Page is opened
        """
        if self.device_type == 'desktop':
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertIn(vec.sb.HORSERACING.upper(), sports.keys(),
                          msg=f'"{vec.sb.HORSERACING.upper()}" is not found in the header sport menu')
            sports.get(vec.sb.HORSERACING.upper()).click()
        else:
            self.navigate_to_page('horse-racing')
        self.site.wait_content_state(state_name='Horseracing')

    def test_003_tap_event_name_on_the_event_section(self):
        """
        DESCRIPTION: Tap Event Name on the Event section
        EXPECTED: *   <Race> Event Details page is opened
        EXPECTED: *   'Win or E/W' market is selected by default
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        active_tab = self.site.racing_event_details.tab_content.event_markets_list.current_market_tab_name
        self.assertEqual(active_tab, vec.racing.RACING_EDP_MARKET_TABS.win_or_ew,
                         msg=f'Actual tab "{active_tab}" is not same as Expected tab "{vec.racing.RACING_EDP_MARKET_TABS.win_or_ew}"')

    def test_004_go_to_race_event_selection_area_where_silks_are_mapped(self):
        """
        DESCRIPTION: Go to <Race> Event Selection area where SILKS are mapped
        EXPECTED: * Correct silks are displayed for mapped selections (silkName)
        EXPECTED: * Generic silks are displayed for missed selections
        """
        markets = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = list(markets.values())[0]
        self.__class__.outcomes = market.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='No outcomes found')
        for outcome_name, outcome in self.outcomes.items():
            # Generic Silk
            if 'Unnamed' in outcome_name:
                self.assertTrue(outcome.has_silks,
                                msg=f'Silk is not displayed for the horse "{outcome.horse_name}" from section "{outcome_name}"')
            # No silk at all
            elif outcome.is_non_runner:
                self.assertTrue(outcome.has_no_silks,
                                msg=f'Silk is displayed for non-runner horse "{outcome.horse_name}" from section "{outcome_name}"')
            # Bespoke Silk
            elif outcome.silk:
                self.assertTrue(outcome.has_bespoke_silks,
                                msg=f'Bespoke silk is not displayed for the horse "{outcome.horse_name}" from section "{outcome_name}"')
            # Generic Silk
            else:
                self.assertTrue(outcome.is_silk_generic, msg=f'Silk icon is not generic for outcome: "{outcome_name}"')

    def test_005_clicks_within_the_race_event_selection_area_or_on_the_arrow_on_the_left_side(self):
        """
        DESCRIPTION: Clicks within the <Race> Event Selection area (or on the arrow on the left side)
        EXPECTED: *   Runner information is expanded showing information about the runner
        EXPECTED: *  For HR: Spotlight text is present
        EXPECTED: *  For GH: Timeform summary with rating starts are present
        """
        for outcome_name, outcome in self.outcomes.items():
            if outcome.silk:
                outcome.scroll_to()
                outcome.click()
                self.assertTrue(outcome.has_show_summary_toggle(),
                                msg=f'Show more button is not present for "{outcome_name}"')
                if outcome.toggle_icon_name.lower() == vec.racing.SHOW_MORE.lower():
                    outcome.show_summary_toggle.click()
                    wait_for_result(lambda: outcome.has_expanded_summary(), timeout=10)
                    sleep(1)
                    if not outcome.has_expanded_summary():
                        outcome.show_summary_toggle.click()
                self.assertTrue(wait_for_result(lambda: outcome.has_expanded_summary(), timeout=10),
                                msg=f'Summary is not shown for outcome "{outcome_name}" after expanding selection')
                has_spotlight_info = outcome.expanded_summary.has_spotlight_info
                if has_spotlight_info:
                    spotlight_label = wait_for_result(lambda: outcome.spotlight_overview.title, timeout=5)
                    if spotlight_label != '':
                        self.assertEqual(spotlight_label, vec.racing.SPOTLIGHT_TITLE.upper(),
                                         msg=f'Actual text is "{spotlight_label}" is not equal to the '
                                             f'Expected text"{vec.racing.SPOTLIGHT_TITLE.upper()}"')

    def test_006_click_on_the_other_race_event_selection_area(self):
        """
        DESCRIPTION: Click on the other <Race> Event Selection area
        EXPECTED: *   First runner information is collapsed and a new one is expanded
        """
        # First runner info will not be collapsed on expanding the other selection info
        # Covered in above step

    def test_007_only_for_horses_go_to_race_event_selection_area_where_no_silks_mapped(self):
        """
        DESCRIPTION: ONLY FOR HORSES: Go to <Race> Event Selection area where no SILKS mapped
        EXPECTED: * NO Generic Pictures, Horse Name, price/Odds and Previous Odds under Price/Odds button are displayed
        EXPECTED: * Only runner numbers are displayed
        """
        for outcome_name, outcome in self.outcomes.items():
            if not outcome.silk and 'Unnamed' not in outcome_name and not outcome.is_non_runner:
                self.assertTrue(outcome.is_silk_generic, msg=f'Silk icon is not generic for outcome: "{outcome_name}"')
                self.assertTrue(outcome.horse_name, msg=f'Horse name is not displayed for outcome: "{outcome_name}"')
                self.assertTrue(outcome.output_price, msg=f'Outcome price is not shown for outcome: "{outcome_name}"')
                self.assertTrue(outcome.runner_number, msg=f'No runner name displayed for outcome "{outcome_name}"')
            if 'Unnamed' in outcome_name:
                self.assertFalse(outcome.previous_price, msg=f'Previous price is shown for outcome: "{outcome_name}"')
