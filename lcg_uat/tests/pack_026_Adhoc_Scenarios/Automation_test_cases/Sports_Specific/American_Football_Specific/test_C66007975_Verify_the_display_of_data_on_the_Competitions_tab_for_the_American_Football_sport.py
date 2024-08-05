from collections import OrderedDict
import pytest
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_haul, wait_for_result
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.reg167_fix
@vtest
@pytest.mark.desktop
@pytest.mark.sports_specific
@pytest.mark.american_football
@pytest.mark.adhoc_suite
class Test_C66007975_Verify_the_display_of_data_on_the_Competitions_tab_for_the_American_Football_sport(Common):
    """
    TR_ID: C66007975
    NAME: Verify the display of data on the Competitions tab for the American Football sport.
    DESCRIPTION: This test case needs to verify the data displayed in the Competitions tab for the American Football sport.
    PRECONDITIONS: 1.User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: 2. Competitions  tab can be configured from CMS-&gt;
    PRECONDITIONS: sports menu-&gt;sportscategory-&gt;Am.Football-&gt;competitions tab-&gt;enable/disable.
    PRECONDITIONS: Note: In mobile when no events are available American Football sport is not displayed in A-Z sports menu and on clicking American Football from Sports ribbon user is navigated back to the sports homepage.
    """
    keep_browser_open = True
    competitions_tab = vec.sb.TABS_NAME_COMPETITIONS.upper()
    home_breadcrumb = vec.sb.HOME_FOOTER_ITEM.upper()

    def test_000_preconditions(self):
        """
        DESCRIPTION : Checking whether competitions tab is enabled in cms or not.
        DESCRIPTION : checking whether time filter is enabled or disable in cms
        """
        self.__class__.category_id = self.ob_config.backend.ti.american_football.category_id
        self.__class__.sport_name = self.get_sport_title(self.category_id)

        competition_tab_status = self.cms_config.get_sport_tab_status(sport_id=self.category_id,
                                                                      tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions)
        self.__class__.matches_tab_status = self.cms_config.get_sport_tab_status(sport_id=self.category_id,
                                                                                 tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches)
        if not competition_tab_status:
            raise CmsClientException(f'Competitions tab is not available in cms')
        # getting American Football competitions tab data
        competitions_tab_data = self.cms_config.get_sports_tab_data(sport_id=self.category_id,
                                                                    tab_name=self.competitions_tab.lower())

        if not competitions_tab_data.get('filters')['time']['enabled']:
            # Making competitions tab enable and enabling time filter for competitions tab in cms for American football.
            self.cms_config.update_sports_event_filters(tab_name=self.competitions_tab.lower(),
                                                        sport_id=self.category_id,
                                                        enabled=True,
                                                        timefilter_enabled=True,
                                                        event_filters_values=[1, 3, 6, 12, 24, 48])

    def test_001_launch_the_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes/Coral application
        EXPECTED: Home page should loaded succesfully
        """
        pass

    def test_002_click_on_american_football_sport(self):
        """
        DESCRIPTION: Click on American Football sport.
        EXPECTED: User should be able to navigate to the American Football landing page.
        """
        self.navigate_to_page(name='sport/american-football')
        self.site.wait_content_state('american-football')

    def test_003_verify_american_football_landing_page(self):
        """
        DESCRIPTION: Verify American Football landing page.
        EXPECTED: Desktop
        EXPECTED: Tabs should be displayed with defualt selected matches tab with today events .
        EXPECTED: In play widget will display if any events are in live when it was enabled in sys config.
        EXPECTED: Mobile
        EXPECTED: Matches module loaded as default with inplay events in it
        """
        if not self.matches_tab_status:
            return "Matches tab is unavailable in cms"

        expected_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.matches.upper()
        current_tab_name = self.site.american_football.tabs_menu.current.upper()
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Default tab is not "{expected_tab_name}", it is "{current_tab_name}"')

        if self.device_type == "desktop":
            grouping_button = self.site.american_football.tab_content.grouping_buttons.current
            self.assertEqual(grouping_button.upper(), vec.sb.SPORT_DAY_TABS.today.upper(), msg=f'Expected tab {vec.sb.SPORT_DAY_TABS.today.upper()} is not equal to Actual tab {grouping_button.upper()}')
        else:
            # For tire two sports in-play is present inside matches tab
            live_event_status = bool(self.get_active_events_for_category(category_id=self.category_id, in_play_event=True))
            in_play_module_status = self.site.sports_page.tab_content.has_inplay_module()
            self.assertEqual(live_event_status, bool(in_play_module_status), msg=f'Actual inplay module status is : "{bool(in_play_module_status)}" not same as Expected inplay module status : "{live_event_status}"')

    def test_004_verify_competitions_tab(self):
        """
        DESCRIPTION: Verify Competitions tab
        EXPECTED: Competitions need to loaded
        """
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.american_football_config.category_id)
        self.site.american_football.tabs_menu.click_button(expected_tab_name)

    def test_005_verify__time_filters(self):
        """
        DESCRIPTION: Verify  time filters.
        EXPECTED: Events should be fetched as per selection
        """
        tab_content = self.site.sports_page.tab_content
        timeline_filters = tab_content.timeline_filters
        filters = timeline_filters.items_as_ordered_dict
        self.assertTrue(filters, msg='filters are not displayed')
        filter = None
        for filter_name, filter in filters.items():
            filter.click()
            result = wait_for_result(lambda: filter_name in list(timeline_filters.selected_filters.keys()),
                            name=f'waiting for filter :{filter_name} to be highlighted')
            self.assertTrue(result, msg=f'selected time filter {filter_name} is not selected')

            no_events_label = tab_content.has_no_events_label()
            if not no_events_label:
                accordion_lists = self.site.competition_league.tab_content.accordions_list.has_items
                self.assertTrue(accordion_lists, '"Accordions" OR "No events found" Label not displayed')

        filter.click()  # to unselect time filter

    def test_006_verify_accordions_are_collapsable_and_expandable(self):
        """
        DESCRIPTION: Verify accordions are collapsable and expandable
        EXPECTED: Accordions should be collapsable and expandable
        """
        self.__class__.accordions = self.site.sports_page.tab_content.tt_competitions_categories_list.items_as_ordered_dict
        self.assertTrue(self.accordions, msg=f'no accordions are found')
        # verifying accordions of competitions tab are expand and collapse successfully
        for accordion_name, accordion in list(self.accordions.items())[:5]:
            if accordion.is_expanded():
                accordion.collapse()
                self.assertFalse(accordion.is_expanded(), msg=f'section "{accordion_name}" is not Collapsed')
                accordion.expand()
                self.assertTrue(accordion.is_expanded(), msg=f'section "{accordion_name}" is not expanded')
            else:
                accordion.expand()
                self.assertTrue(accordion.is_expanded(), msg=f'section "{accordion_name}" is not expanded')
                accordion.collapse()
                self.assertFalse(accordion.is_expanded(), msg=f'section "{accordion_name}" is not Collapsed')
                accordion.expand()

    def test_007_verfiy_more_link_on_above_odds_selection(self):
        """
        DESCRIPTION: Verfiy More link on above odds selection
        EXPECTED: User should be navigated to respective EDP page
        """
        self.__class__.state_changed = False
        drop_down_status = self.site.competition_league.tab_content.has_dropdown_market_selector()
        aggregated_market_status = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item.upper() in ['GAME LINES', 'GAME LINES 3 WAY'] if drop_down_status else False
        for accordion_name, accordion in self.accordions.items():
            accordion.expand()
            for event_name, event in accordion.items_as_ordered_dict.items():
                if 'oddsCard.outrightsTemplate' == event.template.get_attribute('data-crlat'):
                    continue
                self.__class__.event_id = event.template.event_id
                event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.event_id)
                no_of_markets = len(event_resp[0]['event'].get('children'))
                if no_of_markets > 1:
                    if no_of_markets == 3 and aggregated_market_status:
                        continue
                    self.assertTrue(event.has_markets(), msg=f"Event doesn't have more link'{event_name}'")
                    event.more_markets_link.click()
                    wait_for_haul(5)
                    self.site.wait_content_state(state_name='EventDetails')
                    if self.device_type == "desktop":
                        actual_event_name = self.site.sport_event_details.content_title_text.upper().replace(' VS ', ' V ')
                        expected_event_name = event_name.upper().replace(' VS ', ' V ')
                        self.assertEqual(actual_event_name, expected_event_name,msg=f'Actual event title {actual_event_name} is not same as expected event title {expected_event_name}')
                    wait_for_result(lambda: self.site.has_back_button, expected_result=True,
                                    name=f'back Button to be available in EDP "',
                                    timeout=10, bypass_exceptions=VoltronException)
                    wait_for_haul(5)
                    self.__class__.state_changed = True
                    break
                else:
                    self.assertFalse(event.has_markets(), msg=f"Event does have more link'{event_name}'even there are less than one market")

    def test_008_verify_signposting(self):
        """
        DESCRIPTION: Verify signposting.
        EXPECTED: User should be able to see signposting.
        """
        if not self.state_changed:
            return "Not Applicable"

        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.event_id)[0].get('event')['children']
        cashout_markets = {market.get('market')['name'].replace('|', '').title(): True for market in event_resp if market.get('market')['cashoutAvail'] == 'Y'}

        tabs = self.site.sport_event_details.markets_tabs_list.get_items(name="ALL MARKETS")
        self.assertTrue(tabs.get("ALL MARKETS"), f'ALL MARKETS TAB is not available')
        tabs.get("ALL MARKETS").click()

        markets = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
        for market_name, market in markets.items():
            self.assertEqual(cashout_markets.get(market_name.title(), False), market.market_section_header.has_cash_out_mark(expected_result=cashout_markets.get(market_name.title(), False)), f'Expected signposting Status for {market_name.upper()} is {cashout_markets.get(market_name.title(), False)}. but Actual Status is {not cashout_markets.get(market_name.title(), False)}')

    def test_009_click_on_signposting(self):
        """
        DESCRIPTION: Click on signposting.
        EXPECTED: User should be able to see popup text which is related to signposting.
        """
        # currently we don't have odds boost sign post if odds boost sign post is available when we click on it ,
        # popup is displayed which is related to odds boost for that particular market

    def test_010_verify_by_clicking_on_backward_chevron_beside_sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron beside sport header
        EXPECTED: Desktop
        EXPECTED: User should be navigated to home page
        """
        # covered in test_012_verify_breadcrumbs step

    def test_011_verify_by_clicking_on_backward_chevron_on_above__sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron on above  sport header
        EXPECTED: Mobile
        EXPECTED: User should be navigated to sport navigation  page
        """
        # covered in test_012_verify_breadcrumbs step

    def test_012_verify_breadcrumbs(self):
        """
        DESCRIPTION: Verify Breadcrumbs
        EXPECTED: Desktop
        EXPECTED: User should be navigated on the respective page on click
        """
        if self.state_changed:
            # coming back to competitions tab from event details page by click back button
            self.site.back_button_click()
        wait_for_haul(5)
        # # verifying Breadcrumbs
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

            self.assertEqual(list(breadcrumbs.keys()).index(self.competitions_tab), 2,
                             msg=f'" matches " item name is not shown after "{self.sport_name}"')
            self.assertTrue(
                int(breadcrumbs[self.competitions_tab].link.css_property_value('font-weight')) == 700,
                msg=f'" matches " hyperlink from breadcrumbs is not highlighted according to the selected page')

        # verifying backward chevron on above sport header
        self.site.back_button.click()
        self.site.wait_content_state("homepage")

    def test_013_verify_bet_placement_for_single_multiplecomplex(self):
        """
        DESCRIPTION: Verify bet placement for single, multiple,complex
        EXPECTED: Bet placement need to successful
        """
        # Covered in test case C60089526