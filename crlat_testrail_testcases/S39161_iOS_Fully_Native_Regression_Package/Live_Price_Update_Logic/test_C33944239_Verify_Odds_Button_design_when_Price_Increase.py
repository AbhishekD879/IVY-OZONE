import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C33944239_Verify_Odds_Button_design_when_Price_Increase(Common):
    """
    TR_ID: C33944239
    NAME: Verify Odds Button design when Price Increase
    DESCRIPTION: This test case verifies change Odds Button design when Event selection Price Increase.
    DESCRIPTION: Available card for testing:
    DESCRIPTION: * surfaceBet,
    DESCRIPTION: * outrights,
    DESCRIPTION: * highlights,
    DESCRIPTION: * horseRacing,
    DESCRIPTION: * events (ThreeOdds and TwoOdds).
    PRECONDITIONS: * App is installed and launched
    PRECONDITIONS: * Card in opened
    PRECONDITIONS: * Event has selection(s)
    PRECONDITIONS: Scope:
    PRECONDITIONS: * All Live Prices on Application, for all modules & sports
    PRECONDITIONS: * Odds Button UI
    PRECONDITIONS: Design: https://app.zeplin.io/project/5d7764168919b56be93722fb/screen/5d8a25be6dff5665631beae0
    """
    keep_browser_open = True

    def test_001__increase_event_selection_price_in_ti_back_office_observe_the_changes_on_event_card_in_the_app(self):
        """
        DESCRIPTION: * Increase Event selection Price in TI (back office)
        DESCRIPTION: * Observe the changes on Event card in the app
        EXPECTED: * Event selection Price is increased
        EXPECTED: * Animation duration should be 2000 ms
        EXPECTED: * UI Price is changed according to design:
        EXPECTED: * Expected for Normal Price Button:
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/10667814)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/10806594)
        EXPECTED: * Expected for Price Up for Selected Price Button: The price color changes according to design for 2000ms and then becomes white for Selected Price Button
        """
        pass
