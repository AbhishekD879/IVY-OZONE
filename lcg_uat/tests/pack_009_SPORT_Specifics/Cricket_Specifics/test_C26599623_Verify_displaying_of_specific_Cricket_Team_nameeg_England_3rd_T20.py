import pytest
import voltron.environments.constants as vec
from crlat_cms_client.utils.waiters import wait_for_result
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Cannot create events for Prod/Beta
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C26599623_Verify_displaying_of_specific_Cricket_Team_nameeg_England_3rd_T20(BaseBetSlipTest):
    """
    TR_ID: C26599623
    NAME: Verify displaying of specific Cricket Team name(e.g. |England 3rd T20|)
    DESCRIPTION: This test case verified displaying of specific Cricket Team name(e.g. England 3rd T20).
    DESCRIPTION: Created after PROD incident https://jira.egalacoral.com/browse/BMA-48652
    PRECONDITIONS: In TI create/find Cricket event with the following name templates:
    PRECONDITIONS: - **|TeamName1 X T20| |vs| |TeamName2 Y T20|**
    PRECONDITIONS: - **|TeamName1| |vs| |TeamName2 X T20|**
    PRECONDITIONS: where X,Y are sequence numbers(e.g. 2nd, 3rd, 4th)
    PRECONDITIONS: Event name examples:
    PRECONDITIONS: - **|India 3rd T20| |vs| |England 3rd T20|**
    PRECONDITIONS: - **|New Zealand| |vs| |England 3rd T20|**
    PRECONDITIONS: To retrieve information about event use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: where,
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create live event with scores
        EXPECTED: Event is successfully created
        """
        event_params = self.ob_config.add_autotest_cricket_event_for_WW_type()
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
        self.__class__.event_id = event_params.event_id
        self.__class__.team1, self.__class__.team2 = event_params.team1, event_params.team2
        self.__class__.is_mobile = True if self.device_type == 'mobile' else False
        event_resp = \
            self.ss_req.ss_event_to_outcome_for_event(event_id=self.event_id, query_builder=self.ss_query_builder)
        self.__class__.section_name = \
            f'{event_resp[0]["event"]["categoryCode"]} - {event_resp[0]["event"]["typeName"]}'.upper()

        # Live event
        inplay_event = self.ob_config.add_autotest_cricket_event_for_WW_type(is_live=True, perform_stream=True)
        self.__class__.inplay_event_name = f'{inplay_event.team1} v {inplay_event.team2}'
        self.__class__.inplay_event_id = inplay_event.event_id
        inplay_event_resp = \
            self.ss_req.ss_event_to_outcome_for_event(event_id=self.inplay_event_id, query_builder=self.ss_query_builder)
        self.__class__.inplay_section_name = f'{inplay_event_resp[0]["event"]["typeName"]}'

        sport_name_raw = self.get_sport_name_for_event(event=event_resp[0])
        self.__class__.sport_name = sport_name_raw.title() if self.brand == 'ladbrokes' else sport_name_raw.upper()
        self.__class__.expected_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
            self.ob_config.cricket_config.category_id)
        self.site.login()

    def test_001_load_oxygen_applicationverify_that_the_event_names_are_correctly_shown_on_pages_where_the_events_are_present(self):
        """
        DESCRIPTION: Load Oxygen application.
        DESCRIPTION: Verify that the Event names are correctly shown on pages where the Events are present.
        EXPECTED:
        """
        self.navigate_to_page(name='sport/cricket')
        self.site.wait_content_state('cricket', timeout=5)
        sleep(3)
        self.site.sports_page.tabs_menu.items_as_ordered_dict.get(self.expected_tab_name).click()
        current_tab_name = self.site.competition_league.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_tab_name,
                         msg=f'Actual tab is "{current_tab_name}", instead of "{self.expected_tab_name}"')
        expected_section = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.get(
            self.section_name)
        if expected_section:
            event = self.get_event_from_league(event_id=self.event_id, section_name=self.section_name)
            actual_event_name_list = list(expected_section.items_as_ordered_dict.keys())
            self.assertTrue(self.event_name in actual_event_name_list,
                            msg=f'{self.event_name} not present in {actual_event_name_list}')
            if event is None:
                raise VoltronException(f'"{self.event_id}" event not found')
        else:
            raise VoltronException(f'"{self.section_name}" league not found')

    def test_002_for_mobiletabletin_play_page_from_the_sports_menu_ribboncheck_on_watch_live_and_cricket_pagesfor_desktopin_play_page_from_the_main_navigation_menu_at_the_universal_headercheck_on_watch_live_and_cricket_pages(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: **'In-Play'** page from the Sports Menu Ribbon
        DESCRIPTION: Check on **'Watch live'** and **Cricket** pages
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: **'In-Play'** page from the 'Main Navigation' menu at the 'Universal Header'
        DESCRIPTION: Check on **'Watch live'** and **Cricket** pages
        EXPECTED: - Event name is fully displayed
        EXPECTED: - Event name is equal to name received from ** 'name'** attribute in siteserve request
        EXPECTED: - The sequence number is not cut out of the Event name
        """
        if self.brand == 'bma':
            self.navigate_to_page(name='in-play/watchlive')
            self.site.wait_content_state(state_name='in-play')
            sleep(3)
            if self.device_type == 'mobile':
                in_play_events = self.site.inplay.tab_content.live_now.items_as_ordered_dict
            else:
                in_play_events = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(in_play_events, msg='No events found')

            if not in_play_events.get(self.sport_name).is_expanded():
                in_play_events.get(self.sport_name).expand()
            leagues = in_play_events.get(self.sport_name).items_as_ordered_dict
            section_name = self.inplay_section_name.upper() if self.brand == 'bma' and self.device_type == 'desktop' \
                else self.inplay_section_name
            actual_event_name_list = list(leagues.get(section_name).items_as_ordered_dict.keys())
            self.assertTrue(self.inplay_event_name in actual_event_name_list,
                            msg=f'{self.event_name} not present in {actual_event_name_list}')
        else:
            self.navigate_to_page(name='sport/cricket')
            self.site.wait_content_state('cricket', timeout=5)
            sleep(3)
            self.site.sports_page.tabs_menu.items_as_ordered_dict.get(self.expected_tab_name).click()
            current_tab_name = self.site.competition_league.tabs_menu.current
            self.assertEqual(current_tab_name, self.expected_tab_name,
                             msg=f'Actual tab is "{current_tab_name}", instead of "{self.expected_tab_name}"')
            expected_section = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.get(
                self.section_name)
            if expected_section:
                actual_event_name_list = list(expected_section.items_as_ordered_dict.keys())
                self.assertTrue(self.event_name in actual_event_name_list,
                                msg=f'{self.event_name} not present in {actual_event_name_list}')

    def test_003_for_mobiletablethome_page__featured_tab_verify_that_event_names_on_in_play_modulehighlight_carouselfeatured_module_created_by_type_idevent_id(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Home page > **'Featured' tab** :
        DESCRIPTION: Verify that Event names on :
        DESCRIPTION: In-play module
        DESCRIPTION: Highlight carousel
        DESCRIPTION: Featured module (created by Type_id/Event_id)
        EXPECTED: - Event name is fully displayed
        EXPECTED: - Event name is equal to name received from ** 'name'** attribute in siteserve request
        EXPECTED: - The sequence number is not cut out of the Event name
        """
        if self.brand == 'bma':
            if self.brand:
                self.site.inplay.inplay_sport_menu.click_item(self.sport_name)
                self.site.wait_content_state(state_name='in-play')
                sleep(3)
                if self.device_type == 'mobile':
                    in_play_events = self.site.inplay.tab_content.live_now.items_as_ordered_dict
                else:
                    in_play_events = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
                self.assertTrue(in_play_events, msg='No events found')
                if self.brand == 'bma':
                    section_name = self.inplay_section_name.upper() if self.device_type == 'mobile' \
                        else self.section_name
                actual_event_name_list = list(in_play_events.get(section_name).items_as_ordered_dict.keys())
                self.assertTrue(self.inplay_event_name in actual_event_name_list,
                                msg=f'{self.event_name} not present in {actual_event_name_list}')
            else:
                self.navigate_to_page(name='sport/cricket')
                self.site.wait_content_state('cricket', timeout=5)
                sleep(3)
                self.site.sports_page.tabs_menu.items_as_ordered_dict.get(self.expected_tab_name).click()
                current_tab_name = self.site.competition_league.tabs_menu.current
                self.assertEqual(current_tab_name, self.expected_tab_name,
                                 msg=f'Actual tab is "{current_tab_name}", instead of "{self.expected_tab_name}"')
                expected_section = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.get(
                    self.section_name)
                if expected_section:
                    actual_event_name_list = list(expected_section.items_as_ordered_dict.keys())
                    self.assertTrue(self.event_name in actual_event_name_list,
                                    msg=f'{self.event_name} not present in {actual_event_name_list}')
        else:
            self.navigate_to_page(name='sport/cricket')
            self.site.wait_content_state('cricket', timeout=5)
            sleep(3)
            self.site.sports_page.tabs_menu.items_as_ordered_dict.get(self.expected_tab_name).click()
            current_tab_name = self.site.competition_league.tabs_menu.current
            self.assertEqual(current_tab_name, self.expected_tab_name,
                             msg=f'Actual tab is "{current_tab_name}", instead of "{self.expected_tab_name}"')
            expected_section = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.get(
                self.section_name)
            if expected_section:
                actual_event_name_list = list(expected_section.items_as_ordered_dict.keys())
                self.assertTrue(self.event_name in actual_event_name_list,
                                msg=f'{self.event_name} not present in {actual_event_name_list}')

    def test_004_for_mobiletablethome_page__in_play_tabhome_page__live_stream_tabfor_desktophome_page__in_play_and_live_stream_modulecheck_in_play_tab_and_live_stream_tabs(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Home page > **'In Play'** tab
        DESCRIPTION: Home page > **'Live stream'** tab
        DESCRIPTION: **For Desktop**
        DESCRIPTION: Home page > **'In play and live stream'** module
        DESCRIPTION: Check 'In-play' tab and 'Live Stream' tabs
        EXPECTED: - Event name is fully displayed
        EXPECTED: - Event name is equal to name received from ** 'name'** attribute in siteserve request
        EXPECTED: - The sequence number is not cut out of the Event name
        """
        if self.brand == 'bma':
            if self.is_mobile:
                self.navigate_to_page(name='home')
                self.site.wait_content_state('HomePage')
                sleep(3)
                in_play_tab = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play,
                                                       raise_exceptions=False)
                self.site.home.tabs_menu.click_button(in_play_tab)
                self.assertTrue(self.site.home.tabs_menu.items_as_ordered_dict.get(in_play_tab).is_selected(),
                                msg=f'"{in_play_tab}" tab is not selected')
                inplay_list_live = self.site.home.tab_content.live_now.items_as_ordered_dict
                self.assertTrue(inplay_list_live, msg=f'No sports found on homepage {in_play_tab} tab')
                sport_section = inplay_list_live.get(self.sport_name)
                self.assertTrue(sport_section, msg=f'"{self.sport_name}" sport section not found')
                if not sport_section.is_expanded():
                    sport_section.expand()
                self.assertTrue(sport_section.is_expanded(),
                                msg=f'"{self.sport_name}" section is not expanded')
                if sport_section.has_show_more_leagues_button():
                    sport_section.show_more_leagues_button.click()
                leagues = sport_section.items_as_ordered_dict
                self.assertTrue(leagues, msg=f'No leagues found for "{self.sport_name.upper()}"')
                league = leagues.get(self.inplay_section_name)
                self.assertTrue(league, msg=f'"{self.inplay_section_name}" league not found')
                actual_event_name_list = list(league.items_as_ordered_dict.keys())
                self.assertTrue(self.inplay_event_name in actual_event_name_list,
                                msg=f'{self.event_name} not present in {actual_event_name_list}')
            else:
                self.navigate_to_page(name='/')
                self.site.wait_content_state(state_name='Homepage')
                sleep(3)
                inplay_sports = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
                cricket = inplay_sports.get(self.sport_name)
                self.assertTrue(cricket, msg=f'"{self.sport_name}" not found among "{inplay_sports.keys()}"')
                cricket.click()
                self.assertTrue(inplay_sports.get(self.sport_name).is_selected(),
                                msg=f'"{self.sport_name}" tab is not selected')
                module_name = vec.inplay.IN_PLAY_LIVE_STREAM_SECTION_NAME
                leagues = self.site.home.get_module_content(
                    module_name=module_name).accordions_list.items_as_ordered_dict
                section_name = self.section_name if self.brand == 'bma' else self.section_name
                actual_event_name_list = list(leagues.get(section_name).items_as_ordered_dict.keys())
                self.assertTrue(self.inplay_event_name in actual_event_name_list,
                                msg=f'{self.event_name} not present in {actual_event_name_list}')
        else:
            self.navigate_to_page(name='sport/cricket')
            self.site.wait_content_state('cricket', timeout=5)
            sleep(3)
            self.site.sports_page.tabs_menu.items_as_ordered_dict.get(self.expected_tab_name).click()
            current_tab_name = self.site.competition_league.tabs_menu.current
            self.assertEqual(current_tab_name, self.expected_tab_name,
                             msg=f'Actual tab is "{current_tab_name}", instead of "{self.expected_tab_name}"')
            expected_section = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.get(
                self.section_name)
            if expected_section:
                actual_event_name_list = list(expected_section.items_as_ordered_dict.keys())
                self.assertTrue(self.event_name in actual_event_name_list,
                                msg=f'{self.event_name} not present in {actual_event_name_list}')

    def test_005_on_cricket_landing_page__in_play_tab(self):
        """
        DESCRIPTION: On **Cricket Landing page > 'In Play'** tab
        EXPECTED: - Event name is fully displayed
        EXPECTED: - Event name is equal to name received from ** 'name'** attribute in siteserve request
        EXPECTED: - The sequence number is not cut out of the Event name
        """
        # Covered in step 4

    def test_006_on_edp_of_the_appropriate_events(self):
        """
        DESCRIPTION: On **EDP** of the appropriate events
        EXPECTED: - Event name is fully displayed
        EXPECTED: - Event name is equal to name received from ** 'name'** attribute in siteserve request
        EXPECTED: - The sequence number is not cut out of the Event name
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='cricket')
        self.site.wait_content_state(state_name='EventDetails')
        sleep(3)
        wait_for_result(lambda: self.site.sport_event_details.event_title_bar.event_name_we.is_displayed(),
                        name=f'Waiting for event name to display"', timeout=10)
        actual_event_name = self.site.sport_event_details.event_title_bar.event_name
        self.assertEqual(actual_event_name.upper(), self.event_name.upper(),
                         msg='Actual and expected event names not same')

    def test_007_for_desktopon_sports_landing_page__in_play_widget_and_live_stream_widget(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: On Sports Landing page > 'In-Play' widget and 'Live Stream 'widget
        EXPECTED: - Event name is fully displayed
        EXPECTED: - Event name is equal to name received from ** 'name'** attribute in siteserve request
        EXPECTED: - The sequence number is not cut out of the Event name
        """
        if self.device_type == 'desktop':
            if self.brand == 'bma':
                self.navigate_to_page(name='sport/cricket')
                self.site.wait_content_state('cricket', timeout=5)
                sleep(3)
                sections = self.site.cricket.in_play_widget.items_as_ordered_dict.get('In-Play LIVE Cricket')
                widgets = sections.content.items_as_ordered_dict
                self.assertTrue(widgets, msg='Widget are not available')
                actual_event_name = list(widgets.items())[-1][0]
                self.assertEqual(actual_event_name.upper(), self.inplay_event_name.upper(),
                                 msg='Actual and expected event names not same')

    def test_008_for_mobileadd_any_selection_from_created_cricket_events_to_quick_bet_and_verify_displaying_of_event_names_in_quick_bet(self):
        """
        DESCRIPTION: **For Mobile:**
        DESCRIPTION: Add any selection from created Cricket Events to Quick Bet and verify displaying of Event names in **Quick Bet**.
        EXPECTED: - Event name is fully displayed
        EXPECTED: - Event name is equal to name received from ** 'name'** attribute in siteserve request
        EXPECTED: - The sequence number is not cut out of the Event name
        """
        if self.device_type == 'mobile':
            event = list(self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict.values())[0]
            selection = list(event.outcomes.items_as_ordered_dict.values())[0]
            selection.click()
            sleep(3)

            quick_bet = self.site.quick_bet_panel
            quick_bet.selection.content.amount_form.input.value = 0.02

            self.site.quick_bet_panel.place_bet.click()
            bet_receipt = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt, msg='Bet Receipt is not displayed')
            actual_event_name = self.site.quick_bet_panel.bet_receipt.event_name
            self.assertEqual(actual_event_name.upper(), self.event_name.upper(),
                             msg='Actual and expected event names not same')

    def test_009_add_any_selection_from_created_cricket_events_to_betslip_and_verify_displaying_of_event_names_in_betslip_only_ladbrokes(self):
        """
        DESCRIPTION: Add any selection from created Cricket Events to Betslip and verify displaying of Event names in **Betslip**. (Only Ladbrokes)
        EXPECTED: - Event name is fully displayed
        EXPECTED: - Event name is equal to name received from ** 'name'** attribute in siteserve request
        EXPECTED: - The sequence number is not cut out of the Event name
        """
        # Covered in step 8

    def test_010_place_bets_for_created_cricket_events_and_verify_displaying_of_event_names_in_my_bets(self):
        """
        DESCRIPTION: Place bets for created Cricket Events and verify displaying of Event names in **My Bets**.
        EXPECTED: - Event name is fully displayed
        EXPECTED: - Event name is equal to name received from ** 'name'** attribute in siteserve request
        EXPECTED: - The sequence number is not cut out of the Event name
        """
        # Covered in step 8
