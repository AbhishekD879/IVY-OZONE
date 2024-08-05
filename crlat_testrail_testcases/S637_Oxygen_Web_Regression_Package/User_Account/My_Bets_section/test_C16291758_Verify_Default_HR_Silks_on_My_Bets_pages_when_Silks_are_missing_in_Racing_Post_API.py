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
class Test_C16291758_Verify_Default_HR_Silks_on_My_Bets_pages_when_Silks_are_missing_in_Racing_Post_API(Common):
    """
    TR_ID: C16291758
    NAME: Verify Default HR Silks on My Bets pages when Silks are missing in Racing Post API
    DESCRIPTION: This test case verifies that HR bets are properly displayed when data from Racing Post API is unavailable or partially missing
    PRECONDITIONS: * At least 2 Horse Racing Event not mapped with Racing Post data with cashout available
    PRECONDITIONS: (e.g.receiving empty response https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/21/events/508154/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b)
    PRECONDITIONS: * List of Aggregation MS {envs.}: https://confluence.egalacoral.com/display/SPI/Aggregation+Java
    PRECONDITIONS: https://{env.}/silks/racingpost/17058,243739,266307,61763,...
    PRECONDITIONS: * Silk ID is received in response from https://ld-{env.}.api.datafabric.{env.}.aws.ladbrokescoral.com/v4/sportsbook-api/categories/21/events/{event id}/content?locale=en-GB&api-key={api key}
    PRECONDITIONS: in horses.silk: "{silk id}.png" attribute
    PRECONDITIONS: **note**: for vanilla is received in response: https://sb-api-dev.coral.co.uk/v4/sportsbook-api/categories/21/events/{event_id}/content?locale=en-GB&api-key={api_key}
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

    def test_003__tap_on_my_bets_button_on_header__cash_out_tab_check_silks_for_placed_bet_when_racing_post_data_is_unavailable_in_browser_devtools_block_request_to_racing_post_data_from_which_silk_id_is_received(self):
        """
        DESCRIPTION: * Tap on 'My Bets' button on Header > 'Cash out' tab
        DESCRIPTION: * Check silks for placed bet when Racing Post data is unavailable
        DESCRIPTION: ( in browser devtools block request to Racing Post data from which Silk ID is received)
        EXPECTED: * Silk images/Generic silks are NOT displayed for placed bet to the left of a horse name
        """
        pass

    def test_004_repeat_step_3_when_racing_post_data_is_available_but_silk_id_is_not_available_use_charles_tools_to_remove_silk_id_in_response_from_racing_post_data(self):
        """
        DESCRIPTION: Repeat step #3 when Racing Post data is available, but silk id is not available
        DESCRIPTION: ( Use Charles tools to remove silk id in response from Racing Post data)
        EXPECTED: * Generic silk images are displayed for placed bet to the left of a horse name
        """
        pass

    def test_005_repeat_step_3_when_racing_post_data_is_available_but_silk_image_is_unavailable_in_aggregation_ms_use_charles_tools_to_remove_silk_image_in_aggregation_ms_or_in_browser_devtools_block_request_to_aggregation_ms_and_verify_silk_icons_(self):
        """
        DESCRIPTION: Repeat step #3 when Racing Post data is available, but silk image is unavailable in Aggregation MS
        DESCRIPTION: ( Use Charles tools to remove silk image in Aggregation MS or in browser devtools block request to Aggregation MS and verify silk icons )
        EXPECTED: * Generic silk images are displayed for placed bet to the left of a horse name
        """
        pass

    def test_006_repeat_step_2_5_for_multiple_bet__eg_double_hr_bet_when_silks_are_not_available_in_racing_post_data(self):
        """
        DESCRIPTION: Repeat step #2-5 for multiple bet ( e.g. Double HR bet) when silks are not available in Racing Post data
        EXPECTED: Results are the same
        """
        pass

    def test_007_repeat_step_2_5_for_multiple_bet__eg_double_hr_bet_when_silks__for_one_selection_is_available_and_another___not_available_in_racing_post_data(self):
        """
        DESCRIPTION: Repeat step #2-5 for multiple bet ( e.g. Double HR bet) when silks  for one selection is available and another - not available in Racing Post data
        EXPECTED: Results are the same
        """
        pass

    def test_008_navigate_to_my_bets__open_bets_tab(self):
        """
        DESCRIPTION: Navigate to 'My Bets' > 'Open Bets' tab
        EXPECTED: * Open Bets' tab with 'regular' filter is opened by default
        """
        pass

    def test_009_repeat_step_2_6(self):
        """
        DESCRIPTION: Repeat step #2-6
        EXPECTED: Results are the same
        """
        pass

    def test_010_set_results_for_hr_events_from_step_2_and_6(self):
        """
        DESCRIPTION: Set results for HR events from step 2 and 6
        EXPECTED: Events are suspended and finished
        """
        pass

    def test_011_navigate_to_my_bets__settled_bets_tab(self):
        """
        DESCRIPTION: Navigate to 'My Bets' > 'Settled Bets' tab
        EXPECTED: Results are the same
        """
        pass
