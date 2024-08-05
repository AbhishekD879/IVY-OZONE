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
class Test_C64055797_DESKTOP_CHROME_Featured_Module_by_Sport_TypeID__Verify_names_displaying_within_Featured_tab(Common):
    """
    TR_ID: C64055797
    NAME: [DESKTOP CHROME] Featured: Module by <Sport> TypeID - Verify names displaying within Featured tab
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
