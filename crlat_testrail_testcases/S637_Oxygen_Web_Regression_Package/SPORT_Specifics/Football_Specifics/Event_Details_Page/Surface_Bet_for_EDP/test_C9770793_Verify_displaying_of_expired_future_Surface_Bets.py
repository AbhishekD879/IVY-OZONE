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
class Test_C9770793_Verify_displaying_of_expired_future_Surface_Bets(Common):
    """
    TR_ID: C9770793
    NAME: Verify displaying of expired/future Surface Bets
    DESCRIPTION: Test case verifies that expired/future Surface Bet is shown on the EDP
    DESCRIPTION: AUTOTEST: [C12600639]
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the Event Details page (EDP).
    PRECONDITIONS: 2. Open this EDP
    PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_in_the_cms_edit_the_surface_bet_set_display_fromto_to_the_past(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bet: set Display From/To to the past.
        EXPECTED: 
        """
        pass

    def test_002_in_the_application_refresh_the_edp_verify_this_surface_bet_is_displayed(self):
        """
        DESCRIPTION: In the application refresh the EDP verify this Surface bet is displayed
        EXPECTED: Surface Bet is shown
        EXPECTED: _NOTE: Surface Bet is shown on the EDP regardless Display From/To settings!_
        """
        pass

    def test_003_in_the_cms_edit_the_surface_bet_set_display_fromto_to_the_future(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bet: set Display From/To to the future.
        EXPECTED: 
        """
        pass

    def test_004_in_the_application_refresh_the_edp_verify_this_surface_bet_is_displayed(self):
        """
        DESCRIPTION: In the application refresh the EDP verify this Surface bet is displayed
        EXPECTED: Surface Bet is shown
        EXPECTED: _NOTE: Surface Bet is shown on the EDP regardless Display From/To settings!_
        """
        pass
