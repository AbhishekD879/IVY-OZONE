import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C22892383_Verify_Extra_Time_Commentary_Score_displaying_on_Football_EDP_for_BIP_event(Common):
    """
    TR_ID: C22892383
    NAME: Verify Extra Time Commentary Score displaying on Football EDP for BIP event
    DESCRIPTION: This test case verifies Extra Time Commentary Score displaying on Football EDP for BIP event.
    PRECONDITIONS: 
    """
    keep_browser_open = True
