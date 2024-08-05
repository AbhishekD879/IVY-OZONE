import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C2855551_Verify_Smart_Boost_market_on_sports_EDP(Common):
    """
    TR_ID: C2855551
    NAME: Verify 'Smart Boost' market on sports EDP
    DESCRIPTION: This test case verifies Smart Boost market and boosted selection on sports EDP
    PRECONDITIONS: 1. User is on <Sport> EDP, 'All Markets' tab
    PRECONDITIONS: 2. Smart Boost market is created for the event and has flags 'Price Boost'/'Super Smart Boost' in Open Bet TI (on market level)
    PRECONDITIONS: 3. Selection contains 'Was price' value in its name in brackets in Open Bet TI  (in decimal format)
    """
    keep_browser_open = True

    def test_001_verify_the_market_presence_on_edp(self):
        """
        DESCRIPTION: Verify the market presence on EDP
        EXPECTED: 'Smart Boost' market is present on EDP
        """
        pass

    def test_002_verify_the_view_of_selection_with_changed_price(self):
        """
        DESCRIPTION: Verify the view of selection with changed price
        EXPECTED: * Selection name is displayed on the left
        EXPECTED: * Price odds button is displayed opposite to the selection name (on the right)
        EXPECTED: * Previous price ('was price') of selection is placed under price odds button (on the right)
        EXPECTED: * Start time/date of event is located on match card (at the top of EDP)
        """
        pass

    def test_003_switch_to_fractional_format_top_right_menu_gt_settings_gt_odds_format(self):
        """
        DESCRIPTION: Switch to fractional format (top right menu-&gt; Settings-&gt; odds format)
        EXPECTED: Selection previous price remains crossed out and displayed under odd price button
        """
        pass
