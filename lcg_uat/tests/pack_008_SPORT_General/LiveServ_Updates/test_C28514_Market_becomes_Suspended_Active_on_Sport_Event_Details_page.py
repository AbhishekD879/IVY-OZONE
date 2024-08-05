import pytest

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.in_play
@pytest.mark.markets
@pytest.mark.event_details
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.safari
@vtest
class Test_C28514_Market_becomes_Suspended_Active_on_Sport_Event_Details_page(BaseSportTest):
    """
    TR_ID: C28514
    NAME: Market becomes Suspended/Active on <Sport> Event Details page
    DESCRIPTION: This test verifies changes on market after it's being triggered to Suspended/Active status codes
    PRECONDITIONS: LiveServer is available only for **In-Play <Sport> events**
    PRECONDITIONS: **NOTE:** **LivePrice updates are NOT applicable for Outrights and Enhanced Multiples events**
    """
    keep_browser_open = True

    def check_market_output_price_buttons(self, market_name, is_enabled, timeout=40):
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg='There are no markets')
        section = markets_list.get(market_name)
        self.assertTrue(section, msg='Market section is not found')
        output_prices_list = section.outcomes.items_as_ordered_dict
        self.assertTrue(output_prices_list, msg='Market output prices were not found on Event Details page')
        for output_price_name, output_price in output_prices_list.items():
            if is_enabled:
                self.assertTrue(output_price.bet_button.is_enabled(timeout=timeout),
                                msg=f'"{output_price_name}" price is suspended and button is not active. '
                                    f'It should not be suspended.')
            else:
                self.assertFalse(output_price.bet_button.is_enabled(expected_result=False, timeout=timeout),
                                 msg=f'"{output_price_name}" price is not suspended and button is active. '
                                     f'It should be suspended.')

    def test_000_create_test_event(self):
        """
        DESCRIPTION: Create test event
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True,
                                                                                 markets=[('both_teams_to_score',
                                                                                           {'cashout': False})])
        self.__class__.eventID, self.__class__.selection_ids = event_params.event_id, event_params.selection_ids
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.marketID = self.ob_config.market_ids[event_params.event_id][market_short_name]

    def test_001_load_oxygen_application_and_go_to_event_details_page(self):
        """
        DESCRIPTION: Load Oxygen application and go to event details page
        EXPECTED: Event details page is displayed
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_002_trigger_market_status_code_to_suspended_and_watch_event_details_page_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **marketStatusCode="S"** for one of its market types
        DESCRIPTION: and at the same time have Event Details page opened to watch for updates
        EXPECTED: All Price/Odds buttons of changed market type are displayed immediately as greyed out
        EXPECTED: and become disabled on <Sports> Details page but still displaying the prices
        EXPECTED: The rest market types are not changed
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True,
                                           active=False)
        self.check_market_output_price_buttons(market_name=self.expected_market_sections.match_result,
                                               is_enabled=False, timeout=50)
        self.check_market_output_price_buttons(market_name=self.expected_market_sections.both_teams_to_score,
                                               is_enabled=True)

    def test_003_trigger_market_status_code_to_active_and_watch_event_details_page_updates(self):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: **marketStatusCode="A"** for the same market type
        DESCRIPTION: and at the same time have Event Details page opened to watch for updates
        EXPECTED: All Price/Odds buttons  of the market are no more disabled, they become active immediately,
        EXPECTED: The rest market types remain not changed
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True,
                                           active=True)
        self.check_market_output_price_buttons(market_name=self.expected_market_sections.match_result,
                                               is_enabled=True)
        self.check_market_output_price_buttons(market_name=self.expected_market_sections.both_teams_to_score,
                                               is_enabled=True)
