import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C65940581_UnchecK_and_recheck_particular_sport_form_CMS(Common):
    """
    TR_ID: C65940581
    NAME: UnchecK and recheck particular sport form CMS
    DESCRIPTION: This test case is to validate display of  particular sport from  Sports ribbon tab
    PRECONDITIONS: Launch Coral/Ladbrokes Application.
    PRECONDITIONS: Login to CMS and goto Sport pages ->Sport Category ->Click on Any Sport(Football).
    PRECONDITIONS: Click on General sport configuration  .
    PRECONDITIONS: Uncheck Active Checkbox
    PRECONDITIONS: Login to CMS and goto Sport pages ->Sport Category ->Click on Any Sport(Football).
    PRECONDITIONS: Click on General sport configuration  .
    PRECONDITIONS: check Active Checkbox
    """
    keep_browser_open = True

    def test_001_launch_coralladbrokes_application(self):
        """
        DESCRIPTION: Launch Coral/Ladbrokes Application.
        EXPECTED: Application should be launched successfully
        """
        pass

    def test_002_verify_sport_in_sport_ribbon_tab(self):
        """
        DESCRIPTION: Verify Sport in Sport ribbon tab
        EXPECTED: Unchecked sport should not be shown in Sport ribbon tab
        """
        pass

    def test_003_verify_sport_in_sport_ribbon_tab(self):
        """
        DESCRIPTION: Verify Sport in Sport ribbon tab
        EXPECTED: checked sport should  be shown in Sport ribbon tab
        """
        pass
