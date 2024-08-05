import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C9332060_Verify_price_change_displaying_for_In_Play_events_in_front_end_at_once_appropriate_update_is_received_in_Websockets(Common):
    """
    TR_ID: C9332060
    NAME: Verify price change displaying for In-Play events in front-end at once appropriate update is received in Websockets
    DESCRIPTION: this test case verifies price change displaying for Multiples in front-end at once appropriate update is received in Websockets.
    DESCRIPTION: Based on Release OX 95.8 issues analysis
    DESCRIPTION: Note: Cannot be automated as we have no possibility to check whether the received update immediately is started to show on UI (scripts have some delays in finding appropriate elements on UI)
    PRECONDITIONS: 1. User is logged in to application and has positive balance
    PRECONDITIONS: 2. In-Play sport events are available in application
    """
    keep_browser_open = True

    def test_001_1_open_in_play_page_and_add_at_least_3_selections_from_different_sport_events(self):
        """
        DESCRIPTION: 1. Open in-play page and add at least 3 selections from different sport events
        EXPECTED: 1. Selections are added to Betslip
        EXPECTED: 2. 'Place your Acca'  section is displayed with Treble bet available
        EXPECTED: 3. Multiples section is displayed with all multiples created based on added selections
        """
        pass

    def test_002_in_ti_tool_trigger_price_update_for_both_selections_added_to_the_betslip(self):
        """
        DESCRIPTION: In TI tool trigger price update for both selections added to the Betslip
        EXPECTED: 1. Price updates are received in WS from Openbet TI tool
        EXPECTED: 2. Price updates are displayed in application AT ONCE after they were received in WS:
        EXPECTED: Previous odds become crossed out, up/down arrows showing if odds went up or down and current odds are displayed. Arrows and current price are indicated by arrow direction and color format. If odds went up - green, if odds went down - red
        EXPECTED: [Actual from OX 99]
        EXPECTED: The selection price change is displayed via push
        EXPECTED: (Price change from x to y - need to ensure we do not show x to x where price changes quickly away and then back to original price)
        EXPECTED: *info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: *info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed' (Ladbrokes only)
        EXPECTED: Button is updated to:
        EXPECTED: Ladbrokes: 'ACCEPT AND PLACE BET'
        EXPECTED: Coral: 'ACCEPT & PLACE BET'
        """
        pass

    def test_003_place_bet_at_once_after_price_updates_are_received_and_displayed_in_application(self):
        """
        DESCRIPTION: Place bet AT ONCE after price updates are received and displayed in application
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_004_repeat_steps_2_3_for_accumulator_4_accumulator_5_accumulator_6_multiples_available_in_place_your_acca_section(self):
        """
        DESCRIPTION: Repeat steps 2-3 for Accumulator (4), Accumulator (5), Accumulator (6) multiples available in 'Place your acca' section
        EXPECTED: 
        """
        pass
