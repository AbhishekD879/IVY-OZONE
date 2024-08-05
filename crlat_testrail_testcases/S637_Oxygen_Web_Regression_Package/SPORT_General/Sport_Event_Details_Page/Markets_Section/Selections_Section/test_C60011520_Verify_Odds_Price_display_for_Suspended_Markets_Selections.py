import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60011520_Verify_Odds_Price_display_for_Suspended_Markets_Selections(Common):
    """
    TR_ID: C60011520
    NAME: Verify Odds/Price display for Suspended Markets/Selections
    DESCRIPTION: Verify that price/odds button is displayed as SUSP, grayed out and disabled when the market or selection is suspended for any sport in both Landing page and Event details page.
    PRECONDITIONS: 1: Login to TI to trigger market or selection suspension
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_urlfor_mobile_app_launch_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral URL
        DESCRIPTION: For Mobile App: Launch the app
        EXPECTED: URL should be launched
        """
        pass

    def test_002_navigate_to_any_sport(self):
        """
        DESCRIPTION: Navigate to any <Sport>
        EXPECTED: User should be navigated to <Sport> landing page
        """
        pass

    def test_003_tap_event_name_or_more_link_on_the_event_section(self):
        """
        DESCRIPTION: Tap Event Name or 'More' link on the event section
        EXPECTED: User should be navigated to <Sport> event details page
        """
        pass

    def test_004_verify_data_of_priceodds_buttons_in_fractional_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds buttons in fractional format
        EXPECTED: 'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        """
        pass

    def test_005_login_to_ti_and_suspend_any_market_which_is_displayed_in_sport_event_details_pageindexphpattachmentsget120936825indexphpattachmentsget120936827(self):
        """
        DESCRIPTION: Login to TI and suspend any market which is displayed in <Sport> event details page
        DESCRIPTION: ![](index.php?/attachments/get/120936825)
        DESCRIPTION: ![](index.php?/attachments/get/120936827)
        EXPECTED: 1: The price/Odd button for the selection in the suspended market should be greyed out
        EXPECTED: 2: "SUSP" should be displayed
        EXPECTED: 3: The price/ odd button should be disabled
        """
        pass

    def test_006_click_on_the_suspended_selection(self):
        """
        DESCRIPTION: Click on the suspended selection
        EXPECTED: User should not be able to select the selection price
        """
        pass

    def test_007_verify_data_of_priceodds_buttons_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds buttons in Decimal format
        EXPECTED: 'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        """
        pass

    def test_008_login_to_ti_and_suspend_any_market_which_is_displayed_in_sport_event_details_pageindexphpattachmentsget120936825indexphpattachmentsget120936827(self):
        """
        DESCRIPTION: Login to TI and suspend any market which is displayed in <Sport> event details page
        DESCRIPTION: ![](index.php?/attachments/get/120936825)
        DESCRIPTION: ![](index.php?/attachments/get/120936827)
        EXPECTED: 1: The price/Odd button for the selection in the suspended market should be greyed out
        EXPECTED: 2: "SUSP" should be displayed
        EXPECTED: 3: The price/ odd button should be disabled
        """
        pass

    def test_009_click_on_the_suspended_selection(self):
        """
        DESCRIPTION: Click on the suspended selection
        EXPECTED: User should not be able to select the selection price
        """
        pass

    def test_010_login_to_ti_and_suspended_any_selection_in_a_market_which_is_displayed_in_sport_event_details_page(self):
        """
        DESCRIPTION: Login to TI and suspended any selection in a market which is displayed in <Sport> event details page
        EXPECTED: 1: The price/Odd button for the suspended selection should be greyed out
        EXPECTED: 2: "SUSP" should be displayed
        EXPECTED: 3: The price/ odd button should be disabled
        """
        pass

    def test_011_validate_for_both_in_play_and_pre_play_markets_for_all_sports_in_both_sport_landing_page_and_event_details_page(self):
        """
        DESCRIPTION: Validate for both In play and Pre-play markets for all Sports in both Sport Landing page and Event details page
        EXPECTED: 
        """
        pass
