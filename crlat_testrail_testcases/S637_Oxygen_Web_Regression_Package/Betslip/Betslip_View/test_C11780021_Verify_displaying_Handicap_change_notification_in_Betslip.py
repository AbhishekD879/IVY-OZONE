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
class Test_C11780021_Verify_displaying_Handicap_change_notification_in_Betslip(Common):
    """
    TR_ID: C11780021
    NAME: Verify displaying Handicap change notification in Betslip
    DESCRIPTION: This test case verifies displaying Handicap change notification where user has entered a stake
    PRECONDITIONS: Login into app
    PRECONDITIONS: Add selection with handicap value to the Betslip
    """
    keep_browser_open = True

    def test_001_change_handicap_value_of_selection(self):
        """
        DESCRIPTION: Change handicap value of selection
        EXPECTED: *Info message is displayed at the bottom of the betslip
        EXPECTED: text: 'Handicap changed from 'x' to 'y''
        EXPECTED: * Info message is displayed at the top of the betslip with animations and is removed after 5 seconds
        """
        pass

    def test_002_verify_that_place_bet_button_text_is_updated(self):
        """
        DESCRIPTION: Verify that 'Place bet' button text is updated
        EXPECTED: Place bet button text is updated to:
        EXPECTED: Ladbrokes: 'ACCEPT & PLACE BET'
        EXPECTED: Coral: 'ACCEPT & PLACE BET'
        """
        pass
