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
class Test_C29433_Private_Markets_Terms_and_Conditions_page(Common):
    """
    TR_ID: C29433
    NAME: 'Private Markets Terms and Conditions' page
    DESCRIPTION: This test case verifies 'Private Markets Terms and Conditions' page.
    DESCRIPTION: 'Private Markets Terms and Conditions' page is CMS configurable.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    DESCRIPTION: AUTOTEST Mobile: [C2855549]
    DESCRIPTION: AUTOTEST Desktop: [C2855978]
    PRECONDITIONS: 1.  User should be logged in
    PRECONDITIONS: 2.  User should be eligible for one or more private enhanced market offers
    PRECONDITIONS: 3.  Private market offers should be active (not expired)
    PRECONDITIONS: 4.  To load CMS for Private Markets use Static Block "Private Markets Terms And Conditions" (https://CMS_endpoint/keystone/static-blocks)
    PRECONDITIONS: 5. **accountFreebets?freebetTokenType=ACCESS** request is used in order to get a private market for particular user after a page refresh or navigating to Homepage from any other page and **user** request is used to get private market after login(open Dev tools -> Network ->XHR tab)
    PRECONDITIONS: CMS_endpoint can be found using devlog
    PRECONDITIONS: NOTE: for configuration of private enhanced market offers contact UAT
    PRECONDITIONS: UAT configure event. Place a bet on configured event by any user with sufficient funds for bet placement and then verify Private Markets on the Homepage. Private Markets will be shown for all users which placed a bet on configured event.
    """
    keep_browser_open = True

    def test_001_open_oxygen_application(self):
        """
        DESCRIPTION: Open Oxygen application
        EXPECTED: *  Homepage is opened
        """
        pass

    def test_002_clicktap_on_terms_and_conditions_link_onyour_enhancedmarkets_tabsection(self):
        """
        DESCRIPTION: Click/Tap on 'Terms and Conditions' link on 'Your Enhanced Markets' tab/section
        EXPECTED: *    'Private Markets Terms and Conditions' page is opened with  'Private Markets Terms and Conditions' header and 'Back' button
        EXPECTED: *   Page content is displayed correctly (according to CMS configurations in 'Static Blocks')
        """
        pass

    def test_003_clicktap_on_back_button(self):
        """
        DESCRIPTION: Click/Tap on 'Back' button
        EXPECTED: User navigates back to previous page
        """
        pass
