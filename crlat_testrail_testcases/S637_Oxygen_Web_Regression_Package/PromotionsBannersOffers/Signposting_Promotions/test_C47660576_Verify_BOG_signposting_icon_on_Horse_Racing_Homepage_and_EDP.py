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
class Test_C47660576_Verify_BOG_signposting_icon_on_Horse_Racing_Homepage_and_EDP(Common):
    """
    TR_ID: C47660576
    NAME: Verify "BOG" signposting icon on Horse Racing Homepage and EDP
    DESCRIPTION: This test case verifies "BOG" signposting icon on Horse Racing  event level
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: [BMA-49331] [1]
    DESCRIPTION: [1]:https://jira.egalacoral.com/browse/BMA-49331
    PRECONDITIONS: - BOG icon has been enabled in CMS
    PRECONDITIONS: - Events with market configured to show BOG flag available (Market should have 'GP Available' and 'LP Available' checkmarks)
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racing_homepage(self):
        """
        DESCRIPTION: Navigate to Horse Racing homepage
        EXPECTED: * BOG icon is displayed on the right side of Race Grid
        EXPECTED: Ladbrokes designs:
        EXPECTED: https://app.zeplin.io/project/5dca842a25a59d8e77bdad7f/dashboard
        EXPECTED: Coral designs:
        EXPECTED: https://app.zeplin.io/project/5de6962b0c68b753005a2b58/dashboard
        """
        pass

    def test_002_navigate_to_event_with_bog_icon(self):
        """
        DESCRIPTION: Navigate to Event with BOG icon
        EXPECTED: * BOG icon is displayed on top Horse Racing EDP
        """
        pass

    def test_003_return_to_horse_racing_homepage(self):
        """
        DESCRIPTION: Return to Horse Racing homepage
        EXPECTED: * BOG icon is remains displayed on the right side of Race Grid
        """
        pass

    def test_004_navigate_to_event_without_bog_icon(self):
        """
        DESCRIPTION: Navigate to Event without BOG icon
        EXPECTED: * BOG icon is NOT displayed on top of event header
        """
        pass
