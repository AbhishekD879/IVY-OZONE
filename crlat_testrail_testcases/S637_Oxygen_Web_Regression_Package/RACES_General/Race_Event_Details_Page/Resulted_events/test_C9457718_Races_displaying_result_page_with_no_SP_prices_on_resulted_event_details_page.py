import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C9457718_Races_displaying_result_page_with_no_SP_prices_on_resulted_event_details_page(Common):
    """
    TR_ID: C9457718
    NAME: <Races>: displaying result page with no SP prices on resulted event details page
    DESCRIPTION: This test case verifies displaying of result page when there are no SP prices received
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have 2 resulted <Race> events:
    PRECONDITIONS: 1) With only LP price type enabled
    PRECONDITIONS: 2) With only SP price type enabled, but not provided SP rices during resulting
    PRECONDITIONS: - You should be on result details page of the event with LP price type
    PRECONDITIONS: NOTE: Horse Racing and Greyhounds should be verified separately
    """
    keep_browser_open = True

    def test_001_verify_race_result_section(self):
        """
        DESCRIPTION: Verify "Race Result" section
        EXPECTED: "Race Result" section includes all placed runners/greyhounds and prices are not displayed
        """
        pass

    def test_002_go_to_the_event_details_page_with_sp_price_type_and_verify_race_result_section(self):
        """
        DESCRIPTION: Go to the event details page with SP price type and verify "Race Result" section
        EXPECTED: "Race Result" section includes all placed runners/greyhounds and prices are not displayed
        """
        pass
