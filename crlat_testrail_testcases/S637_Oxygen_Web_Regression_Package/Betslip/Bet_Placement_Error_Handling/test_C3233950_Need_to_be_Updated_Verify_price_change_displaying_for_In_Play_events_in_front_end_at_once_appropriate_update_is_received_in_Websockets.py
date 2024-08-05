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
class Test_C3233950_Need_to_be_Updated_Verify_price_change_displaying_for_In_Play_events_in_front_end_at_once_appropriate_update_is_received_in_Websockets(Common):
    """
    TR_ID: C3233950
    NAME: [Need to be Updated] Verify price change displaying for In-Play events in front-end at once appropriate update is received in Websockets
    DESCRIPTION: This test case verifies price change displaying for Multiples in front-end at once appropriate update is received in Websockets
    DESCRIPTION: Based on Release OX 95.8 issues analysis
    DESCRIPTION: AUTOTEST: [C9698618]
    PRECONDITIONS: 1. User is logged in to application and has positive balance
    PRECONDITIONS: 2. In-Play sport events are available in application
    PRECONDITIONS: **NOTE** Regarding BMA-36865:
    PRECONDITIONS: Ladbrokes design https://app.zeplin.io/project/5c01259e7c06af027fe0065a/screen/5c094b54a424142fbf0847d2
    PRECONDITIONS: Coral Design https://app.zeplin.io/project/5b801d678d472e7c23e481fa/screen/5bc5bcaec5588f18fa351734
    PRECONDITIONS: Step 1 - 'Place your Acca' is NOT displayed
    PRECONDITIONS: Step 2 - Previous odds don't become crossed out, 'Clear Betslip' button is not exist anymore
    """
    keep_browser_open = True

    def test_001_open_in_play_page_and_add_at_least_3_selections_from_different_sport_events(self):
        """
        DESCRIPTION: Open in-play page and add at least 3 selections from different sport events
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
        EXPECTED: **[Not actual from OX 99]**
        EXPECTED: 2. Notification banner appears above Betslip footer section on the yellow background: "Please beware that <number of bets with changed price> of your selections had a price change."
        EXPECTED: 'Bet Now' button is changed to 'Accept & Bet (<number of selections with price change>)'
        EXPECTED: 'Clear Betslip' and 'Accept & Bet (<number of selections with price change>)' buttons are enabled
        EXPECTED: **[Actual from OX 99]** (according to BMA-36865)
        EXPECTED: 2. info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: The Place bet button text is updated to 'ACCEPT & PLACE BET'
        EXPECTED: 'Clear Betslip' and 'ACCEPT & PLACE BET' buttons are enabled
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
