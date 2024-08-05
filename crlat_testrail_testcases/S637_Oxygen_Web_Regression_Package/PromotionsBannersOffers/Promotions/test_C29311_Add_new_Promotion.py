import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C29311_Add_new_Promotion(Common):
    """
    TR_ID: C29311
    NAME: Add new Promotion
    DESCRIPTION: This test case verifies adding and displaying new promotion
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/promotions
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_go_to_promotion_section(self):
        """
        DESCRIPTION: Go to 'Promotion' section
        EXPECTED: 'Promotion' section is opened
        """
        pass

    def test_003_click_on_create_promotion_button(self):
        """
        DESCRIPTION: Click on "Create Promotion" button
        EXPECTED: "Create a new Promotion" page appears
        """
        pass

    def test_004_verify_the_page(self):
        """
        DESCRIPTION: Verify the page
        EXPECTED: The following elements are present on the page:
        EXPECTED: * 'Active' check-box;
        EXPECTED: * 'Title' text field;
        EXPECTED: * 'Promo Key' text field;
        EXPECTED: * 'Show on Competitions' field;
        EXPECTED: * 'Short Description' text field;
        EXPECTED: * 'Description' field;
        EXPECTED: * Targeted Promos section
        EXPECTED: * Promotion ID field
        EXPECTED: * OB promotion ID field
        EXPECTED: * 'Use Upload image' / 'Use Image URL' radiobuttons;
        EXPECTED: * 'Validity Period Start date' and 'Validity Period End Date' date fields;
        EXPECTED: * 'Is Signposting Promotion' checkbox;
        EXPECTED: * Event-level flag field
        EXPECTED: * Market-level flag field
        EXPECTED: * Overlay BET NOW button url
        EXPECTED: * 'Include VIP levels' text field;
        EXPECTED: * 'Opt In Request ID' text field;
        EXPECTED: * 'Show To Customer' drop-down selector;
        EXPECTED: * 'Category' field;
        EXPECTED: * 'T&C' field;
        EXPECTED: * Popup title field;
        EXPECTED: * Popup text field;
        EXPECTED: * 'Create' button;
        EXPECTED: * 'Cancel' button;
        """
        pass

    def test_005_populate_all_fields_with_valid_data_and_click_the_create_button(self):
        """
        DESCRIPTION: Populate all fields with valid data and click the "Create" button
        EXPECTED: * New Promotion <offer_name> created
        EXPECTED: * Success message appears
        EXPECTED: * Promotion edit page is opened
        """
        pass

    def test_006_verify_the_image_upload_fields(self):
        """
        DESCRIPTION: Verify the image upload fields
        EXPECTED: * 'Use Upload image' / 'Use Image URL' radiobuttons are present
        EXPECTED: * 'Use Upload image' radio button is checked by default
        """
        pass

    def test_007_upload_an_image_for_the_promotion_using_the_use_upload_image_option(self):
        """
        DESCRIPTION: Upload an image for the Promotion using the 'Use Upload image' option
        EXPECTED: Image is uploaded
        """
        pass

    def test_008_click_on_save_button(self):
        """
        DESCRIPTION: Click on "Save" button
        EXPECTED: Success message appears
        """
        pass

    def test_009_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_010_navigate_to_promotions_page_from_sports_menu_ribbon_or_left_navigation_menu(self):
        """
        DESCRIPTION: Navigate to 'Promotions' page from 'Sports Menu Ribbon' or 'Left Navigation' menu
        EXPECTED: 'Promotions' page is opened
        """
        pass

    def test_011_verify_presence_of_just_added_promotions(self):
        """
        DESCRIPTION: Verify presence of just added Promotions
        EXPECTED: * Just added Promotions is shown on 'Promotions' page
        EXPECTED: * Promotion is displayed within correct uploaded image
        EXPECTED: * All data is displayed according to CMS
        """
        pass

    def test_012_navigate_to_the_relevant_promotion_in_the_cms(self):
        """
        DESCRIPTION: Navigate to the relevant Promotion in the CMS
        EXPECTED: Promotion edit page is opened
        """
        pass

    def test_013_select_the_use_image_url_option(self):
        """
        DESCRIPTION: Select the 'Use Image URL' option
        EXPECTED: 'Use Image URL' radiobutton is selected
        """
        pass

    def test_014_upload_an_image_to_the_image_url__field_using_the_absolute_url(self):
        """
        DESCRIPTION: Upload an image to the 'Image URL ' field using the Absolute URL
        EXPECTED: Image is uploaded
        """
        pass

    def test_015_click_on_save_button(self):
        """
        DESCRIPTION: Click on "Save" button
        EXPECTED: Success message appears
        """
        pass

    def test_016_repeat_steps_9_11(self):
        """
        DESCRIPTION: Repeat steps 9-11
        EXPECTED: * Promotions is shown on 'Promotions' page
        EXPECTED: * All data is displayed according to CMS
        EXPECTED: * Promotion is displayed within image uploaded by using 'Image URL' field
        """
        pass
