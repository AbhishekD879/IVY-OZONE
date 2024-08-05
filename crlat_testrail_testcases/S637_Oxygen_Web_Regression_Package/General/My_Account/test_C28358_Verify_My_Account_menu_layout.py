import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C28358_Verify_My_Account_menu_layout(Common):
    """
    TR_ID: C28358
    NAME: Verify 'My Account' menu layout
    DESCRIPTION: This test case verifies 'My Account' menu layout.
    DESCRIPTION: **Note:**
    DESCRIPTION: My Account Menu or User Menu is handled and set on GVC side.
    PRECONDITIONS: 1. Load the application
    PRECONDITIONS: 2. Log in with valid credentials
    PRECONDITIONS: 3. Make sure that 'My Account' button is displayed on Header with 'FB' icon available when the user has free bets
    """
    keep_browser_open = True

    def test_001_clicktap_the_my_account_button_on_the_header(self):
        """
        DESCRIPTION: Click/Tap the 'My Account' button on the Header
        EXPECTED: Menu Overlay appears on full screen on Mobile and as a pop-up on Tablet/Desktop with next items (configurable on GVC side):
        EXPECTED: **Coral**
        EXPECTED: * 'Menu' title and 'Close' button
        EXPECTED: * Banking
        EXPECTED: * Offers & Free Bets
        EXPECTED: * History
        EXPECTED: * Messages
        EXPECTED: * Connect
        EXPECTED: * Settings
        EXPECTED: * Gambling Controls
        EXPECTED: * Help & Contact
        EXPECTED: * Log Out
        EXPECTED: * Green'DEPOSIT' button
        EXPECTED: ![](index.php?/attachments/get/115420225)
        EXPECTED: **Ladbrokes**
        EXPECTED: * 'Menu' title and 'Close' button
        EXPECTED: * Banking & Balances
        EXPECTED: * Promotions
        EXPECTED: * Odds Boosts
        EXPECTED: * Sports Free Bets
        EXPECTED: * My Bets
        EXPECTED: * Messages
        EXPECTED: * History
        EXPECTED: * The Grid
        EXPECTED: * Settings
        EXPECTED: * Gambling Controls
        EXPECTED: * Help & Contact
        EXPECTED: * Log Out
        EXPECTED: * Green'DEPOSIT' button
        EXPECTED: ![](index.php?/attachments/get/115420219)
        """
        pass

    def test_002_verify_every_item_view(self):
        """
        DESCRIPTION: Verify every item view
        EXPECTED: * Every item has an icon an is left aligned
        EXPECTED: * 'Offers & Free Bets' have 'FB' icon if user has freebets
        EXPECTED: * 'Messages' have counter badge if user has rich inbox messages unread
        EXPECTED: * Arrow is present from right side for items that have further pop-up/overlay navigation ( e.g. Banking,Offers & Free Bets,History,Connect,Settings)
        """
        pass
