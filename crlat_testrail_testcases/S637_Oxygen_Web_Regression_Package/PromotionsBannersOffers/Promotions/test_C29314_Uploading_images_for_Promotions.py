import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.promotions_banners_offers
@vtest
class Test_C29314_Uploading_images_for_Promotions(Common):
    """
    TR_ID: C29314
    NAME: Uploading images for Promotions
    DESCRIPTION: The purpose of this test case is to verify images uploading into CMS->Promotions and their displaying in the application
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_open_cms_promotions(self):
        """
        DESCRIPTION: Open CMS->Promotions
        EXPECTED: 
        """
        pass

    def test_002_click_on_create_promotion_button(self):
        """
        DESCRIPTION: Click on "Create Promotion" button
        EXPECTED: "Create a new Promotion" page appears
        """
        pass

    def test_003_verify_the_page(self):
        """
        DESCRIPTION: Verify the page
        EXPECTED: The following elements are present on the page:
        EXPECTED: * 'Active' check-box;
        EXPECTED: * 'Title' text field;
        EXPECTED: * 'Promo Key' text field;
        EXPECTED: * 'Show on Competitions' field;
        EXPECTED: * 'Short Description' text field;
        EXPECTED: * 'Description' field;
        EXPECTED: * 'Use Upload image' / 'Use Image URL' radiobuttons;
        EXPECTED: * 'Validity Period Start date' and 'Validity Period End Date' date fields;
        EXPECTED: * 'Is Signposting Promotion' section;
        EXPECTED: * 'Include VIP levels' text field;
        EXPECTED: * 'Opt In Request ID' text field;
        EXPECTED: * 'Show To Customer' drop-down selector;
        EXPECTED: * 'Category' field;
        EXPECTED: * 'T&C' field;
        EXPECTED: * 'Create' button;
        """
        pass

    def test_004_populate_all_fields_with_valid_data_and_click_the_create_button(self):
        """
        DESCRIPTION: Populate all fields with valid data and click the "Create" button
        EXPECTED: * New Promotion <offer_name> created
        EXPECTED: * Success message appears
        EXPECTED: * Promotion edit page is opened
        """
        pass

    def test_005_verify_the_image_upload_fields(self):
        """
        DESCRIPTION: Verify the image upload fields
        EXPECTED: * 'Use Upload image' / 'Use Image URL' radiobuttons are present
        EXPECTED: * 'Use Upload image' radio button is checked by default
        """
        pass

    def test_006_upload_an_image_for_the_promotion_using_the_use_upload_image_option(self):
        """
        DESCRIPTION: Upload an image for the Promotion using the 'Use Upload image' option
        EXPECTED: Image is uploaded
        """
        pass

    def test_007_click_on_save_button(self):
        """
        DESCRIPTION: Click on "Save" button
        EXPECTED: Success message appears
        """
        pass

    def test_008_load_oxygen_application_and_verify_that_the_promotion_is_displayed(self):
        """
        DESCRIPTION: Load Oxygen application and verify that the Promotion is displayed
        EXPECTED: * Just added Promotions is shown on 'Promotions' page
        EXPECTED: * All data is displayed according to CMS
        """
        pass

    def test_009_verify_images_uploading_for_promotions_in_cms_and_their_displaying_in_the_application(self):
        """
        DESCRIPTION: Verify images uploading for Promotions in CMS and their displaying in the application
        EXPECTED: * Uploaded image is displayed correctly in the application on Promotions page and Promotion Details page (after tapping "More information" button)
        EXPECTED: * It is possible to change image for a Promotion, new image will be displayed in the application
        EXPECTED: * If image was not uploaded in CMS then it will not be displayed in the application, Promotions and Promotion Details page will still look properly
        """
        pass

    def test_010_go_to_cms_promotions(self):
        """
        DESCRIPTION: Go to CMS->Promotions
        EXPECTED: 
        """
        pass

    def test_011_choose_available_promotions_and_upload_image_in_a_size_640x200(self):
        """
        DESCRIPTION: Choose available promotions and upload image in a size 640x200
        EXPECTED: 
        """
        pass

    def test_012_go_back_to_invictus_app__promotions_page(self):
        """
        DESCRIPTION: Go back to Invictus app-> 'Promotions' page
        EXPECTED: 
        """
        pass

    def test_013_verify_just_uploaded_image_and_its_displaying_use_inspect_element_to_check_image_size(self):
        """
        DESCRIPTION: Verify just uploaded image and its displaying (use Inspect element to check image size)
        EXPECTED: Uploaded image has size 640x200 on web desktop on the following pages:
        EXPECTED: *   Promotions page
        EXPECTED: *   Promotion Details page (after tapping "More information" button)
        EXPECTED: On mobile devices image is displayed properly according to screen size. The image is NOT stretched, distorted or cut
        """
        pass

    def test_014_navigate_to_the_relevant_promotion_in_the_cms(self):
        """
        DESCRIPTION: Navigate to the relevant Promotion in the CMS
        EXPECTED: Promotion edit page is opened
        """
        pass

    def test_015_select_the_use_image_url_option(self):
        """
        DESCRIPTION: Select the 'Use Image URL' option
        EXPECTED: 'Use Image URL' radiobutton is selected
        """
        pass

    def test_016_upload_an_image_to_the_image_url_field_using_the_absolute_url(self):
        """
        DESCRIPTION: Upload an image to the 'Image URL' field using the Absolute URL
        EXPECTED: Image is uploaded
        """
        pass

    def test_017_click_on_save_button(self):
        """
        DESCRIPTION: Click on "Save" button
        EXPECTED: Success message appears
        """
        pass

    def test_018_repeat_steps_8_13(self):
        """
        DESCRIPTION: Repeat steps 8-13
        EXPECTED: * Promotions is shown on 'Promotions' page in proper size
        EXPECTED: * All data is displayed according to CMS
        EXPECTED: * Promotion is displayed within image uploaded by using 'Image URL' field
        """
        pass
