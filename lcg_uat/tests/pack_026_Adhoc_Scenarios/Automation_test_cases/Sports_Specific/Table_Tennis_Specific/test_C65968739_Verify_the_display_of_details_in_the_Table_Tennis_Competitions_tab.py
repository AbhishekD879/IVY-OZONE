from json import JSONDecodeError
import pytest
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from collections import OrderedDict
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_response_url, do_request
from voltron.utils.waiters import wait_for_haul, wait_for_result
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.sports_specific
@pytest.mark.table_tennis_specific
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C65968739_Verify_the_display_of_details_in_the_Table_Tennis_Competitions_tab(BaseBetSlipTest):
    """
    TR_ID: C65968739
    NAME: Verify the display of details in the Table Tennis Competitions tab
    DESCRIPTION: This test case needs to verify details displayed in the Competitions tab for Table Tennis.
    PRECONDITIONS: 1.User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: 2. Competitions  tab can be configured from CMS-&gt;
    PRECONDITIONS: Sports menu-&gt; Sports Category-&gt;Table Tennis-&gt; Competitions tab-&gt; Enable/Disable.
    PRECONDITIONS: Note: In mobile when no events are available table tennis sport is not displayed in A-Z sports menu and on clicking table tennis  from Sports ribbon user is navigated back to the sports homepage.
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    sport_name = 'table tennis'
    table_tennis_Category_id = 59
    highlight_tab = vec.sb.TABS_NAME_COMPETITIONS.lower()
    home_breadcrumb = vec.sb.HOME_FOOTER_ITEM.title()

    def get_response_url(self, url,not_req):
        """
        Get the complete URL from the performance logs matching the provided URL.
        :param url: The URL to search for in the performance logs.
        :return: The complete URL if found, else None.
        """
        perflog = self.device.get_performance_log()
        for log in reversed(perflog):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url and not_req not in request_url :
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue
        return None

    def select_active_odds(self, sections, count=1):
        odds = []
        for section_name, section in reversed(sections.items()):
            section.expand()
            events = section.items_as_ordered_dict
            for event_name, event in events.items():
                odd = next((odd for odd in list(event.template.get_available_prices().values()) if
                            odd.name.upper() not in ['N/A', 'SUSP']), None)
                if odd:
                    odds.append(odd)
                if len(odds) == count:
                    break
            if len(odds) == count:
                break
        return odds

    def test_000_preconditions(self):
        """
        DESCRIPTION : Checking whether competitions tab is enabled in cms or not.
        DESCRIPTION : checking whether time filter is enabled or disable in cms
        """
        # getting table tennis competitions tab data
        competitions_tab_data = self.cms_config.get_sports_tab_data(sport_id=self.table_tennis_Category_id,tab_name=self.highlight_tab)
        if not competitions_tab_data.get('enabled') or not competitions_tab_data.get('filters')['time']['enabled']:
            # Making competitions tab enable and enabling time filter for competitions tab in cms for table tennis.
            self.cms_config.update_sports_event_filters(tab_name='competitions', sport_id=59, enabled=True,
                                                        timefilter_enabled=True,
                                                        event_filters_values=[1, 3, 6, 12, 24, 48])

    def test_001_launch_the_ladbrokes_and_coral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes and Coral application
        EXPECTED: Home page should be loaded successfully
        """
        self.site.login()
        self.site.wait_content_state('Homepage')

    def test_002_click_on_table_tennis_sport(self):
        """
        DESCRIPTION: Click on table tennis sport.
        EXPECTED: User should be able to navigate table tennis landing page.
        """
        self.navigate_to_page(name='sport/table-tennis')
        self.site.wait_content_state(state_name='table-tennis')

    def test_003_verify_competitions_tab(self):
        """
        DESCRIPTION: Verify Competitions tab
        EXPECTED: Competitions need to loaded successfully.
        """
        actual_tab_name = self.site.sports_page.tabs_menu.current
        expected_tab = vec.sb.SPORT_TABS_INTERNAL_NAMES.matches.upper()
        self.assertEqual(actual_tab_name, expected_tab, msg=f'Default tab is not "{actual_tab_name}", it is "{expected_tab}"')
        competitions_tab = self.site.sports_page.tabs_menu.items_as_ordered_dict.get("COMPETITIONS")
        expected_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.competitions.upper()
        self.assertEqual(competitions_tab.name, expected_tab_name, msg=f'Default tab is not "{competitions_tab.name}", it is "{expected_tab_name}"')
        competitions_tab.click()
        # getting competitions event type names from ss response
        self.__class__.actual_url = self.get_response_url(url='/EventToOutcomeForClass', not_req="event.eventSortCode:intersects:")
        # If the URL is not available, refresh the page and try again
        if not self.actual_url:
            self.device.refresh_page()
            self.__class__.actual_url = get_response_url(self, url='/EventToMarketForClass')
        response = do_request(method='GET', url=self.actual_url)
        event_type_name = {}
        for event in response['SSResponse']['children']:
            if not event.get('event'):
                break
            type_name = f"{event['event']['categoryName']} - {event['event']['typeName'].encode('utf-8').decode('unicode-escape')}".strip().upper()
            event_name = event['event']['name'].strip().upper()
            event_type_name[event_name] = type_name
        self.__class__.competitions_event_type_name = list(set(event_type_name.values()))

    def test_004_verify_the_functionality_of_time_filters_by_selecting_the_time_filter(self):
        """
        DESCRIPTION: Verify the functionality of time filters by selecting the time filter.
        EXPECTED: Events should be fetched as per the time filter selected
        """
        # waiting for to load competitions tab data
        wait_for_haul(5)
        filter = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict.get('1h')
        filter.click()
        selected_filters = self.site.competition_league.tab_content.timeline_filters.selected_filters
        self.assertIn("1h", list(selected_filters.keys()), msg=f'selected time filter {"1h"} is not selected')
        accordion_lists = self.site.sports_page.tab_content.tt_competitions_categories_list.items_as_ordered_dict
        self.assertTrue(accordion_lists, msg=f'no accordions are found under competitions tab for time filter {"1h"} for table tennis')
        filter.click()

    def test_005_verify_accordions_are_collapsable_and_expandable(self):
        """
        DESCRIPTION: Verify accordion's are collapsable and expandable
        EXPECTED: Accordion's should be collapsable and expandable
        """
        self.__class__.accordion_lists = self.site.sports_page.tab_content.tt_competitions_categories_list.items_as_ordered_dict
        # if we get see all link beside accordion,while reading accordion see all also added to accordion name
        accordions = list(self.accordion_lists)
        competition_accordions = [accordian.replace("\nSEE ALL", "") for accordian in accordions]
        # verifying whether accordions in front end and from ss response are equal or not
        self.assertListEqual(sorted(competition_accordions), sorted(self.competitions_event_type_name), msg=f'Accordions in ui {competition_accordions} are not same as site server call {self.competitions_event_type_name} for competitions tab ')
        self.assertTrue(accordions, msg=f'no accordions are found under competitions tab for table tennis')
        for accordion_list_name, accordion_list in list(self.accordion_lists.items())[:3]:
            accordion_list.expand()
            self.assertTrue(accordion_list.is_expanded(), msg=f'accordion list is not expanded')
            accordion_list.collapse()
            self.assertFalse(accordion_list.is_expanded(), msg=f'section is not Collapsed')

    def test_006_click_the_more_link_above_the_odds_selection(self):
        """
        DESCRIPTION: Click the More link above the odds selection
        EXPECTED: User should be navigated to respective EDP page
        """
        is_more_link_verified = False
        for accordion_name, accordion in self.accordion_lists.items():
            if not accordion.is_expanded():
                accordion.expand()
            events = wait_for_result(
                lambda: accordion.items_as_ordered_dict,
                timeout=2,
                expected_result=True,
                name='Accordian items are not accessible',
                bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, IndexError, VoltronException)
            )
            for event_name, event in events.items():
                if event.template.has_markets(timeout=5) and not is_more_link_verified:
                    event.template.more_markets_link.click()
                    # waiting for event details page to load
                    wait_for_haul(10)
                    self.site.wait_content_state(state_name="EVENTDETAILS", timeout=20)
                    self.site.back_button.click()
                    wait_for_haul(5)
                    is_more_link_verified = True
                    break
            if is_more_link_verified:
                break
        if is_more_link_verified:
            self.assertTrue(is_more_link_verified,"more link not verified")
        else:
            raise VoltronException('more link is not verified')

    def test_007_verify_breadcrumbs(self):
        """
        DESCRIPTION: Verify Breadcrumbs
        EXPECTED: Desktop
        EXPECTED: User should be navigated to the respective page on click
        """
        if self.device_type != 'mobile':
            page = self.site.sports_page
            breadcrumbs = OrderedDict((key.strip(), page.breadcrumbs.items_as_ordered_dict[key])
                                      for key in page.breadcrumbs.items_as_ordered_dict)
            self.assertTrue(breadcrumbs, msg='No breadcrumbs found')
            self.assertEqual(list(breadcrumbs.keys()).index(self.home_breadcrumb), 0,
                             msg='Home page is not shown the first by default')
            self.assertTrue(breadcrumbs[self.home_breadcrumb].angle_bracket,
                            msg=f'Angle bracket is not shown after "{self.home_breadcrumb}" breadcrumb')
            self.assertEqual(list(breadcrumbs.keys()).index(self.sport_name.title()), 1,
                             msg=f'"{self.sport_name}" sport title is not shown after "{self.home_breadcrumb}"')
            self.assertTrue(breadcrumbs[self.sport_name.title()].angle_bracket,
                            msg=f'Angle bracket is not shown after "{self.sport_name}" breadcrumb')
            self.assertEqual(list(breadcrumbs.keys()).index(self.highlight_tab.title()), 2,
                             msg=f'" matches " item name is not shown after "{self.sport_name}"')
            self.assertTrue(int(breadcrumbs[self.highlight_tab.title()].link.css_property_value('font-weight')) == 700,
                            msg=f'" matches " hyperlink from breadcrumbs is not highlighted according to the selected page')

    def test_008_verify_by_clicking_on_backward_chevron_beside_sports_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron beside sports header
        EXPECTED: Desktop
        EXPECTED: User should be redirected to home page
        EXPECTED: User should navigate to sport navigation  page
        EXPECTED: Mobile
        EXPECTED: User should be redirected to sport navigation  page
        """
        self.site.back_button.click()
        self.site.wait_content_state("homepage")
        self.test_002_click_on_table_tennis_sport()
        self.test_003_verify_competitions_tab()

    def test_009_verify_bet_placement_for_single_multiplecomplex(self):
        """
        DESCRIPTION: Verify bet placement for single, multiple,complex
        EXPECTED: Bet placement should be successful
        """
        accordions = self.site.sports_page.tab_content.tt_competitions_categories_list.items_as_ordered_dict
        self.assertTrue(accordions, msg="Accordions are not displayed on table tennis landing page")
        odds = self.select_active_odds(sections=accordions)
        self.assertTrue(odds, 'There is no active events to place bet')
        # placing single bet
        odds[0].click()
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip()
        self.site.open_betslip()
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()
        # placing multiple bet
        odds = self.select_active_odds(sections=accordions, count=3)
        if len(odds) < 2:
            self._logger.info(f'there is no events to place double bet"')
        else:
            odds[0].click()
            if self.device_type == 'mobile':
                self.site.add_first_selection_from_quick_bet_to_betslip()
            odds[1].click()
            self.site.open_betslip()
            self.place_multiple_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
        # ***************  validate complex bets ********************************
        odds = self.select_active_odds(sections=accordions, count=3)
        if len(odds) < 3:
            self._logger.info(f'there is no events to place double bet"')
        else:
            odds[0].click()
            if self.device_type == 'mobile':
                self.site.add_first_selection_from_quick_bet_to_betslip()
            odds[1].click()
            odds[2].click()
        self.site.open_betslip()
        self.place_bet_on_all_available_stakes()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()