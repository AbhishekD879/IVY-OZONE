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
class Test_C11366885_Verify_module_created_by_Race_Win_or_Each_Way_market(Common):
    """
    TR_ID: C11366885
    NAME: Verify module created by <Race> Win or Each Way market
    DESCRIPTION: This test case verifies Featured module created by <Race> Win or Each Way market
    PRECONDITIONS: 1. CMS, TI:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: 2. <Race> event created in TI
    PRECONDITIONS: 3. Featured module by Market Id is created in CMS > Featured tab module and check "Expanded by default" check box
    PRECONDITIONS: 4. User is on Homepage > Featured tab
    """
    keep_browser_open = True

    def test_001_navigate_to_module_from_preconditions_and_verify_its_header(self):
        """
        DESCRIPTION: Navigate to Module from preconditions and verify it's header
        EXPECTED: * Module Header contains Event time and name and 'More' button.
        EXPECTED: More button navigates user to EDP
        EXPECTED: * Header CANNOT be collapsed/expanded
        """
        pass

    def test_002_verify_area_below_header(self):
        """
        DESCRIPTION: Verify area below header
        EXPECTED: * Area contains:
        EXPECTED: - Each Way terms
        EXPECTED: - Cashout icon (if available)
        EXPECTED: - Watch icon (of available)
        """
        pass

    def test_003_verify_list_of_runners(self):
        """
        DESCRIPTION: Verify List of runners
        EXPECTED: * Number of runners displayed corresponds to number of selections set in CMS
        EXPECTED: * Price buttons displayed near each selection with price set in TI
        """
        pass

    def test_004_verify_bottom_of_module(self):
        """
        DESCRIPTION: Verify bottom of module
        EXPECTED: * See All button displayed at the bottom of the page if # of selections to display set in CMS is < than # of selections available
        EXPECTED: * Clicking See All button expands module to display all selections
        """
        pass
