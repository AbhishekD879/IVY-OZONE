from collections import OrderedDict
import pytest
from datetime import datetime
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_response_url, do_request
from voltron.utils.waiters import wait_for_result, wait_for_haul


def categorize_date(input_date_str):
    # Convert the input string to a datetime object
    input_date = datetime.strptime(input_date_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=None)
    # Get the current date
    current_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    # Calculate the difference between the input date and the current date
    time_difference = input_date - current_date
    # Compare the date with today, tomorrow, or future
    if time_difference.days == 0:
        return "TODAY"
    elif time_difference.days == 1:
        return "TOMORROW"
    elif time_difference.days > 1:
        return "FUTURE"
    else:
        return "past"


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.sports_specific
@pytest.mark.american_football
@pytest.mark.adhoc_suite
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.timeout(900)
@vtest
class Test_C66007970_Verify_the_display_of_data_for_the_American_Football_sport_in_the_Matches_tab(Common):
    """
    TR_ID: C66007970
    NAME: Verify the display of data for the American Football sport in the Matches tab.
    DESCRIPTION: This test case needs to verify Matches
    DESCRIPTION: tab display for the American Football sport.
    PRECONDITIONS: 1..User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: 2. Matches tab can be configured from CMS-&gt;
    PRECONDITIONS: Sports menu-&gt; Sports category-&gt; American Football-&gt; Matches tab-&gt;enable/disable.
    PRECONDITIONS: Note: In mobile when no events are available American Football sport is not displayed in A-Z sports menu and on clicking American Football  from Sports ribbon user is navigated back to the sports homepage.
    """
    keep_browser_open = True
    default_date_tab = vec.sb.SPORT_DAY_TABS.today
    home_breadcrumb = vec.sb.HOME_FOOTER_ITEM.upper()
    highlight_tab = vec.sb.TABS_NAME_MATCHES.upper()
    enable_bs_performance_log = True

    def get_sport_tab_name(self, name: str, category_id: int):
        tabs_data = self.cms_config.get_sport_config(category_id=category_id).get('tabs')
        sport_tab = next((tab for tab in tabs_data if tab.get('name') == name), '')
        sport_tab_name = sport_tab.get('label').upper()
        return sport_tab_name

    def test_001_launch_the_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes/Coral application
        EXPECTED: Home page should loaded succesfully
        """
        category_id = self.ob_config.american_football_config.category_id
        self.__class__.sport_name = self.get_sport_title(category_id)
        self.__class__.status = self.cms_config.get_sport_tab_status(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches, sport_id=category_id)
        self.__class__.matches_tab_name = self.get_sport_tab_name(
            name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches, category_id=category_id)

    def test_002_click_on_american_football_sport(self):
        """
        DESCRIPTION: Click on American Football sport.
        EXPECTED: User should be able to navigate American Football landing page.
        """
        self.site.open_sport(self.sport_name, content_state="AmericanFootball")

    def test_003_verify_american_football_landing_page(self):
        """
        DESCRIPTION: Verify American Football landing page.
        EXPECTED: Desktop
        EXPECTED: Tabs should be displayed with defualt selected matches tab with today events.
        EXPECTED: In play widget will display if any events are in live when it was enabled in sys config.
        EXPECTED: Mobile
        EXPECTED: Matches module loaded as default with inplay events in it
        """
        current_tab_on_sport_slp = self.site.sports_page.tabs_menu.current
        if self.device_type == 'mobile' and not self.status and current_tab_on_sport_slp != self.matches_tab_name.upper():
            raise SiteServeException("events  are not present in Matches tab of American Football")
        if self.device_type == 'mobile' and self.status and current_tab_on_sport_slp !="MATCHES" :
                raise SiteServeException("events  are not present in any tab of AmericanFootball")
        self.assertEqual(current_tab_on_sport_slp.upper(), "MATCHES",
                         msg=f"Current Active tab is {current_tab_on_sport_slp},"
                             f"Expected tab is Matches")
        # Get the URL for fetching event data
        self.__class__.actual_url = get_response_url(self, url='/EventToOutcomeForClass')
        # If the URL is not available, refresh the page and try again
        if not self.actual_url:
            self.device.refresh_page()
            self.__class__.actual_url = get_response_url(self, url='/EventToOutcomeForClass')
        response = do_request(method='GET', url=self.actual_url)
        self.__class__.event_type_name = {}
        self.__class__.today_events = {}
        self.__class__.tomorrow_events = {}
        self.__class__.future_events = {}
        self.__class__.event_ids = {}
        for event in response['SSResponse']['children']:
            if not event.get('event'):
                break
            type_name = f"{event['event']['categoryName']} - {event['event']['typeName'].encode('utf-8').decode('unicode-escape')}".strip().upper()
            event_name = event['event']['name'].strip().upper()
            self.__class__.event_type_name[event_name] = type_name
            self.__class__.event_ids[event_name] = event['event']['id']
            time = event['event']['startTime']
            if "TODAY" == categorize_date(input_date_str=time):
                self.__class__.today_events[event_name] = type_name
            elif "TOMORROW" == categorize_date(input_date_str=time):
                self.__class__.tomorrow_events[event_name] = type_name
            elif "FUTURE" == categorize_date(input_date_str=time):
                self.__class__.future_events[event_name] = type_name
        if (len(self.event_type_name) and self.device_type == "mobile") and (
                len(self.today_events) or len(self.tomorrow_events)):
            sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
            for section_name, section in sections.items():
                expanded = section.is_expanded()
                if expanded:
                    section.collapse()
                    self.assertFalse(section.is_expanded(expected_result=False),
                                     msg=f"accordion with section name {section_name} is still expanded even after clicking")
                else:
                    section.expand()
                    self.assertTrue(section.is_expanded(),
                                    msg=f"accordion with section name {section_name} is not expanded even after clicking")
                self.assertTrue(section_name.split('\n')[0] in self.event_type_name.values(),
                                msg=f"according with {section_name} is not present in {self.event_type_name.values()}")

    def test_004_verify_matches_tab(self):
        """
        DESCRIPTION: Verify Matches tab
        EXPECTED: Default today tab should be selected and events to be loaded.
        """
        # covered in above step

    def test_005_desktopverify_today_tomorrow_future_tabs(self):
        """
        DESCRIPTION: Desktop
        DESCRIPTION: Verify Today ,Tomorrow, Future tabs
        EXPECTED: Events should be loaded based on tab selection.
        """
        if self.device_type == 'desktop':
            current_date_tab = self.site.sports_page.date_tab.current_date_tab
            self.assertEqual(current_date_tab, self.default_date_tab, msg=f'"{self.default_date_tab}" date tab is not '
                                                                          f'active, Current date tab is "{current_date_tab}"')
            if len(self.today_events):

                sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
                for section_name, section in sections.items():
                    self.assertTrue(section_name.split('\n')[0] in self.today_events.values())
                    expanded = section.is_expanded()
                    if expanded:
                        section.collapse()
                        self.assertFalse(section.is_expanded(expected_result=False),
                                         msg=f"accordion with section name {section_name} is still expanded even after clicking")
                    else:
                        section.expand()
                        self.assertTrue(section.is_expanded(),
                                        msg=f"accordion with section name {section_name} is not expanded even after clicking")
            else:
                self.assertTrue(self.site.sports_page.tab_content.has_no_events_label(),
                                msg="No events message is not displayed even when there are no events available")
            # ********* tomorrow event validation ****************************
            date_tabs = self.site.sports_page.date_tab.items_as_ordered_dict
            tomorrow_tab = next(
                (date_tab for date_tab in date_tabs if date_tab.upper() == vec.sb.SPORT_DAY_TABS.tomorrow.upper()),
                None)
            date_tabs.get(tomorrow_tab).click()
            wait_for_haul(3)
            self.__class__.actual_url = get_response_url(self, url='/EventToOutcomeForClass')
            # If the URL is not available, refresh the page and try again
            if not self.actual_url:
                self.device.refresh_page()
                self.__class__.actual_url = get_response_url(self, url='/EventToOutcomeForClass')
            response = do_request(method='GET', url=self.actual_url)
            for event in response['SSResponse']['children']:
                if not event.get('event'):
                    break
                type_name = f"{event['event']['categoryName']} - {event['event']['typeName'].encode('utf-8').decode('unicode-escape')}".strip().upper()
                event_name = event['event']['name'].strip().upper()
                self.__class__.event_type_name[event_name] = type_name
                self.__class__.event_ids[event_name] = event['event']['id']
                time = event['event']['startTime']
                if "TODAY" == categorize_date(input_date_str=time):
                    self.__class__.today_events[event_name] = type_name
                elif "TOMORROW" == categorize_date(input_date_str=time):
                    self.__class__.tomorrow_events[event_name] = type_name
                elif "FUTURE" == categorize_date(input_date_str=time):
                    self.__class__.future_events[event_name] = type_name
            if len(self.tomorrow_events):
                sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
                for section_name, section in sections.items():
                    self.assertTrue(section_name.split('\n')[0] in self.tomorrow_events.values(),
                                    msg=f'event name {section_name} is not present in {self.tomorrow_events.values()}')
                    expanded = section.is_expanded()
                    if expanded:
                        section.collapse()
                        self.assertFalse(section.is_expanded(expected_result=False),
                                         msg=f"accordion with section name {section_name} is still expanded even after clicking")
                    else:
                        section.expand()
                        self.assertTrue(section.is_expanded(),
                                        msg=f"accordion with section name {section_name} is not expanded even after clicking")
            else:
                self.assertTrue(self.site.sports_page.tab_content.has_no_events_label(),
                                msg="No events message is not displayed even when there are no events available")
            # ***************** validating future events *********************
            self.device.refresh_page()
            date_tabs = self.site.sports_page.date_tab.items_as_ordered_dict
            future_tab = next(
                (date_tab for date_tab in date_tabs if date_tab.upper() == vec.sb.SPORT_DAY_TABS.future.upper()),
                None)
            date_tabs.get(future_tab).click()
            wait_for_haul(3)
            self.__class__.actual_url = get_response_url(self, url='/EventToOutcomeForClass')
            # If the URL is not available, refresh the page and try again
            if not self.actual_url:
                self.device.refresh_page()
                self.__class__.actual_url = get_response_url(self, url='/EventToOutcomeForClass')
            response = do_request(method='GET', url=self.actual_url)
            for event in response['SSResponse']['children']:
                if not event.get('event'):
                    break
                type_name = f"{event['event']['categoryName']} - {event['event']['typeName'].encode('utf-8').decode('unicode-escape')}".strip().upper()
                event_name = event['event']['name'].strip().upper()
                self.__class__.event_type_name[event_name] = type_name
                self.__class__.event_ids[event_name] = event['event']['id']
                time = event['event']['startTime']
                if "TODAY" == categorize_date(input_date_str=time):
                    self.__class__.today_events[event_name] = type_name
                elif "TOMORROW" == categorize_date(input_date_str=time):
                    self.__class__.tomorrow_events[event_name] = type_name
                elif "FUTURE" == categorize_date(input_date_str=time):
                    self.__class__.future_events[event_name] = type_name
            if len(self.future_events):
                sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
                for section_name, section in sections.items():
                    self.assertTrue(section_name.split('\n')[0] in self.future_events.values())
                    expanded = section.is_expanded()
                    if expanded:
                        section.collapse()
                        self.assertFalse(section.is_expanded(expected_result=False),
                                         msg=f"accordion with section name {section_name} is still expanded even after clicking")
                    else:
                        section.expand()
                        self.assertTrue(section.is_expanded(),
                                        msg=f"accordion with section name {section_name} is not expanded even after clicking")
            else:
                self.assertTrue(self.site.sports_page.tab_content.has_no_events_label(),
                                msg="No events message is not displayed even when there are no events available")

    def test_006_verify_the_league_filters_and_time_filters(self):
        """
        DESCRIPTION: Verify the League filters and Time filters
        EXPECTED: Events should be fetched as per selection
        """
        # covered in another test case

    def test_007_verify_created_modules_for_sport_category_page_from_cms(self):
        """
        DESCRIPTION: Verify created modules for sport category page from CMS
        EXPECTED: Mobile:
        EXPECTED: Quiclinks, Surfacebets, Highlights corousels, super buttons
        EXPECTED: should be displayed as per CMS config
        EXPECTED: Desktop:
        EXPECTED: Surfacebets, Highlights corousels should be displayed
        """
        # can't verify the module as we can short list them we are validating in creation test cases

    def test_008_verify_accordians_are_collapsable_and_expandable(self):
        """
        DESCRIPTION: Verify accordians are collapsable and expandable
        EXPECTED: Accordians should be collapsable and expandable
        """
        # covered in above steps

    def test_009_verify_see_all_link_navigation(self):
        """
        DESCRIPTION: Verify SEE ALL Link navigation
        EXPECTED: User should be naviagted to respective competitions page for both mobile and dekstop
        """
        if len(self.today_events):
            expected_tab = vec.sb.SPORT_DAY_TABS.today
        elif len(self.tomorrow_events):
            expected_tab = vec.sb.SPORT_DAY_TABS.tomorrow
        elif len(self.future_events):
            expected_tab = vec.sb.SPORT_DAY_TABS.future
        else:
            raise SiteServeException("events  are not present in any tab of AmericanFootball")
        if self.device_type != "mobile":
            date_tabs = self.site.sports_page.date_tab.items_as_ordered_dict
            self.__class__.active_tab = next(
                (date_tab for date_tab in date_tabs if date_tab.upper() == expected_tab.upper()),
                None)
            date_tabs.get(self.active_tab).click()
        accordions = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(accordions, msg="Accordions are not displayed on AmericanFootball landing page")
        first_accordion_name, first_accordion = list(accordions.items())[0]
        first_accordion.expand()
        if self.device_type == "desktop" and self.brand == "bma":
            self.assertFalse(first_accordion.group_header.has_see_all_link(),
                             msg="Accordion as see all in coral desktop which shouldn't be shown")
        else:
            self.assertTrue(first_accordion.group_header.has_see_all_link(), msg="Accordion doesn't have see all link")
            first_accordion.group_header.see_all_link.click()
            self.site.wait_content_state('CompetitionLeaguePage')
            competition_name = self.site.competition_league.title_section.type_name.text
            self.assertIn(competition_name.upper(), first_accordion_name.upper())
            self.site.back_button.click()

    def test_010_verfiy_more_link_on_above_odds_selection(self):
        """
        DESCRIPTION: Verfiy More link on above odds selection
        EXPECTED: User should be navigated to respective EDP page
        """
        if self.device_type == 'desktop':
            date_tabs = self.site.sports_page.date_tab.items_as_ordered_dict
            date_tabs.get(self.active_tab).click()
        accordions = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(accordions, msg="Accordions are not displayed on AmericanFootball landing page")
        for accordion_name, accordion in accordions.items():
            accordion.expand()
            events = accordion.items_as_ordered_dict
            event_name = list(events.keys())[0]
            event_obj = events[event_name].template
            event_id = self.event_ids.get(f"{event_name.upper()}")
            event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
            if len(event_resp[0]['event'].get('children')) > 1:
                self.assertTrue(event_obj.has_markets(), msg=f"Event doesn't have more link'{event_name}'")
                event_obj.more_markets_link.click()
                self.site.wait_content_state(state_name='EventDetails')
                wait_for_result(lambda: self.site.has_back_button, expected_result=True,
                                name=f'back Button to be available in EDP "',
                                timeout=10, bypass_exceptions=VoltronException)
                self.site.back_button.click()
                break
            else:
                self.assertFalse(event_obj.has_markets(),
                                 msg=f"Event does have more link'{event_name}'even there are less than one market")

    def test_011_verify_signposting(self):
        """
        DESCRIPTION: Verify signposting.
        EXPECTED: User should be able to see signposting.
        """
        # covered in C66007978

    def test_012_click_on_signposting(self):
        """
        DESCRIPTION: Click on signposting.
        EXPECTED: User should be able to see popup text wich is related to signposting.
        """
        # covered in C66007978

    def test_013_verify_breadcrumbs(self):
        """
        DESCRIPTION: Verify Breadcrumbs
        EXPECTED: Desktop
        EXPECTED: User should be navigated on the respective page on click.
        """
        if self.device_type != 'mobile':
            page = self.site.sports_page
            breadcrumbs = OrderedDict((key.strip().upper(), page.breadcrumbs.items_as_ordered_dict[key])
                                      for key in page.breadcrumbs.items_as_ordered_dict)

            self.assertTrue(breadcrumbs, msg='No breadcrumbs found')

            self.assertEqual(list(breadcrumbs.keys()).index(self.home_breadcrumb), 0,
                             msg='Home page is not shown the first by default')
            self.assertTrue(breadcrumbs[self.home_breadcrumb].angle_bracket,
                            msg=f'Angle bracket is not shown after "{self.home_breadcrumb}" breadcrumb')

            self.assertEqual(list(breadcrumbs.keys()).index('AMERICAN FOOTBALL'), 1,
                             msg=f'"{self.sport_name}" sport title is not shown after "{self.home_breadcrumb}"')
            self.assertTrue(breadcrumbs['AMERICAN FOOTBALL'].angle_bracket,
                            msg=f'Angle bracket is not shown after "{self.sport_name}" breadcrumb')

            self.assertEqual(list(breadcrumbs.keys()).index(self.highlight_tab), 2,
                             msg=f'" matches " item name is not shown after "{self.sport_name}"')
            self.assertTrue(
                int(breadcrumbs[self.highlight_tab].link.css_property_value('font-weight')) == 700,
                msg=f'" matches " hyperlink from breadcrumbs is not highlighted according to the selected page')

    def test_014_verify_by_clicking_on_backward_chevron_beside_sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron beside sport header
        EXPECTED: Desktop
        EXPECTED: User should be naviagted to homepage
        """
        self.site.back_button.click()
        self.site.wait_content_state("homepage")

    def test_015_verify_bet_placement_for_single_multiplecomplex(self):
        """
        DESCRIPTION: Verify bet placement for single, multiple,complex
        EXPECTED: Bet placement need to successful
        """
        # covered in C66007951
