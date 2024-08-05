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
class Test_C62764602_Verify_enabling_disabling_of_Highlights_Carousel_Module(Common):
    """
    TR_ID: C62764602
    NAME: Verify enabling/disabling of 'Highlights Carousel' Module
    DESCRIPTION: This test case verifies enabling/disabling of "Highlights Carousel" Module on Home page/SLP via CMS, If we disable one Highlights Carousel next available Highlights Carousel should display
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >home page> Highlights Carousel
    PRECONDITIONS: Configure multiple Highlights Carousels with different publish dates
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_go_to_sports_pages__gt_highlights_carousel_section__gt_open_existing_highlights_carousel(self):
        """
        DESCRIPTION: Go to Sports Pages -&gt; Highlights Carousel section -&gt; open existing Highlights Carousel
        EXPECTED: Highlights Carousel details page is opened
        """
        pass

    def test_003_validate_the_user_is_able_to_enabledisable_and_save_the_changes_successfully(self):
        """
        DESCRIPTION: Validate the User is able to enable/disable and save the changes successfully.
        EXPECTED: User should be able to enable/ disable the check box.
        """
        pass

    def test_004_set_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Set 'Active' checkbox and save changes
        EXPECTED: a)Existing Highlights Carousel is active
        EXPECTED: b)Changes is saved successfully
        """
        pass

    def test_005_load_oxygen_app_and_verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify Highlights Carousel displaying
        EXPECTED: Highlights Carousel is displayed on Front End
        """
        pass

    def test_006_go_back_to_the_same_highlights_carousel_unselect_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go back to the same Highlights Carousel, unselect 'Active' checkbox and save changes
        EXPECTED: a)Existing Highlights Carousel is inactive
        EXPECTED: b)Changes is saved successfully
        """
        pass

    def test_007_load_oxygen_app_and_verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify Highlights Carousel displaying
        EXPECTED: a) Highlights Carousel is NOT displayed on Front End
        EXPECTED: b) If we have other Highlights Carousel with valid date it should display
        """
        pass
