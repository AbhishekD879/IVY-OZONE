import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.quick_bet
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.google_analytics
@pytest.mark.low
@pytest.mark.next_races
@pytest.mark.mobile_only
@pytest.mark.other
@vtest
class Test_C811234_Tracking_of_successful_adding_selection_to_Quick_Bet(BaseDataLayerTest, BaseSportTest, BaseRacing):
    """
    TR_ID: C811234
    VOL_ID: C9698324
    NAME: Tracking of successful adding selection to Quick Bet
    DESCRIPTION: This test case verifies tracking of successful adding selection to Quick Bet
    PRECONDITIONS: * Test case should be run on Mobile Only
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * User is logged out
    """
    keep_browser_open = True
    inplay_event_selection_ids = None
    inplay_event_id = None
    next_races = None
    expected_next_races_name = None
    next4_event_id = None
    next4_selection_ids = None
    first_runner_name = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_ids, self.__class__.event_id = event_params.selection_ids, event_params.event_id
        self.__class__.event_name1 = f'{event_params.team1} v {event_params.team2}'

        event_params2 = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.inplay_event_selection_ids, self.__class__.inplay_event_id = \
            event_params2.selection_ids, event_params2.event_id
        self.__class__.inplay_event_name = f'{event_params2.team1} v {event_params2.team2}'

        type_id = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.type_id
        self.check_and_setup_cms_next_races_for_type(type_id=type_id)

        event_params3 = self.ob_config.add_UK_racing_event(number_of_runners=2, ew_terms=self.ew_terms,
                                                           lp_prices={0: '1/7', 1: '2/3'}, time_to_start=1)
        self.__class__.next4_event_id, self.__class__.event_off_time, self.__class__.next4_selection_ids = \
            event_params3.event_id, event_params3.event_off_time, event_params3.selection_ids
        self.__class__.event_name = \
            '%s %s' % (self.event_off_time, self.horseracing_autotest_uk_name_pattern)

    def test_001_add_sport_selection_to_quick_bet(self):
        """
        DESCRIPTION: Navigate to Event Details page
        DESCRIPTION: Add <Sport> selection to Quick Bet
        EXPECTED: Quick bet appears at the bottom of the page
        """
        self.navigate_to_edp(self.event_id)
        self.add_selection_from_event_details_to_quick_bet()
        self.assertTrue(self.site.wait_for_quick_bet_panel(expected_result=True), msg='Quick Bet is not present')

    def test_002_verify_tracking_for_sport_event(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next push is sent:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'quickbet',
        EXPECTED: 'eventAction' : 'add to quickbet',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'ecommerce': {
        EXPECTED: 'add': {
        EXPECTED: 'products': [{
        EXPECTED: 'name': '<<EVENT NAME>>', e.g. 'Kempton- 19:55'
        EXPECTED: 'category': '<<EVENT CATEGORY>>', e.g. '21'
        EXPECTED: 'variant': '<<EVENT TYPE>>', e.g. '1941'
        EXPECTED: 'brand': '<<EVENT MARKET NAME>>', e.g. 'Win or EW'
        EXPECTED: 'cd100': '<<EVENT ID>>', e.g. '11564441'
        EXPECTED: 'cd101': '<<SELECTION ID>>', e.g. '852419294'
        EXPECTED: 'cd102': <<IN PLAY STATUS>>,
        EXPECTED: 'cd102' = '1' belongs to In Play event
        EXPECTED: 'cd102' = '0' belongs to Pre Match event
        EXPECTED: 'cd106': <<CUSTOMER BUILT>>,
        EXPECTED: 'cd106' = '1' bet type = BYB
        EXPECTED: 'cd106' = '0' bet was built by Trader
        EXPECTED: 'cd107': '<<LOCATION>>', e.g. "Matches. Today" - the page bet originated from
        EXPECTED: 'cd108': '<<MODULE>>' e.g. "England - Premier League" - the accordion bet originated from
        EXPECTED: }]
        EXPECTED: Parameters 'category', 'variant' and 'cd100' correspond to Openbet info for event that was added to Quick Bet
        """
        self.verify_ga_tracking_record(brand=vec.siteserve.EXPECTED_MARKETS_NAMES.match_result,
                                       category=self.ob_config.backend.ti.football.category_id,
                                       event_id=self.event_id,
                                       selection_id=self.selection_ids['Draw'],
                                       inplay_status=0, customer_built=0,
                                       location=self.get_default_tab_name_on_sports_edp(event_id=self.event_id),
                                       module='edp',
                                       name=self.event_name1,
                                       variant=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
                                       event='trackEvent',
                                       event_action='add to quickbet',
                                       event_category='quickbet',
                                       event_label='success',
                                       stream_active=False,
                                       stream_ID=None,
                                       dimension86=0,
                                       dimension87=0,
                                       dimension88=None,
                                       metric1=0)
        self.site.quick_bet_panel.header.close_button.click()
        self.site.wait_quick_bet_overlay_to_hide(timeout=15)

    def test_003_add_sport_inplay_selection_to_quick_bet(self):
        """
        DESCRIPTION: Navigate to Event Details page
        DESCRIPTION: Add <Sport> In play selection to Quick Bet
        EXPECTED: Quick bet appears at the bottom of the page
        """
        self.navigate_to_edp(self.inplay_event_id)
        self.add_selection_from_event_details_to_quick_bet()

        self.assertTrue(self.site.wait_for_quick_bet_panel(expected_result=True), msg='Quick Bet is not present')

    def test_004_verify_tracking_for_inplay(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next push is sent:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'quickbet',
        EXPECTED: 'eventAction' : 'add to quickbet',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'ecommerce': {
        EXPECTED: 'add': {
        EXPECTED: 'products': [{
        EXPECTED: 'name': '<<EVENT NAME>>', e.g. 'Kempton- 19:55'
        EXPECTED: 'category': '<<EVENT CATEGORY>>', e.g. '21'
        EXPECTED: 'variant': '<<EVENT TYPE>>', e.g. '1941'
        EXPECTED: 'brand': '<<EVENT MARKET NAME>>', e.g. 'Win or EW'
        EXPECTED: 'cd100': '<<EVENT ID>>', e.g. '11564441'
        EXPECTED: 'cd101': '<<SELECTION ID>>', e.g. '852419294'
        EXPECTED: 'cd102': <<IN PLAY STATUS>>,
        EXPECTED: 'cd102' = '1' belongs to In Play event
        EXPECTED: 'cd102' = '0' belongs to Pre Match event
        EXPECTED: 'cd106': <<CUSTOMER BUILT>>,
        EXPECTED: 'cd106' = '1' bet type = BYB
        EXPECTED: 'cd106' = '0' bet was built by Trader
        EXPECTED: 'cd107': '<<LOCATION>>', e.g. "Matches. Today" - the page bet originated from
        EXPECTED: 'cd108': '<<MODULE>>' e.g. "England - Premier League" - the accordion bet originated from
        EXPECTED: }]
        EXPECTED: Parameters 'category', 'variant' and 'cd100' correspond to Openbet info for event that was added to Quick Bet
        """
        self.verify_ga_tracking_record(brand=vec.siteserve.EXPECTED_MARKETS_NAMES.match_result,
                                       category=self.ob_config.backend.ti.football.category_id,
                                       event_id=self.inplay_event_id,
                                       selection_id=self.inplay_event_selection_ids['Draw'],
                                       inplay_status=1, customer_built=0,
                                       location=self.get_default_tab_name_on_sports_edp(event_id=self.inplay_event_id),
                                       module='edp',
                                       name=self.inplay_event_name,
                                       variant=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
                                       event='trackEvent',
                                       event_action='add to quickbet',
                                       event_category='quickbet',
                                       event_label='success',
                                       stream_active=False,
                                       stream_ID=None,
                                       dimension86=0,
                                       dimension87=0,
                                       dimension88=None,
                                       metric1=0)
        self.site.quick_bet_panel.header.close_button.click()
        self.site.wait_quick_bet_overlay_to_hide(timeout=15)

    def test_005_add_next4_selection_to_quick_bet(self):
        """
        DESCRIPTION: Tap 'Horse Racing' icon from the sports menu ribbon
        DESCRIPTION: Add <Race> selection from Next Races module to Quick Bet
        EXPECTED: Horse Racing landing page is opened
        """
        self.device.refresh_page()  # so the old dataLayer responses are gone
        self.site.wait_splash_to_hide()
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing')

        autotest_event = self.get_event_from_next_races_module(event_name=self.event_name.upper(), timeout=5)

        runners = autotest_event.items_as_ordered_dict
        self.assertTrue(runners, msg='No runners found')

        self.__class__.first_runner_name, first_runner = list(runners.items())[0]
        self.__class__.second_runner_name, self.__class__.second_runner = list(runners.items())[-1]

        self._logger.debug('*** Selected first runner: "%s"' % self.first_runner_name)
        first_runner.bet_button.click()
        self.site.wait_for_quick_bet_panel(timeout=5)

    def test_006_verify_tracking_for_next4_event(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next push is sent:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'quickbet',
        EXPECTED: 'eventAction' : 'add to quickbet',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'ecommerce': {
        EXPECTED: 'add': {
        EXPECTED: 'products': [{
        EXPECTED: 'name': '<<EVENT NAME>>', e.g. 'Kempton- 19:55'
        EXPECTED: 'category': '<<EVENT CATEGORY>>', e.g. '21'
        EXPECTED: 'variant': '<<EVENT TYPE>>', e.g. '1941'
        EXPECTED: 'brand': '<<EVENT MARKET NAME>>', e.g. 'Win or EW'
        EXPECTED: 'cd100': '<<EVENT ID>>', e.g. '11564441'
        EXPECTED: 'cd101': '<<SELECTION ID>>', e.g. '852419294'
        EXPECTED: 'cd102': <<IN PLAY STATUS>>,
        EXPECTED: 'cd102' = '1' belongs to In Play event
        EXPECTED: 'cd102' = '0' belongs to Pre Match event
        EXPECTED: 'cd106': <<CUSTOMER BUILT>>,
        EXPECTED: 'cd106' = '1' bet type = BYB
        EXPECTED: 'cd106' = '0' bet was built by Trader
        EXPECTED: 'cd107': '<<LOCATION>>', e.g. "Matches. Today" - the page bet originated from
        EXPECTED: 'cd108': '<<MODULE>>' e.g. "England - Premier League" - the accordion bet originated from
        EXPECTED: }]
        EXPECTED: Parameters 'category', 'variant' and 'cd100' correspond to Openbet info for event that was added to Quick Bet
        """
        self.verify_ga_tracking_record(brand='Win or Each Way',
                                       category=self.ob_config.horseracing_config.category_id,
                                       event_id=self.next4_event_id,
                                       selection_id=self.next4_selection_ids[self.first_runner_name],
                                       inplay_status=0, customer_built=0,
                                       location=vec.racing.RACING_DEFAULT_TAB_NAME,
                                       module='next races',
                                       name=self.event_name,
                                       variant=self.ob_config.horseracing_config.horse_racing_live.autotest_uk.type_id,
                                       event='trackEvent',
                                       event_action='add to quickbet',
                                       event_category='quickbet',
                                       event_label='success',
                                       stream_active=False,
                                       stream_ID=None,
                                       dimension86=0,
                                       dimension87=0,
                                       dimension88=None,
                                       metric1=0)
