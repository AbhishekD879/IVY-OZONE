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
class Test_C44882514_Verify_Greyhound_Racing_Events_Selection_is_shown_correctly_when_Vacant_Trap(Common):
    """
    TR_ID: C44882514
    NAME: Verify Greyhound Racing Events Selection is shown correctly when Vacant Trap
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
