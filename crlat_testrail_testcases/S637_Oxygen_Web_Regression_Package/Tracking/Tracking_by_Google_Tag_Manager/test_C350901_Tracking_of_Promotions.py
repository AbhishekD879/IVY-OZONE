import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C350901_Tracking_of_Promotions(Common):
    """
    TR_ID: C350901
    NAME: Tracking of Promotions
    DESCRIPTION: This test case verifies tracking on 'Promotion' page
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. Browser console should be opened
    PRECONDITIONS: 3. Promotions are configured in CMS (Link to DEV CMS: https://invictus.coral.co.uk/keystone/)
    PRECONDITIONS: Test case should be run on Mobile/Tablet/Desktop
    PRECONDITIONS: **Note**:
    PRECONDITIONS: All embedded videos cannot be tracked
    """
    keep_browser_open = True

    def test_001_navigate_to_promotions_page(self):
        """
        DESCRIPTION: Navigate to 'Promotions' page
        EXPECTED: 'Promotions' page is opened
        """
        pass

    def test_002_select_any_promotion_and_click_more_information_button(self):
        """
        DESCRIPTION: Select any promotion and click 'More information' button
        EXPECTED: Page for selected promotion is opened
        """
        pass

    def test_003_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: Objects are displayed within Console window
        """
        pass

    def test_004_expand_corresponding_object(self):
        """
        DESCRIPTION: Expand corresponding object
        EXPECTED: The next static parameters are present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'promotions',
        EXPECTED: 'eventAction' : 'cta click',
        EXPECTED: 'eventLabel' : '<< PROMOTION NAME >>', (The title of the promotion)
        EXPECTED: 'vipLevel' : '<< VIP LEVEL >>', (VIP level of logged in user)
        EXPECTED: 'promoAction' : '<< BUTTON TEXT >>' (i.e more information)
        EXPECTED: });
        EXPECTED: NOTE: All custom values are sent in lowercase and without underscore
        """
        pass

    def test_005_click_any_button_if_present_on_page_for_selected_promotion(self):
        """
        DESCRIPTION: Click any button (if present) on page for selected promotion
        EXPECTED: 
        """
        pass

    def test_006_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: Objects are displayed within Console window
        """
        pass

    def test_007_expand_corresponding_object(self):
        """
        DESCRIPTION: Expand corresponding object
        EXPECTED: The next static parameters are present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'promotions',
        EXPECTED: 'eventAction' : 'link click',
        EXPECTED: 'eventLabel' : '<< PROMOTION NAME >>', (The title of the promotion)
        EXPECTED: 'vipLevel' : '<< VIP LEVEL >>', (VIP level of logged in user)
        EXPECTED: 'promoAction' : '<< LINK TEXT >>' (link text on clicked button i.e bet now, more info)
        EXPECTED: });
        EXPECTED: NOTE: All custom values are sent in lowercase and without underscore
        """
        pass

    def test_008_click_any_link_if_present_on_page_for_selected_promotion(self):
        """
        DESCRIPTION: Click any link (if present) on page for selected promotion
        EXPECTED: 
        """
        pass

    def test_009_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: Objects are displayed within Console window
        """
        pass

    def test_010_expand_corresponding_object(self):
        """
        DESCRIPTION: Expand corresponding object
        EXPECTED: The next static parameters are present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'promotions',
        EXPECTED: 'eventAction' : 'link click',
        EXPECTED: 'eventLabel' : '<< PROMOTION NAME >>', (The title of the promotion)
        EXPECTED: 'vipLevel' : '<< VIP LEVEL >>', (VIP level of logged in user)
        EXPECTED: 'promoAction' : '<< LINK TEXT >>' (url address of clicked hyperlink)
        EXPECTED: });
        EXPECTED: NOTE: All custom values are sent in lowercase and without underscore
        """
        pass

    def test_011_click_any_banner_image_if_present_on_page_for_selected_promotion(self):
        """
        DESCRIPTION: Click any banner image (if present) on page for selected promotion
        EXPECTED: 
        """
        pass

    def test_012_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: * Objects are displayed within Console window
        EXPECTED: * There is no object for not clickable banner within 'Promotions' page
        """
        pass

    def test_013_log_out_user_from_oxygen_application(self):
        """
        DESCRIPTION: Log out user from Oxygen application
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps_1_12(self):
        """
        DESCRIPTION: Repeat steps #1-12
        EXPECTED: Results are the same, but 'vipLevel' field is blank
        """
        pass
