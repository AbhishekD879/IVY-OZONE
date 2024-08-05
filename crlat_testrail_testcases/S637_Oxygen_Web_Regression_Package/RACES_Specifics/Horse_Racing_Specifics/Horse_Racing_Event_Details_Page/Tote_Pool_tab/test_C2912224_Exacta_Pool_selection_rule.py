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
class Test_C2912224_Exacta_Pool_selection_rule(Common):
    """
    TR_ID: C2912224
    NAME: Exacta Pool selection rule
    DESCRIPTION: Test case verifies exacta pool selection rule for the 1st and 2nd place
    PRECONDITIONS: **Instruction on Tote events mapping on test environment**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+International+Tote+events+with+Regular+Horse+Racing+events
    PRECONDITIONS: **CMS configuration**
    PRECONDITIONS: System configuration > Structure: InternationalTotePool is enabled
    PRECONDITIONS: **International Tote Event Race card is opened and Exacta pool is selected**
    """
    keep_browser_open = True

    def test_001_select_1st_place_for_one_of_the_runners(self):
        """
        DESCRIPTION: Select 1st place for one of the runners
        EXPECTED: - 1st place is selected
        EXPECTED: - 2nd place is disabled for the same runner
        EXPECTED: - 1st place is disabled for all other runners
        EXPECTED: - "Any" is disabled for all runners
        EXPECTED: - Message "Please add another selection"
        EXPECTED: - ADD TO BETSLIP button is disabled
        """
        pass

    def test_002_select_2nd_place_for_different_runner(self):
        """
        DESCRIPTION: Select 2nd place for different runner
        EXPECTED: - Message "Please add another selection" disappears
        EXPECTED: - ADD TO BETSLIP button is enabled
        """
        pass

    def test_003_verify_text_in_the_footer(self):
        """
        DESCRIPTION: Verify text in the footer
        EXPECTED: "One exacta bet" text is displayed
        """
        pass
