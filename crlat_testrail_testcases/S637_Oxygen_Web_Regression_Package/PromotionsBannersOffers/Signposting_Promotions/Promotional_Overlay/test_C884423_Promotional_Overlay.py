import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C884423_Promotional_Overlay(Common):
    """
    TR_ID: C884423
    NAME: Promotional Overlay
    DESCRIPTION: The purpose of this test case is to verify Promotional Overlay and its content
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: [BMA-22956 Promotional Overlay] [1]
    DESCRIPTION: [BMA-33420 Promo / Signposting : CMS Story for Promo Title and Text] [2]
    DESCRIPTION: [BMA-34455 Promo/Signposting: Pop-up: Customer no longer sees pop-ups appear as a Footer Banner] [3]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-22956
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-33420
    DESCRIPTION: [3]: https://jira.egalacoral.com/browse/BMA-34455
    PRECONDITIONS: This test case should be run for both Mobile and Tablet
    PRECONDITIONS: Make sure that there are promotion created in CMS and linked to active signposting promotions (by Event/Market Flags)
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/promotions
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: *NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_navigate_to_the_any_page_with_promo_signposting_and_tap_on_promo_signposting_icon(self):
        """
        DESCRIPTION: Navigate to the any page with Promo Signposting and tap on promo signposting icon
        EXPECTED: * Promo Signposting Pop-up appear
        EXPECTED: * 'MORE' button is present on pop-up
        EXPECTED: * 'OK' button is present on pop-up
        """
        pass

    def test_002_click_on_more_button_on_promo_pop_up(self):
        """
        DESCRIPTION: Click on 'MORE' button on Promo pop-up
        EXPECTED: 'Promotional overlay' is appear
        """
        pass

    def test_003_verify_promotional_overlay_content(self):
        """
        DESCRIPTION: Verify 'Promotional overlay' content
        EXPECTED: 'Promotional overlay' consists of:
        EXPECTED: *   'Promotion' title
        EXPECTED: *   'Promotion banner'
        EXPECTED: *   'Promotion main content'
        EXPECTED: *   'Promotion T&Cs'
        EXPECTED: *   'CTA Button'
        EXPECTED: *   'Close' button on Overlay header
        """
        pass

    def test_004_scroll_the_page(self):
        """
        DESCRIPTION: Scroll the page
        EXPECTED: * 'Promotion' title with 'Close' button & 'CTA Button' are sticky
        EXPECTED: * Everything else is scrollable (IE: Banner, Short description, Main content & T&Cs)
        """
        pass

    def test_005_verify_promotion_title(self):
        """
        DESCRIPTION: Verify Promotion title
        EXPECTED: * Promotion title is set in CMS ('Title' field)
        EXPECTED: * Promotion title is the same as on the main promotion's detail page
        """
        pass

    def test_006_verify_promotion_image(self):
        """
        DESCRIPTION: Verify Promotion image
        EXPECTED: * Promotion image is downloaded in CMS
        EXPECTED: * Promotion image is the same as on the main promotion's detail page
        """
        pass

    def test_007_verify_main_content(self):
        """
        DESCRIPTION: Verify Main content
        EXPECTED: * Promotion Main content is set in CMS
        EXPECTED: * Promotion Main content is the same as on the main promotion's detail page
        """
        pass

    def test_008_verify_short_description(self):
        """
        DESCRIPTION: Verify short description
        EXPECTED: * Short description is set in CMS ('Short description' field)
        EXPECTED: * Short description is the same as on the main promotion's detail page
        """
        pass

    def test_009_verify_tcs(self):
        """
        DESCRIPTION: Verify T&Cs
        EXPECTED: * T&C section is expanded by default
        EXPECTED: * Promotion T&Cs are set in CMS ('T&Cs' field)
        EXPECTED: * T&Cs is the same as on the main promotion's detail page
        """
        pass

    def test_010_verify_cta_button(self):
        """
        DESCRIPTION: Verify 'CTA' button
        EXPECTED: * "CTA" button is set in CMS
        EXPECTED: * By tapping on the 'CTA' button, user is navigated to the specific URL configured within CMS
        """
        pass

    def test_011_verify_close_button(self):
        """
        DESCRIPTION: Verify 'Close' button
        EXPECTED: * By tapping the 'Close' button the Overlay is closed
        """
        pass

    def test_012_repeat_steps_1_11_for_the_following_promotions___beaten_by_a_length___double_your_winnings___extra_place_race___your_call(self):
        """
        DESCRIPTION: Repeat steps 1-11 for the following promotions:
        DESCRIPTION: *   Beaten by a Length
        DESCRIPTION: *   Double your Winnings
        DESCRIPTION: *   Extra Place Race
        DESCRIPTION: *   Your Call
        EXPECTED: All promotions behave in the same way
        """
        pass

    def test_013_update__modify_a_promotions___title___image___short_description___main_content___tcs(self):
        """
        DESCRIPTION: Update & Modify a promotions':
        DESCRIPTION: *   Title
        DESCRIPTION: *   Image
        DESCRIPTION: *   Short Description
        DESCRIPTION: *   Main Content
        DESCRIPTION: *   T&Cs
        EXPECTED: All items are updated with the new content, after caching
        """
        pass
