import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2604118_Coral_Only_Shop_locator_map(Common):
    """
    TR_ID: C2604118
    NAME: [Coral Only] Shop locator map
    DESCRIPTION: This test case verifies integrating third-party Shop Locator into Sportsbook.
    DESCRIPTION: Info:
    DESCRIPTION: 'In-Shop' - user with card number and pin (The Grid - Ladbrokes; Connect - Coral).
    DESCRIPTION: 'Online' - user with username and password.
    DESCRIPTION: 'Multi-channel' - user who was 'In-Shop' and is upgraded to 'Online' (e.g. has both card#/pin and username/password)
    PRECONDITIONS: A user has opened the Shop Locator
    PRECONDITIONS: The way to get to Shop Locator:
    PRECONDITIONS: Open SB app -> Sports Menu Ribbon -> 'A-Z Sports' button -> Connect -> Shop Locator
    PRECONDITIONS: Open SB app -> Sports Menu Ribbon -> Connect -> Shop Locator
    PRECONDITIONS: Open SB app -> Right Hand Menu -> Connect -> Shop Locator (For logged in user)
    PRECONDITIONS: Contact GVC (Venugopal Rao Joshi / Abhinav Goel) and/or Souparna Datta + Oksana Tkach in order to generate In-Shop users
    """
    keep_browser_open = True

    def test_001_open_shop_locator(self):
        """
        DESCRIPTION: Open Shop Locator
        EXPECTED: Shop locator screen is opened:
        EXPECTED: * Breadcrumb shows '<' and 'Shop Locator'
        EXPECTED: * A search box with default value 'NW1', 'Near me' button, and 'List ' button are under 'Shop Locator' title
        EXPECTED: * A map is opened on 'NW1' location by default
        EXPECTED: Note! User is asked for access to the user's location in IOS. If he allowed, there is no default value 'NW1' in Shop locator and current user position is displayed on the map (the same behavior in Ladbrokes The Grid Shop Locator for IOS)
        """
        pass
