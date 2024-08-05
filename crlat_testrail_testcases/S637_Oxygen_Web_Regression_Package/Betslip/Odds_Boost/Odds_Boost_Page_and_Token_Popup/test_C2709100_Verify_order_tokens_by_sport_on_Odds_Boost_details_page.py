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
class Test_C2709100_Verify_order_tokens_by_sport_on_Odds_Boost_details_page(Common):
    """
    TR_ID: C2709100
    NAME: Verify order tokens by sport on Odds Boost details page
    DESCRIPTION: This test case verifies order tokens by sport on Odds Boost details page
    PRECONDITIONS: 'Odds Boost' Feature Toggle is enabled in CMS
    PRECONDITIONS: Add Odds Boost tokens to user in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: There should be tokens added for **ANY** and for **different sport categories**. This value is selected while adding the Odds Boost token to the user in the Redemption Value field.
    PRECONDITIONS: NOTE: Appropriate Sport Categories values should be added to 'Redemption Value'
    PRECONDITIONS: ![](index.php?/attachments/get/7078854)
    PRECONDITIONS: How to create Odds boost token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: How to create Upcoming Boosts https://confluence.egalacoral.com/display/SPI/How+to+create+Upcoming+Boosts
    PRECONDITIONS: Login into the application with User that has Odds Boost tokens available
    """
    keep_browser_open = True

    def test_001_navigate_to_the_odds_boost_page(self):
        """
        DESCRIPTION: Navigate to the Odds Boost page
        EXPECTED: - User is navigated to the Odds Boost page
        EXPECTED: - The tokens are displayed
        EXPECTED: - Tokens are segmented by 'Boosts Available now' and 'Upcoming Boosts'
        """
        pass

    def test_002_verify_that_tokens_are_segmented_by_sport_category_under_the_now__upcoming_segments(self):
        """
        DESCRIPTION: Verify that tokens are segmented by sport category under the now & upcoming segments
        EXPECTED: Tokens are segmented by sport on now & upcoming segments:
        EXPECTED: - Tokens are shown under the Sports category title appropriate to Sport category in Redemption Value
        EXPECTED: - Tokens for ANY are shown on the top without sport tittle
        EXPECTED: ![](index.php?/attachments/get/7078855)
        EXPECTED: ![](index.php?/attachments/get/7078856)
        """
        pass

    def test_003_verify_that_sport_headers_contain_sports_name_for_now__upcoming_segments(self):
        """
        DESCRIPTION: Verify that sport headers contain sports name for now & upcoming segments
        EXPECTED: Sport headers are displayed as per site - contain sport name for now & upcoming segments
        """
        pass

    def test_004_verify_that_sport_is_ordered_as_per_openbet_display_order_for_now__upcoming_segments(self):
        """
        DESCRIPTION: Verify that sport is ordered as per Openbet display order for now & upcoming segments
        EXPECTED: Sport is ordered as per Openbet display order according to Category_ID for now & upcoming segments
        EXPECTED: The higher ID the higher category
        """
        pass

    def test_005_verify_that__tokens_for_any_event_are_displayed_at_the_top_of_appropriate_available_now__upcoming_segments(self):
        """
        DESCRIPTION: Verify that  tokens for ANY event are displayed at the top of appropriate available now & upcoming segments
        EXPECTED: - Available now boosts tokens with ANY category are displayed at the top of 'available now' segment
        EXPECTED: - Upcoming boosts tokens with ANY category are displayed at the top of 'upcoming' segment
        """
        pass
