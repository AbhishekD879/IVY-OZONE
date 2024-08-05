import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C12834350_Tracking_of_adding_selections_to_Quickbet_using_Reuse_Selection_button(Common):
    """
    TR_ID: C12834350
    NAME: Tracking of adding selections to Quickbet using 'Reuse Selection' button
    DESCRIPTION: This test case verifies adding of selections to Betslip using 'Reuse Selection' button
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Quick Bet GA tracking documentation: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91470520
    PRECONDITIONS: - Quick bet should be enabled in CMS &gt; System Configuration &gt; Structure &gt; quickBet
    PRECONDITIONS: - You should be logged in and have a bet placed via quickBet
    """
    keep_browser_open = True

    def test_001___type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: - Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: dataLayer.push{
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "add to quickbet"
        EXPECTED: eventCategory: "quickbet"
        EXPECTED: eventLabel: "success"
        EXPECTED: ecommerce.add.products{
        EXPECTED: brand: "&lt;&lt;EVENT_MARKET&gt;&gt;"
        EXPECTED: category: "&lt;&lt;OPENBET_SPORT_CATEGORY_ID&gt;&gt;"
        EXPECTED: dimension60: "&lt;&lt;EVENT_ID&gt;&gt;"
        EXPECTED: dimension61: "&lt;&lt;SELECTION_ID&gt;&gt;"
        EXPECTED: dimension62: "&lt;&lt;IN-PLAY_STATUS&gt;&gt;"
        EXPECTED: dimension63: "&lt;&lt;CUSTOMER BUILT&gt;&gt;"
        EXPECTED: dimension64: "&lt;&lt;LOCATION&gt;&gt;"
        EXPECTED: dimension65: "&lt;&lt;MODULE&gt;&gt;"
        EXPECTED: name: "&lt;&lt;EVENT_NAME&gt;&gt;"
        EXPECTED: variant: "&lt;&lt;OPENBET_TYPE_ID&gt;&gt;"
        EXPECTED: }}
        """
        pass
