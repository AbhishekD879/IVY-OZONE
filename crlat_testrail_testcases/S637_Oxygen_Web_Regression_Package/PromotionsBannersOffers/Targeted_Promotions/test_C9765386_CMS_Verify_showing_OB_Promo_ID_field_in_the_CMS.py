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
class Test_C9765386_CMS_Verify_showing_OB_Promo_ID_field_in_the_CMS(Common):
    """
    TR_ID: C9765386
    NAME: [CMS] Verify showing OB Promo ID field in the CMS
    DESCRIPTION: This test case verifies showing OB Promo ID Field in the CMS within the Promotion section
    PRECONDITIONS: Navigate to Oxygen CMS (Coral/Ladbrokes)
    PRECONDITIONS: Go to 'Promotion' page from Navigation menu
    PRECONDITIONS: Tap 'Create Promotion' button -> User is redirected to 'Create Promotion' page
    """
    keep_browser_open = True

    def test_001_verify_that_ob_promo_id_field_is_shown_on_create_promotion_page(self):
        """
        DESCRIPTION: Verify that 'OB Promo ID' field is shown on Create Promotion page
        EXPECTED: 'OB Promo ID' field is shown on Create Promotion page
        """
        pass

    def test_002_fill_all_fields_except_ob_promo_id_and_tap_create_promotion_buttonverify_that_ob_promo_id_is_not_mandatory___the_promotion_is_created(self):
        """
        DESCRIPTION: Fill all fields except 'OB Promo ID' and tap 'Create Promotion' button
        DESCRIPTION: Verify that 'OB Promo ID' is not mandatory - the promotion is created
        EXPECTED: Promotion is created without 'OB Promo ID'
        """
        pass

    def test_003_tap_create_promotion_button_one_more_timefill_all_fields_and_enter_appropriate_id_into_ob_promo_id_fieldtap_create_promotion_buttonverify_that_promotion_is_created(self):
        """
        DESCRIPTION: Tap 'Create Promotion' button one more time
        DESCRIPTION: Fill all fields and enter appropriate ID into 'OB Promo ID' field
        DESCRIPTION: Tap 'Create Promotion' button
        DESCRIPTION: Verify that Promotion is created
        EXPECTED: Promotion is created with 'OB Promo ID'
        """
        pass
