import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound
from voltron.utils.exceptions.cms_client_exception import CmsClientException


# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.greyhounds
@vtest
class Test_C59535338_Verify_Greyhounds_sorting_in_Next_Races_Page(BaseGreyhound):
    """
    TR_ID: C59535338
    NAME: Verify Greyhounds sorting in Next Races Page
    DESCRIPTION: This test case verifies Greyhounds sorting  in Next Races Page
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User is at Greyhound Race Card (Event Details page)
    """
    keep_browser_open = True

    def test_001_set_up_greyhounds_to_be_displayed_in_the_next_races_module_on_the_greyhound_landing_page(self):
        """
        DESCRIPTION: Set up Greyhounds to be displayed in the next races module on the greyhound landing page
        EXPECTED: Greyhounds configured in the next races module on the greyhound landing page
        """
        greyhound_next_races_toggle = \
        self.cms_config.get_initial_data(device_type=self.device_type)['systemConfiguration'][
            'GreyhoundNextRacesToggle']['nextRacesTabEnabled']
        if not greyhound_next_races_toggle:
            raise CmsClientException('Next Races Tab is not enabled for greyhounds in CMS')

    def test_002_check_greyhounds_selections_order_in_next_races_module(self):
        """
        DESCRIPTION: Check Greyhounds selections order in next races module
        EXPECTED: Selections should be shown in numerical order unless  until there is a price available
        """
        event_info = self.get_event_details()
        event_id = event_info.event_id
        self.navigate_to_edp(event_id=event_id, sport_name='greyhound-racing')
        self.site.wait_content_state(state_name='GreyHoundEventDetails')

        markets = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = list(markets.values())[0]
        self.__class__.outcomes = market.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='Market does not have any items')

        runner = 0
        for outcome_name, outcome in list(self.outcomes.items()):
            self.outcomes = market.items_as_ordered_dict
            outcome.scroll_to()
            if 'Unnamed' not in outcome_name and not outcome.is_non_runner:
                if outcome.bet_button.name == 'SP':
                    runner_number = int(list(outcome.greyhound_runner_number)[-1])
                    runner += 1
                    self.assertEqual(runner, runner_number,
                                     msg='Selections are not shown in numerical order')
                else:
                    self._logger.info(msg="***Prices are available No numerical order***")
