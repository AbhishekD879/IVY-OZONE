import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C58424381_Verify_animation_during_expanding_collapsing_the_bet_slip(Common):
    """
    TR_ID: C58424381
    NAME: Verify animation during expanding/collapsing the bet slip
    DESCRIPTION: This test case verifies animation during expanding/collapsing the bet slip
    PRECONDITIONS: - Application is installed and launched
    PRECONDITIONS: - One selection is added to the Betslip
    """
    keep_browser_open = True

    def test_001_expand_collapse_the_bet_slip(self):
        """
        DESCRIPTION: Expand /collapse the bet slip
        EXPECTED: The relevant animation is applied during the transition as per designs:
        EXPECTED: Ladbrokes:
        EXPECTED: https://coralracing.sharepoint.com/sites/NATIVEPROJECTDELIVERY/Shared%20Documents/General/03-Betslip%20Optimisation/Ladbrokes/03-Prototypes/betslip-makingselections.mp4
        """
        pass
