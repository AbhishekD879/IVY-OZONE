import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.
@vtest
class Test_C44870442_Verify_StreamBet_functionality(Common):
    """
    TR_ID: C44870442
    NAME: Verify Stream&Bet functionality
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
