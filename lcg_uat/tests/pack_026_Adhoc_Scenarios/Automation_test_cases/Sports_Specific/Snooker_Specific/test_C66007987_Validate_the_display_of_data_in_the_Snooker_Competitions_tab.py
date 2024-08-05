import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
@pytest.mark.time_league_filters
@pytest.mark.sports_specific
@pytest.mark.snooker_specific
@pytest.mark.adhoc_suite
@pytest.mark.desktop
class Test_C66007987_Validate_the_display_of_data_in_the_Snooker_Competitions_tab(Common):
    """
    TR_ID: C66007987
    NAME: Validate the display of data in the Snooker Competitions tab.
    DESCRIPTION: This test case needs to verify Competitions tab display for the Snooker sport.
    PRECONDITIONS: 1.User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: 2. Competitions  tab can be configured from CMS-&gt;
    PRECONDITIONS: Sports menu-&gt; Sportscategory -&gt; Snooker-&gt; Competitions tab -&gt; Enable/Disable.
    PRECONDITIONS: Note: In mobile when no events are available Snooker sport is not displayed in A-Z sports menu and on clicking Snooker  from Sports ribbon user is navigated back to the sports homepage.
    """
    keep_browser_open = True
    home_breadcrumb = vec.sb.HOME_FOOTER_ITEM.title()

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if not cls.competitions_tab_status:
            cms_config = cls.get_cms_config()
            cms_config.update_sports_tab_status(sport_tab_id=cls.tab_id, enabled=cls.competitions_tab_status)

    def verify_events_are_sorted_by_time(self):
        """
        EXPECTED: * Page loads only events that are in line to selected League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        event_time_list = []
        sections = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
        if len(sections) > 0:
            for league in sections:
                events = list(league.items_as_ordered_dict.values())
                self.assertTrue(events, msg='Events not found')
                for event in events:
                    event_template = event.template
                    self.assertTrue(event_template.event_time.split(" ")[0],
                                    msg='"Event time" not displayed')
                    event_time_list.append(event_template.event_time.split(" ")[0])

            self.assertListEqual(sorted(event_time_list), sorted(event_time_list),
                                 msg=f'Actual event time  "{sorted(event_time_list)}"'
                                     f' is not matching with expected list "{sorted(event_time_list)}"')
        else:
            no_events = self.site.contents.tab_content.has_no_events_label()
            self.assertTrue(no_events, msg=' "No Events Found" msg not displayed')

    def test_000_preconditions(self):
        """
        PRECONDITIONS : Checking whether competitions tab is enabled in cms or not.
        PRECONDITIONS : checking whether time filter is enabled or disable in cms
        PRECONDITIONS: Time filters should be enabled in the Sports Categories -&gt; -&gt; Competitions Tab -&gt; Add time filters and save.
        """
        self.__class__.category_id = self.ob_config.backend.ti.snooker.category_id
        self.__class__.sport_name = self.get_sport_title(self.category_id)
        self.__class__.in_play_status = self.get_initial_data_system_configuration().get('DesktopWidgetsToggle').get(
            'inPlay')
        if not self.in_play_status:
            if tests.settings.cms_env != 'prd0':
                self.cms_config.update_system_configuration_structure(config_item='DesktopWidgetsToggle',
                                                                      field_name='inPlay', field_value=True)
                self.__class__.in_play_status = self.get_initial_data_system_configuration().get(
                    'DesktopWidgetsToggle').get(
                    'inPlay')
            else:
                raise CmsClientException('Desktop widget is disabled in cms"')

        # getting Basketball competitions tab data
        competitions_tab_data = self.cms_config.get_sports_tab_data(sport_id=self.category_id,
                                                                    tab_name='competitions')
        self.__class__.competitions_tab_status = competitions_tab_data.get('enabled')
        if not self.competitions_tab_status:
            self.__class__.tab_id = self.cms_config.get_sport_tab_id(sport_id=self.ob_config.snooker_config.category_id,
                                                      tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions)
            self.cms_config.update_sports_tab_status(sport_tab_id=self.tab_id, enabled=True)

        if not competitions_tab_data.get('enabled') or not competitions_tab_data.get('filters').get('enabled'):
            # Making competitions tab enable and enabling time filter for competitions tab in cms for Basketball.
            self.cms_config.update_sports_event_filters(tab_name='competitions',
                                                        sport_id=self.category_id,
                                                        enabled=True,
                                                        timefilter_enabled=True,
                                                        event_filters_values=[1, 3, 6, 12, 24, 48])
        competitions_tab_data = self.cms_config.get_sports_tab_data(sport_id=self.category_id,
                                                                    tab_name='competitions')
        if competitions_tab_data.get('filters').get('time').get('enabled') and sorted(competitions_tab_data.get('filters').get('time').get('values')) != [1, 3, 6, 12, 24, 48]:
            self.cms_config.update_sports_event_filters(tab_name='competitions',
                                                        sport_id=self.category_id,
                                                        enabled=True,
                                                        timefilter_enabled=True,
                                                        event_filters_values=[1, 3, 6, 12, 24, 48])

    def test_001_launch_the_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes/Coral application
        EXPECTED: Home page should loaded succesfully
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='HomePage')

    def test_002_click_on_snooker_sport(self):
        """
        DESCRIPTION: Click on Snooker sport.
        EXPECTED: User should be able to navigate Snooker landing page.
        """
        self.site.open_sport(name=self.sport_name, timeout=5)

    def test_003_verify_snooker_landing_page(self):
        """
        DESCRIPTION: Verify Snooker landing page.
        EXPECTED: Desktop
        EXPECTED: Tabs should be displayed with Matches tab selected by default with today events .
        EXPECTED: In play widget will display if any events are in live when it was enabled in sys config.
        EXPECTED: Mobile
        EXPECTED: Matches module loaded by default with inplay events in it
        """
        events = self.get_active_events_for_category(category_id=self.category_id, in_play_event=True,
                                                     raise_exceptions=False)
        if events and self.device_type != "mobile" and self.in_play_status:
            sections = self.site.snooker.in_play_widget.items_as_ordered_dict.get(
                'In-Play LIVE Snooker')
            self.__class__.widgets = sections.content.items_as_ordered_dict
            sections.is_expanded()
            self.assertTrue(self.widgets, msg='Widget are not available')
            self.__class__.event_name, self.__class__.event = list(self.widgets.items())[-1]
            self.assertTrue(self.event.is_displayed(), msg=f'Widget {self.event_name} is not displayed')
            event_header = (list(sections.content.items_as_ordered_dict.items())[0][1]).fixture_header
            self.assertTrue(event_header.is_displayed(), msg=f'Widget {event_header} is not displayed')
            cashout = self.event.cashout_inplay_icon
            self.assertTrue(cashout, msg=f'Widget {cashout} is not displayed')
            score = self.event.in_play_card.in_play_score
            self.assertTrue(score.is_displayed(), msg=f'Widget {score} is not displayed')
            markets = self.event.in_play_card.more_markets_link_inplay
            self.assertTrue(markets, msg=f'Widget {markets} is not displayed')
            header = self.event.fixture_header
            self.assertTrue(header, msg=f'Fixture {header} is not displayed')
            odds_buttons = self.event.odds_buttons
            self.assertTrue(odds_buttons, msg=f'"{odds_buttons}" are not displayed')

    def test_004_verify_competitions_tab_by_clicking_on_it(self):
        """
        DESCRIPTION: Verify Competitions tab by clicking on it
        EXPECTED: Competitions need to loaded
        """
        self.__class__.expected_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            self.ob_config.snooker_config.category_id)
        competition_tab = self.site.snooker.tabs_menu.items_as_ordered_dict.get(self.expected_tab_name)
        self.assertTrue(competition_tab, msg=f'"{self.expected_tab_name}" tab is not enabled in CMS')
        competition_tab.click()
        current_tab_name = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as Expected Tab: "{self.expected_tab_name}"')

    def test_005_verify__time_filters_by_selecting_one_of_the_time_filters_available(self):
        """
        DESCRIPTION: Verify  time filters by selecting one of the time filters available.
        EXPECTED: Events should be fetched as per filter selection
        """
        filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        self.assertTrue(filters, msg='filters are not displayed')
        # waiting for to load competitions tab data
        wait_for_haul(5)
        for i in filters.keys():
            _filter = filters.get(i)
            _filter.click()
            wait_for_haul()
            selected_filter = list(self.site.sports_page.tab_content.timeline_filters.selected_filters.keys())[0]
            self.assertEqual(i, selected_filter, msg=f'selected time filter {i} is not selected')
            accordion_lists = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
            if accordion_lists:
                self.assertTrue(accordion_lists,
                                msg=f'no events are found under matches tab for time filter {i} for basketball in competitions tab')
            else:
                no_events_label = self.site.sports_page.tab_content.has_no_events_label()
                self.assertTrue(no_events_label, msg='No events found message is not displayed')
        filters.get("48h").click()  # for to unselect time filter

    def test_006_verify_accordions_are_collapsable_and_expandable(self):
        """
        DESCRIPTION: Verify accordions are collapsable and expandable
        EXPECTED: Accordions should be collapsable and expandable
        """
        # verifying accordions expandable and collapsable
        verified_accordions_count = 0
        accordions = self.site.sports_page.tab_content.competitions_categories_list.items_as_ordered_dict
        for accordion_name, accordion in accordions.items():
            if verified_accordions_count >= 4:
                break
            if accordion.is_expanded():
                accordion.collapse()
                self.assertFalse(accordion.is_expanded(),
                                 f'Accordion: "{accordion_name}" is not collapsed after clicking on it')
                accordion.expand()
                self.assertTrue(accordion.is_expanded(),
                                f'Accordion: "{accordion_name}"  is not expanded after clicking on it')
            else:
                accordion.expand()
                self.assertTrue(accordion.is_expanded(),
                                f'Accordion: "{accordion_name}"  is not expanded after clicking on it')
                accordion.collapse()
                self.assertFalse(accordion.is_expanded(),
                                 f'Accordion: "{accordion_name}"  is not collapsed after clicking on it')
            verified_accordions_count += 1

    def test_007_verify_more_link_on_above_odds_selection(self):
        """
        DESCRIPTION: Verify More link on above odds selection
        EXPECTED: User should be navigated to respective EDP page
        """
        date_accordions = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(date_accordions, msg="events are not displayed on matches tab in competitions tab")
        for event_name, event in date_accordions.items():
            events = event.items_as_ordered_dict
            event_name = list(events.keys())[0]
            event_obj = events[event_name]
            event_id = event_obj.template.event_id
            event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
            if len(event_resp[0]['event'].get('children')) > 1:
                self.assertTrue(event_obj.has_markets(), msg=f"Event doesn't have more link'{event_name}'")
                event_obj.more_markets_link.click()
                wait_for_haul(5)
                self.site.wait_content_state(state_name='EventDetails')
                wait_for_result(lambda: self.site.has_back_button, expected_result=True,
                                name='back Button to be available in EDP "',
                                timeout=10, bypass_exceptions=VoltronException)
                wait_for_haul(5)
                break
            else:
                self.assertFalse(event_obj.has_markets(expected_result=False),
                                 msg=f"Event does have more link'{event_name}'even there are less than one market")

    def test_008_verify_sign_posting(self):
        """
        DESCRIPTION: Verify sign posting.
        EXPECTED: User should be able to see sign posting.
        """
        # covered in C66007999

    def test_009_click_on_sign_posting(self):
        """
        DESCRIPTION: Click on sign posting.
        EXPECTED: User should be able to see popup text wich is related to sign posting.
        """
        # covered in C66007999

    def test_010_verify_by_clicking_on_backward_chevron_beside_sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron beside sport header
        EXPECTED: Desktop
        EXPECTED: User should be navigated to home page
        """
        # covered in step 11

    def test_011_verify_by_clicking_on_backward_chevron_on_above__sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron on above  sport header
        EXPECTED: Mobile
        EXPECTED: User should be navigated to sport navigation  page
        """
        if self.device_type == "mobile":
            self.site.back_button.click()
            self.site.wait_content_state(self.sport_name)
        else:
            self.site.sports_page.breadcrumbs.items_as_ordered_dict[self.home_breadcrumb].click()
            self.site.wait_content_state("homepage")

    def test_012_verify_breadcrumbs(self):
        """
        DESCRIPTION: Verify Breadcrumbs
        EXPECTED: Desktop
        EXPECTED: User should be navigated on the respective page on click
        """
        if self.device_type != 'mobile':
            self.site.open_sport(name=self.sport_name, timeout=5)
            self.test_004_verify_competitions_tab_by_clicking_on_it()
            page = self.site.sports_page
            from collections import OrderedDict
            breadcrumbs = OrderedDict((key.strip(), page.breadcrumbs.items_as_ordered_dict[key])
                                      for key in page.breadcrumbs.items_as_ordered_dict)
            self.assertTrue(breadcrumbs, msg='No breadcrumbs found')
            self.assertEqual(list(breadcrumbs.keys()).index(self.home_breadcrumb), 0,
                             msg='Home page is not shown the first by default')
            self.assertTrue(breadcrumbs[self.home_breadcrumb].angle_bracket,
                            msg=f'Angle bracket is not shown after "{self.home_breadcrumb}" breadcrumb')
            self.assertEqual(list(breadcrumbs.keys()).index(self.sport_name), 1,
                             msg=f'"{self.sport_name}" sport title is not shown after "{self.home_breadcrumb}"')
            self.assertTrue(breadcrumbs[self.sport_name].angle_bracket,
                            msg=f'Angle bracket is not shown after "{self.sport_name}" breadcrumb')
            self.assertEqual(list(breadcrumbs.keys()).index(self.expected_tab_name.title()), 2,
                             msg=f'"Competetions" item name is not shown after "{self.sport_name}"')
            self.assertTrue(
                int(breadcrumbs[self.expected_tab_name.title()].link.css_property_value('font-weight')) == 700,
                msg='" matches " hyperlink from breadcrumbs is not highlighted according to the selected page')

    def test_013_verify_bet_placements_for_single_multiple_complex(self):
        """
        DESCRIPTION: Verify bet placements for single, multiple, complex
        EXPECTED: Bet placements should be successful
        """
        # covered in test case C60089575
