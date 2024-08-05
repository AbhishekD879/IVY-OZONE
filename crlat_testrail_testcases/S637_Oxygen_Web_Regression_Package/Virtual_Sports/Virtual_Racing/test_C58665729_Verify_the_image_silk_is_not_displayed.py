import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C58665729_Verify_the_image_silk_is_not_displayed(Common):
    """
    TR_ID: C58665729
    NAME: Verify the image (silk) is not displayed
    DESCRIPTION: This test case verifies the image (silk) is not displayed on FE:
    DESCRIPTION: - when the 'Display runner images' checkbox is unchecked on CMS.
    DESCRIPTION: - the image (silk) is deleted on CMS.
    PRECONDITIONS: 1. The CMS User is logged in.
    PRECONDITIONS: 2. Navigate to Virtual Sport.
    PRECONDITIONS: 3. Select a Parent sport (e.g., Horse Racing).
    PRECONDITIONS: 4. Select a Child Sport.
    PRECONDITIONS: 5. [OX102.1] Uncheck the 'Display runner images' checkbox.
    PRECONDITIONS: 6. Save the changes.
    """
    keep_browser_open = True

    def test_001_open_coralladbrokes_test_environment(self):
        """
        DESCRIPTION: Open Coral/Ladbrokes test environment.
        EXPECTED: The FE is successfully opened.
        """
        pass

    def test_002_navigate_to_virtual_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Virtual Sports->Horse Racing.
        EXPECTED: The images (silks) are not displayed.
        """
        pass

    def test_003_ox1021_check_the_display_runner_images_checkbox_on_cms_and_save_the_changes(self):
        """
        DESCRIPTION: [OX102.1] Check the 'Display runner images' checkbox on CMS and save the changes.
        EXPECTED: The changes are successfully saved.
        """
        pass

    def test_004_open_horse_racing_on_incognito_tab(self):
        """
        DESCRIPTION: Open Horse Racing on incognito tab.
        EXPECTED: The images (silks) are displayed.
        """
        pass

    def test_005_remove_an_image_on_cms(self):
        """
        DESCRIPTION: Remove an image on CMS.
        EXPECTED: The image is successfully removed on CMS.
        """
        pass

    def test_006_open_horse_racing_on_incognito_tab(self):
        """
        DESCRIPTION: Open Horse Racing on incognito tab.
        EXPECTED: The previously deleted image (silk) is not displayed.
        """
        pass
