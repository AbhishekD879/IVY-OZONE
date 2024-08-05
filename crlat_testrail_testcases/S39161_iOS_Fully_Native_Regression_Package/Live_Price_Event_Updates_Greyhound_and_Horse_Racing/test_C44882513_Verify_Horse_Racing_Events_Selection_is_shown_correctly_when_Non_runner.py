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
class Test_C44882513_Verify_Horse_Racing_Events_Selection_is_shown_correctly_when_Non_runner(Common):
    """
    TR_ID: C44882513
    NAME: Verify Horse Racing Events Selection is shown correctly when Non-runner
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
