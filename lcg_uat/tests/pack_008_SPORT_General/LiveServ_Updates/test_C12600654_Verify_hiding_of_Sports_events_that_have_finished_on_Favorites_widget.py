import pytest

import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.crl_tst2  # Сoral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_hl
# @pytest.mark.crl_prod
@pytest.mark.football
@pytest.mark.favourites
@pytest.mark.desktop_only
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.login
@vtest
class Test_C12600654_Verify_hiding_of_Sports_events_that_have_finished_on_Favorites_widget(BaseSportTest):
    """
    TR_ID: C12600654
    VOL_ID: C12797069
    NAME: Verify hiding of <Sports> events that have finished on Favorites widget
    DESCRIPTION: This test case verifies hiding of <Sports> events that have finished on Favorites widget
    PRECONDITIONS: 1. LiveServer is available for In-Play <Sport> events with the following attributes:
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL"
    PRECONDITIONS: isMarketBetInRun = "true"
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: 2. http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: 3. To verify 'Displayed' and 'Result_conf' attributes values check Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket
    PRECONDITIONS: 4. Use http://backoffice-tst2.coral.co.uk/ti/ for triggering events undisplaying or setting results
    PRECONDITIONS: *NOTE:* *LiveServe pushes with updates also are received if selection is added to the betslip*
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def check_widget_content(self, expected_events: list, expected_result=True) -> None:
        """
        Verifies that 'FAVOURITES' widget contains expected events
        :param expected_events: list of expected events
        """
        self.__class__.favorites_widget = self.site.favourites
        widget_odds_cards = self.favorites_widget.items_as_ordered_dict
        displayed_odds_cards = list(widget_odds_cards.keys())
        if expected_result:
            self.assertEqual(expected_events, displayed_odds_cards,
                             msg=f'Expected events to be displayed in the widget: "{expected_events}". '
                                 f'Actually displayed events: "{displayed_odds_cards}"')
        else:
            self.assertNotIn(expected_events, displayed_odds_cards, msg=f'"{expected_events}" is still displaying in '
                                                                        f'section "{displayed_odds_cards}"')

    def add_selection_to_favourites(self, event_name: str):
        """
        :param event_name: name of event created in preconditions
        :return:
        """
        self.__class__.favorites_widget = self.site.favourites
        self.assertTrue(self.favorites_widget.is_displayed(), msg='"FAVORITES" widget is not displayed')

        self.favorites_widget.collapse()
        self.assertFalse(self.favorites_widget.is_expanded(expected_result=False),
                         msg='\'FAVORITES\' widget is not collapsed')
        self.favorites_widget.expand()
        self.assertTrue(self.favorites_widget.is_expanded(), msg='\'FAVORITES\' widget is not expanded')

        self.site.sport_event_details.favourite_icon.click()
        self.assertTrue(self.site.sport_event_details.favourite_icon.is_selected(),
                        msg=f'Favourite icon is not selected for "{event_name}" event')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add live football events
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.eventID = event_params.event_id
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'

        event_params2 = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.eventID2, self.__class__.selection_id, self.__class__.team1_1, self.__class__.team2_2 \
            = event_params2.event_id, event_params2.selection_ids, event_params2.team1, event_params2.team2
        self.__class__.event_name2 = f'{self.team1_1} v {self.team2_2}'
        self.site.login(timeout=30)

    def test_001_navigate_to_football_landing_page_from_sports_ribbonleft_navigation_menu(self):
        """
        DESCRIPTION: Navigate to Football event details page
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_002_add_event_to_favorites_star_icon(self):
        """
        DESCRIPTION: Add event to favorites (star icon)
        EXPECTED: Event is added to the favorites widget
        """
        self.add_selection_to_favourites(event_name=self.event_name)
        self.check_widget_content(expected_events=[self.event_name])

    def test_003_undisplay_event_from_the_current_page(self):
        """
        DESCRIPTION: Undisplay event from the current page
        EXPECTED: * [displayed:"N"] attribute is received in LIVE SERV push/WS
        EXPECTED: * Event disappears on front end
        EXPECTED: * Whole type section disappears on front end if it contains only one event
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=False)
        self.check_widget_content(expected_events=[self.event_name], expected_result=False)

    def test_004_set_results_for_another_event_from_the_current_page(self):
        """
        DESCRIPTION: Navigate to EDP and set results for another event from the current page
        EXPECTED: * [displayed:"N"] or [result_conf:"Y"] attributes are received in LIVE SERV push/WS
        EXPECTED: * Event disappears on front end
        EXPECTED: * Whole type section disappears on front end if it contains only one event
        """
        self.navigate_to_edp(event_id=self.eventID2)
        self.add_selection_to_favourites(event_name=self.event_name2)
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        market_id = self.ob_config.market_ids[self.eventID2][market_short_name]
        for selection in (list(self.selection_id.values())):
            self.ob_config.update_selection_result(selection_id=selection, market_id=market_id, event_id=self.eventID2)

        self.check_widget_content(expected_events=[self.event_name], expected_result=False)
