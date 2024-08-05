import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C44870324_Verify_each_tab_live_push_price_updates(Common):
    """
    TR_ID: C44870324
    NAME: Verify each tab live push price updates
    DESCRIPTION: this test case verify price updates
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen Application
        EXPECTED: Home Page is opened
        """
        pass

    def test_002_go_to_in_play_tab(self):
        """
        DESCRIPTION: Go to In-Play tab
        EXPECTED: In-Play tab is opened
        """
        pass

    def test_003_verify_oddsprice_updates_for_all_inplay_sports(self):
        """
        DESCRIPTION: Verify odds/Price updates for all Inplay sports
        EXPECTED: Odd/price updated successfully
        """
        pass
