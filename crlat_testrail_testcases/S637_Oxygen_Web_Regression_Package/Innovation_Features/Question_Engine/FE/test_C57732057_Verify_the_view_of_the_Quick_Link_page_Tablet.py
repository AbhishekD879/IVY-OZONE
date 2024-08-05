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
class Test_C57732057_Verify_the_view_of_the_Quick_Link_page_Tablet(Common):
    """
    TR_ID: C57732057
    NAME: Verify the view of the Quick Link page [Tablet]
    DESCRIPTION: This test case verifies view of the Quick Link page [Tablet]
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
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a
        EXPECTED: - All data retrieved from CMS and correctly displayed
        """
        pass

    def test_002_tap_on_each_quick_links_buttons_in_the_footer(self):
        """
        DESCRIPTION: Tap on each 'Quick links' buttons in the footer
        EXPECTED: User navigated to the relevant content page displayed as per the design:
        EXPECTED: Prizes: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d8887b627da7a15ab2555c9
        EXPECTED: T&C's : https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d8887b6e4bb440268025990
        EXPECTED: FAQ's : https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d8887b6bcf7fd15edfd3d23
        """
        pass

    def test_003___make_changes_to_each_field_on_cms__question_enginee__quick_links__quicklinks__save_changes(self):
        """
        DESCRIPTION: - Make changes to each field on CMS > Question Enginee > Quick Links > [quicklinks]
        DESCRIPTION: - Save changes
        EXPECTED: Changes saved on CMS
        """
        pass

    def test_004_tap_on_each_quick_links_buttons_in_the_footer_again(self):
        """
        DESCRIPTION: Tap on each 'Quick links' buttons in the footer again
        EXPECTED: - All data retrieved from CMS and correctly displayed
        EXPECTED: - All successfully styled
        """
        pass
