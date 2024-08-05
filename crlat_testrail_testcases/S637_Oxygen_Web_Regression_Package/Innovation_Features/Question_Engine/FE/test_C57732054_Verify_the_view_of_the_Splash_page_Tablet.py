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
class Test_C57732054_Verify_the_view_of_the_Splash_page_Tablet(Common):
    """
    TR_ID: C57732054
    NAME: Verify the view of the Splash page [Tablet]
    DESCRIPTION: This test case verifies view of the Splash page [Tablet]
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    """
    keep_browser_open = True

    def test_001_tap_on_correct_4_link(self):
        """
        DESCRIPTION: Tap on Correct 4 link
        EXPECTED: - Splash page displayed and designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d8887b6bcf7fd15edfd3d30
        EXPECTED: - All data retrieved from CMS and correctly displayed
        """
        pass

    def test_002___make_changes_to_each_field_on_cms__question_enginee__splash_page__splashpage__save_changes(self):
        """
        DESCRIPTION: - Make changes to each field on CMS > Question Enginee > Splash Page > [splashpage]
        DESCRIPTION: - Save changes
        EXPECTED: Changes saved on CMS
        """
        pass

    def test_003_open_splash_page_again(self):
        """
        DESCRIPTION: Open 'Splash' page again
        EXPECTED: - All data retrieved from CMS and correctly displayed
        EXPECTED: - All successfully styled
        """
        pass