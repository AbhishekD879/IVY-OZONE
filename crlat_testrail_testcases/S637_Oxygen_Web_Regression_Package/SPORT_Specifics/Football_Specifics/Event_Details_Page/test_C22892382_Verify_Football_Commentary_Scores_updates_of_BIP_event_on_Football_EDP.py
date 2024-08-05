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
class Test_C22892382_Verify_Football_Commentary_Scores_updates_of_BIP_event_on_Football_EDP(Common):
    """
    TR_ID: C22892382
    NAME: Verify Football Commentary Scores updates of BIP event on Football EDP
    DESCRIPTION: This test case verifies Football Commentary Scores updates of BIP event on Football EDP.
    PRECONDITIONS: 
    """
    keep_browser_open = True
