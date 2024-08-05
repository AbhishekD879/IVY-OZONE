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
class Test_C44870267_Verify_Odds_boost_page_below__User_can_navigate_to_Odds_boost_page_through_See_more_button_click_on_banner_and_My_Account_Odds_boost_menu_Odds_boost_page_logo_and_hard_corded_messages_Terms_and_conditions_section_Verify_token_display_order_(Common):
    """
    TR_ID: C44870267
    NAME: "Verify Odds boost page below  - User can navigate to Odds boost page through 'See more' button click on banner and My Account >Odds boost menu -Odds boost page logo and hard corded messages -Terms and conditions section -Verify token display order (
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_navigate_to_the_odds_boost_information_page(self):
        """
        DESCRIPTION: Navigate to the Odds Boost information page
        EXPECTED: User is navigated to the Odds Boost information page
        EXPECTED: User can navigate to Odds boost page through 'show more' button click on banner and My Account >Odds boost menu
        EXPECTED: -Odds boost page logo and hard corded messages
        EXPECTED: -Terms and conditions section
        """
        pass

    def test_002_tap_on_generic_token_which_can_be_used_on_any_bet(self):
        """
        DESCRIPTION: Tap on generic token which can be used on ANY bet
        EXPECTED: User is navigated to the homepage
        """
        pass

    def test_003_tap_on_generic_token_which_has_a_category_class_or_type_hierarchy_associated_with_it(self):
        """
        DESCRIPTION: Tap on generic token which has a category, class or type hierarchy associated with it
        EXPECTED: User is navigated to the respective category landing page
        """
        pass

    def test_004_tap_on_token_which_has_an_event_market_or_selection_hierarchy_associated_with_it(self):
        """
        DESCRIPTION: Tap on token which has an event, market or selection hierarchy associated with it
        EXPECTED: User is navigated to the respective event detail page
        """
        pass
