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
class Test_C28063_Drag_and_Drop_option_for_Offers(Common):
    """
    TR_ID: C28063
    NAME: Drag and Drop option for Offers
    DESCRIPTION: This test case verifies possibility to edit offers ordering within the module uisng Drug and Drop option in CMS
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-7820 CMS Offer Module
    PRECONDITIONS: 1. User is logged in to CMS and Offers section is opened.
    PRECONDITIONS: 2. To view changes in application wait for 5 min becuse of ACAMAI caching
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_verify_offers_displaying_according_to_current_its_ordering_in_cms(self):
        """
        DESCRIPTION: Verify Offers displaying according to current its ordering in CMS
        EXPECTED: All Offers are displayed in application according to its current ordering WITHIN Offer Module to which they are linked.
        EXPECTED: For Example: Offer can be fifth in general offers list  but other two offers from the same Module have 7th and 10th position.
        EXPECTED: So within one Module 5th Offer will be the first one, 7th  - the second one and 10th - the third one.
        """
        pass

    def test_003_click_on_drag_and_drop_button_and_change_offers_ordering_in_cmsdo_not_click_on_any_other_buttons(self):
        """
        DESCRIPTION: Click on 'Drag and Drop' button and change Offers ordering in CMS.
        DESCRIPTION: Do not click on any other buttons.
        EXPECTED: 
        """
        pass

    def test_004_repeat_step_1(self):
        """
        DESCRIPTION: Repeat step 1
        EXPECTED: 
        """
        pass

    def test_005_verify_offers_displaying_in_application_accroding_to_updated_ordering(self):
        """
        DESCRIPTION: Verify Offers displaying in application accroding to updated ordering
        EXPECTED: Offers displaying in application is updated according to CMS changes within their Offer Modules
        """
        pass
