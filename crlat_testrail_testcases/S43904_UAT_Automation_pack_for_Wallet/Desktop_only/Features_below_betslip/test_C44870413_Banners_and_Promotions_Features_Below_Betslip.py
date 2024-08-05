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
class Test_C44870413_Banners_and_Promotions_Features_Below_Betslip(Common):
    """
    TR_ID: C44870413
    NAME: Banners and Promotions Features  Below Betslip
    DESCRIPTION: Features  as Banners, Promotions are displayed below betslip as CMS configuration
    PRECONDITIONS: Features configurated in CMS: Banners and Promotions
    PRECONDITIONS: User loads the Ladbrokes desktop web page and log in
    """
    keep_browser_open = True

    def test_001_verify_that_banners_are_displayed_under_betslip_area_as_per_cms_configurationverify_that_the_order_of_the_banner_is_conform_with_the_cms_settingsverify_that_on_click_banners_functionality_works_fine(self):
        """
        DESCRIPTION: Verify that Banners are displayed under Betslip area as per CMS configuration
        DESCRIPTION: Verify that the order of the banner is conform with the CMS settings
        DESCRIPTION: Verify that on click Banners functionality works fine
        EXPECTED: Banner feature is displayed as per configuration and works as designed
        """
        pass

    def test_002_verify_that_promotions_are_displayed_under_betslip_area_as_per_cms_configuration_and_orderverify_that_on_click_promotion_functionality_works_fine(self):
        """
        DESCRIPTION: Verify that Promotions are displayed under Betslip area as per CMS configuration and order
        DESCRIPTION: Verify that on click Promotion functionality works fine
        EXPECTED: Promotions feature is displayed as per configuration and works as designed
        """
        pass

    def test_003_tbccheck_that_events_are_added_to_favorite_column_when_clicked_on__next_to_event(self):
        """
        DESCRIPTION: TBC:
        DESCRIPTION: Check that Events are added to Favorite column when clicked on * next to event
        EXPECTED: Feature works fine
        """
        pass
