import pytest
from faker import Faker

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.Promotions.BasePromotionTest import BasePromotionTest
from voltron.utils.helpers import cleanhtml


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot create promotions on PROD
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.cms
@pytest.mark.promotions
@pytest.mark.promotions_banners_offers
@vtest
class Test_C29317_Promotion_Details_page(BasePromotionTest):
    """
    TR_ID: C29317
    NAME: Promotion Details page
    DESCRIPTION: The purpose of this test case is to verify Promotions details page and its content
    PRECONDITIONS: Make sure that there are promotions in CMS
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/promotions
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    """
    keep_browser_open = True
    promo_page_title = vec.promotions.PROMOTIONS
    promo_title = promo_short_description = promo_description = promo_id = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: create test promotion in CMS
        """
        if tests.settings.cms_env == 'prd0':
            self._logger.warning('*** Skipping promotion creation since it is PROD')
        else:
            f = Faker()
            short_description = f.text(max_nb_chars=500).replace('\n', ' ')
            promotion = self.cms_config.add_promotion(shortDescription=short_description)
            self.__class__.promo_title, self.__class__.promo_short_description = \
                promotion.title.upper(), promotion.short_description
            self.__class__.promo_description, self.__class__.promo_id = \
                promotion.description.replace('\n', ' '), promotion.id

        if self.device_type == 'desktop' and self.brand == 'ladbrokes':
            self.__class__.promo_page_title = self.promo_page_title.title()

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('HomePage')

    def test_002_navigate_to_promotions_page(self):
        """
        DESCRIPTION: Navigate to 'Promotions' page
        EXPECTED: * 'Promotions' page is opened
        EXPECTED: * List of all available promotions is present
        """
        self.navigate_to_page(name='promotions/all')
        self.site.wait_content_state(state_name='promotions')

        self.__class__.promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(self.promotions,
                        msg='No promotions found on page')

    def test_003_click_or_tap_more_information_button(self):
        """
        DESCRIPTION: Click/Tap 'More information' button
        EXPECTED: Promotion Details page is opened
        """
        promotion = self.promotions.get(self.promo_title)
        self.assertTrue(promotion, msg=f'"{self.promo_title}" promotion not found on page')

        promotion.more_info_button.click()
        self.site.wait_content_state(state_name='PromotionDetails')

    def test_004_verify_promotion_details_page(self):
        """
        DESCRIPTION: Verify Promotion Details page
        EXPECTED: Promotion Details page consists of:
        EXPECTED: *   'Back' button
        EXPECTED: *   **'Promotions'** page title
        EXPECTED: *   Section title
        EXPECTED: *   Promotion image
        EXPECTED: *   Promotion description
        EXPECTED: *   'Terms and Conditions' panel
        """
        promotion_details = self.site.promotion_details
        self.assertTrue(promotion_details,
                        msg=f'"{self.promo_title}" promotion details page was not found')

        self.assertTrue(self.site.has_back_button, msg='Back Button is not displayed on Promotions page')

        promotion_page_title = promotion_details.content_title_text
        self.assertTrue(promotion_details.content_title_text,
                        msg=f'"{self.promo_page_title}" page title is not displayed')
        self.assertEqual(promotion_page_title, self.promo_page_title,
                         msg=f'\nActual page title: \n"{promotion_page_title}" '
                         f'\nis not as expected: \n"{self.promo_page_title}')

        promotion_description = promotion_details.tab_content.promotion
        has_image = promotion_description.has_image
        self.assertTrue(has_image,
                        msg=f'"{self.promo_title}" promotion has no image')

        detail_description = promotion_description.detail_description
        self.assertTrue(detail_description,
                        msg=f'"{self.promo_title}" promotion has no description')

        terms_and_conditions = promotion_details.tab_content.terms_and_conditions
        terms_and_conditions_title = terms_and_conditions.name
        self.assertTrue(terms_and_conditions,
                        msg=f'"{self.promo_title}" promotion has no "{terms_and_conditions_title}" section')

    def test_005_verify_back_button(self):
        """
        DESCRIPTION: Verify 'Back' button
        EXPECTED: By clicking/tapping the 'Back' button user is navigated to the previous page
        """
        self.site.back_button_click()
        self.site.wait_content_state(state_name='promotions')

        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(self.promotions,
                        msg='No promotions found on page')

        promotion = promotions.get(self.promo_title)
        self.assertTrue(promotion, msg=f'"{self.promo_title}" promotion not found on page')

        promotion.more_info_button.click()
        self.site.wait_content_state(state_name='PromotionDetails')

    def test_006_verify_section_title(self):
        """
        DESCRIPTION: Verify Section title
        EXPECTED: * Section title is set in CMS ('Title' field)
        EXPECTED: * Accordion is expanded by default
        EXPECTED: * Section title is displayed on expandable/collapsible accordion
        """
        self.__class__.promotion_details = self.site.promotion_details.tab_content.promotion
        self.assertTrue(self.promotion_details,
                        msg=f'"{self.promo_title}" promotion details page was not found')

        promotion_title = self.promotion_details.name
        self.assertEqual(promotion_title, self.promo_title,
                         msg=f'\nActual promotion title: \n"{promotion_title}" '
                         f'\nis not as expected: \n"{self.promo_title}"')

        self.assertTrue(self.promotion_details.is_expanded(),
                        msg='Promotion details section is not expanded')

        self.promotion_details.collapse()
        self.assertFalse(self.promotion_details.is_expanded(expected_result=False, timeout=3),
                         msg='Promotion details section is not collapsed')

        self.promotion_details.expand()
        self.assertTrue(self.promotion_details.is_expanded(timeout=3),
                        msg=f'"{self.promotion_details.name}" section is not expanded')

    def test_007_verify_promotion_image(self):
        """
        DESCRIPTION: Verify Promotion image
        EXPECTED: Promotion image is downloaded in CMS
        """
        self.assertTrue(self.promotion_details.has_image,
                        msg=f'"{self.promo_title}" has no image')

    def test_008_verify_promotion_description(self):
        """
        DESCRIPTION: Verify Promotion description
        EXPECTED: Promotion description is set in CMS ('Description' field)
        """
        promotion_description = self.promotion_details.detail_description
        self.assertTrue(promotion_description,
                        msg=f'"{self.promo_title}" promotion description not found')
        self.assertEqual(promotion_description.text, self.promo_description,
                         msg=f'\nActual promotion description: \n"{promotion_description.text}" '
                         f'\nis not as expected: \n"{self.promo_description}"')

    def test_009_verify_terms_and_conditions_panel(self):
        """
        DESCRIPTION: Verify 'Terms and Conditions' panel
        EXPECTED: * 'Terms and Conditions' panel is configured in CMS ('T&C' field)
        EXPECTED: * 'Terms and Conditions' panel is expanded by default
        EXPECTED: * 'Terms and Conditions' panel is expandable/collapsible
        """
        terms_and_conditions = self.site.promotion_details.tab_content.terms_and_conditions
        self.assertTrue(terms_and_conditions,
                        msg=f'"{terms_and_conditions.name}" section not found on page')
        self.assertTrue(terms_and_conditions.details,
                        msg=f'"{terms_and_conditions.name}" section is empty')

        promotion = self.cms_config.get_promotion(promotion_id=self.promo_id)
        actual_terms = cleanhtml(terms_and_conditions.details)
        expected_terms = cleanhtml(promotion['htmlMarkup'])
        self.assertEqual(actual_terms, expected_terms,
                         msg=f'\nActual T&C text: \n"{actual_terms}" '
                         f'\nis not as expected: \n"{expected_terms}"')

        self.assertTrue(terms_and_conditions.is_expanded(),
                        msg=f'"{terms_and_conditions.name}" section is not expanded')

        terms_and_conditions.collapse()
        self.assertFalse(terms_and_conditions.is_expanded(expected_result=False, timeout=3),
                         msg=f'"{terms_and_conditions.name}" section is not collapsed')

        terms_and_conditions.expand()
        self.assertTrue(terms_and_conditions.is_expanded(timeout=3),
                        msg=f'"{terms_and_conditions.name}" section is not expanded')
