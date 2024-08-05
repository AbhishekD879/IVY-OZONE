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
class Test_C44882505_Verify_Greyhound_and_Horse_Racing_Events_Markets_Updates(Common):
    """
    TR_ID: C44882505
    NAME: Verify Greyhound and Horse Racing Events Markets Updates
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
