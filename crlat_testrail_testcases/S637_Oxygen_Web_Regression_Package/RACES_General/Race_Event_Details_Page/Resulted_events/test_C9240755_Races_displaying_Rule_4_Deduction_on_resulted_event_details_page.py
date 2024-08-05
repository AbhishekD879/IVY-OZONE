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
class Test_C9240755_Races_displaying_Rule_4_Deduction_on_resulted_event_details_page(Common):
    """
    TR_ID: C9240755
    NAME: <Races>: displaying Rule 4 Deduction on resulted event details page
    DESCRIPTION: This test case verifies displaying of Rule 4 Deduction
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have 4 resulted <Race> events:
    PRECONDITIONS: 1) With couple Rules 4 Deduction configured and with non runners
    PRECONDITIONS: 2) With Rule 4 Deduction configured and without non runners
    PRECONDITIONS: 3) Without Rule 4 Deduction configured and with non runners
    PRECONDITIONS: 4) Without Rule 4 Deduction configured and without non runners
    PRECONDITIONS: - You should be on a <Race> details page with Rule 4 Deduction and with non runners
    PRECONDITIONS: NOTE: Horse Racing and Greyhounds should be verified separately
    """
    keep_browser_open = True

    def test_001_verify_deductions_section(self):
        """
        DESCRIPTION: Verify "Deductions" section
        EXPECTED: For Horse racing and Greyhounds:
        EXPECTED: - "DEDUCTION" section is displayed with the most recent Rule 4
        EXPECTED: - "NON RUNNERS" section is displayed
        EXPECTED: UI elements:
        EXPECTED: - Section name is "DEDUCTION" displayed in bold
        EXPECTED: - Deduction name is "Rule 4" displayed in bold
        EXPECTED: - Deduction value (e.g. "10p") is right aligned
        """
        pass

    def test_002_go_to_race_details_page_with_rule_4_deduction_configured_and_without_non_runners(self):
        """
        DESCRIPTION: Go to <Race> details page with Rule 4 Deduction configured and without non runners
        EXPECTED: For Horse racing and Greyhounds:
        EXPECTED: - "DEDUCTION" section is not displayed
        EXPECTED: - "NON RUNNERS" section is not displayed
        """
        pass

    def test_003_go_to_race_details_page_without_rule_4_deduction_configured_and_with_non_runners(self):
        """
        DESCRIPTION: Go to <Race> details page without Rule 4 Deduction configured and with non runners
        EXPECTED: For Horse racing and Greyhounds:
        EXPECTED: - "DEDUCTION" section is not displayed
        EXPECTED: - "NON RUNNERS" section is displayed
        """
        pass

    def test_004_go_to_race_details_page_without_rule_4_deduction_configured_and_without_non_runners(self):
        """
        DESCRIPTION: Go to <Race> details page without Rule 4 Deduction configured and without non runners
        EXPECTED: For Horse racing and Greyhounds:
        EXPECTED: - "DEDUCTION" section is not displayed
        EXPECTED: - "NON RUNNERS" section is not displayed
        """
        pass
