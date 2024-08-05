import pytest
import tests
from tests.base_test import vtest
from collections import OrderedDict
import voltron.environments.constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_haul, wait_for_result
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
@pytest.mark.sports_specific
@pytest.mark.basket_ball_specific
@pytest.mark.adhoc_suite
@pytest.mark.desktop
class Test_C66007943_Verify_the_display_of_details_in_the_Basketball_Competitions_tab(BaseBetSlipTest):
    """
    TR_ID: C66007943
    NAME: Verify the display of details in the Basketball Competitions tab
    DESCRIPTION: This test case needs to verify details displayed in the Competitions tab for Basketball.
    PRECONDITIONS: 1.User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: Competitions  tab can be configured from CMS-&gt;
    PRECONDITIONS: Sports menu-&gt; Sports Category-&gt; Basketball -&gt; Competitions tab-&gt; Enable/Disable.
    PRECONDITIONS: Note: In mobile when no events are available Basketball sport is not displayed in A-Z sports menu and on clicking Basketball  from Sports ribbon user is navigated back to the sports homepage.
    """
    keep_browser_open = True
    sport_name = 'Basketball'
    basketball_Category_id = 6
    competitions_tab = vec.sb.TABS_NAME_COMPETITIONS.title()
    home_breadcrumb = vec.sb.HOME_FOOTER_ITEM.title()

    def test_000_preconditions(self):
        """
        DESCRIPTION : Checking whether competitions tab is enabled in cms or not.
        DESCRIPTION : checking whether time filter is enabled or disable in cms
        DESCRIPTION : Add basketball event for specific league
        """
        # getting Basketball competitions tab data
        competitions_tab_data = self.cms_config.get_sports_tab_data(sport_id=self.basketball_Category_id,
                                                                    tab_name=self.competitions_tab.lower())
        if not competitions_tab_data.get('enabled') or not competitions_tab_data.get('filters')['time']['enabled']:
            # Making competitions tab enable and enabling time filter for competitions tab in cms for Basketball.
            self.cms_config.update_sports_event_filters(tab_name=self.competitions_tab.lower(),
                                                        sport_id=self.basketball_Category_id,
                                                        enabled=True,
                                                        timefilter_enabled=True,
                                                        event_filters_values=[1, 3, 6, 12, 24, 48])
        # Adding basketball event for specific league for lower environments
        self.__class__.is_mobile = self.device_type == 'mobile'
        if tests.settings.backend_env != 'prod':
            competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsBasketball')
            if not competitions_countries:
                competitions_countries = self.cms_config.get_system_configuration_item('CompetitionsBasketball')
            if str(self.ob_config.basketball_config.basketball_autotest.class_id) not in competitions_countries.get(
                    'A-ZClassIDs').split(','):
                raise CmsClientException('Basketball competition class is not configured on Competitions tab')
            self.ob_config.add_basketball_event_to_autotest_league()
            self.ob_config.add_basketball_outright_event_to_autotest_league(ew_terms=self.ew_terms)
            self.__class__.section_name_list = 'Basketball Auto Test' if self.brand == 'ladbrokes' else "BASKETBALL AUTO TEST"
            self.__class__.league = tests.settings.basketball_autotest_competition_league.title()

        else:
            event = self.get_active_events_for_category(category_id=self.ob_config.basketball_config.category_id)[0]
            self._logger.info(f'*** Found event: {event}')
            self.__class__.section_name_list = event['event']['className']
            self.__class__.league = event['event']['typeName']

    def test_001_launch_the_ladbrokes_and_coral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes and Coral application
        EXPECTED: Home page should be loaded successfully
        """
        self.site.login()
        self.navigate_to_page("Homepage")
        self.site.wait_content_state(state_name='HomePage')

    def test_002_click_on_basketball_sport(self):
        """
        DESCRIPTION: Click on Basketball sport.
        EXPECTED: User should be able to navigate Basketball landing page.
        """
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='basketball')

    def test_003_verify_competitions_tab(self):
        """
        DESCRIPTION: Verify Competitions tab
        EXPECTED: Competitions need to loaded successfully.
        """
        competitions_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            self.ob_config.basketball_config.category_id)
        self.assertTrue(competitions_tab_name, msg='competition tab is not available')
        self.site.basketball.tabs_menu.click_button(competitions_tab_name.upper())
        if self.device_type == 'mobile':
            sections = self.site.basketball.tab_content.all_competitions_categories.items_as_ordered_dict
        else:
            self.site.basketball.tab_content.grouping_buttons.items_as_ordered_dict.get('A - Z').click()
            sections = self.site.basketball.tab_content.accordions_list.items_as_ordered_dict
        # verifying accordions of competitions tab are expand and collapse successfully
        for accordion_list_name, accordion_list in list(sections.items())[:3]:
            accordion_list.expand()
            self.assertTrue(accordion_list.is_expanded(), msg=f'accordion list is not expanded')
            accordion_list.collapse()
            self.assertFalse(accordion_list.is_expanded(), msg=f'section is not Collapsed')
        section_name_list = self.section_name_list.upper() \
            if (self.brand == 'bma') or (self.brand == 'ladbrokes' and self.device_type == 'mobile') \
            else self.section_name_list
        if self.device_type == 'desktop':
            self.site.basketball.tab_content.grouping_buttons.items_as_ordered_dict.get('A - Z').click()
            sections = self.site.basketball.tab_content.accordions_list.items_as_ordered_dict
        else:
            sections = self.site.basketball.tab_content.all_competitions_categories.get_items(name=section_name_list)
        self.assertTrue(sections, msg=f'Competitions page does not have any "{self.section_name_list}" section')
        section = sections.get(section_name_list)
        self.assertTrue(section, msg=f'Cannot find "{self.section_name_list}" section on Competitions page')
        section.expand()
        leagues = wait_for_result(lambda: section.get_items(name=self.league),
                                  name=f'"{self.section_name_list}" to expand for "{self.league}"', timeout=3)
        self.assertTrue(leagues, msg=f'No events are present for the league "{self.league}"')
        league = leagues.get(self.league)
        self.assertTrue(league, msg=f'Cannot find "{self.league}" on Competitions page')
        league.click()
        self.site.wait_content_state('CompetitionLeaguePage')

    def test_004_verify_the_functionality_of_time_filters_by_selecting_the_time_filter(self):
        """
        DESCRIPTION: Verify the functionality of time filters by selecting the time filter.
        EXPECTED: Events should be fetched as per the time filter selected
        """
        filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        self.assertTrue(filters, msg='filters are not displayed')
        # waiting for to load competitions tab data
        wait_for_haul(5)
        for i in filters.keys():
            filter = filters.get(i)
            filter.click()
            selected_filter = list(self.site.sports_page.tab_content.timeline_filters.selected_filters.keys())[0]
            self.assertEqual(i, selected_filter, msg=f'selected time filter {i} is not selected')
            accordion_lists = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
            if accordion_lists:
                self.assertTrue(accordion_lists,
                                msg=f'no events are found under matches tab for time filter {i} for basketball in competitions tab')
            else:
                no_events_label = self.site.contents.tab_content.has_no_events_label()
                self.assertTrue(no_events_label, msg=f'No events found message is not displayed')
        filters.get("48h").click()  # for to unselect time filter

    def test_005_verify_accordions_are_collapsable_and_expandable(self):
        """
        DESCRIPTION: Verify accordions are collapsable and expandable
        EXPECTED: Accordion's should be collapsable and expandable
        """
        # covered in "test_003_verify_competitions_tab" step

    def test_006_click_the_more_link_above_the_odds_selection(self):
        """
        DESCRIPTION: Click the More link above the odds selection
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
                                name=f'back Button to be available in EDP "',
                                timeout=10, bypass_exceptions=VoltronException)
                wait_for_haul(5)
                self.site.back_button.click()
                break
            else:
                self.assertFalse(event_obj.has_markets(),
                                 msg=f"Event does have more link'{event_name}'even there are less than one market")
        self.site.back_button.click()

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
            self.assertEqual(list(breadcrumbs.keys()).index(self.sport_name), 1,
                             msg=f'"{self.sport_name}" sport title is not shown after "{self.home_breadcrumb}"')
            self.assertTrue(breadcrumbs[self.sport_name].angle_bracket,
                            msg=f'Angle bracket is not shown after "{self.sport_name}" breadcrumb')
            self.assertEqual(list(breadcrumbs.keys()).index(self.competitions_tab), 2,
                             msg=f'"Competetions" item name is not shown after "{self.sport_name}"')
            self.assertTrue(
                int(breadcrumbs[self.competitions_tab].link.css_property_value('font-weight')) == 700,
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
        self.assertTrue(self.site.has_back_button, msg=f'backward chevron is not displayed beside sports header')
        self.site.back_button.click()
        self.site.wait_content_state("Homepage")

    def test_009_verify_bet_placement_for_single_multiplecomplex(self):
        """
        DESCRIPTION: Verify bet placement for single, multiple,complex
        EXPECTED: Bet placement should be successful
        """
        # covered in test case C60089511
        pass
