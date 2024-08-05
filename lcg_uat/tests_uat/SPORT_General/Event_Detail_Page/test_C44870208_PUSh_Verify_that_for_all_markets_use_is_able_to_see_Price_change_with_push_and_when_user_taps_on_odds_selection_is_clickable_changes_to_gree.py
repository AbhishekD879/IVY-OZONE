import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
# @pytest.mark.prod - Not valid as Ob is involved in event creation and price change
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.p2
@vtest
class Test_C44870208_PUSh_Verify_that_for_all_markets_use_is_able_to_see_Price_change_with_push_and_when_user_taps_on_odds_selection_is_clickable_changes_to_green_and_is_added_to_bet_slip_Verify_that_Market_drop_off_with_Push_at_the_right_time(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C44870208
    NAME: PUSh : "Verify that for all markets, use is able to see Price change with push and when user taps on odds, selection is clickable (changes to green) and is added to bet slip. Verify that Market drop off with Push at the right time."
    DESCRIPTION: "Verify that for all markets, use is able to see Price change with push and when user taps on odds, selection is clickable (changes to green) and is added to bet slip.
    DESCRIPTION: Verify that Market drop off with Push at the right time."
    PRECONDITIONS: Price change , Market drop off with Push
    """
    keep_browser_open = True
    increased_price = '3/1'
    decreased_price = '1/14'

    def get_selection_details(self):
        sections = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found on page')
        if self.device_type == 'mobile':
            section = sections.get(tests.settings.football_autotest_competition_league)
            self.assertTrue(section, msg=f'Section: "{tests.settings.football_autotest_competition_league}" is not found')
        else:
            section = sections.get(tests.settings.football_autotest_league)
            self.assertTrue(section, msg=f'Section: "{tests.settings.football_autotest_league}" is not found')
        if not section.is_expanded():
            section.expand()
        events = section.items_as_ordered_dict
        self.assertTrue(events, msg='No events found')
        event = events.get(self.event_name)
        self.assertTrue(event, msg=f'event: "{self.event_name}" is not found')
        selections = event.template.items_as_ordered_dict
        self.assertTrue(selections, msg='No selections found')
        selection_button = list(selections.values())[0]
        return selection_button

    def edp_get_selection_details(self):
        market = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(market, msg='No market found')
        if self.brand == 'ladbrokes':
            outcomes = market['Match Betting'].outcomes.items_as_ordered_dict
        else:
            if self.device_type == 'mobile':
                outcomes = market['MATCH RESULT'].outcomes.items_as_ordered_dict
            else:
                outcomes = market['Match Result'].outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes found')
        outcome = list(outcomes.values())[0]
        self.assertTrue(outcome, msg='No outcome found')
        return outcome

    def test_000_preconditions(self):
        """
        DESCRIPTION: "Creating event"
        """
        event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.event_id = event.event_id
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.market_id = self.ob_config.market_ids[self.event_id][market_short_name]
        selection_ids = event.selection_ids
        self.__class__.team1_selection_id = list(selection_ids.values())[0]
        self.__class__.event_name = f'{event.team1} v {event.team2}'

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_verify_price_change_for_all_inplay_events_on_homepage_sports_landing_page_and_edp(self):
        """
        DESCRIPTION: Verify Price change for all inplay events on HomePage, Sports landing page and EDP
        EXPECTED: Price change with Push successfully
        """
        self.navigate_to_page(name='in-play/football')
        self.site.wait_content_state(state_name='InPlay')
        selection_button = self.get_selection_details()
        self.assertTrue(selection_button, msg='selection value not found')
        self.ob_config.change_price(selection_id=self.team1_selection_id, price=self.increased_price)
        self.assertTrue(selection_button.is_price_changed(expected_price=self.increased_price, timeout=30),
                        msg=f'Price for Bet Button did not change. '
                            f'Actual price: "{selection_button.name}", Expected price: "{self.increased_price}"')
        self.navigate_to_page(name='sport/football/live')
        self.site.wait_content_state(state_name=vec.sb.FOOTBALL)
        selection_button = self.get_selection_details()
        self.assertTrue(selection_button, msg='selection value not found')
        self.ob_config.change_price(selection_id=self.team1_selection_id, price=self.decreased_price)
        self.assertTrue(selection_button.is_price_changed(expected_price=self.decreased_price, timeout=30),
                        msg=f'Price for Bet Button did not change. '
                            f'Actual price: "{selection_button.name}", Expected price: "{self.decreased_price}"')
        self.navigate_to_edp(event_id=self.event_id)
        outcome = self.edp_get_selection_details()
        selection_button = outcome.bet_button
        self.assertTrue(selection_button, msg='selection value not found')
        self.ob_config.change_price(selection_id=self.team1_selection_id, price=self.increased_price)
        sleep(5)
        self.device.refresh_page()
        outcome = self.edp_get_selection_details()
        selection_button = outcome.bet_button
        self.assertTrue(selection_button, msg='selection value not found')
        self.assertTrue(selection_button.is_price_changed(expected_price=self.increased_price, timeout=30),
                        msg=f'Price for Bet Button did not change. '
                            f'Actual price: "{selection_button.name}", Expected price: "{self.increased_price}"')
        selection_button.click()

    def test_003_verify_when_user_taps_on_odds_selection_is_clickablechanges_to_green(self):
        """
        DESCRIPTION: Verify when user taps on odds, selection is clickable(changes to green)
        EXPECTED: Price is highlighted in green
        """
        #  Color change Not in scope of automation

    def test_004_verify_selected_selections_are_added_to_quickbetbetslip(self):
        """
        DESCRIPTION: Verify selected selections are added to Quickbet/Betslip
        EXPECTED: Selections are added successfully
        """
        if self.device_type == 'mobile':
            if self.site.wait_for_quick_bet_panel(timeout=5):
                quick_bet_event_name = self.site.quick_bet_panel.selection.content.event_name
                self.assertEqual(quick_bet_event_name, self.event_name,
                                 msg=f'Actual event name : "{quick_bet_event_name}" is not equal to Expected event name : "{self.event_name}"')
                self.site.quick_bet_panel.close()
                self.site.wait_quick_bet_overlay_to_hide()
        else:
            singles_section = self.get_betslip_sections().Singles
            self.assertTrue(singles_section.items(), msg='No stakes found')
            _, stake = list(singles_section.items())[0]
            self.assertEquals(self.event_name, stake.event_name, msg=f'{self.event_name} not matching '
                                                                     f'with {stake.event_name} in single section')

    def test_005_verify_that_market_drop_off_with_push_at_the_right_time(self):
        """
        DESCRIPTION: Verify that Market drop off with Push at the right time
        EXPECTED: Market drop off successfully
        """
        self.ob_config.change_market_state(event_id=self.event_id, market_id=self.market_id)
        sleep(3)
        self.device.refresh_page()
        self.assertTrue(self.site.sport_event_details.tab_content.has_no_events_label(timeout=10),
                        msg='Market drop off is unsuccessful')
