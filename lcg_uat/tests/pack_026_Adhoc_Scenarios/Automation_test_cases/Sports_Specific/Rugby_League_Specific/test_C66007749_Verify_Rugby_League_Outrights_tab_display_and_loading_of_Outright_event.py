from typing import List

import pytest
from crlat_cms_client.utils.exceptions import CMSException
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@pytest.mark.sports_specific
@pytest.mark.rugby_league_specific
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@vtest
class Test_C66007749_Verify_Rugby_League_Outrights_tab_display_and_loading_of_Outright_event(BaseBetSlipTest):
    """
    TR_ID: C66007749
    NAME: Verify Rugby League Outrights tab display and loading of Outright event.
    DESCRIPTION: This test case validates the display of data in the Rugby League - Outright's tab
    PRECONDITIONS: In CMS, Sport pages -&gt; Sport Categories-&gt; Rugby league sport -&gt; Tabs and modules should be configured
    """
    keep_browser_open = True
    event_id = None

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
        TR_ID: C66007749
        NAME: Verify Rugby League Outrights tab display and loading of Outright event.
        DESCRIPTION: This test case validates the display of data in the Rugby League - Outright's tab
        PRECONDITIONS: In CMS, Sport pages -&gt; Sport Categories-&gt; Rugby league sport -&gt; Tabs and modules should be configured
        """
        self.__class__.rugby_league_category_id = self.ob_config.rugby_league_config.category_id
        outright = self.cms_config.get_sport_tab_status(sport_id=self.ob_config.rugby_league_config.category_id,
                                                        tab_name=self.cms_config.constants.
                                                        SPORT_TABS_INTERNAL_NAMES.outrights)
        if not outright:
            raise CMSException("Outright Tab Does Not Have Events For Rugby Union")

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application
        EXPECTED: Application should be launched successfully.
        """
        self.site.login()
        self.site.wait_content_state('Homepage')

    def test_002_navigate_to_rugby_league_sport(self):
        """
        DESCRIPTION: Navigate to Rugby league sport
        EXPECTED: Navigation should be successful.
        EXPECTED: By default application navigates to Matches tab/Today subtab.
        """
        self.navigate_to_page(name='sport/rugby-league')
        self.site.wait_content_state(state_name='rugby-league')
        self.site.wait_content_state_changed(timeout=15)

    def test_003_navigate_to_outright_tab(self):
        """
        DESCRIPTION: Navigate to Outright tab
        EXPECTED: Outright tab should be loaded.
        """
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights,
                                                    self.ob_config.rugby_league_config.category_id)
        self.site.contents.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        self.site.wait_content_state_changed()
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab is "{current_tab_name}", instead of "{expected_tab_name}"')

    def test_004_verify_the_data_display(self):
        """
        DESCRIPTION: Verify the data display
        EXPECTED: Type name should be displayed as header and events should be displayed under it.
        """
        # Get the sections from the sports page
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        # Assert that at least one section is found
        self.assertTrue(sections, msg='No sections found')
        # Get the first section
        section = list(sections.values())[0]
        section.click()
        # Get the events within the section
        events = section.items_as_ordered_dict
        # Assert that at least one event is found
        self.assertTrue(events, msg='No events found in the section')
        event = list(events.values())[0]
        self.__class__.event_id = event.event_id
        event.click()
        self.site.wait_content_state(state_name="EVENTDETAILS")
        # Get the markets from the sport event details page
        markets = list(self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict.values())[0]

        # Assert that at least one market is found
        self.assertTrue(markets, msg='No leagues sections found')
        # Get the outcomes within the markets
        outcomes = list(markets.outcomes.items_as_ordered_dict.values())
        # Assert that at least one outcome is found
        self.assertTrue(outcomes, msg='No outcomes found in the markets')
        outcomes[0].bet_button.click()

    def test_005_click_on_type_name_header(self):
        """
        DESCRIPTION: Click on type name header
        EXPECTED: Type section should expand and all the events should be displayed.
        """
        # covered in above steps
    def test_006_click_on_event_name(self):
        """
        DESCRIPTION: Click on event name
        EXPECTED: Should navigate to event details page.
        """
        # covered in above steps

    def test_007_add_any_selection_to_betslip_and_place_bet(self):
        """
        DESCRIPTION: Add any selection to betslip and place bet.
        EXPECTED: Bet should be placed successfully.
        """
        outright_selections = self.get_selection_for_event_id(events=[self.event_id])
        if len(outright_selections) >= 1:
            # Single Bet
            self.__class__.expected_betslip_counter_value = 0
            self.open_betslip_with_selections(selection_ids=outright_selections[0])
            self.place_single_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
