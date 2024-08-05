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
class Test_C64881006_Super_button__Universal_view_before_login(Common):
    """
    TR_ID: C64881006
    NAME: Super button - Universal view before login
    DESCRIPTION: This testcases verifies Universal view before user login
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > super button >Create superbutton
    PRECONDITIONS: Select Universal Radio button while creating super button.
    PRECONDITIONS: For Universal,There is at least one super button added to the Homepage in CMS
    """
    keep_browser_open = True

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application.
        EXPECTED: Application should launch successfully.
        """
        pass

    def test_002_(self):
        """
        DESCRIPTION: 
        EXPECTED: Home page should be opened.
        """
        pass

    def test_003_verify_universal_view_by_default_before_login(self):
        """
        DESCRIPTION: Verify universal view (by default) before login
        EXPECTED: User should able to view Universal record(The first valid Super button) as configured in CMS
        """
        pass

    def test_004_(self):
        """
        DESCRIPTION: 
        EXPECTED: Add:CMS SS ,FE before login SS
        """
        pass
