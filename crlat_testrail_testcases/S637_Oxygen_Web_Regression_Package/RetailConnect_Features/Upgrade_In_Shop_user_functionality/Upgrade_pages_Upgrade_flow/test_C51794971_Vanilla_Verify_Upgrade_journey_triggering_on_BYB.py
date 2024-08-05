import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C51794971_Vanilla_Verify_Upgrade_journey_triggering_on_BYB(Common):
    """
    TR_ID: C51794971
    NAME: [Vanilla] Verify Upgrade journey triggering on BYB
    DESCRIPTION: This test case verifies triggering of the Upgrade Pop-up when the In-Shop user attempts to place a BYB
    PRECONDITIONS: - In-Shop user (card number and pin) are available
    PRECONDITIONS: - BYB events are present (Bet Builder for Ladbrokes)
    PRECONDITIONS: ---
    PRECONDITIONS: User type ('In-shop', 'Online', 'Multi-channel') received in https://{env}/en/api/clientconfig/partial?configNames=vnUser&configNames=vnClaims in
    PRECONDITIONS: "http://api.bwin.com/v3/user/accBusinessPhase:" attribute after login and stored in local storage > OX.USER > accountBusinessPhase attribute
    PRECONDITIONS: ![](index.php?/attachments/get/74407650) ![](index.php?/attachments/get/74407651)
    PRECONDITIONS: ---
    PRECONDITIONS: 'In-Shop' - user with card number and pin (The Grid - Ladbrokes; Connect - Coral).
    PRECONDITIONS: 'Online' - user with username and password.
    PRECONDITIONS: 'Multi-channel' - user who was 'In-Shop' and is upgraded to 'Online' (e.g. has both card#/pin and username/password)
    PRECONDITIONS: ---
    PRECONDITIONS: Contact Venugopal Rao Joshi in order to generate In-Shop users for Ladbrokes brand (currently no known flows to generate In-Shop users for Coral)
    """
    keep_browser_open = True

    def test_001_login_with_in_shop_user(self):
        """
        DESCRIPTION: Login with In-Shop user
        EXPECTED: User is logged in
        """
        pass

    def test_002_navigate_to_byb_bet_builder_event__add_selections_and_try_to_place_bet(self):
        """
        DESCRIPTION: Navigate to BYB (Bet Builder) event / add selections and try to place bet
        EXPECTED: Upgrade pop-up/journey is triggered
        """
        pass

    def test_003_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: User is logged out
        """
        pass

    def test_004_navigate_to_byb_bet_builder_event__add_selections_and_try_to_place_bet(self):
        """
        DESCRIPTION: Navigate to BYB (Bet Builder) event / add selections and try to place bet
        EXPECTED: Login form displayed
        """
        pass

    def test_005_login_with_in_shop_user(self):
        """
        DESCRIPTION: Login with In-Shop user
        EXPECTED: Upgrade pop-up/journey is triggered
        """
        pass
