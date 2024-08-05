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
class Test_C64055823_DESKTOP_SAFARI_Featured_Module_by_Sport_TypeID__Price_Change(Common):
    """
    TR_ID: C64055823
    NAME: [DESKTOP SAFARI] Featured Module by Sport TypeID - Price Change
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
