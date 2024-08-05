import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C29391_Featured_Price_is_Changed_for_One_Sport_Boosted_Selection(Common):
    """
    TR_ID: C29391
    NAME: Featured: Price is Changed for One Sport Boosted Selection
    DESCRIPTION: This test case verifies price change for one Sport Boosted selection.
    DESCRIPTION: AUTOTEST [C2854886]
    DESCRIPTION: AUTOTEST [C2855504]
    PRECONDITIONS: 1. Featured Module by <Sport> Selection ID is created in CMS
    PRECONDITIONS: 2. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 3. User is on Homepage > Featured tab
    """
    keep_browser_open = True

    def test_001_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        EXPECTED: 
        """
        pass

    def test_002_trigger_price_change_for_an_outcome_in_this_module(self):
        """
        DESCRIPTION: Trigger price change for an outcome in this module
        EXPECTED: The 'Price/Odds' button is displayed new price immediately and it change its color to:
        EXPECTED: *   blue color if a price has decreased
        EXPECTED: *   pink color if a price has increased
        """
        pass

    def test_003_collapseevent_section(self):
        """
        DESCRIPTION: Collapse event section
        EXPECTED: 
        """
        pass

    def test_004_trigger_price_change_for_an_outcome_in_this_module(self):
        """
        DESCRIPTION: Trigger price change for an outcome in this module
        EXPECTED: 
        """
        pass

    def test_005_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        EXPECTED: The 'Price/Odds' button is displayed new price without highlighting in any color
        """
        pass
