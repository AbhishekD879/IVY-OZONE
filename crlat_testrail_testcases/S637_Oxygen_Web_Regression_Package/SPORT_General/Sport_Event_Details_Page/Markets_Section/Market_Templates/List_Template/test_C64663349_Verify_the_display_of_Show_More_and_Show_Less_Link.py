import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C64663349_Verify_the_display_of_Show_More_and_Show_Less_Link(Common):
    """
    TR_ID: C64663349
    NAME: Verify the display of Show More and Show Less Link
    DESCRIPTION: This test case verifies display od Show More/Show Less links  for list market templet
    PRECONDITIONS: 1.Market with List templet should be available ex:Outright,GetAPrice etc..
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_edp_page(self):
        """
        DESCRIPTION: Navigate to EDP page
        EXPECTED: EDP page should be displayed
        """
        pass

    def test_003_expand_any_market_which_has_list_templetexoutrightgetaprice(self):
        """
        DESCRIPTION: Expand any market which has list templet
        DESCRIPTION: Ex:Outright,GetAPrice
        EXPECTED: * Market Header should be displayed along with signposting if available
        EXPECTED: * List of Options (each with a Price Button)
        EXPECTED: * “SHOW MORE/LESS” option available(when user selects show more link it should be replace with Show Less)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/c39e26ab-ecaa-4a64-802b-d9ca7bd6202f)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/7e4874a3-2dfa-4b95-b0a6-b7ce41c690f2)     ![](index.php?/attachments/get/b673881a-1444-48e2-8eb8-7a2ff7b4e11b)
        """
        pass
