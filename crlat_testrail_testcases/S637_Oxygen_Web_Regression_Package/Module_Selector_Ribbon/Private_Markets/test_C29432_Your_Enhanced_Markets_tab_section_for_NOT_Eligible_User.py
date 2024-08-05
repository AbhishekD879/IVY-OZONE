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
class Test_C29432_Your_Enhanced_Markets_tab_section_for_NOT_Eligible_User(Common):
    """
    TR_ID: C29432
    NAME: 'Your Enhanced Markets' tab/section for NOT Eligible User
    DESCRIPTION: This test case verifies 'Your Enhanced Markets' tab/section for the user which is NOT eligible for private market offers.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1.  User should be logged in
    PRECONDITIONS: 2.  User should NOT be eligible for one or more private enhanced market offers
    PRECONDITIONS: 3. **accountFreebets?freebetTokenType=ACCESS** request is used in order to get a private market for particular user after a page refresh or navigating to Homepage from any other page and **user** request is used to get private market after login(open Dev tools -> Network ->XHR tab)
    """
    keep_browser_open = True

    def test_001_open_oxygen_app(self):
        """
        DESCRIPTION: Open Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_verify_your_enhancedmarkets_tabsection(self):
        """
        DESCRIPTION: Verify 'Your Enhanced Markets' tab/section
        EXPECTED: *  'Your Enhanced Markets' tab/section is not displayed on the Homepage
        EXPECTED: *  'Featured' (or other tab with highest priority in the Module Selector Ribbon list) tab is selected by default **for mobile/tablet**
        EXPECTED: * 'In-Play & Live Stream' section is displayed at the top of the page **for desktop**
        """
        pass
