import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C64055818_GALAXY_S9_Featured_Module_by_Sport_TypeID__Price_Change(Common):
    """
    TR_ID: C64055818
    NAME: [GALAXY S9] Featured Module by Sport TypeID - Price Change
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001___________create_event_and_add_to_the_featured_tab(self):
        """
        DESCRIPTION: *          create event and add to the featured tab
        EXPECTED: *
        """
        pass

    def test_002___________expand_module_from_preconditions(self):
        """
        DESCRIPTION: *          Expand module from Preconditions
        EXPECTED: *
        """
        pass

    def test_003___________trigger_price_change_for_one_outcome(self):
        """
        DESCRIPTION: *          Trigger price change for one outcome
        EXPECTED: *          The 'Price/Odds' button is displayed new price immediately and it changes its color to:
        EXPECTED: *          *   blue color if a price has decreased
        EXPECTED: *          *   pink color if a price has increased
        EXPECTED: *          Other buttons are not changed if they are available
        """
        pass

    def test_004___________collapse_module_from_preconditions(self):
        """
        DESCRIPTION: *          Collapse module from Preconditions
        EXPECTED: *
        """
        pass

    def test_005___________trigger_price_change_for_one_outcome(self):
        """
        DESCRIPTION: *          Trigger price change for one outcome
        EXPECTED: *
        """
        pass

    def test_006___________expand_module_from_preconditions(self):
        """
        DESCRIPTION: *          Expand module from Preconditions
        EXPECTED: *          Price / Odds button displays new prices without any highlighting
        """
        pass

    def test_007___________trigger_price_change_for_a_few_outcomes_from_the_same_market(self):
        """
        DESCRIPTION: *          Trigger price change for a few outcomes from the same market
        EXPECTED: *          All 'Price/Odds' buttons display new price immediately and it changes its color to:
        EXPECTED: *          *   blue color if a price has decreased
        EXPECTED: *          *   pink color if a price has increased
        """
        pass