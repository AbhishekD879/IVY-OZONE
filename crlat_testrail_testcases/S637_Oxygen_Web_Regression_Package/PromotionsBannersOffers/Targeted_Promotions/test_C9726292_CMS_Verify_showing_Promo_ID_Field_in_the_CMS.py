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
class Test_C9726292_CMS_Verify_showing_Promo_ID_Field_in_the_CMS(Common):
    """
    TR_ID: C9726292
    NAME: [CMS] Verify showing Promo ID Field in the CMS
    DESCRIPTION: This test case verifies showing Promo ID Field in the CMS
    PRECONDITIONS: Navigate to Oxygen CMS (Coral/Ladbrokes)
    PRECONDITIONS: Go to 'Promotion' page from Navigation menu
    PRECONDITIONS: Tap 'Create Promotion' button -> User is redirected to 'Create Promotion' page
    """
    keep_browser_open = True

    def test_001_verify_that_promo_id_field_is_available_on_create_promotion_page(self):
        """
        DESCRIPTION: Verify that 'Promo ID' field is available on 'Create Promotion' page
        EXPECTED: 'Promo ID' field is available on 'Create Promotion' page
        """
        pass

    def test_002_fill_all_fields_on_create_promotion_page_and_tap_create_promotion_button(self):
        """
        DESCRIPTION: Fill all fields on 'Create Promotion' page and tap 'Create Promotion' button
        EXPECTED: - New Promotion with 'Promo ID' is saved
        """
        pass
