import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C9770810_Verify_Surface_Bet_module_displaying_on_the_Racing_Card(Common):
    """
    TR_ID: C9770810
    NAME: Verify Surface Bet module displaying on the Racing Card
    DESCRIPTION: Test case verifies that Surface Bet isn't shown on the Racing card
    PRECONDITIONS: 1. There is a single Surface Bet added to the racing event (Horse/Greyhound racing)
    PRECONDITIONS: 2. Valid Selection Id is set
    PRECONDITIONS: 3. Open this event's racing card
    """
    keep_browser_open = True

    def test_001_verify_the_surface_bet_isnt_displayed_on_the_racing_cards(self):
        """
        DESCRIPTION: Verify the Surface Bet isn't displayed on the Racing cards
        EXPECTED: Surface Bet isn't shown
        """
        pass
