import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result
from time import sleep


@pytest.mark.crl_tst2  # Favourites is Coral only feature
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.football
@pytest.mark.navigation
@pytest.mark.favourites
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.sanity
@vtest
class Test_C874355_Verify_Football_Favourites_functionality(BaseBetSlipTest, BaseFeaturedTest):
    """
    TR_ID: C874355
    NAME: Verify Football Favourites functionality
    DESCRIPTION: This Test Case verifies Football 'Favourites’ functionality
    DESCRIPTION: *NOTE:*
    DESCRIPTION: Steps 7-12 should be ran only on Mobile/Tablet
    PRECONDITIONS: * Football Events are present on FE (not older than 12 hours from the start time of the event)
    PRECONDITIONS: * User is Logged Out
    """
    keep_browser_open = True
    sport_name = vec.sb.FOOTBALL
    other_sport_name = vec.sb.TENNIS

    def verify_favorite_counter_change(self, expected_counter: int, event_name: str = None):
        if self.device_type == 'mobile':
            wait_for_result(lambda: int(self.site.football.header_line.favourites_counter) == expected_counter,
                            timeout=expected_counter,
                            name='Favorite counter to change')
            counter = self.site.football.header_line.favourites_counter
        else:
            self.site.favourites.expand()
            sections = self.site.favourites.items_as_ordered_dict
            counter = len(sections)

            if expected_counter == 0:
                self.assertFalse(sections, msg='Favourites widget is not empty')
            else:
                self.assertTrue(sections, msg='No selections found on Favourites widget')

                event = sections.get(event_name)
                self.assertTrue(event, msg=f'Event: "{event_name}" not found among: {list(sections.keys())}')

        self.assertEqual(int(counter), expected_counter,
                         msg=f'Actual favourites counter {counter} != "{expected_counter}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create / Found events for test
        """
        self.__class__.football_category_id = self.ob_config.football_config.category_id
        tennis_category_id = self.ob_config.tennis_config.category_id

        favourites_enabled_status = self.get_favourites_enabled_status()
        if not favourites_enabled_status:
            raise CmsClientException(f'"Favourites" is not enabled for device type: "{self.device_type}" in CMS')

        if self.cms_config.get_widgets(widget_type='favourites')[0]['disabled']:
            raise CmsClientException('"Favourites" widget is disabled in CMS')

        if tests.settings.backend_env == 'prod':
            # Football
            events = self.get_active_events_for_category(
                category_id=self.football_category_id, number_of_events=1)
            self.__class__.type_id = events[0]['event']['typeId']
            self.__class__.eventID = events[0]['event']['id']
            self.__class__.event_name = normalize_name(events[0]['event']['name'])
            self.__class__.league_name = self.get_accordion_name_for_event_from_ss(event=events[0])

            outcomes = next(((market['market'].get('children')) for market in events[0]['event']['children']), None)
            if outcomes is None:
                raise SiteServeException('There are no outcomes available')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.team1 = list(self.selection_ids.keys())[0]
            self._logger.info(
                f'*** Found football event with name: "{self.event_name}" and league: "{self.league_name}"')

            # Tennis
            events = self.get_active_events_for_category(
                category_id=tennis_category_id, number_of_events=1)
            self.__class__.eventID_other = events[0]['event']['id']
            self.__class__.event_name_other = normalize_name(events[0]['event']['name'])
            self.__class__.league_other = self.get_accordion_name_for_event_from_ss(event=events[0])

            outcomes = next(((market['market'].get('children')) for market in events[0]['event']['children']), None)
            if outcomes is None:
                raise SiteServeException('There are no outcomes available')
            self._logger.info(
                f'*** Found tennis event with name: "{self.event_name_other}" and league: "{self.league_other}"')
        else:
            # Football
            event_params = self.ob_config.add_football_event_to_featured_autotest_league()
            self.__class__.eventID = event_params.event_id
            self.__class__.type_id = self.ob_config.football_config.autotest_class.featured_autotest_league.type_id

            event_resp = self.ss_req.ss_event_to_outcome_for_event(
                event_id=self.eventID, query_builder=self.ss_query_builder)

            self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
            self.__class__.league_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])
            self.__class__.selection_ids = event_params.selection_ids
            self.__class__.team1 = list(self.selection_ids.keys())[0]
            self._logger.info(f'*** Created football event with name: "{self.event_name}"')

            # Football live
            start_time = self.get_date_time_formatted_string(seconds=10)
            event_params = self.ob_config.add_football_event_to_featured_autotest_league(
                is_live=True, start_time=start_time)
            self.__class__.eventID_live = event_params.event_id

            event_resp_live = self.ss_req.ss_event_to_outcome_for_event(
                event_id=self.eventID_live, query_builder=self.ss_query_builder)

            self.__class__.event_name_live = normalize_name(event_resp_live[0]['event']['name'])
            self.__class__.league_live = self.get_accordion_name_for_event_from_ss(event=event_resp[0], in_play=True)
            self._logger.info(f'*** Created live football event with name: "{self.event_name_live}"')

            # Tennis
            event_params = self.ob_config.add_tennis_event_to_autotest_trophy()
            self.__class__.eventID_other = event_params.event_id

            event_resp = self.ss_req.ss_event_to_outcome_for_event(
                event_id=self.eventID, query_builder=self.ss_query_builder)

            self.__class__.event_name_other = normalize_name(event_resp[0]['event']['name'])
            self.__class__.league_other = self.get_accordion_name_for_event_from_ss(event=event_resp[0])
            self._logger.info(f'*** Created tennis event with name: "{self.event_name_other}"')

    def test_001_navigate_to_the_football_landing_page(self):
        """
        DESCRIPTION: Navigate to the Football Landing page
        EXPECTED: * Football Landing page is opened
        EXPECTED: * 'Favourite' icon (star icon) is displayed next to 'Event (Team A v Team B)'
        EXPECTED: * 'Favourite' icon (star icon) is NOT displayed near Enhanced Multiples
        EXPECTED: * 'Favourites' widget is empty **(Desktop)**
        EXPECTED: * 'Favourites' counter on 'Football' top header = 0 **(Mobile/Tablet)**
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name=self.sport_name)

        self.__class__.event = self.get_event_from_league(
            event_id=self.eventID, section_name=self.league_name)
        self.assertTrue(self.event.has_favourite_icon(),
                        msg=f'Favorite icon is not displayed for event: "{self.event_name}"')

        self.verify_favorite_counter_change(expected_counter=0)

    def test_002_tap_on_the_favourite_icon_star_icon_next_to_event(self):
        """
        DESCRIPTION: Tap on the 'Favourite' icon (star icon) next to 'Event (Team A v Team B)'
        EXPECTED: 'Log In' pop-up appears
        """
        self.event.favourite_icon.click()

        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg='Login dialog is not present on page')

    def test_003_enter_valid_user_name_and_password_and_press_log_in(self):
        """
        DESCRIPTION: Enter valid user name and password and press 'Log In'
        EXPECTED: * User is Logged In
        EXPECTED: * 'Favourite' icon becomes bold (yellow)
        EXPECTED: * The event is added to the 'Favourite Matches'
        EXPECTED: * 'Favourites' widget has one Favourite event **(Desktop)**
        EXPECTED: * 'Favourites' counter on 'Football' top header = exact amount of added to Favourites events **(Mobile/Tablet)**
        """
        self.dialog.username = tests.settings.betplacement_user
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login()
        dialog_closed = self.dialog.wait_dialog_closed(timeout=25)
        self.assertTrue(dialog_closed, msg='Login dialog is not closed yet')
        if self.site.root_app.has_loss_limit_dialog(timeout=2, expected_result=True):
            self.site.loss_limit_dialog.im_happy_with_limit.click()
            self.navigate_to_page(name='sport/football')
            self.site.wait_content_state(state_name=self.sport_name)
            self.event = self.get_event_from_league(
                event_id=self.eventID, section_name=self.league_name)
        try:
            self.site.close_qe_or_fanzone_popup()
            self.site.close_all_dialogs(async_close=False)
        except Exception as e:
            self._logger.warning(e)
        try:
            favourite_icon = self.event.favourite_icon
            self.assertTrue(favourite_icon.is_selected(), msg=f'Event favourite icon is not selected')
        except Exception:
            self.event.favourite_icon.click()
            self.assertTrue(self.event.favourite_icon.is_selected(), msg=f'Event favourite icon is not selected')

        self.verify_favorite_counter_change(event_name=self.event_name, expected_counter=1)

    def test_004_tap_on_selected_favourite_icon_star_icon_next_to_the_same_event(self):
        """
        DESCRIPTION: Tap on selected 'Favourite' icon (star icon) next to the same Event
        EXPECTED: * 'Favourite' icon is not filled (not selected)
        EXPECTED: * The event is removed from the 'Favourite Matches'
        EXPECTED: * 'Favourites' widget is empty **(Desktop)**
        EXPECTED: * 'Favourites' counter on 'Football' top header = 0 **(Mobile/Tablet)**
        """
        try:
            self.site.timeline.timeline_splash_page.close_button.click()
        except:
            pass
        self.event.favourite_icon.click()
        self.assertFalse(self.event.favourite_icon.is_selected(expected_result=False),
                         msg=f'Event favourite icon is selected, after unselect it for event {self.event_name}')

        self.verify_favorite_counter_change(expected_counter=0)

    def test_005_navigate_to_the_football_event_details_page(self):
        """
        DESCRIPTION: Navigate to the Football Event Details page
        EXPECTED: * Football Event Details page is opened
        EXPECTED: * **For Desktop:** 'Favourite' icon (star icon) is displayed at the left side of the Event Bar
        EXPECTED: * **For Mobile/Tablet:** 'Favourite' icon (star icon) is displayed at the right side icon block (under 'Statistics' section)
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name=self.sport_name)
        self.assertTrue(self.site.sport_event_details.has_favourite_icon(),
                        msg='Favourite icon is not displayed on Football Event Details page')

    def test_006_tap_on_favourite_icon(self):
        """
        DESCRIPTION: Tap on 'Favourite' icon (star icon)
        EXPECTED: * 'Favourite' icon becomes bold (yellow)
        EXPECTED: * The event is added to the 'Favourite Matches'
        EXPECTED: * 'Favourites' widget has one Favourite event **(Desktop)**
        EXPECTED: * 'Favourites' counter on 'Football' top header = exact amount of added to Favourites events **(Mobile/Tablet)**
        """
        favourite_icon = self.site.sport_event_details.favourite_icon
        favourite_icon.click()
        self.assertTrue(favourite_icon.is_selected(), msg=f'Favourite icon is not selected')

        self.verify_favorite_counter_change(expected_counter=1, event_name=self.event_name)

    def test_007_tap_on_favourite_icon_on_football_page_header(self):
        """
        DESCRIPTION: Tap on 'Favourite' icon (star icon) on Football page header **(Mobile/Tablet)**
        EXPECTED: 'Favourite Matches' page is opened **(Mobile/Tablet)**
        """
        if self.device_type != 'desktop':
            self.site.sport_event_details.header_line.go_to_favourites_page.click()
            self.site.wait_content_state('Favourites', timeout=3)

            actual_page_title = self.site.favourites.header_line.page_title.title
            expected_page_title = vec.sb.FAVOURITE_MATCHES
            self.assertEqual(actual_page_title, expected_page_title,
                             msg=f'Actual page title: "{actual_page_title}" '
                                 f'is not as expected: "{expected_page_title}"')

    def test_008_verify_favourite_matches_elements(self):
        """
        DESCRIPTION: Verify 'Favourite Matches' elements **(Mobile/Tablet)**
        EXPECTED: * 'Clear All Favourites' button is displayed at the top of the page
        EXPECTED: * Football matches which user has previously selected as favourites are displayed
        EXPECTED: * Information text is displayed as follows:
        EXPECTED: "Browse through the matches currently available and add them to your favourite list."
        EXPECTED: * 'Go to Matches' button
        EXPECTED: * 'Go to In-Play Matches' button
        """
        if self.device_type != 'desktop':
            favourites_page = self.site.favourites
            self.assertTrue(favourites_page.clear_all_favourites.is_displayed(),
                            msg='"Clear All Favourites" button is not displayed')

            self.verify_event_on_favourites_page(expected_events=[self.event_name])

            actual_message = favourites_page.info_label
            expected_message = vec.favourites.BROWSE_FAVOURITE_MATCHES
            self.assertEqual(actual_message, expected_message,
                             msg=f'Actual message: "{actual_message}" '
                                 f'is not as expected: "{expected_message}"')

            self.assertTrue(favourites_page.go_to_matches_button.is_displayed(),
                            msg='"Go to Matches" button is not displayed')
            self.assertTrue(favourites_page.go_to_in_play_matches.is_displayed(),
                            msg='"Go to In-Play Matches" button is not displayed')

    def test_009_tap_on_clear_all_favourites_button(self):
        """
        DESCRIPTION: Tap on 'Clear All Favourites' button **(Mobile/Tablet)**
        EXPECTED: Football matches which user has previously selected as favourites disappear
        """
        if self.device_type != 'desktop':
            self.site.favourites.clear_all_favourites.click()

            actual_message = self.site.favourites.info_label.strip()
            expected_message = vec.sb_desktop.NO_FAVOURITE_MATCHES
            self.assertEqual(expected_message, vec.sb_desktop.NO_FAVOURITE_MATCHES,
                             msg=f'Actual message: "{actual_message}" '
                                 f'is not as expected: "{expected_message}"')

    def test_010_tap_on_go_to_matches_button(self):
        """
        DESCRIPTION: Tap on 'Go to Matches' button **(Mobile/Tablet)**
        EXPECTED: * Football Landing page is opened
        EXPECTED: * 'Matches' tab is opened
        """
        if self.device_type != 'desktop':
            self.site.favourites.go_to_matches_button.click()
            self.site.wait_content_state(state_name=self.sport_name)

            current_tab = self.site.football.tabs_menu.current
            expected_tab = self.expected_sport_tabs.matches
            self.assertEqual(current_tab, expected_tab,
                             msg=f'Actual tab: "{current_tab}" '
                                 f'is not as expected: "{expected_tab}"')

    def test_011_navigate_to_the_favourite_matches_page_by_tapping_on_favourite_icon_on_football_page_header(self):
        """
        DESCRIPTION: Navigate to the 'Favourite Matches' page by tapping on 'Favourite' icon (star icon) on Football page header **(Mobile/Tablet)**
        EXPECTED: 'Favourite Matches' page is opened
        """
        if self.device_type != 'desktop':
            self.site.football.header_line.go_to_favourites_page.click()
            self.site.wait_content_state('Favourites', timeout=3)

            actual_page_title = self.site.favourites.header_line.page_title.title
            expected_page_title = vec.sb.FAVOURITE_MATCHES
            self.assertEqual(actual_page_title, expected_page_title,
                             msg=f'Actual page title: "{actual_page_title}" '
                                 f'is not as expected: "{expected_page_title}"')

    def test_012_tap_on_go_to_in_play_matches_button(self):
        """
        DESCRIPTION: Tap on 'Go to In-Play Matches' button **(Mobile/Tablet)**
        EXPECTED: * Football Landing page is opened
        EXPECTED: * 'In-Play' tab is opened
        """
        if self.device_type != 'desktop':
            self.site.favourites.go_to_in_play_matches.click()
            self.site.wait_content_state(state_name=self.sport_name)

            current_tab = self.site.football.tabs_menu.current
            expected_tab = self.expected_sport_tabs.in_play
            self.assertEqual(current_tab, expected_tab,
                             msg=f'Actual tab: "{current_tab}" '
                                 f'is not as expected: "{expected_tab}"')

    def test_013_add_in_play_football_event_to_favourite(self):
        """
        DESCRIPTION: Add In-Play Football Event to 'Favourite'
        EXPECTED: The event is added to the 'Favourite Matches'
        EXPECTED: * 'Favourites' widget has one Favourite event **(Desktop)**
        EXPECTED: * 'Favourites' counter on 'Football' top header = exact amount of added to Favourites events **(Mobile/Tablet)**
        """
        if self.device_type == 'desktop':
            favourite_icon = self.site.sport_event_details.favourite_icon
            favourite_icon.click()
            self.assertFalse(favourite_icon.is_selected(expected_result=False), msg=f'Favourite icon is not selected')

        if tests.settings.backend_env == 'prod':
            # Football live
            events = self.get_active_events_for_category(
                category_id=self.football_category_id, in_play_event=True)
            self.__class__.eventID_live = events[0]['event']['id']
            self.__class__.event_name_live = normalize_name(events[0]['event']['name'])
            self.__class__.league_live = self.get_accordion_name_for_event_from_ss(event=events[0], in_play=True)
            self.__class__.type_name = events[0]['event']['typeName']

            outcomes = next(((market['market'].get('children')) for market in events[0]['event']['children']), None)
            if outcomes is None:
                raise SiteServeException('There are no outcomes available')
            self._logger.info(
                f'*** Found live football event with name: "{self.event_name_live}" and league: "{self.league_live}"')

        self.navigate_to_page(name='sport/football/live')
        self.site.wait_content_state(state_name=self.sport_name)

        if self.device_type == 'desktop':
            event = self.get_event_from_league(
                event_id=self.eventID_live, section_name=self.league_live)
        else:
            event = self.get_event_from_league(
                event_id=self.eventID_live, section_name=self.type_name.upper())
        event.favourite_icon.click()
        sleep(5)
        self.verify_favorite_counter_change(expected_counter=1, event_name=self.event_name_live)

    def test_014_place_a_bet_on_football_event_that_is_not_added_to_favourites(self):
        """
        DESCRIPTION: Place a bet on Football Event that is not added to Favourites (not Enhanced Multiples or Outrights)
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is shown on the Bet Slip
        EXPECTED: * 'Favourite all' with 'Favourite' icon is displayed at the top of Bet Receipt
        EXPECTED: * 'Favourite' icon (star icon) is displayed at the Bet Receipt
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

        self.__class__.bet_receipt = self.site.bet_receipt
        self.assertTrue(self.bet_receipt.receipt_sub_header.has_add_all_to_favourites_button(),
                        msg=f'"Favourite all" icon is not displayed at the top of Bet Receipt')

        bet_receipt_sections = self.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found')

        section = bet_receipt_sections.get(vec.betslip.SINGLE)
        self.assertTrue(section, msg=f'"{vec.betslip.SINGLE}" Bet Receipt section not found')

        receipts = section.items_as_ordered_dict
        self.assertTrue(receipts, msg='No Bet Receipts found')

        self.__class__.receipt = receipts.get(self.team1)
        self.assertTrue(self.receipt, msg=f'Receipt section not found for team: "{self.team1}"')
        self.assertTrue(self.receipt.favourite_icon.is_displayed(),
                        msg='Favourite button is not displayed at the Bet Receipt')

    def test_015_tap_on_favourite_icon_star_icon_on_bet_receipt(self):
        """
        DESCRIPTION: Tap on 'Favourite' icon (star icon) on Bet Receipt
        EXPECTED: * 'Favourite' icon becomes bold
        EXPECTED: * The event is added to the 'Favourite Matches'
        EXPECTED: * 'Favourites' widget has one Favourite event **(Desktop)**
        EXPECTED: * 'Favourites' counter on 'Football' top header = exact amount of added to Favourites events **(Mobile/Tablet)**
        """
        favourite_icon = self.receipt.favourite_icon
        favourite_icon.click()
        self.assertTrue(favourite_icon.is_selected(), msg=f'Favourite icon is not selected')

        self.bet_receipt.footer.click_done()

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name=self.sport_name)

        self.verify_favorite_counter_change(expected_counter=2, event_name=self.event_name)

    def test_016_navigate_to_the_football_outrights_page(self):
        """
        DESCRIPTION: Navigate to the Football Outrights page
        EXPECTED: * Outrights page is opened
        EXPECTED: * Favourites Matches functionality is not included on the Outrights page
        """
        outrights_cms_name = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights
        if self.is_tab_present(tab_name=outrights_cms_name, category_id=self.football_category_id):
            self.navigate_to_page(name='sport/football/outrights')
            self.site.wait_content_state(state_name=self.sport_name)

            current_tab = self.site.football.tabs_menu.current
            expected_tab = self.expected_sport_tabs.outrights
            self.assertEqual(current_tab, expected_tab,
                             msg=f'Actual tab: "{current_tab}" '
                                 f'is not as expected: "{expected_tab}')

    def test_017_navigate_to_the_other_sport_or_race_pages(self):
        """
        DESCRIPTION: Navigate to the other <Sport> or Race pages
        EXPECTED: * Favourites Matches functionality is not included on the other <Sport> pages
        EXPECTED: * Favourites Matches functionality is not included on the Race pages
        """
        self.navigate_to_page(name='sport/tennis/matches')
        self.site.wait_content_state(state_name=self.other_sport_name)
        event = self.get_event_from_league(
            event_id=self.eventID_other, section_name=self.league_other)
        self.assertFalse(event.has_favourite_icon(expected_result=False),
                         msg=f'Favorite icon is displayed for event: "{self.event_name_other}"')

    def test_018_verify_favourite_icon_presence_on_the_homepage(self):
        """
        DESCRIPTION: Verify Favourite icon presence on the Homepage
        EXPECTED: Favourite icon is present near Football Match events on the Featured modules on the Homepage
        """
        if tests.settings.cms_env != 'prd0':
            module_name = self.cms_config.add_featured_tab_module(
                select_event_by='Type', id=self.type_id, events_time_from_hours_delta=-10, module_time_from_hours_delta=-10,
                show_all_events=True)['title'].upper()

            self.navigate_to_page(name='/')
            self.site.wait_content_state(state_name='Homepage')

            self.wait_for_featured_module(name=module_name)
            featured_modules = self.site.home.get_module_content(
                self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))

            module = featured_modules.accordions_list.items_as_ordered_dict.get(module_name)
            self.assertTrue(module, msg=f'Module: "{module_name}" not found')

            event = module.items_as_ordered_dict.get(self.event_name)
            self.assertTrue(event, msg=f'Event: "{self.event_name}" not found')
            self.assertTrue(event.favourite_icon.is_displayed(),
                            msg=f'Favourite icon is not displayed for event: "{self.event_name}"')
