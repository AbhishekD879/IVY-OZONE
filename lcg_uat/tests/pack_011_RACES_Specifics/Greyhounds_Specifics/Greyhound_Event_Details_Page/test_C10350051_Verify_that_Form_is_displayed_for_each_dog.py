import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.greyhounds
@pytest.mark.event_details
@pytest.mark.ladbrokes_only
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C10350051_Verify_that_Form_is_displayed_for_each_dog(BaseGreyhound):
    """
    TR_ID: C10350051
    NAME: Verify that 'Form' is displayed for each dog
    DESCRIPTION: This test case verifies displaying of 'Form' information for each dog on race card
    PRECONDITIONS: update: After BMA-40744 implementation we'll use RDH feature toggle:
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: we'll receive needed data from DF api:
    PRECONDITIONS: Racing Data Hub link:
    PRECONDITIONS: Coral DEV : cd-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: Ladbrokes DEV : https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b
    PRECONDITIONS: URI : /v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: {categoryKey} : 21 - Horse racing, 19 - Greyhound
    PRECONDITIONS: {eventKey} : OB Event id
    PRECONDITIONS: -------
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: - User is logged in
        PRECONDITIONS: - User is at Greyhound Race Card (Event Details page)
        PRECONDITIONS: - 'Form' information for each selection is present in response from DF API https://raceinfo-api.ladbrokes.com/race_info/ladbrokesdog/[eventID]
        PRECONDITIONS: - Form value is taken from 'last5Runs' param (e.g. last5Runs: "23522")
        """
        event_info = self.get_event_details(datafabric_data=True)
        event_id = event_info.event_id
        self.navigate_to_edp(event_id=event_id, sport_name='greyhound-racing')
        self.site.wait_content_state(state_name='GreyHoundEventDetails')
        tab_name = vec.racing.RACING_EDP_DEFAULT_MARKET_TAB
        racing_event_tab_content = self.site.greyhound_event_details.tab_content.event_markets_list
        racing_event_tab_content.market_tabs_list.open_tab(tab_name)
        sections = wait_for_result(lambda: racing_event_tab_content.items_as_ordered_dict,
                                   timeout=5, name='Section is not empty')
        self.assertTrue(sections, msg='No sections was found')
        self.__class__.form_info = \
            {runner['dogName']: runner['last5Runs'] for runner in event_info.datafabric_data['runners'] if runner['dogName'] != 'VACANT'}
        self.site.login(async_close_dialogs=False)

    def test_001_verify_that_form_information_for_each_selection(self):
        """
        DESCRIPTION: Verify that 'Form' information for each selection
        EXPECTED: Form information is displayed for each selection under Dog's name:
        EXPECTED: text "Form:" and 'value' in bold (e.g. "Form: **12345**")
        """
        markets = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = list(markets.values())[0]
        outcomes = market.items_as_ordered_dict
        self.assertTrue(outcomes, msg='Market does not have any items')
        for outcome_name, outcome in outcomes.items():
            outcome.scroll_to()
            if 'Unnamed' not in outcome_name and 'Vacant N/R' not in outcome_name:
                form_value = self.form_info.get(outcome_name, False)
                self.assertTrue(form_value,
                                msg=f'Cannot find form_value on UI "{outcome_name}", '
                                f'among selections received from response: {self.form_info.keys()}')
                form_value = f'Form: {form_value}'
                self.assertEqual(form_value, outcome.form,
                                 msg=f'Actual Form value: "{outcome.form}" for outcome "{outcome_name}" '
                                 f'is not the same as Expected: "{form_value}"')
