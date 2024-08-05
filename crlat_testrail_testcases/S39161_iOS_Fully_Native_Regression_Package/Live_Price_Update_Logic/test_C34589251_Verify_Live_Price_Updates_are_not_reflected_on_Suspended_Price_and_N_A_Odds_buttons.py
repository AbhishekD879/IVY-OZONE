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
class Test_C34589251_Verify_Live_Price_Updates_are_not_reflected_on_Suspended_Price_and_N_A_Odds_buttons(Common):
    """
    TR_ID: C34589251
    NAME: Verify Live Price Updates are not reflected on Suspended Price and N/A Odds buttons
    DESCRIPTION: This test case verifies Live Price Updates are not reflected on Suspended Price and N/A Odds buttons
    DESCRIPTION: Available card for testing:
    DESCRIPTION: * surfaceBet,
    DESCRIPTION: * outrights,
    DESCRIPTION: * highlights,
    DESCRIPTION: * horseRacing,
    DESCRIPTION: * events (ThreeOdds and TwoOdds).
    PRECONDITIONS: * App is installed and launched
    PRECONDITIONS: * Card in opened
    PRECONDITIONS: * Event has Suspended and N/A selection(s)
    PRECONDITIONS: Scope:
    PRECONDITIONS: * All Live Prices on Application, for all modules & sports
    PRECONDITIONS: * Odds Button UI
    """
    keep_browser_open = True

    def test_001__change_event_selection_price_in_ti_back_office_observe_the_changes_on_event_card_in_the_app(self):
        """
        DESCRIPTION: * Change Event selection Price in TI (back office)
        DESCRIPTION: * Observe the changes on Event card in the app
        EXPECTED: * Live Price Updates are not reflected on Suspended Price and N/A buttons
        """
        pass
