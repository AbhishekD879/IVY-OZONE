import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C9770808_Verify_Surface_Bet_module_displaying_on_a_few_Event_Details_Pages(Common):
    """
    TR_ID: C9770808
    NAME: Verify Surface Bet module displaying on a few Event Details Pages
    DESCRIPTION: Test case verifies possibility to add a Surface Bet to a few Event Details Pages
    PRECONDITIONS: 1. There is a single Surface Bet added to a few Event Details pages (EDP).
    PRECONDITIONS: 2. Valid Selection Id is set
    PRECONDITIONS: 3. Open those EDPs in Oxygen application.
    PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_verify_the_surface_bet_is_shown_on_the_all_edps_its_added_to(self):
        """
        DESCRIPTION: Verify the Surface Bet is shown on the all EDPs it's added to
        EXPECTED: Surface bet is shown on the all EDPs
        """
        pass
