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
class Test_C650618_Cash_Out_icon(Common):
    """
    TR_ID: C650618
    NAME: 'Cash Out' icon
    DESCRIPTION: This test case verifies 'Cash Out' icon displaying for market with available cash out
    PRECONDITIONS: * Oxygen application is loaded
    PRECONDITIONS: * There are <Race> events with **cashoutAvail="Y"** attribute on Market level
    """
    keep_browser_open = True

    def test_001_navigate_to_event_details_page_of_event_with_cashoutavaily_attribute_on_market_level(self):
        """
        DESCRIPTION: Navigate to Event details page of event with **cashoutAvail="Y"** attribute on Market level
        EXPECTED: 'CASH OUT' icon is displayed in the same line as the Each-way terms from the right side (next to BPG icon if available)
        """
        pass
