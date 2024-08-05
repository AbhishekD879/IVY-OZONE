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
class Test_C58836075_Verify_swapping_logic_of_Non_runner_and_Reserved_Greyhound(Common):
    """
    TR_ID: C58836075
    NAME: Verify swapping logic of Non-runner and Reserved Greyhound
    DESCRIPTION: Verify swapping logic of Non-runner and Reserved Greyhound (reserved dogs take place of non runners)
    PRECONDITIONS: Make sure you have events with Non-Runners selections:
    PRECONDITIONS: 'Non-Runners' is a selection which contains ** N/R ** text next to its name
    PRECONDITIONS: For those selections 'outcomeStatusCode'='S' - those selections are always suspended.
    PRECONDITIONS: Make sure you have Reserved dog selection:
    PRECONDITIONS: 'Reserved' dog is a selection which contains ** (RES) ** text to its name.
    PRECONDITIONS: This works for all Greyhounds, USA UK/IRE, Australia.
    """
    keep_browser_open = True

    def test_001_verify_logic_within_greyhound_event(self):
        """
        DESCRIPTION: Verify logic within Greyhound event
        EXPECTED: From preconditions please mark Runner 1(with runnerNumber - 1) with N/R (Non-runner) next to its name in TI.
        EXPECTED: Mark other runner for example Runner 9(with runnerNumber - 9) with (RES) next to its name, also change its DispOrder to  1(this means that he changes Runner 1 N/R place.
        """
        pass

    def test_002_verify_the_result_of_the_change(self):
        """
        DESCRIPTION: Verify the result of the change
        EXPECTED: Runner 1 should be displayed above the Unnamed Favourite selections, and it should be Suspended (price).
        EXPECTED: Runner 9 should be on the place of Runner 1 with RES text next to him.
        """
        pass

    def test_003_verify_correctness_of_silks_change_after_the_runners_swapping(self):
        """
        DESCRIPTION: Verify correctness of Silks change after the runners swapping
        EXPECTED: Silks should be swapped for Runner 1 and Runner 9.
        """
        pass
