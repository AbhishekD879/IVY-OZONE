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
class Test_C59987930_Verify_expanded_Betslip_with_multiple_selections(Common):
    """
    TR_ID: C59987930
    NAME: Verify expanded Betslip with multiple selections
    DESCRIPTION: Test case verifies displaying Betslip with multiple selections (Bottom Bar Behaviour)
    PRECONDITIONS: App is installed and launched
    PRECONDITIONS: Design
    PRECONDITIONS: https://zpl.io/blkQB8G - Ladbrokes
    PRECONDITIONS: https://zpl.io/bWmlDxj - Coral
    """
    keep_browser_open = True

    def test_001__add_4_different_selections_to_betslip(self):
        """
        DESCRIPTION: * Add 4 different selections to Betslip
        EXPECTED: * Selected selections were successfully added to Betslip
        EXPECTED: * Betslip displays in collapsed state
        EXPECTED: * Betslip displays under bottom bar
        EXPECTED: * Bottom bar is not overlapped by Betslip
        """
        pass

    def test_002__swipe_up_to_expand_betslip(self):
        """
        DESCRIPTION: * Swipe up to expand Betslip
        EXPECTED: * Betslip was expanded with added selections
        EXPECTED: * Expanded Betslip correctly display information about each selection
        EXPECTED: * Betslip displays under bottom bar
        EXPECTED: * Bottom bar is not overlapped by Betslip
        EXPECTED: * Header is visible and not overlapped by Betslip
        """
        pass

    def test_003__remove_1_selection_from_betslip(self):
        """
        DESCRIPTION: * Remove 1 selection from Betslip
        EXPECTED: * Selection was successfully deleted from Betslip
        EXPECTED: * Betslip counter correctly updated with actual amount of selections
        EXPECTED: * Betslip displays in expanded state
        EXPECTED: * Betslip displays under bottom bar
        EXPECTED: * Bottom bar is not overlapped by Betslip
        EXPECTED: * Header is visible and not overlapped by Betslip
        """
        pass

    def test_004__swipe_down_to_collapse_betslip(self):
        """
        DESCRIPTION: * Swipe down to collapse Betslip
        EXPECTED: * Betslip collapsed
        """
        pass

    def test_005__add_4_new_selections_to_betslip(self):
        """
        DESCRIPTION: * Add 4 new selections to Betslip
        EXPECTED: * Betslip collapsed
        EXPECTED: * New 4 selections were successfully added to betslip
        EXPECTED: * Betslip counter correctly updated with actual amount of selections
        """
        pass

    def test_006__expand_betslip(self):
        """
        DESCRIPTION: * Expand Betslip
        EXPECTED: * Betslip displays in expanded state
        EXPECTED: * Header is visible and not overlapped by Betslip
        EXPECTED: * Betslip displays under bottom bar
        EXPECTED: * Bottom bar is not overlapped by Betslip
        EXPECTED: * Expanded Betslip correctly display information about each selection
        """
        pass

    def test_007__scroll_betslip_up_and_down_to_display_all_selections(self):
        """
        DESCRIPTION: * Scroll Betslip up and down to display all selections
        EXPECTED: * All selections correctly display during Betslip scrolling
        EXPECTED: * Header is visible and not overlapped by Betslip
        EXPECTED: * Betslip displays under bottom bar
        EXPECTED: * Bottom bar is not overlapped by Betslip
        """
        pass

    def test_008__tap_on_inplay_item_on_bottom_bar(self):
        """
        DESCRIPTION: * Tap on 'InPlay' item on bottom bar
        EXPECTED: * Betslip collapsed
        EXPECTED: * User is directed to 'InPlay'
        EXPECTED: * Betslip displays under bottom bar
        EXPECTED: * Bottom bar is not overlapped by Betslip
        EXPECTED: * Header is visible and not overlapped by Betslip
        """
        pass
