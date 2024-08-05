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
class Test_C2604119_Coral_Only_In_shop_Promotions(Common):
    """
    TR_ID: C2604119
    NAME: [Coral Only] In-shop Promotions
    DESCRIPTION: This test case verifies in-shop promotions functionality
    DESCRIPTION: AUTOTESTS https://ladbrokescoral.testrail.com/index.php?/suites/view/3779&group_by=cases:section_id&group_id=740752&group_order=asc
    DESCRIPTION: Info:
    DESCRIPTION: 'In-Shop' - user with card number and pin (The Grid - Ladbrokes; Connect - Coral).
    DESCRIPTION: 'Online' - user with username and password.
    DESCRIPTION: 'Multi-channel' - user who was 'In-Shop' and is upgraded to 'Online' (e.g. has both card#/pin and username/password)
    PRECONDITIONS: CMS:
    PRECONDITIONS: https://CMS_ENDPOINT/keystone/ -> Pick 'sportsbook' brand from the drop-down -> 'Promotions'
    PRECONDITIONS: Contact GVC (Venugopal Rao Joshi / Abhinav Goel) and/or Souparna Datta + Oksana Tkach in order to generate In-Shop users
    """
    keep_browser_open = True

    def test_001_go_to_promotion_section_on_cms_and_click_plus_create_promotion_button(self):
        """
        DESCRIPTION: Go to 'Promotion' section on CMS and Click "+ Create Promotion" button
        EXPECTED: * Promotion edit page is opened
        """
        pass

    def test_002_populate_all_fields_with_valid_data_add_promo_key_description_short_description_image_validity_period_set_category_as_connect_promotions_click_on_create_promotion_button(self):
        """
        DESCRIPTION: Populate all fields with valid data:
        DESCRIPTION: * Add Promo Key, Description, Short description, Image, Validity Period
        DESCRIPTION: * Set 'category' as **'Connect Promotions'**
        DESCRIPTION: * Click on "Create promotion" button
        EXPECTED: * New Promotion <offer_name> created
        """
        pass

    def test_003__get_back_to_sportbook_open_connect_landing_page___shop_exclusive_promos(self):
        """
        DESCRIPTION: * Get back to SportBook
        DESCRIPTION: * Open Connect landing page -> Shop exclusive promos
        EXPECTED: * Promotion page with two tabs ('All', 'Connect Exclusive') is opened
        EXPECTED: * User is on the 'Connect/Shop Exclusive' tab with active connect promotions
        """
        pass

    def test_004_verify_promotion_view(self):
        """
        DESCRIPTION: Verify promotion view
        EXPECTED: There are such elements for created promotion:
        EXPECTED: * Banner
        EXPECTED: * Promotion title (White text on a blue area)
        EXPECTED: * Short Description (Grey text on a grey area)
        EXPECTED: * Green 'More info' button on a grey area
        """
        pass

    def test_005_tapclick_more_info_button_on_any_promotion(self):
        """
        DESCRIPTION: Tap/Click 'More info' button on any promotion
        EXPECTED: The list of elements:
        EXPECTED: * Promotion title
        EXPECTED: * Banner
        EXPECTED: * Description
        EXPECTED: * 'T&C's' section
        """
        pass

    def test_006_tap_all_tab(self):
        """
        DESCRIPTION: Tap 'All' tab
        EXPECTED: Promotions with other categories than 'Connect Promotions' category are opened
        """
        pass
