import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C44882512_Verify_Greyhound_Racing_Events_Selections_Ordering_is_correct(Common):
    """
    TR_ID: C44882512
    NAME: Verify Greyhound Racing Events Selections Ordering is correct
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
