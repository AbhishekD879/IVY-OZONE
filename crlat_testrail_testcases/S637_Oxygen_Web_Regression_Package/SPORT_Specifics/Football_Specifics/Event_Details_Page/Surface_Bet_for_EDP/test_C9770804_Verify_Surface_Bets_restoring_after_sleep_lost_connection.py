import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.homepage_featured
@vtest
class Test_C9770804_Verify_Surface_Bets_restoring_after_sleep_lost_connection(Common):
    """
    TR_ID: C9770804
    NAME: Verify Surface Bets restoring after sleep/lost connection
    DESCRIPTION: Test Case verified the Surface Bet is successfully restored after lost connection or sleep mode
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the Event Details page (EDP).
    PRECONDITIONS: 2. Open this EDP
    PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_staying_on_the_edp_initiate_the_connection_lost_verify_the_surface_bet_is_restored_properly_without_disappearing_or_page_refresh(self):
        """
        DESCRIPTION: Staying on the EDP initiate the connection lost. Verify the Surface Bet is restored properly, without disappearing or page refresh
        EXPECTED: Surface Bet is restored properly
        """
        pass

    def test_002_staying_on_the_edp_initiate_the_device_sleepwake_up_verify_the_surface_bet_is_restored_properly_without_disappearing_or_page_refresh(self):
        """
        DESCRIPTION: Staying on the EDP initiate the device sleep/wake up. Verify the Surface Bet is restored properly, without disappearing or page refresh
        EXPECTED: Surface Bet is restored properly
        """
        pass
