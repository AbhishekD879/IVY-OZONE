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
class Test_C34126551_Verify_Price_updates(Common):
    """
    TR_ID: C34126551
    NAME: Verify Price updates
    DESCRIPTION: This test case verifies change price value on Odds Button after Event selection Price is Increased/Decreased
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
    """
    keep_browser_open = True

    def test_001__change_event_selection_price_do_not_refresh_page(self):
        """
        DESCRIPTION: * Change Event selection Price (do NOT refresh page)
        EXPECTED: * Odds price value is increased/decreased immediately
        EXPECTED: * Odds price value is changed across the whole app and modules
        """
        pass
