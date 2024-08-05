import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C64055815_DESKTOP_SAFARI_Verify_Price_Odds_for_3_Way_Market(Common):
    """
    TR_ID: C64055815
    NAME: [DESKTOP SAFARI] Verify Price/Odds for 3-Way Market
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
