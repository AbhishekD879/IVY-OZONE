import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C14253863_Event_hub_Verify_module_created_by_Race_Win_or_Each_Way_market(Common):
    """
    TR_ID: C14253863
    NAME: Event hub: Verify module created by <Race> Win or Each Way market
    DESCRIPTION: This test case verifies Featured events module created by <Race> Win or Each Way market on Event Hub
    PRECONDITIONS: 1. CMS, TI:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: 2. <Race> event created in TI
    PRECONDITIONS: 3. Event Hub is created and configured to be displayed on FE in CMS > Sport Pages > Event Hub
    PRECONDITIONS: 4. Featured module by Market Id (Win Or Each Way) is created in CMS > Sport Pages > Event Hub > %Specific event hub% > Featured events
    PRECONDITIONS: 5. User is on Homepage > Event Hub tab
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
        EXPECTED: - Watch icon (if available)
        """
        pass

    def test_003_verify_list_of_runners(self):
        """
        DESCRIPTION: Verify List of runners
        EXPECTED: * Number of runners displayed corresponds to number of selections set in CMS
        EXPECTED: * Price buttons displayed near each selection with price set in TI
        """
        pass

    def test_004_verify_the_bottom_of_the_module(self):
        """
        DESCRIPTION: Verify the bottom of the module
        EXPECTED: * There is no 'See all' button displayed at the bottom of the page for the *<Race> Win or Each Way market* module
        EXPECTED: (After redesign 'See all' selection button has been removed)
        EXPECTED: * Number of selections that are shown equals to *Number of Selections to Display* value in module configuration in CMS
        """
        pass
