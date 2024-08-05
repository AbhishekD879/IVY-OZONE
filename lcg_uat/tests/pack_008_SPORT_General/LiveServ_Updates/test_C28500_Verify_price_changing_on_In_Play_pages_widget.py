import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from voltron.utils.helpers import wait_for_category_in_inplay_module_from_ws
from voltron.utils.helpers import wait_for_category_in_inplay_structure
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.football
@pytest.mark.slow
@pytest.mark.timeout(800)
@pytest.mark.in_play
@pytest.mark.liveserv_updates
@vtest
class Test_C28500_Verify_price_changing_on_In_Play_pages_widget(BaseSportTest):
    """
    TR_ID: C28500
    NAME: Verify price changing on In-Play pages/widget
    DESCRIPTION: This test case verifies price changing on In-Play pages/widget
    PRECONDITIONS: 1) LiveServer is available only for In-Play <Sport> events with the following attributes:
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL"
    PRECONDITIONS: isMarketBetInRun = "true"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: 3) To verify price updates check new received values in "lp_den" and "lp_num" attributes using Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: PRICE
    PRECONDITIONS: **NOTE:**LivePrice updates are NOT applicable for Outrights and Enhanced Multiples events
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to 'In-play' page from Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for desktop)
    PRECONDITIONS: 3. Select 'Watch live' tab
    """
    keep_browser_open = True
    new_price = '1/7'
    new_price_2 = '1/13'
    widget_section_name = 'In-Play LIVE Football'

    def get_price_button(self, event):
        price_buttons = event.get_active_prices()
        self.assertTrue(price_buttons, msg='Price buttons were not found')
        _, price_button = list(price_buttons.items())[0]
        if price_button:
            price_button.scroll_to()
        return price_button

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create live now and upcoming events
        """
        inplay_module = self.cms_config.get_sport_module(module_type='INPLAY')
        if inplay_module[0]['disabled']:
            raise CmsClientException('"In play module" module is disabled for homepage')
        league = tests.settings.football_autotest_competition_league
        self.__class__.league_name = league.title() if self.brand == 'bma' else league
        self.__class__.sport_name = 'Football' if self.brand == 'bma' else 'FOOTBALL'
        self.__class__.sport_name_homepage_inplay_module = 'FOOTBALL'

        event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.live_now_event_id = event_params.event_id
        live_now_event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.live_now_event_id,
                                                                        query_builder=self.ss_query_builder)

        self.__class__.live_now_event_name = normalize_name(live_now_event_resp[0]['event']['name'])
        self.__class__.live_now_selection_id = list(event_params.selection_ids.values())[0]

        event_params_2 = self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True)
        self.__class__.upcoming_event_id = event_params_2.event_id
        upcoming_event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.upcoming_event_id,
                                                                        query_builder=self.ss_query_builder)

        self.__class__.upcoming_event_name = normalize_name(upcoming_event_resp[0]['event']['name'])
        self.__class__.upcoming_selection_id = list(event_params_2.selection_ids.values())[0]

        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=live_now_event_resp[0],
                                                                                in_play_tab_slp=True)

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        in_play_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                              self.ob_config.football_config.category_id)
        result = self.site.football.tabs_menu.click_button(in_play_tab)
        self.assertTrue(result, msg=f'"{in_play_tab}" tab was not opened')

    def test_001_trigger_price_change_for_primary_market_outcome_for_one_of_events_within_live_now_section(self):
        """
        DESCRIPTION: Trigger price change for <Primary market> outcome for one of events within 'Live now' section
        EXPECTED: Corresponding 'Price/Odds' button immediately displays new price and for a few seconds it changes its color to:
        EXPECTED: - blue color if price has decreased
        EXPECTED: - red color if price has increased
        """
        event = self.get_event_from_league(event_id=self.live_now_event_id, section_name=self.section_name)

        self.ob_config.change_price(selection_id=self.live_now_selection_id, price=self.new_price)
        result = wait_for_result(lambda: self.get_price_button(event=event).name == self.new_price,
                                 timeout=40,
                                 expected_result=True,
                                 bypass_exceptions=(
                                     NoSuchElementException, StaleElementReferenceException, VoltronException),
                                 name=f'Price to be changed')
        self.assertTrue(result, msg=f'Price was not changed')

        self.ob_config.change_price(selection_id=self.live_now_selection_id, price=self.new_price_2)
        result = wait_for_result(lambda: self.get_price_button(event=event).name == self.new_price_2,
                                 timeout=40,
                                 expected_result=True,
                                 bypass_exceptions=(
                                     NoSuchElementException, StaleElementReferenceException, VoltronException),
                                 name=f'Price to be changed')
        self.assertTrue(result, msg=f'Price was not changed')

    def test_002__collapse_sporttype_accordion_trigger_price_change_expand_sporttype_accordion_and_verify_prices_changes(self):
        """
        DESCRIPTION: * Collapse sport/type accordion
        DESCRIPTION: * Trigger price change
        DESCRIPTION: * Expand sport/type accordion and verify prices changes
        EXPECTED: If section is collapsed and price was changed, after expanding the section - updated price will be shown there
        """
        self.__class__.section = self.get_section(section_name=self.section_name)
        self.section.collapse()
        self.ob_config.change_price(selection_id=self.live_now_selection_id, price=self.new_price)

        event = self.get_event_from_league(event_id=self.live_now_event_id, section_name=self.section_name)
        price_buttons = event.get_active_prices()
        self.assertTrue(price_buttons, msg='Price buttons were not found')
        _, price_button = list(price_buttons.items())[0]

        result = wait_for_result(lambda: self.get_price_button(event=event).name == self.new_price,
                                 timeout=40,
                                 expected_result=True,
                                 bypass_exceptions=(
                                     NoSuchElementException, StaleElementReferenceException, VoltronException),
                                 name=f'Price to be changed')
        self.assertTrue(result, msg=f'Price was not changed')

        self.section.collapse()
        self.ob_config.change_price(selection_id=self.live_now_selection_id, price=self.new_price_2)

        event = self.get_event_from_league(event_id=self.live_now_event_id, section_name=self.section_name)
        price_buttons = event.get_active_prices()
        self.assertTrue(price_buttons, msg='Price buttons were not found')
        _, price_button = list(price_buttons.items())[0]

        result = wait_for_result(lambda: price_button.name == self.new_price_2,
                                 timeout=40,
                                 expected_result=True,
                                 bypass_exceptions=(
                                     NoSuchElementException, StaleElementReferenceException, VoltronException),
                                 name=f'Price to be changed')
        self.assertTrue(result, msg=f'Price was not changed. Current price is "{price_button.name}", '
                                    f'expected is {self.new_price_2}')

    def test_003_trigger_price_change_for_primary_market_outcome_for_one_of_events_within_upcoming_events_section(self):
        """
        DESCRIPTION: Trigger price change for <Primary market> outcome for one of events within 'Upcoming events' section
        EXPECTED: Corresponding 'Price/Odds' button immediately displays new price and for a few seconds it changes its color to:
        EXPECTED: - blue color if price has decreased
        EXPECTED: - red color if price has increased
        """
        if self.device_type == 'desktop':
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
        self.ob_config.change_price(selection_id=self.upcoming_selection_id, price=self.new_price)

        event = self.get_event_from_league(event_id=self.upcoming_event_id, section_name=self.section_name, inplay_section=vec.inplay.UPCOMING_SWITCHER)
        result = wait_for_result(lambda: self.get_price_button(event=event).name == self.new_price,
                                 timeout=40,
                                 expected_result=True,
                                 bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException),
                                 name=f'Price to be changed')
        self.assertTrue(result, msg=f'Price was not changed')

        self.ob_config.change_price(selection_id=self.upcoming_selection_id, price=self.new_price_2)
        result = wait_for_result(lambda: self.get_price_button(event=event).name == self.new_price_2,
                                 timeout=40,
                                 expected_result=True,
                                 bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException),
                                 name=f'Price to be changed')
        self.assertTrue(result, msg=f'Price was not changed.')

    def test_004__collapse_sport_type_accordion_trigger_price_change_expand_sporttype_accordion_and_verify_prices_changes(self):
        """
        DESCRIPTION: * Collapse sport/type accordion
        DESCRIPTION: * Trigger price change
        DESCRIPTION: * Expand sport/type accordion and verify prices changes
        EXPECTED: If section is collapsed and price was changed, after expanding the section - updated price will be shown there
        """
        self.__class__.section = self.get_section(section_name=self.section_name)
        self.section.collapse()
        self.ob_config.change_price(selection_id=self.upcoming_selection_id, price=self.new_price)

        event = self.get_event_from_league(event_id=self.upcoming_event_id, section_name=self.section_name,
                                           inplay_section=vec.inplay.UPCOMING_SWITCHER)
        result = wait_for_result(lambda: self.get_price_button(event=event).name == self.new_price,
                                 timeout=40,
                                 expected_result=True,
                                 bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException),
                                 name=f'Price to be changed')
        self.assertTrue(result, msg=f'Price was not changed')

        self.section.collapse()
        self.ob_config.change_price(selection_id=self.upcoming_selection_id, price=self.new_price_2)

        event = self.get_event_from_league(event_id=self.upcoming_event_id, section_name=self.section_name,
                                           inplay_section=vec.inplay.UPCOMING_SWITCHER)
        result = wait_for_result(lambda: self.get_price_button(event=event).name == self.new_price_2,
                                 timeout=40,
                                 expected_result=True,
                                 bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException),
                                 name=f'Price to be changed')
        self.assertTrue(result, msg=f'Price was not changed')

    def test_005__navigate_back_to_homepage_trigger_price_change_for_any_sport_live_event(self):
        """
        DESCRIPTION: * Navigate back to Homepage
        DESCRIPTION: * Trigger price change for any <Sport> live event
        EXPECTED: If In-Play Sports page was not opened and price was changed there, after opening In-Play Sports page - updated price will be shown there
        """
        self.navigate_to_page(name='home')
        self.site.wait_splash_to_hide()
        self.site.wait_content_state(state_name='HomePage')

        self.ob_config.change_price(selection_id=self.live_now_selection_id, price=self.new_price)

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        in_play_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                              self.ob_config.football_config.category_id)
        result = self.site.football.tabs_menu.click_button(in_play_tab)
        self.assertTrue(result, msg='"IN-PLAY" tab was not opened')

        event = self.get_event_from_league(event_id=self.live_now_event_id, section_name=self.section_name)
        result = wait_for_result(lambda: self.get_price_button(event=event).name == self.new_price,
                                 timeout=40,
                                 expected_result=True,
                                 bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException),
                                 name=f'Price to be changed')
        self.assertTrue(result, msg=f'Price was not changed')

    def test_006_verify_prices_changes_before_application_is_opened(self):
        """
        DESCRIPTION: Verify prices changes before application is opened
        EXPECTED: If application was not started/opened and price was changed for live sports event market 'Match Betting', after opening application and In-Play Sports page - updated price will be shown there
        """
        pass  # covered in previous step

    def test_007_repeat_steps_1_6_on_in_play_page__when_any_sport_is_selected_in_sports_menu_ribbon_home_page__in_play_tab_home_page__featured_in_play_module_sport_landing_page__in_play_tab_sport_landing_page__featured_in_play_module_on_matches_tab(self):
        """
        DESCRIPTION: Repeat steps 1-6 on:
        DESCRIPTION: * 'In-play' page > when any sport is selected in Sports Menu Ribbon
        DESCRIPTION: * Home page > 'In-play' tab
        DESCRIPTION: * Home page > featured 'In-play' module
        DESCRIPTION: * Sport Landing page > 'In-play' tab
        DESCRIPTION: * Sport Landing page > featured 'In-play' module on 'Matches' tab
        EXPECTED:
        """
        # 'In-play' page
        self.navigate_to_page(name='/in-play/football')
        self.site.wait_content_state(state_name='in-play')

        event = self.get_event_from_league(event_id=self.live_now_event_id, section_name=self.section_name)
        self.ob_config.change_price(selection_id=self.live_now_selection_id, price=self.new_price_2)

        price_buttons = event.get_active_prices()
        self.assertTrue(price_buttons, msg='Price buttons were not found')
        _, price_button = list(price_buttons.items())[0]

        result = wait_for_result(lambda: price_button.name == self.new_price_2,
                                 timeout=40,
                                 expected_result=True,
                                 name=f'Price to be changed')
        self.assertTrue(result, msg=f'Price was not changed. Current price is "{price_button.name}", '
                                    f'expected is {self.new_price_2}')

        # Home page > 'In-play' tab
        if self.device_type == 'mobile':
            self.navigate_to_page(name='home/in-play')
            self.site.wait_content_state('Homepage')

            wait_for_category_in_inplay_structure(category_id=self.ob_config.football_config.category_id)

            event = self.get_event_for_homepage_inplay_tab(sport_name=self.sport_name_homepage_inplay_module,
                                                           league_name=self.league_name,
                                                           event_name=self.live_now_event_name)

            self.ob_config.change_price(selection_id=self.live_now_selection_id, price=self.new_price_2)

            result = wait_for_result(lambda: self.get_price_button(event=event).name == self.new_price_2,
                                     timeout=40,
                                     expected_result=True,
                                     bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException),
                                     name=f'Price to be changed')
            self.assertTrue(result, msg=f'Price was not changed. Current price is "{self.get_price_button(event=event).name}", '
                                        f'expected is {self.new_price_2}')

        # Home page > featured 'In-play' module
            self.navigate_to_page(name='/')
            self.site.wait_content_state('Homepage')

            wait_for_category_in_inplay_module_from_ws(category_id=self.ob_config.football_config.category_id)

            in_play_module = self.site.home.tab_content.in_play_module
            sports = in_play_module.items_as_ordered_dict
            self.assertIn(self.sport_name, sports.keys(), msg=f'{self.sport_name} container is not displayed')
            sport = sports.get(self.sport_name)
            events = sport.items_as_ordered_dict
            self.assertTrue(events, msg='No events found')
            self.assertIn(self.live_now_event_name, list(events.keys()),
                          msg=f'{self.live_now_event_name} event was not found in '
                              f'the list of events {list(events.keys())}')
            event = events.get(self.live_now_event_name)

            self.ob_config.change_price(selection_id=self.live_now_selection_id, price=self.new_price_2)

            result = wait_for_result(lambda: self.get_price_button(event=event).name == self.new_price_2,
                                     timeout=40,
                                     expected_result=True,
                                     name=f'Price to be changed')
            self.assertTrue(result, msg=f'Price was not changed')

        # Sport Landing page > featured 'In-play' module on 'Matches' tab
            self.navigate_to_page(name='sport/football')
            self.site.wait_content_state(state_name='Football')

            wait_for_category_in_inplay_module_from_ws(category_id=self.ob_config.football_config.category_id,
                                                       delimiter=f'42/{self.ob_config.football_config.category_id},')

            in_play_module = self.site.football.tab_content.in_play_module
            self.assertTrue(in_play_module, msg='In-Play module was not found')
            leagues = in_play_module.items_as_ordered_dict
            self.assertIn(self.league_name, list(leagues.keys()),
                          msg=f'{self.league_name} league was not found in '
                              f'the list of leagues {list(leagues.keys())}')
            league = leagues.get(self.league_name)
            events = league.items_as_ordered_dict
            self.assertIn(self.live_now_event_name, events,
                          msg=f'{self.live_now_event_name} event was not found in '
                              f'the list of events {list(events.keys())}')
            event = events.get(self.live_now_event_name)

            self.ob_config.change_price(selection_id=self.live_now_selection_id, price=self.new_price)

            result = wait_for_result(lambda: self.get_price_button(event=event).name == self.new_price,
                                     timeout=35,
                                     expected_result=True,
                                     name=f'Price to be changed')
            self.assertTrue(result, msg=f'Price was not changed')

    def test_008_for_desktop_repeat_steps_1_6_on_sport_landing_page_for_in_play_widget_and_live_stream_widget(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 1-6 on Sport Landing page for 'In-play' widget and 'Live Stream' widget
        EXPECTED:
        """
        if self.device_type == 'desktop':
            self.navigate_to_page(name='sport/football')
            self.site.wait_splash_to_hide()
            self.site.wait_content_state(state_name='Football')

            sections = self.site.football.in_play_widget.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found on Football page')
            self.assertIn(self.widget_section_name, sections.keys(),
                          msg=f'{self.widget_section_name} not found in {sections.keys()}')
            section = sections[self.widget_section_name]
            events = section.content.items_as_ordered_dict
            self.softAssert(self.assertIn, self.live_now_event_name, events,
                            msg=f'Event {self.live_now_event_name} was not found in the list of events {events.keys()} on In Play widget')

            event = events.get(self.live_now_event_name)
            event.scroll_to()

            price_buttons = event.odds_buttons.items
            self.assertTrue(price_buttons, msg='Price buttons were not found')

            self.ob_config.change_price(selection_id=self.live_now_selection_id, price=self.new_price_2)

            result = wait_for_result(lambda: price_buttons[0].name == self.new_price_2,
                                     timeout=40,
                                     expected_result=True,
                                     name=f'Price to be changed')
            self.assertTrue(result, msg=f'Price was not changed')

    def test_009_for_desktop_repeat_steps_1_6_on_home_page_for_in_play__live_stream_section_for_both_switchers(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 1-6 on Home page for 'In-play & Live Stream' section for both switchers
        EXPECTED:
        """
        if self.device_type == 'desktop':
            self.navigate_to_page(name='/')
            self.site.wait_content_state('Homepage')

            inplay_sports = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            inplay_football_tab = inplay_sports.get(vec.inplay.IN_PLAY_FOOTBALL)
            self.assertTrue(inplay_football_tab, msg=f'"{vec.inplay.IN_PLAY_FOOTBALL}" tab not found')
            inplay_football_tab.click()
            self.assertTrue(inplay_football_tab.is_selected(),
                            msg=f'"{vec.inplay.IN_PLAY_FOOTBALL}" tab is not selected')

            in_play = self.site.home.get_module_content(vec.inplay.IN_PLAY_LIVE_STREAM_SECTION_NAME)
            if in_play.has_view_all_in_play_sport_events_button():
                in_play.view_all_in_play_sport_events_button.click()
            leagues = in_play.accordions_list.items_as_ordered_dict

            self.assertIn(self.section_name, leagues, msg=f'League {self.section_name} was not found among "{leagues.keys()}"')
            league = leagues.get(self.section_name)

            events = league.items_as_ordered_dict
            self.assertIn(self.live_now_event_name, events,
                          msg=f'Event {self.live_now_event_name} was not found in the list of events {events.keys()}')
            event = events.get(self.live_now_event_name)

            self.ob_config.change_price(selection_id=self.live_now_selection_id, price=self.new_price)

            result = wait_for_result(lambda: self.get_price_button(event=event.template).name == self.new_price,
                                     timeout=40,
                                     expected_result=True,
                                     name=f'Price to be changed')
            self.assertTrue(result, msg=f'Price was not changed')
