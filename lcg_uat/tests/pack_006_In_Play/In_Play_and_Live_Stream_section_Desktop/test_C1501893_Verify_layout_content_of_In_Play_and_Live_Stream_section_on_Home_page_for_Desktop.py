import pytest
import tests
from tests.base_test import vtest
from time import sleep
from voltron.utils.exceptions.precondition_not_met_exception import PreconditionNotMetException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can not create events in prod/beta
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C1501893_Verify_layout_content_of_In_Play_and_Live_Stream_section_on_Home_page_for_Desktop(BaseBetSlipTest):
    """
    TR_ID: C1501893
    NAME: Verify layout/content of 'In-Play and Live Stream' section on Home page for Desktop
    DESCRIPTION: This test case verifies layout/content of 'In-Play and Live Stream' section on Home page for Desktop
    PRECONDITIONS: 1) Use the following link for checking attributes of In-Play events:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL" - means Bet In Play List
    PRECONDITIONS: isStarted="true" - means event is started
    PRECONDITIONS: 2) Types of available streams:
    PRECONDITIONS: EVFLAG_IVM - IMG Video Mapped for this event
    PRECONDITIONS: EVFLAG_PVM - Perform Video Mapped for this event
    PRECONDITIONS: EVFLAG_AVA - At The Races stream available
    PRECONDITIONS: EVFLAG_RVA - RacingUK stream available
    PRECONDITIONS: EVFLAG_RPM - RPGTV Greyhound streaming Mapped
    PRECONDITIONS: EVFLAG_GVM - iGameMedia streaming Mapped
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/Get live events
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True, img_stream=True,
                                                                                 perform_stream=True)
        live_now_event_id = event_params.event_id
        live_now_event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=live_now_event_id)
        self.get_accordion_name_for_event_from_ss(event=live_now_event_resp[0],
                                                  live_stream_tab_homepage=True)

    def test_001_load_oxygen_app_on_desktop(self):
        """
        DESCRIPTION: Load Oxygen app on Desktop
        EXPECTED: Homepage is opened
        """
        self.site.login()
        self.site.wait_content_state('Homepage')

    def test_002_scroll_the_page_down_to_view_in_play_and_live_stream_section(self):
        """
        DESCRIPTION: Scroll the page down to view 'In-play and Live Stream' section
        EXPECTED: * 'In-play and Live Stream' section is displayed below 'Enhances Multiples' carousel
        EXPECTED: * Two switchers are visible: 'In-Play' and 'Live Stream'
        EXPECTED: * 'In-Play' switcher is selected by default
        EXPECTED: * First 'Sport' tab is selected by default
        """
        sports = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
        self.assertTrue(sports.keys(), msg='"Menu Carousel" of sports is not displayed')
        if vec.SB.FOOTBALL.upper() in sports.keys():
            tab = sports[vec.SB.FOOTBALL.upper()]
            if tab.is_selected():
                self.assertTrue(tab.is_selected(), msg='"football" tab is not selected by default')
            else:
                tab.click()
        try:
            self.__class__.leagues = self.site.home.get_module_content(
                'IN-PLAY AND LIVE STREAM').accordions_list.items_as_ordered_dict
        except VoltronException:
            raise PreconditionNotMetException('No events found in "INPLAY" section')

    def test_003_verify_header(self):
        """
        DESCRIPTION: Verify header
        EXPECTED: Header consist of:
        EXPECTED: * 'In-Play and Live Stream' section name
        EXPECTED: * In-play Sports Ribbon
        """
        self.assertTrue(self.site.home.desktop_modules.inplay_live_stream_module.is_displayed(),
                        msg='"In-play and live stream" ribbon is not present on Homepage')
        sports = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
        self.assertTrue(sports.keys(), msg='"Menu Carousel" of sports is not displayed')

    def test_004_verify_in_play_view(self):
        """
        DESCRIPTION: Verify 'In-play' view
        EXPECTED: * Max 4 events are shown
        EXPECTED: * Events are grouped by 'typeId'
        EXPECTED: * It is possible to collapse/expand all of the accordions by clicking the accordion's header
        EXPECTED: * 'Cash out' icon is displayed if available
        """
        comp_count = []
        competitions = self.site.home.desktop_modules.inplay_live_stream_module.tab_content.accordions_list.items_as_ordered_dict
        for comp_name, comp in list(competitions.items()):
            if len(comp_count) < 4:
                comp_count.append(comp)
                self.assertTrue(comp.is_expanded(), msg='First 4 events are not expanded by default')

    def test_005_verify_events_that_are_shown_when_in_play_is_selected(self, drilldowntagnames=['EVFLAG_BL'],
                                                                       livestream=False):
        """
        DESCRIPTION: Verify events that are shown when 'In-play' is selected
        EXPECTED: All events with attributes:
        EXPECTED: *   Event's/market's/outcome's attribute 'siteCannels' contains 'M'
        EXPECTED: *   Attribute 'isStarted="true"' is present
        EXPECTED: *   Event's attribute 'drilldownTagNames' contains "EVFLAG_BL"
        EXPECTED: *   Attribute 'isLiveNowEvent="true"' is present
        EXPECTED: *   Time in 'suspendAtTime' attribute of the event is NOT in the past or it is not present
        EXPECTED: *   At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: *   At least one market is not resulted (there is no attribute 'isResulted="true")
        EXPECTED: *   At least one market is displayed (available in the response)
        """
        if self.leagues:
            for league in self.leagues.values():
                events = league.items_as_ordered_dict
                for event in events.values():
                    event_id = event.template.event_id
                    event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)[0]['event']
                    self.assertIn('M', event_details['siteChannels'],
                                  msg='Event attribute siteChannels does not contain "M".')
                    self.assertEqual(event_details['isStarted'], 'true',
                                     msg='Event attribute isStarted does not contain "true".')
                    self.assertEqual(event_details['isLiveNowEvent'], 'true',
                                     msg='Event attribute isLiveNowEvent does not contain "true".')
                    if livestream:
                        self.assertTrue(
                            drilldowntagnames[0] or drilldowntagnames[1] or drilldowntagnames[2] in event_details[
                                'drilldownTagNames'],
                            msg=f'Event attribute drilldownTagNames does not contain "{drilldowntagnames}"')
                        self.assertTrue('IVA,' or 'PVA,' or 'GVA,' in event_details['typeFlagCodes'],
                                        msg='"IVA" or "PVA" or "GVA" not present in "typeFlagCodes" attribute')
                    else:
                        self.assertIn(drilldowntagnames[0], event_details['drilldownTagNames'],
                                      msg=f'Event attribute drilldownTagNames does not contain "{drilldowntagnames}"')
                    for market in event_details['children']:
                        market_details = market['market']
                        if market_details['isMarketBetInRun'] == 'true' and 'isResulted' not in event_details:
                            break
                    else:
                        raise VoltronException(
                            'Not even one market contains attribute "isMarketBetInRun=true" and "isResulted!=true"')
        else:
            raise PreconditionNotMetException('No live events found to verify')

    def test_006_verify_in_play_view_footer(self):
        """
        DESCRIPTION: Verify 'In-play' view footer
        EXPECTED: Footer link redirects to In-play page with 'All sports' or specific <sport> tab selected, depending on number of events
        """
        self.site.home.desktop_modules.inplay_live_stream_module.view_all_live_stream_sport_events_button.click()
        leagues = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(leagues,
                        msg='"Events" are not displayed.')

    def test_007_verify_live_stream_view(self):
        """
        DESCRIPTION: Verify 'Live Stream' view
        EXPECTED: * Max 4 events are shown
        EXPECTED: * Events are grouped by 'typeId'
        EXPECTED: * It is possible to collapse/expand all of the accordions by clicking the accordion's header
        EXPECTED: * 'Cash out' icon is displayed if available
        """
        self.site.back_button.click()
        self.site.wait_content_state_changed(timeout=20)
        sports = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
        if vec.SB.FOOTBALL.upper() in sports.keys():
            tab = sports[vec.SB.FOOTBALL.upper()]
            if tab.is_selected():
                self.assertTrue(tab.is_selected(), msg='"football" tab is not selected by default')
            else:
                tab.click()

        self.site.home.desktop_modules.inplay_live_stream_module.tabs_menu.click_item(vec.sb.LIVE_STREAM.upper())
        comp_count = []
        competitions = self.site.home.desktop_modules.inplay_live_stream_module.tab_content.accordions_list.items_as_ordered_dict
        for comp_name, comp in list(competitions.items()):
            if len(comp_count) < 4:
                comp_count.append(comp)
                self.assertTrue(comp.is_expanded(), msg='First 4 events are not expanded by default')

    def test_008_verify_events_that_are_shown_when_live_stream_is_selected(self):
        """
        DESCRIPTION: Verify events that are shown when 'Live Stream' is selected
        EXPECTED: * Event's/market's/outcome's attribute 'siteCannels' contains 'M'
        EXPECTED: * Attribute 'isStarted="true"' is present
        EXPECTED: * drilldownTagNames **should include the following attributes: {EVFLAG_BL and EVFLAG_IVM} OR {EVFLAG_BL, EVFLAG_PVM} OR {EVFLAG_BL, EVFLAGIVM, EVFLAG_PVM} OR {EVFLAG_BL, EVFLAG_GVM}(on the Event level) **
        EXPECTED: * Attribute 'isLiveNowEvent="true"' is present
        EXPECTED: * At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: * event startTime **is today**
        """
        try:
            self.leagues = self.site.home.desktop_modules.inplay_live_stream_module.tab_content.accordions_list.items_as_ordered_dict
        except VoltronException:
            raise PreconditionNotMetException('No live stream events found to verify')
        self.test_005_verify_events_that_are_shown_when_in_play_is_selected(livestream=True,
                                                                            drilldowntagnames=['EVFLAG_BL,EVFLAG_IVM',
                                                                                               'EVFLAG_BL,EVFLAG_PVM',
                                                                                               'EVFLAG_BL,EVFLAG_GVM'])

    def test_009_verify_live_stream_view_footer(self):
        """
        DESCRIPTION: Verify 'Live Stream' view footer
        EXPECTED: Footer link is always shown and redirects to 'Live Stream' page
        """
        self.site.home.desktop_modules.inplay_live_stream_module.view_all_live_stream_sport_events_button.click()
        self.site.wait_content_state(state_name='LiveStream', timeout=20)
        leagues = self.site.live_stream.tab_content.accordions_list.items_as_ordered_dict

        self.assertTrue(leagues,
                        msg='"Events" are not displayed.')
        sleep(3)
        length = len(list(leagues.keys()))
        number_of_leagues = 2 if length > 3 else length
        for league in list(leagues.values())[::number_of_leagues]:
            events = league.items_as_ordered_dict
            selection = list(events.values())[0]
            self.__class__.event = list(selection.items_as_ordered_dict.values())[0]
            bet_button = self.site.home.bet_buttons[0]
            self.assertTrue(bet_button, msg='No bet buttons present in the EDP')
            bet_button.click()
            self.site.open_betslip()
            self.assertTrue(self.site.has_betslip_opened(), msg='Failed to open Betslip')
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()

    def test_010_click_on_any_selection_from_the_widget(self):
        """
        DESCRIPTION: Click on any selection from the widget
        EXPECTED: * Selection is successfully added to Betslip
        EXPECTED: * Selection is marked as added in 'In-Play & Live Stream' section
        """
        # covered in step 009

    def test_011_place_a_bet_for_added_selection(self):
        """
        DESCRIPTION: Place a bet for added selection
        EXPECTED: Bet is placed successfully
        EXPECTED: Selection is unmarked in 'In-Play & Live Stream' section
        """
        # covered in step 009

    def test_012_click_on_event_card_section(self):
        """
        DESCRIPTION: Click on Event card section
        EXPECTED: User is redirected to Event Details page
        """
        self.event.click()
        self.site.wait_content_state('EventDetails', timeout=20)

    def test_013_repeat_steps_10_12_when_live_stream_view_is_selected(self):
        """
        DESCRIPTION: Repeat steps 10-12 when 'Live Stream' view is selected
        EXPECTED:
        """
        # covered in step 009
