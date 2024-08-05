import pytest
import voltron.environments.constants as vec
from typing import List
from collections import OrderedDict
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_response_url, do_request
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.adhoc_suite
@pytest.mark.reg_170_fix
@pytest.mark.american_football
@pytest.mark.sports_specific
@vtest

class Test_C66007972_Verify_American_Football_Outright_tab_display_and_loading_of_outright_events(BaseBetSlipTest):
    """
    TR_ID: C66007972
    NAME: Verify American Football Outright tab display and loading of outright events.
    DESCRIPTION: This test case need to verify outrights tab display for American Football
    PRECONDITIONS: 1.User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: 2. outrights tab can be configured from CMS-&gt;
    PRECONDITIONS: sports menu-&gt;sportscategory-&gt;American Football-&gt;outrights tab-&gt;enable/disable.
    PRECONDITIONS: Note: In mobile when no events are available American Football sport is not displayed in A-Z sports menu and on clikcing  American Football from Sports ribbon user is navigated back to the sports homepage.
    """
    keep_browser_open = True
    events = []
    sport_name = 'AMERICAN FOOTBALL'
    default_date_tab = vec.sb.SPORT_DAY_TABS.today
    home_breadcrumb = vec.sb.HOME_FOOTER_ITEM.upper()
    highlight_tab = vec.sb.TABS_NAME_OUTRIGHTS.upper()
    enable_bs_performance_log = True

    def get_sport_tab_name(self, name: str, category_id: int):
        tabs_data = self.cms_config.get_sport_config(category_id=category_id).get('tabs')
        sport_tab = next((tab for tab in tabs_data if tab.get('name') == name), '')
        sport_tab_name = sport_tab.get('label').upper()
        return sport_tab_name

    def get_selection_for_event_id(self, events) -> List[str]:
        outright_selection = set()
        for event_id in events:
            event = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id).pop()
            for market in event['event']['children']:
                market_info = market['market']
                if market_info.get('templateMarketName') == '|Outright|' \
                        and \
                        int(market_info.get('maxAccumulators')) > 1:
                    outright_selection.add(market_info['children'][0]['outcome']['id'])
                    break
        return list(outright_selection)

    def test_000_preconditions(self):
        """
        TR_ID: C66007972
        NAME: Verify American Football Outright tab display and loading of outright events.
        DESCRIPTION: This test case need to verify outrights tab display for American Football
        PRECONDITIONS: 1.User should have access to oxygen CMS
        PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
        PRECONDITIONS: 2. outrights tab can be configured from CMS-&gt;
        PRECONDITIONS: sports menu-&gt;sportscategory-&gt;American Football-&gt;outrights tab-&gt;enable/disable.
        PRECONDITIONS: Note: In mobile when no events are available American Football sport is not displayed in A-Z sports menu and on clikcing  American Football from Sports ribbon user is navigated back to the sports homepage.
        """
        category_id = self.ob_config.backend.ti.american_football.category_id
        self.__class__.sport_name = self.get_sport_title(category_id)
        self.__class__.status = self.cms_config.get_sport_tab_status(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights, sport_id=category_id)
        self.__class__.expected_tab_name = self.get_sport_tab_name(
            name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights, category_id=category_id)
        self.__class__.matches_tab_name = self.get_sport_tab_name(
            name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches, category_id=category_id)

    def test_000_launch_the_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes/Coral application
        EXPECTED: Home page should loaded succesfully
        """
        self.site.login()
        self.site.wait_content_state('Homepage')

    def test_001_click_on_american_football_sport(self):
        """
        DESCRIPTION: Click on American Football sport.
        EXPECTED: User should be able to navigate to the American Football landing page.
        """
        self.site.open_sport(self.sport_name, content_state='american-football')

    def test_002_verify_outrights_tab(self):
        """
        DESCRIPTION: Verify Outright's tab
        EXPECTED: Accordions should be in collapsed mode by default if data present.
        EXPECTED: Outright tab should not be visble to the user if no data present in it .
        """
        tabs = self.site.contents.tabs_menu.items_as_ordered_dict
        if not self.status and self.expected_tab_name not in tabs:
            raise SiteServeException("events  are not present in outright tab of American Football")
        tabs.get(self.expected_tab_name).click()
        self.site.wait_content_state_changed()
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name.upper(), self.expected_tab_name.upper(),
                         msg=f'Actual tab is "{current_tab_name}", instead of "{self.expected_tab_name.upper()}"')
        self.__class__.actual_url = get_response_url(self, url='/EventToOutcomeForClass')
        # If the URL is not available, refresh the page and try again
        if not self.actual_url:
            self.device.refresh_page()
            self.__class__.actual_url = get_response_url(self, url='/EventToOutcomeForClass')
        response = do_request(method='GET', url=self.actual_url)
        self.__class__.event_type_name = {}
        self.__class__.event_time = {}
        for event in response['SSResponse']['children']:
            if not event.get('event'):
                break
            type_name = f"{event['event']['categoryName']} - {event['event']['typeName'].encode('utf-8').decode('unicode-escape')}".strip().upper()
            event_name = event['event']['name'].strip().upper()
            self.__class__.event_type_name[event_name] = type_name

    def test_003_verify_accordions_are_collapsable_and_expandable(self):
        """
        DESCRIPTION: Verify accordions are collapsable and expandable
        EXPECTED: Accordions should be collapsable and expandable
        """
        if len(self.event_type_name):
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
                    section.collapse()
                self.assertTrue(section_name.split('\n')[0].upper() in self.event_type_name.values(),
                                msg=f"according with {section_name} is not present in {self.event_type_name.values()}")
        else:
            self.assertTrue(self.site.sports_page.tab_content.has_no_events_label(),
                            msg="No events message is not displayed even when there are no events available")

    def test_004_verify_breadcrumbs(self):
        """
        DESCRIPTION: Verify Breadcrumbs
        EXPECTED: Desktop
        EXPECTED: User should be navigated on the respective page on click
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

            self.assertEqual(list(breadcrumbs.keys()).index('american football'.upper()), 1,
                             msg=f'"{self.sport_name}" sport title is not shown after "{self.home_breadcrumb}"')
            self.assertTrue(breadcrumbs['american football'.upper()].angle_bracket,
                            msg=f'Angle bracket is not shown after "{self.sport_name}" breadcrumb')
            self.assertEqual(list(breadcrumbs.keys()).index(self.highlight_tab), 2,
                             msg=f'" matches " item name is not shown after "{self.sport_name}"')
            self.assertTrue(
                int(breadcrumbs[self.highlight_tab].link.css_property_value('font-weight')) == 700,
                msg=f'" outright " hyperlink from breadcrumbs is not highlighted according to the selected page')
        accordions = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(accordions, msg="Events are not shown in outright tab")
        accordion = list(accordions.values())[0]
        accordion.expand()
        events = accordion.items_as_ordered_dict
        # Assert that at least one event is found
        self.assertTrue(events, msg='No events found in the section')
        event = list(events.values())[0]
        self.__class__.event_id = event.event_id
        event.click()
        self.site.wait_content_state("EVENTDETAILS")
        if self.device_type != 'mobile':
            sport_breadcrumb = self.site.sport_event_details.breadcrumbs.items_as_ordered_dict.get('american football')
            sport_breadcrumb.click()
            self.site.wait_content_state(state_name='american football')

    def test_005_verify_by_clicking_on_backward_chevron_beside_sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron beside sport header
        EXPECTED: Desktop
        EXPECTED: User should be naviagted to homepage
        """
        if self.device_type != 'mobile':
            self.site.back_button.click()
            self.site.wait_content_state("EVENTDETAILS")
            sport_breadcrumb = self.site.sport_event_details.breadcrumbs.items_as_ordered_dict.get("Home")
            sport_breadcrumb.click()
            self.site.wait_content_state("homepage")
            self.site.open_sport(self.sport_name, content_state='american-football')
            self.site.contents.tabs_menu.items_as_ordered_dict.get(self.expected_tab_name).click()

    def test_006_verify_by_clicking_on_backward_chevron_on_above__sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron on above  sport header
        EXPECTED: Mobile
        EXPECTED: User should be naviagted to sport navigation page
        """
        if self.device_type == 'mobile':
            self.site.back_button.click()
            self.site.wait_content_state(state_name='american football')
            current_tab_on_sport_slp = self.site.sports_page.tabs_menu.current
            self.assertTrue(current_tab_on_sport_slp.upper() == self.expected_tab_name.upper(),
                            msg="After clicking on back button from event detail page outright tab is not selected by defualt ")
    def test_007_verify_by_expanding_the_accordion_and_click_on_events(self):
        """
        DESCRIPTION: verify by expanding the accordion and click on events
        EXPECTED: User should be naviagted to respective page .
        """
        if self.device_type != 'mobile':
            accordions = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(accordions, msg="Events are not shown in outright tab")
            accordion = list(accordions.values())[0]
            accordion.expand()
            events = accordion.items_as_ordered_dict
            # Assert that at least one event is found
            self.assertTrue(events, msg='No events found in the section')
            event = list(events.values())[0]
            self.__class__.event_id = event.event_id
            event.click()
            self.site.wait_content_state("EVENTDETAILS")

    def test_008_verify_by_clicking_on_backward_chevron_beside_outright__header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron beside Outright  header
        EXPECTED: Desktop
        EXPECTED: User should be navigated to Outright's page
        """
        if self.device_type != 'mobile':
            wait_for_result(lambda: self.site.back_button, name='Back button to be available', timeout=10,
                            bypass_exceptions=VoltronException)
            self.site.back_button.click()
            self.site.wait_content_state(state_name='american football')
            current_tab_on_sport_slp = self.site.sports_page.tabs_menu.current
            self.assertTrue(current_tab_on_sport_slp.upper() == self.expected_tab_name.upper(),
                            msg="After clicking on back button from event detail page outright tab is not selected by defualt ")

    def test_009_verify_by_clicking_on_backward_chevron_on_above__outright__header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron on above  outright  header
        EXPECTED: Mobile
        EXPECTED: User should be naviagted to outrights page
        """
        # covered in above steps

    def test_010_verify_bet_placement_for_single_multiple_complex(self):
        """
        DESCRIPTION: Verify bet placement for single, multiple, complex
        EXPECTED: Bet placement needs to be successful
        """
        outright_selections = self.get_selection_for_event_id(events=self.events)
        if len(outright_selections) >= 1:
            # Single Bet
            self.__class__.expected_betslip_counter_value = 0
            self.open_betslip_with_selections(selection_ids=outright_selections[0])
            self.place_single_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
        if len(outright_selections) >= 2:
            # Multiple bet
            self.__class__.expected_betslip_counter_value = 0
            self.open_betslip_with_selections(selection_ids=[outright_selections[0], outright_selections[1]])
            self.place_multiple_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
        if len(outright_selections) >= 4:
            # Complex bet
            self.__class__.expected_betslip_counter_value = 0
            self.open_betslip_with_selections(selection_ids=[outright_selections[0],outright_selections[1], outright_selections[2],outright_selections[3]])
            self.place_multiple_bet(number_of_stakes=2)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()     
