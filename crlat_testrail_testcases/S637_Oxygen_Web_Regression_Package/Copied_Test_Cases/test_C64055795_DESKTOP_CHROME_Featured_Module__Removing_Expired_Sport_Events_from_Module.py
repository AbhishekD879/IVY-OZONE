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
class Test_C64055795_DESKTOP_CHROME_Featured_Module__Removing_Expired_Sport_Events_from_Module(Common):
    """
    TR_ID: C64055795
    NAME: [DESKTOP CHROME] Featured Module - Removing Expired <Sport> Events from Module
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
