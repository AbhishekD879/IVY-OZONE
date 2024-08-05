import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C2555577_Verify_Odd_Boost_pop_up_notification_for_the_user_with_different_Offer_ID_configuration(Common):
    """
    TR_ID: C2555577
    NAME: Verify 'Odd Boost' pop-up notification for the user with different  'Offer ID' configuration
    DESCRIPTION: This test case verifies User closes login notification
    PRECONDITIONS: Enable "Odds Boost" Feature Toggle in CMS > Odds Boost
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Load app
    """
    keep_browser_open = True

    def test_001_log_in_to_application_by_user_with_generated_odds_boost_token(self):
        """
        DESCRIPTION: Log in to Application by user with generated Odds boost token
        EXPECTED: * User is logged in successfully
        EXPECTED: * OddsBoost token ID is displayed in Local storage
        EXPECTED: * The "Odds Boost" token notification is displayed
        EXPECTED: * ContentText1:'You have 1 Odds Boost available' (1 is a value specific to the user as fetched on login)
        EXPECTED: * On the login journey, this should be **last** notification in the queue to appear - after any login messages, onboarding, touch ID etc.
        """
        pass

    def test_002_log_out_from_application(self):
        """
        DESCRIPTION: Log Out from application
        EXPECTED: User is logged out
        """
        pass

    def test_003_login_into_application_by_the_same_user_and_verify_that_odds_boost_token_notification_is_not_displaying(self):
        """
        DESCRIPTION: Login into Application by the same user and verify that "Odds Boost" token notification is NOT displaying
        EXPECTED: * User is logged in successfully
        EXPECTED: * The "Odds Boost" token notification is not displayed
        """
        pass

    def test_004_log_out_from_application(self):
        """
        DESCRIPTION: Log Out from application
        EXPECTED: User is logged out
        """
        pass

    def test_005_add_new_odds_boost_token_for_the_same_user_in_httpbackoffice_tst2coralcoukoffice_see_precondition(self):
        """
        DESCRIPTION: Add New Odds Boost token for the same user in http://backoffice-tst2.coral.co.uk/office (see precondition)
        EXPECTED: New Odds Boost token is added for this user
        """
        pass

    def test_006_login_into_application_with_the_same_user(self):
        """
        DESCRIPTION: Login into Application with the same user
        EXPECTED: * The "Odds Boost" token notification is displayed
        EXPECTED: * ContentText1:'You have 2 Odds Boost available' (2 is a value specific to the user as fetched on login)
        EXPECTED: * New Odd Boost OfferId (added in backoffice) is saved in Local Storage under the previous one
        """
        pass
