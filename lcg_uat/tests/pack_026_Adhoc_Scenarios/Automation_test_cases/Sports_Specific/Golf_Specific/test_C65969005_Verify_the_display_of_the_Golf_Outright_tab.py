import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from typing import List


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.sports_specific
@pytest.mark.golf_specific
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@vtest
class Test_C65969005_Verify_the_display_of_the_Golf_Outright_tab(BaseBetSlipTest):
    """
    TR_ID: C65969005
    NAME: Verify the display of the Golf Outright tab
    DESCRIPTION: This test case verifies the Golf Outright tab display and loading of outright events.
    PRECONDITIONS: CMS-&gt; Sport pages-&gt; Sport category-&gt; Golf
    PRECONDITIONS: CMS-&gt; Sport pages-&gt; Sport category-&gt; Golf-&gt; General Sport Configuration
    PRECONDITIONS: CMS-&gt; Sport pages-&gt; Sport category-&gt; Golf-&gt; General Sport Configuration-&gt; Active/Inactive sport
    """
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

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application
        EXPECTED: User should be able to launch the application successfully
        """
        self.site.login()

    def test_002_navigate_to_golf_page(self):
        """
        DESCRIPTION: Navigate to Golf page
        EXPECTED: User should be able to navigate to the Golf page
        """
        self.site.open_sport(name="Golf")

    def test_003_click_on_the_outright_tab(self):
        """
        DESCRIPTION: Click on the Outright tab
        EXPECTED: User should be able to navigate to Outright's page
        EXPECTED: Outright events should be displayed in this tab.
        """
        all_sub_tabs_for_golf_fe = self.site.sports_page.tabs_menu.items_as_ordered_dict
        all_sub_tabs_names_for_golf_fe = [tab.upper() for tab in list(all_sub_tabs_for_golf_fe.keys())]
        self.assertIn("OUTRIGHTS", all_sub_tabs_names_for_golf_fe, msg="OUTRIGHTS Tab Not Found on Golf SLP")
        all_sub_tabs_for_golf_fe.get('OUTRIGHTS').click()

    def test_004_verify_the_accordions(self):
        """
        DESCRIPTION: Verify the accordion's
        EXPECTED: User should be able to expand/collape accordion's
        """
        events_accordian = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        for type_name, event_type in events_accordian.items():
            is_expanded = event_type.is_expanded()
            self.assertFalse(is_expanded, msg=f"Accordion for type {type_name} expanded by default even if not clicked")
            event_type.expand()
            self.__class__.events.append(event_type.items_as_ordered_dict.popitem()[1].event_id)
            is_expanded = event_type.is_expanded()
            self.assertTrue(is_expanded, msg=f"Accordion for type {type_name} Not expanded even After Clicking")

    def test_005_verify_the_bet_placement_for_a_selection_from_the_outright_event(self):
        """
        DESCRIPTION: Verify the bet placement for a selection from the Outright event.
        EXPECTED: The user should be able to place a bet successfully on the Outright event.
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
