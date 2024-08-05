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
class Test_C28060_Drag_and_Drop_option_for_Offer_Modules(Common):
    """
    TR_ID: C28060
    NAME: Drag and Drop option for Offer Modules
    DESCRIPTION: This test case verifies possibility to edit offers ordering using drag and drop option in CMS
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-7820 CMS Offer Module
    PRECONDITIONS: 1. User is logged in to CMS and Offer Module section is opened.
    PRECONDITIONS: 2. To view changes in application wait for 5 min becuse of ACAMAI caching
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_verify_offer_modules_displaying_according_to_current_its_ordering_in_cms(self):
        """
        DESCRIPTION: Verify Offer Modules displaying according to current its ordering in CMS
        EXPECTED: All Modules are displayed in application according to its current ordering
        """
        pass

    def test_003_click_on_drag_and_drop_button_and_change_offer_modules_ordering_in_cmsdo_not_click_on_any_other_buttons(self):
        """
        DESCRIPTION: Click on 'Drag and Drop' button and change Offer Modules ordering in CMS.
        DESCRIPTION: Do not click on any other buttons.
        EXPECTED: 
        """
        pass

    def test_004_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_005_verify_offer_modules_displaying_in_application(self):
        """
        DESCRIPTION: verify Offer Modules displaying in application
        EXPECTED: Offer Modules displaying in application is updated according to CMS changes
        """
        pass
