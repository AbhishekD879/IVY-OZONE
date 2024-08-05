import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C2298143_Verify_HR_Silks_on_My_Bets_pages(Common):
    """
    TR_ID: C2298143
    NAME: Verify HR Silks on My Bets pages
    DESCRIPTION: This test case verifies that Silks are loaded from Aggregation MS (which uses DF API) and return Silk via ID from silks sprite on My Bets page (Open and settled bets tabs)
    PRECONDITIONS: * At least 2 Horse Racing Event is mapped with DF API data (Racing Post) with cashout available
    PRECONDITIONS: * List of Aggregation MS {envs.}: https://confluence.egalacoral.com/display/SPI/Aggregation+Java
    PRECONDITIONS: https://{env.}/silks/racingpost/17058,243739,266307,61763,...
    PRECONDITIONS: * Silk ID is received in response from https://ld-{env.}.api.datafabric.{env.}.aws.ladbrokescoral.com/v4/sportsbook-api/categories/21/events/{event id}/content?locale=en-GB&api-key={api key}
    PRECONDITIONS: in horses.silk: "{silk id}.png" attribute
    """
    keep_browser_open = True

    def test_001_load_oxygenladbrokes_app_and_log_in(self):
        """
        DESCRIPTION: Load Oxygen/Ladbrokes app and log in
        EXPECTED: 
        """
        pass

    def test_002_place_a_bet__single_hr_bet_for_event_from_preconditions(self):
        """
        DESCRIPTION: Place a bet  (Single HR bet) for event from preconditions
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_003_tap_on_my_bets_button_on_headertap_on_cash_out_tab_and_check_silks_are_displayed(self):
        """
        DESCRIPTION: Tap on 'My Bets' button on Header
        DESCRIPTION: Tap on 'Cash out' tab and check silks are displayed
        EXPECTED: * Silks are displayed for placed bet to the left of a horse name
        """
        pass

    def test_004_in_browser_devtools_check_how_silks_are_loadedeg_call_to_aggregation_ms_httpsaggregation_dev0coralsportsdevcloudladbrokescoralcomsilksracingpost123203144359184671b187111218882221353238386249844252924(self):
        """
        DESCRIPTION: In browser DevTools check how silks are loaded
        DESCRIPTION: (e.g. call to Aggregation MS: https://aggregation-dev0.coralsports.dev.cloud.ladbrokescoral.com/silks/racingpost/123203,144359,184671b,187111,218882,221353,238386,249844,252924)
        EXPECTED: Silks should be loaded from Aggregation MS by silksIDs (e.g. silk Id of specific horse received in https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/21/events/502368/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b corresponds to same silk id from Aggregation MS)
        """
        pass

    def test_005_repeat_step_2_4_for_multiple_bet__eg_double_hr_bet(self):
        """
        DESCRIPTION: Repeat step #2-4 for multiple bet ( e.g. Double HR bet)
        EXPECTED: Results are the same
        """
        pass

    def test_006__tap_on_open_bets_tab_repeat_step_4_5(self):
        """
        DESCRIPTION: * Tap on 'Open Bets' tab
        DESCRIPTION: * Repeat step 4-5
        EXPECTED: * 'Open Bets' tab with 'regular' filter is opened by default
        EXPECTED: * Results are the same
        """
        pass

    def test_007_set_results_for_hr_events_from_step_2_and_5(self):
        """
        DESCRIPTION: Set results for HR events from step 2 and 5
        EXPECTED: Events are suspended and finished
        """
        pass

    def test_008_navigate_to_my_bets__settled_bets_tab(self):
        """
        DESCRIPTION: Navigate to 'My Bets' > 'Settled Bets' tab
        EXPECTED: HR Bets are displayed with silks available
        """
        pass

    def test_009_in_browser_devtools_check_how_silks_are_loadedeg_call_to_aggregation_ms_httpsaggregation_dev0coralsportsdevcloudladbrokescoralcomsilksracingpost123203144359184671b187111218882221353238386249844252924(self):
        """
        DESCRIPTION: In browser DevTools check how silks are loaded
        DESCRIPTION: (e.g. call to Aggregation MS: https://aggregation-dev0.coralsports.dev.cloud.ladbrokescoral.com/silks/racingpost/123203,144359,184671b,187111,218882,221353,238386,249844,252924)
        EXPECTED: Silks should be loaded from Aggregation MS by silksIDs (e.g. silk Id of specific horse received in https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/21/events/502368/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b corresponds to same silk id from Aggregation MS)
        """
        pass
