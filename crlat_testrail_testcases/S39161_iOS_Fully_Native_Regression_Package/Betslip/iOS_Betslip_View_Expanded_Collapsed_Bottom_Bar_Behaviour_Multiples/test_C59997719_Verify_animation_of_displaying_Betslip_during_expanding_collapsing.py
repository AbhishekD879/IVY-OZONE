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
class Test_C59997719_Verify_animation_of_displaying_Betslip_during_expanding_collapsing(Common):
    """
    TR_ID: C59997719
    NAME: Verify animation of displaying Betslip during expanding/collapsing
    DESCRIPTION: Test case verifies animation of Betslip with multiples  during expanding/collapsing
    PRECONDITIONS: App is installed and launched
    PRECONDITIONS: Design
    PRECONDITIONS: https://zpl.io/blkQB8G - Ladbrokes
    PRECONDITIONS: https://zpl.io/bWmlDxj - Coral
    """
    keep_browser_open = True

    def test_001__add_2_selections_to_betslip(self):
        """
        DESCRIPTION: * Add 2 selections to Betslip
        EXPECTED: * 2 selections were added to Betslip
        EXPECTED: * Betslip in collapsed state
        EXPECTED: * Betslip displays under bottom bar
        """
        pass

    def test_002__swipe_up_to_expand_betslip_verify_animation_of_betslip_during_expanding(self):
        """
        DESCRIPTION: * Swipe up to expand Betslip
        DESCRIPTION: * Verify animation of Betslip during expanding
        EXPECTED: * Betslip expands with added selections
        EXPECTED: * Animation properly  displays during expanding (No UI overlaps)
        """
        pass

    def test_003__swipe_down_to_collapse_betslip(self):
        """
        DESCRIPTION: * Swipe down to collapse Betslip
        EXPECTED: * Betslip collapses with added selections
        EXPECTED: * Animation properly  displays during collapsing (No UI overlaps)
        """
        pass

    def test_004__add_6_new_selections_to_betslip(self):
        """
        DESCRIPTION: * Add 6 new selections to Betslip
        EXPECTED: * 6 selections were added to Betslip
        EXPECTED: * Betslip counter correctly updated with actual amount of selections
        EXPECTED: * Betslip in collapsed state
        EXPECTED: * Betslip displays under bottom bar
        """
        pass

    def test_005__swipe_up_to_expand_betslip_verify_animation_of_betslip_during_expanding(self):
        """
        DESCRIPTION: * Swipe up to expand Betslip
        DESCRIPTION: * Verify animation of Betslip during expanding
        EXPECTED: * Betslip expands with added selections
        EXPECTED: * Animation properly  displays during expanding (No UI overlaps)
        """
        pass

    def test_006__scroll_betslip_down(self):
        """
        DESCRIPTION: * Scroll Betslip down
        EXPECTED: * Betslip scrolled
        """
        pass

    def test_007__swipe_down_to_collapse_betslip(self):
        """
        DESCRIPTION: * Swipe down to collapse Betslip
        EXPECTED: * Betslip collapses with added selections
        EXPECTED: * Animation properly  displays during collapsing (No UI overlaps)
        """
        pass
