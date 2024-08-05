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
class Test_C2855962_Verify_the_Smart_Boost_market_on_EDP(Common):
    """
    TR_ID: C2855962
    NAME: Verify the 'Smart Boost' market on EDP
    DESCRIPTION: This test case verifies the  'Smart Boost' market on EDP and its content
    PRECONDITIONS: 1. User is on <Race> EDP
    PRECONDITIONS: 2. 'Smart Boost' market is created for the event and has flags 'Price Boost'/'Super Smart Boost' in Open Bet TI (on market level)
    PRECONDITIONS: 3. 'Smart Boost' market contains 1 selection with price change (indicated previous price) within type
    PRECONDITIONS: 4. Selection contains 'Was price' value in its name in brackets in Open Bet TI  (in decimal format)
    """
    keep_browser_open = True

    def test_001_verify_the_market_presence_on_edp(self):
        """
        DESCRIPTION: Verify the market presence on EDP
        EXPECTED: 'Smart Boost' market is present on race EDP
        """
        pass

    def test_002_verify_the_view_of_selection_with_changed_price(self):
        """
        DESCRIPTION: Verify the view of selection with changed price
        EXPECTED: * Selection name is displayed on the left
        EXPECTED: * Price odds button is displayed opposite to the selection name (on the right)
        EXPECTED: * Previous price ('was price') of selection is placed under price odds button (on the right)
        """
        pass

    def test_003_switch_to_fractional_format_top_right_menu__settings__odds_format(self):
        """
        DESCRIPTION: Switch to fractional format (top right menu-> Settings-> odds format)
        EXPECTED: Selection previous price remains crossed out and displayed under odd price button
        """
        pass
