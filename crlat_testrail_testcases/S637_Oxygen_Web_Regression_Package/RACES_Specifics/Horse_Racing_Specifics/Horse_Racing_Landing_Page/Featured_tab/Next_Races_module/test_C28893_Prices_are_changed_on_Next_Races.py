import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C28893_Prices_are_changed_on_Next_Races(Common):
    """
    TR_ID: C28893
    NAME: Prices are changed on 'Next  Races'
    DESCRIPTION: This test case verifies prices changes on 'Next Races' module on <Race> Landing page
    PRECONDITIONS: 'Next  Races' module is present on <Race> Landing page
    PRECONDITIONS: There is <Race> event with LP prices in 'Next Races' module
    PRECONDITIONS: **Updates are received in push notifications**
    """
    keep_browser_open = True

    def test_001_navigate_to_next_races_module(self):
        """
        DESCRIPTION: Navigate to 'Next Races' module
        EXPECTED: 
        """
        pass

    def test_002_trigger_price_change_for_win_or_each_way_market_outcome_for_the_event_from_next_races(self):
        """
        DESCRIPTION: Trigger price change for 'Win or Each Way' market outcome for the event from 'Next Races'
        EXPECTED: * Corresponding 'Price/Odds' button immediately displays new price and for a few seconds it changes its colour to:
        EXPECTED: blue colour if price has decreased
        EXPECTED: red colour if price has increased
        EXPECTED: * Previous Odds under Price/Odds button are updated/added respectively
        """
        pass
