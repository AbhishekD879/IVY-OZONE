from collections import OrderedDict
import pytest
from crlat_cms_client.utils.exceptions import CMSException
from typing import List
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.sports_specific
@pytest.rugby_union_specific
@pytest.adhoc_suite
@pytest.mark.desktop
@vtest
class Test_C65969081_Verify_the_display_of_data_in_the_Rugby_Union_Outrights_tab(BaseBetSlipTest):
    """
    TR_ID: C65969081
    NAME: Verify the display of data in the Rugby Union Outrights tab
    DESCRIPTION: This test case needs to verify Outright's tab display for the Rugby Union sport.
    """
    home_breadcrumb = 'Home'
    sport_name = 'rugby union'
    keep_browser_open = True
    events = []

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
        PRECONDITIONS: 1.User should have access to oxygen CMS
        PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
        PRECONDITIONS: 2.Outrights tab can be configured from CMS-&gt;
        PRECONDITIONS: Sports menu-&gt; Sports category-&gt; Rugby Union-&gt; Outright's tab-&gt; Enable/Disable.
        PRECONDITIONS: Note: In mobile when no events are available Rugby Union sport is not displayed in A-Z sports menu and on clicking Rugby Union  from Sports ribbon user is navigated back to the sports homepage.
        """
        outright = self.cms_config.get_sport_tab_status(sport_id=self.ob_config.rugby_union_config.category_id,
                                                        tab_name=self.cms_config.constants.
                                                        SPORT_TABS_INTERNAL_NAMES.outrights)
        if not outright:
            raise CMSException("Outright Tab Does Not Have Events For Rugby Union")

    def test_001_launch_the_ladbrokes_and_coral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes and Coral application
        EXPECTED: Home page should loaded successfully
        """
        self.site.login()

    def test_002_click_on_rugby_union_sport(self):
        """
        DESCRIPTION: Click on Rugby Union sport.
        EXPECTED: User should be able to navigate to the Rugby Union landing page.
        """
        # Covered in Step 3

    def test_003_verify_outrights_tab(self):
        """
        DESCRIPTION: Verify Outright's tab
        EXPECTED: Accordions should be in collapsed mode by default if data present.
        EXPECTED: Outright tab should not be visble to the user if no data present in it.
        """
        self.site.open_sport("Rugby Union")
        all_tabs_on_fe = self.site.sports_page.tabs_menu.items_as_ordered_dict
        self.assertIn(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights.upper(), all_tabs_on_fe.keys())
        all_tabs_on_fe.get(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights.upper()).click()

    def test_004_verify_accordions_are_collapsable_and_expandable(self):
        """
        DESCRIPTION: Verify accordions are collapsable and expandable
        EXPECTED: Accordion's should be collapsable and expandable
        """
        events_accordian = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        for type_name, event_type in events_accordian.items():
            is_expanded = event_type.is_expanded()
            self.assertFalse(is_expanded, msg=f"Accordion for type {type_name} expanded by default even if not clicked")
            event_type.expand()
            self.__class__.events.append(event_type.items_as_ordered_dict.popitem()[1].event_id)
            is_expanded = event_type.is_expanded()
            self.assertTrue(is_expanded, msg=f"Accordion for type {type_name} Not expanded even After Clicking")

    def test_005_verify_breadcrumbs(self):
        """
        DESCRIPTION: Verify Breadcrumbs
        EXPECTED: Desktop
        EXPECTED: User should be navigated on the respective page on click
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

            self.assertEqual(list(breadcrumbs.keys()).index("Outrights"), 2,
                             msg=f'" matches " item name is not shown after "{self.sport_name}"')
            self.assertTrue(
                int(breadcrumbs["Outrights"].link.css_property_value('font-weight')) == 700,
                msg='" outrights " hyperlink from breadcrumbs is not highlighted according to the selected page')

    def test_006_verify_by_clicking_on_backward_chevron_beside_sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron beside sport header
        EXPECTED: Desktop
        EXPECTED: User should be naviagted to homepage
        EXPECTED: Mobile
        EXPECTED: User should be naviagted to sport navigation page
        """
        if self.device_type == "mobile" and tests.settings.brand == "ladbrokes":
            back_button = self.site.header.back_button
            back_button.click()
        else:
            self.site.sports_page.back_button_click()
        self.site.wait_content_state(state_name="Home")
        self.test_003_verify_outrights_tab()

    def test_007_verify_by_expanding_the_accordion_and_click_on_events(self):
        """
        DESCRIPTION: Verify by expanding the accordion and click on events.
        EXPECTED: User should be navigated to respective page.
        """
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        _, event_type = sections.popitem()
        event_type.expand()
        _, event = event_type.items_as_ordered_dict.popitem()
        event.click()
        self.site.wait_content_state(state_name="EVENTDETAILS")

    def test_008_verify_bet_placements_for_single_multiple_complex(self):
        """
        DESCRIPTION: Verify bet placements for Single, Multiple, Complex
        EXPECTED: Bet placements needs to be successful
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
            self.open_betslip_with_selections(selection_ids=[outright_selections[0],
                                                             outright_selections[1],
                                                             outright_selections[2],
                                                             outright_selections[3]])
            self.place_multiple_bet(number_of_stakes=2)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
