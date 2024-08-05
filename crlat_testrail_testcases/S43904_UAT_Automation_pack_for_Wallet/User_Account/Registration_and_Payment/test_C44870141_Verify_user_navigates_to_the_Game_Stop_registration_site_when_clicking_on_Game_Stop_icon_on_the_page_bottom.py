import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870141_Verify_user_navigates_to_the_Game_Stop_registration_site_when_clicking_on_Game_Stop_icon_on_the_page_bottom(Common):
    """
    TR_ID: C44870141
    NAME: "Verify user navigates to the 'Game Stop' registration site when clicking on 'Game Stop' icon on the page bottom
    DESCRIPTION: 
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is shown
        """
        pass

    def test_002_verify_the_presence_of__footer_items(self):
        """
        DESCRIPTION: Verify the presence of  Footer items
        EXPECTED: 
        """
        pass

    def test_003_click_on_gamstop(self):
        """
        DESCRIPTION: Click on GamStop
        EXPECTED: User is taken  to the 'Game Stop' registration site (https://www.gamstop.co.uk/)
        """
        pass
