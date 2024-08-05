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
class Test_C64894687_DESKTOP_CHROME_Verify_Coral_site_logo_display_and_navigation(Common):
    """
    TR_ID: C64894687
    NAME: [DESKTOP CHROME] Verify Coral site logo display and navigation
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
