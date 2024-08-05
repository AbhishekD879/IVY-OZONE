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
class Test_C2912228_Trifecta_Pool_Any_place_selection(Common):
    """
    TR_ID: C2912228
    NAME: Trifecta Pool "Any" place selection
    DESCRIPTION: Test case verifies Trifecta pool selection rule for "Any" place
    PRECONDITIONS: **Instruction on Tote events mapping on test environment**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+International+Tote+events+with+Regular+Horse+Racing+events
    PRECONDITIONS: **CMS configuration**
    PRECONDITIONS: System configuration > Structure: InternationalTotePool is enabled
    PRECONDITIONS: **International Tote Event Race card is opened and Trifecta pool is selected**
    """
    keep_browser_open = True

    def test_001_select_any_place_for_one_of_the_runners(self):
        """
        DESCRIPTION: Select "Any" place for one of the runners
        EXPECTED: - "Any" place is selected for the runner
        EXPECTED: - 1st, 2nd, 3rd places are disabled for all runners
        EXPECTED: - Message "Please add another selection"
        EXPECTED: - ADD TO BETSLIP button is disabled
        """
        pass

    def test_002_select_any_place_for_different_runner(self):
        """
        DESCRIPTION: Select "Any" place for different runner
        EXPECTED: - "Any" place is selected for one more runner
        EXPECTED: - Message "Please add another selection"
        EXPECTED: - ADD TO BETSLIP button is disabled
        """
        pass

    def test_003_select_any_place_for_one_more_runner(self):
        """
        DESCRIPTION: Select "Any" place for one more runner
        EXPECTED: - "Any" place is selected for one more runner
        EXPECTED: - Message "Please add another selection" disappears
        EXPECTED: - ADD TO BETSLIP button is enabled
        """
        pass

    def test_004_verify_text_in_the_footer(self):
        """
        DESCRIPTION: Verify text in the footer
        EXPECTED: "6 combination trifecta bets" is displayed in the footer
        """
        pass
