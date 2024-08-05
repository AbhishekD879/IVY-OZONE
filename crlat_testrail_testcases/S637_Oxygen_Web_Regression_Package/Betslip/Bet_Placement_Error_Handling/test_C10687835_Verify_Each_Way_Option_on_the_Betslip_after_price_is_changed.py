import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C10687835_Verify_Each_Way_Option_on_the_Betslip_after_price_is_changed(Common):
    """
    TR_ID: C10687835
    NAME: Verify Each Way Option on the Betslip after price is changed
    DESCRIPTION: AUTOTEST [C13828775]
    PRECONDITIONS: To disable live updates, please enter and save next string into Host file (File: /etc/hosts). Reload the app.
    PRECONDITIONS: PROD - 127.0.0.1 liveserve-publisher-prd0.coralsports.prod.cloud.ladbrokescoral.com
    PRECONDITIONS: DEV0 - 127.0.0.1 liveserve-publisher-dev0.coralsports.dev.cloud.ladbrokescoral.com
    PRECONDITIONS: TST2 - 127.0.0.1 liveserve-publisher-tst0.coralsports.nonprod.cloud.ladbrokescoral.com
    PRECONDITIONS: TI TST2 system - http://backoffice-tst2.coral.co.uk/ti
    """
    keep_browser_open = True

    def test_001_add_multiple_selections_from_different_horse_racing_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Add multiple selections (from different Horse Racing events) to the bet slip
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_the_bet_slip(self):
        """
        DESCRIPTION: Navigate to the bet slip
        EXPECTED: All selections from the previous step are present in the list
        EXPECTED: Accumulator bet is available
        """
        pass

    def test_003_change_price_for_any_event_from_the_accumulator_please_note_that_stake_should_increase_eg_from_115_to_111(self):
        """
        DESCRIPTION: Change Price for any event from the accumulator (please note that stake should increase e.g. from 11/5 to 11/1)
        EXPECTED: Live updates should not work. User can't see price updates on the UI
        """
        pass

    def test_004_check_each_way_checkbox_enter_stake_into_accumulators_field(self):
        """
        DESCRIPTION: Check 'each way' checkbox enter stake into Accumulators field
        EXPECTED: 
        """
        pass

    def test_005_tap_on_bet_now_button(self):
        """
        DESCRIPTION: Tap on Bet now button
        EXPECTED: Button changes to 'Accept & Place bet' button
        """
        pass

    def test_006_tap_on_accept__place_bet_button(self):
        """
        DESCRIPTION: Tap on 'Accept & Place bet' button
        EXPECTED: Bet should be placed successfully
        """
        pass
