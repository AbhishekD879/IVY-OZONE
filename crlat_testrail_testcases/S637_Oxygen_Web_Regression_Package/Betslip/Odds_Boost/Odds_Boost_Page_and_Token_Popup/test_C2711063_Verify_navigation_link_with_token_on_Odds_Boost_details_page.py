import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C2711063_Verify_navigation_link_with_token_on_Odds_Boost_details_page(Common):
    """
    TR_ID: C2711063
    NAME: Verify navigation link with token on Odds Boost details page
    DESCRIPTION: This test case verifies navigation link with token on Odds Boost details page
    PRECONDITIONS: 'Odds Boost' Feature Toggle is enabled in CMS
    PRECONDITIONS: Add Odds Boost tokens to user in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: - Odds Boost token available to Any bet
    PRECONDITIONS: - Odds Boost token available to some category, class or type hierarchy associated with it
    PRECONDITIONS: - Odds Boost token available to an event, market or selection hierarchy associated with it
    PRECONDITIONS: Hierarch value is selected while adding the Odds Boost token to the user in the Redemption Value field.
    PRECONDITIONS: NOTE: Appropriate values for category, type, class, event, market, selection should be added to 'Redemption Value'
    PRECONDITIONS: ![](index.php?/attachments/get/7078854)
    PRECONDITIONS: How to create Odds boost token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: How to create Upcoming Boosts https://confluence.egalacoral.com/display/SPI/How+to+create+Upcoming+Boosts
    PRECONDITIONS: Load application and Login into the application with user that has Odds Boost tokens available
    """
    keep_browser_open = True

    def test_001_navigate_to_the_odds_boost_information_page(self):
        """
        DESCRIPTION: Navigate to the Odds Boost information page
        EXPECTED: User is navigated to the Odds Boost information page
        """
        pass

    def test_002_tap_on_the_token_which_can_be_used_on_any_bet_token_which_is_added_for_any_bet(self):
        """
        DESCRIPTION: Tap on the token which can be used on ANY bet (token which is added for ANY bet)
        EXPECTED: User is navigated to the Homepage
        """
        pass

    def test_003_tap_on_the_token_which_has_a_category_class_or_type_hierarchy_associated_with_it(self):
        """
        DESCRIPTION: Tap on the token which has a category, class or type hierarchy associated with it
        EXPECTED: User is navigated to the respective sport landing page
        """
        pass

    def test_004_tap_on_token_which_has_an_event_market_or_selection_hierarchy_associated_with_it(self):
        """
        DESCRIPTION: Tap on token which has an event, market or selection hierarchy associated with it
        EXPECTED: User is navigated to the respective event detail page
        """
        pass
