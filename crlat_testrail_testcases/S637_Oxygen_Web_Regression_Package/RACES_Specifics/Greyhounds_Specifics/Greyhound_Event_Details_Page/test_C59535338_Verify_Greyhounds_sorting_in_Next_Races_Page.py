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
class Test_C59535338_Verify_Greyhounds_sorting_in_Next_Races_Page(Common):
    """
    TR_ID: C59535338
    NAME: Verify Greyhounds sorting in Next Races Page
    DESCRIPTION: This test case verifies Greyhounds sorting  in Next Races Page
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User is at Greyhound Race Card (Event Details page)
    """
    keep_browser_open = True

    def test_001_set_up_greyhounds_to_be_displayed_in_the_next_races_module_on_the_greyhound_landing_page(self):
        """
        DESCRIPTION: Set up Greyhounds to be displayed in the next races module on the greyhound landing page
        EXPECTED: Greyhounds configured in the next races module on the greyhound landing page
        """
        pass

    def test_002_check_greyhounds_selections_order_in_next_races_module(self):
        """
        DESCRIPTION: Check Greyhounds selections order in next races module
        EXPECTED: Selections should be shown in numerical order unless  until there is a price available
        """
        pass
