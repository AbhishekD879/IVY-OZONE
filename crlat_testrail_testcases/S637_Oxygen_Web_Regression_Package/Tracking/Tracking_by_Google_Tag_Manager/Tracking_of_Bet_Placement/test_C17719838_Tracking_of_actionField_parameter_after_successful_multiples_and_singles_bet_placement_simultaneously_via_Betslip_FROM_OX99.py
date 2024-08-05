import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C17719838_Tracking_of_actionField_parameter_after_successful_multiples_and_singles_bet_placement_simultaneously_via_Betslip_FROM_OX99(Common):
    """
    TR_ID: C17719838
    NAME: Tracking of  'actionField' parameter after successful multiples and singles bet placement simultaneously via Betslip [FROM OX99]
    DESCRIPTION: This test case verifies GA tracking of 'actionField' parameter after successful multiples and singles bet placement simultaneously via Betslip
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Betslip GA tracking documentation: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91091847
    PRECONDITIONS: - Quick bet should be disabled in CMS > System Configuration > Structure > quickBet
    PRECONDITIONS: - You should be logged in
    """
    keep_browser_open = True

    def test_001_add_the_selections_to_the_betslip_from_different_events(self):
        """
        DESCRIPTION: Add the selections to the Betslip from different events
        EXPECTED: - Selections are added to the Betslip
        """
        pass

    def test_002___make_a_stake_for_multiples_and_several_singles_simultaneously_eg_3_singles_and_treble__tap_bet_now__type_datalayer_in_browsers_console_and_verify_actionfield_parameter_in_ga_tracking_record(self):
        """
        DESCRIPTION: - Make a stake for multiples and several singles simultaneously (e.g. 3 singles and Treble)
        DESCRIPTION: - Tap 'BET NOW'
        DESCRIPTION: - Type 'dataLayer' in browser's console and verify 'actionField' parameter in GA tracking record
        EXPECTED: - 'actionField' parameter is present
        EXPECTED: - 'actionField' contains the minimum (smallest) receipt number then number of bets (e.g lowest Receipt ID: Number of Bets)
        """
        pass
