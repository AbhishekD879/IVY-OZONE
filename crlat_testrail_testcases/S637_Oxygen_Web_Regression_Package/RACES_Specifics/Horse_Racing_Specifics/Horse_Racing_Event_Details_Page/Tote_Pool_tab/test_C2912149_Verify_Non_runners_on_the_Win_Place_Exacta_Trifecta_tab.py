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
class Test_C2912149_Verify_Non_runners_on_the_Win_Place_Exacta_Trifecta_tab(Common):
    """
    TR_ID: C2912149
    NAME: Verify Non runners on the Win/Place/Exacta /Trifecta tab
    DESCRIPTION: This test case verifies Non runners on the Win/Place/Exacta/Trifecta tab
    PRECONDITIONS: **Instruction on Tote events mapping on test environment**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+International+Tote+events+with+Regular+Horse+Racing+events
    PRECONDITIONS: **Request on EDP**: PoolForEvent/ {event_id} ?&translationLang=en
    PRECONDITIONS: International Tote Races with tote pool are available
    PRECONDITIONS: **User is on Int Horse Race EDP and Win/Place/Exacta/Trifecta pool is selected**
    """
    keep_browser_open = True

    def test_001___select_any_runner__set_selected_runner_as_a_non_runner_nr_in_ti(self):
        """
        DESCRIPTION: - Select any runner
        DESCRIPTION: - Set selected runner as a non-runner (NR) in TI
        EXPECTED: - Runner is set as a non-runner (NR) and go to the bottom of the page(with page refresh)
        EXPECTED: - Selection should be deselected
        """
        pass
