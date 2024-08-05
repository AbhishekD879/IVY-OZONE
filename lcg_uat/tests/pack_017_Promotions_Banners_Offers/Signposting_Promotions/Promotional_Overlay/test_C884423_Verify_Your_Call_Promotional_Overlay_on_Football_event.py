import html
import pytest
import voltron.environments.constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.helpers import cleanhtml, normalize_name
from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.Promotions.BasePromotionTest import BasePromotionTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.cms
@pytest.mark.promotions
@pytest.mark.promotions_banners_offers
@vtest
class Test_C884423_Verify_Your_Call_Overlay_on_Race_event(BaseSportTest, BaseRacing, BasePromotionTest):
    """
    TR_ID: C884423
    NAME: Verify 'Your Call' Promotional Overlay on Race_event
    DESCRIPTION: The purpose of this test case is to verify Promotional Overlay and its content
    PRECONDITIONS: This test case should be run for both Mobile and Tablet
    PRECONDITIONS: Make sure that there are promotion created in CMS and linked to active signposting promotions (by Event/Market Flags)
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/promotions
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    """
    keep_browser_open = True
    promo_name = 'Your call'
    event_level_flag, market_level_flag = 'EVFLAG_YC', 'MKTFLAG_YC'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event with promotions
        """
        self.__class__.promo_key = self.cms_config.constants.PROMO_KEY_YOUR_CALL
        dialog_name = self.get_promotion_details_from_cms(event_level_flag=self.event_level_flag,
                                                          market_level_flag=self.market_level_flag)['popupTitle'].upper()
        vec.dialogs.DIALOG_MANAGER_YOUR_CALL = vec.dialogs.DIALOG_MANAGER_YOUR_CALL.format(dialog_name.strip())

        event = self.ob_config.add_autotest_premier_league_football_event(your_call=True)
        self.__class__.eventID = event.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.today_event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.today_event_name}"')

        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

    def test_001_navigate_to_any_page_with_promo_signposting_and_tap_on_promo_icon(self):
        """
        DESCRIPTION: Navigate to the any page with Promo Signposting and tap on promo signposting icon
        EXPECTED: * Promo Signposting Pop-up appear
        EXPECTED: * 'MORE' button is present on pop-up
        EXPECTED: * 'OK' button is present on pop-up
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')

        event = self.get_event_from_league(section_name=self.section_name, event_id=self.eventID)

        event.scroll_to()
        self.assertTrue(event.promotion_icons.has_your_call(),
                        msg=f'"{self.promo_name}" promotion icon is not shown')

        event.promotion_icons.your_call.click()

        self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_YOUR_CALL, timeout=2)
        self.assertTrue(self.dialog, msg=f'"{self.promo_name}" promotion dialog is not shown')

        self.assertTrue(self.dialog.more_button.is_displayed(), msg='"MORE" button is not displayed')
        self.assertTrue(self.dialog.ok_button.is_displayed(), msg='"OK" button is not displayed')

    def test_002_click_on_more_button_on_promo_pop_up(self):
        """
        DESCRIPTION: Click on 'MORE' button on Promo pop-up
        EXPECTED: 'Promotional overlay' is appear
        """
        self.dialog.more_button.click()

        self.__class__.promotion_overlay = self.site.promotion_overlay
        self.assertTrue(self.promotion_overlay, msg='"Promotion overlay" is not shown')

    def test_003_scroll_the_page(self):
        """
        DESCRIPTION: Scroll the page
        EXPECTED: * 'Promotion' title with 'Close' button & 'CTA' Button' are sticky
        EXPECTED: * Everything else is scrollable (IE: Banner, Short description, Main content & T&Cs)
        """
        self.promotion_overlay.details.terms_and_conditions.scroll_to()

        self.assertTrue(self.promotion_overlay.header.close_button.is_displayed(),
                        msg='"Close" button is not sticky')
        self.assertTrue(self.promotion_overlay.details.bet_now_button.is_displayed(),
                        msg='"Bet Now" button is not sticky')

    def test_004_verify_promotion_title(self):
        """
        DESCRIPTION: Verify Promotion title
        EXPECTED: * Promotion title is set in CMS ('Title' field)
        EXPECTED: * Promotion title is the same as on the main promotion's detail page
        """
        self.__class__.promo_details = self.get_promotion_details_from_cms(event_level_flag=self.event_level_flag,
                                                                           market_level_flag=self.market_level_flag)

        actual_promo_title = self.promotion_overlay.header.title
        expected_promo_title = self.promo_details['title'].upper()
        self.assertEqual(actual_promo_title, expected_promo_title,
                         msg=f'Actual Promotion title: "{actual_promo_title}" '
                         f'is not as expected: "{expected_promo_title}"')

    def test_005_verify_promotion_image(self):
        """
        DESCRIPTION: Verify Promotion image
        EXPECTED: * Promotion image is downloaded in CMS
        EXPECTED: * Promotion image is the same as on the main promotion's detail page
        """
        expected_promo_banner = self.promo_details['uriMedium'] or self.promo_details['directFileUrl']
        if expected_promo_banner:
            actual_promo_banner = self.site.promotion_overlay.details.image_source
            self.assertIn(expected_promo_banner, actual_promo_banner,
                          msg=f'Actual Promotion banner image: "{actual_promo_banner}" '
                              f'is not as expected: "{expected_promo_banner}"')
        else:
            self._logger.warning('*** Promotion image is not configured in cms')

    def test_006_verify_main_content(self):
        """
        DESCRIPTION: Verify Main content
        EXPECTED: * Promotion Main content is set in CMS
        EXPECTED: * Promotion Main content is the same as on the main promotion's detail page
        """
        actual_promo_description = self.promotion_overlay.details.description.replace(' ', '')
        promo_description = html.unescape(cleanhtml(self.promo_details['description']))
        expected_promo_description = promo_description.strip().replace('\r', '').replace('\n', '').replace(' ', '')
        self.assertEqual(actual_promo_description, expected_promo_description,
                         msg=f'Actual Promotion main content: "{actual_promo_description}" '
                         f'is not as expected: "{expected_promo_description}"')

    def test_007_verify_short_description(self):
        """
        DESCRIPTION: Verify short description
        EXPECTED: * Short description is set in CMS ('Short description' field)
        EXPECTED: * Short description is the same as on the main promotion's detail page
        """
        actual_promo_short_description = self.promotion_overlay.details.short_description
        expected_promo_short_description = cleanhtml(self.promo_details['shortDescription']).upper()
        self.assertEqual(actual_promo_short_description, expected_promo_short_description,
                         msg=f'Actual Promotion description: "{actual_promo_short_description}" '
                         f'is not as expected: "{expected_promo_short_description}"')

    def test_008_verify_terms_and_conditions(self):
        """
        DESCRIPTION: Verify T&Cs
        EXPECTED: * T&C section is expanded by default
        EXPECTED: * Promotion T&Cs are set in CMS ('T&Cs' field)
        EXPECTED: * T&Cs is the same as on the main promotion's detail page
        """
        promo_terms_section = self.promotion_overlay.details.terms_and_conditions
        self.assertTrue(promo_terms_section.is_expanded(), msg='Promotion "Terms & Conditions" section is not expanded')

        actual_promo_terms = cleanhtml(promo_terms_section.content).replace(' ', '')
        promo_terms = html.unescape(cleanhtml(self.promo_details['htmlMarkup']))
        expected_promo_terms = promo_terms.strip().replace('\r', '').replace('\n', '').replace(' ', '')
        self.assertEqual(actual_promo_terms, expected_promo_terms,
                         msg=f'Actual Promotion title: "{actual_promo_terms}" '
                         f'is not as expected: "{expected_promo_terms}"')

    def test_009_verify_cta_button(self):
        """
        DESCRIPTION: Verify 'CTA' button
        EXPECTED: * "CTA" button is set in CMS
        EXPECTED: * By tapping on the 'CTA' button, user is navigated to the specific URL configured within CMS
        """
        bet_now_button = self.promotion_overlay.details.bet_now_button
        self.assertTrue(bet_now_button.is_displayed(), msg=f'"{bet_now_button.name}" button is not displayed')

        expected_url = bet_now_button.href
        bet_now_button.click()

        result = wait_for_result(lambda: expected_url in self.device.get_current_url(),
                                 name='Page URL to change', timeout=2)
        self.assertTrue(result, msg=f'Actual page URL:"{self.device.get_current_url()}" '
                                    f'is not as expected: "{expected_url}"')

    def test_010_verify_close_button(self):
        """
        DESCRIPTION: Verify 'Close' button
        EXPECTED: * By tapping the 'Close' button the Overlay is closed
        """
        self.test_001_navigate_to_any_page_with_promo_signposting_and_tap_on_promo_icon()
        self.test_002_click_on_more_button_on_promo_pop_up()

        promo_close_button = self.promotion_overlay.header.close_button
        self.assertTrue(promo_close_button.is_displayed(), msg='Promotion "Close" button is not displayed')

        promo_close_button.click()
        self.site.wait_content_state(state_name='Football')
