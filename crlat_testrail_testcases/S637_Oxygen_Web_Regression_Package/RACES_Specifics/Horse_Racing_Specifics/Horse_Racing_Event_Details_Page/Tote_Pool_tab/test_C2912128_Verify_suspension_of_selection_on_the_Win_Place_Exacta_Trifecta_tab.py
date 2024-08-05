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
class Test_C2912128_Verify_suspension_of_selection_on_the_Win_Place_Exacta_Trifecta_tab(Common):
    """
    TR_ID: C2912128
    NAME: Verify suspension of selection on the Win/Place/Exacta /Trifecta tab
    DESCRIPTION: This test case verifies suspension of selection on Win/Place/Exacta/Trifecta tab
    PRECONDITIONS: **Instruction on Tote events mapping on test environment**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+International+Tote+events+with+Regular+Horse+Racing+events
    PRECONDITIONS: **Request on EDP:** PoolForEvent/ {event_id} ?&translationLang=en
    PRECONDITIONS: International Tote Races with tote pool are available
    PRECONDITIONS: **User is on Int Horse Race EDP and Win/Place/Exacta/Trifecta pool is selected**
    """
    keep_browser_open = True

    def test_001_suspend_horse_race_event_inti(self):
        """
        DESCRIPTION: Suspend horse race event inTI
        EXPECTED: - Selection should suspended and be displayed as greyed Out (in real time)
        EXPECTED: - Checkbox for that suspended selection is NOT clickable
        """
        pass

    def test_002_unsuspend_horse_race_event_inti(self):
        """
        DESCRIPTION: Unsuspend horse race event inTI
        EXPECTED: - Selection should unsuspended (in real time)
        EXPECTED: - Checkbox for that unsuspended selection is clickable
        """
        pass

    def test_003_suspend_selection_in_ti_for_tote_event(self):
        """
        DESCRIPTION: Suspend selection in TI for tote event
        EXPECTED: - Selection should suspended and be displayed as greyed Out (with page refresh)
        EXPECTED: - Checkbox for that suspended selection is NOT clickable
        """
        pass

    def test_004_unsuspend_selection_in_ti_for_tote_event(self):
        """
        DESCRIPTION: Unsuspend selection in TI for tote event
        EXPECTED: - Selection should unsuspended (with page refresh)
        EXPECTED: - Checkbox for that unsuspended selection is clickable
        """
        pass
