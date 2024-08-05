import pytest
import time
from faker import Faker

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.user_journey_promo_2
@pytest.mark.cms
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.promotions
@pytest.mark.promotions_banners_offers
@vtest
class Test_C29316_Promotions_Page(BaseUserAccountTest):
    """
    TR_ID: C29316
    NAME: Promotions page
    DESCRIPTION: The purpose of this test case is to verify Promotions page and its content
    """
    keep_browser_open = True
    promotion_title = promo_short_description = promo_id = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create Promotion in CMS
        """
        if tests.settings.cms_env == 'prd0':
            self._logger.warning('*** Skipping promotion creation since it is PROD')
        else:
            f = Faker()
            short_description = f.text(max_nb_chars=500).replace('\n', ' ')
            promotion = self.cms_config.add_promotion(shortDescription=short_description)
            self.__class__.promotion_title, self.__class__.promo_short_description, self.__class__.promo_id =\
                promotion.title.upper(), promotion.short_description, promotion.id

    def test_001_tap_promotions_button(self):
        """
        DESCRIPTION: Tap 'Promotions'
        EXPECTED: 'Promotions' page is opened
        EXPECTED: List of available Promotions is shown
        EXPECTED: 'Back' button us shown
        EXPECTED: **'Promotions'** page title
        """
        self.navigate_to_page(name='promotions/all')
        self.site.wait_content_state(state_name=vec.sb.PROMOTIONS, timeout=5)

    def test_002_verify_promotions_page(self):
        """
        DESCRIPTION: Verify 'Promotions' page
        EXPECTED: 'Promotions' page consists of:
        EXPECTED: 'Back' button
        EXPECTED: Page content
        EXPECTED: Section content
        """
        promotions_page = self.site.promotions
        self.assertTrue(self.site.has_back_button, msg='Back Button is not displayed on Promotions page')
        title = promotions_page.content_title_text
        self.assertEqual(title, vec.sb.PROMOTIONS,
                         msg=f'Current title name "{title}" is not equal to expected "{vec.sb.PROMOTIONS}"')
        all_promotions = promotions_page.tab_content.items_as_ordered_dict
        self.assertTrue(all_promotions, msg='No Promotions found in the page')

    def test_003_verify_back_button(self):
        """
        DESCRIPTION: Verify 'Back' button
        EXPECTED: By tapping the 'Back' button user is navigated to the previous page
        """
        self.site.back_button_click()
        self.site.wait_content_state('Homepage')

    def test_004_verify_page_content(self):
        """
        DESCRIPTION: Verify Page content
        EXPECTED: The list of all active promotions is shown
        """
        self.navigate_to_page(name='promotions/all')
        self.site.wait_content_state(state_name=vec.sb.PROMOTIONS, timeout=5)
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No Promotions found in the page')

    def test_005_verify_section_title(self):
        """
        DESCRIPTION: Verify Section title
        EXPECTED: Section title is set in CMS ('Title' field)
        """
        time.sleep(20)  # Promotion is taking time to reflect
        all_promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(all_promotions, msg='No promotions found')
        if tests.settings.cms_env != 'prd0':
            self.assertIn(self.promotion_title, all_promotions,
                          msg=f'"{self.promotion_title}" not found in {list(all_promotions.keys())}')
            self.__class__.promotion = all_promotions[self.promotion_title]
        else:
            self.__class__.promotion = list(all_promotions.values())[0]

    def test_006_verify_section_content(self):
        """
        DESCRIPTION: Verify Section title
        EXPECTED: The section consists of:
        EXPECTED: Promotion image
        EXPECTED: Section title
        EXPECTED: Short description
        EXPECTED: 'More info' button
        """
        self.promotion.scroll_to()
        name = self.promotion.name
        self.assertTrue(name, msg='Promo name is empty')

        promotions = self.cms_config.get_promotions()
        first_promotion = [promotion for promotion in promotions if promotion['title'].title() == name.title()][0]
        if not (first_promotion['useDirectFileUrl'] and first_promotion['uriMedium']):
            self._logger.warning(f'*** Promotion image for "{name}" is not downloaded in CMS')
        else:
            self.assertTrue(self.promotion.has_image, msg=f'Promotion "{name}" has no image')

        if first_promotion['shortDescription']:
            self.assertTrue(self.promotion.short_description.text, msg='Short description is not found')
        else:
            self._logger.warning(f'*** Short description for "{name}" is not filled in CMS')

        self.assertTrue(self.promotion.more_info_button.is_displayed(),
                        msg=f'"More Info" button for Promotion "{name}" is not shown')

    def test_007_verify_promotion_image(self):
        """
        DESCRIPTION: Verify Promotion image
        EXPECTED: Promotion image is downloaded in CMS
        """
        # verified in previous step

    def test_008_verify_short_description(self):
        """
        DESCRIPTION: Verify short description
        EXPECTED: Short description is set in CMS ('Short description' field)
        EXPECTED: Only the first 3 lines of text will be shown then the text will be truncated
        """
        self.promotion.scroll_to()
        self.assertTrue(self.promotion.short_description.has_3_lines,
                        msg='Short description on Promotions has not shortened to three lines')
        short_description = self.promotion.short_description.text
        self.assertTrue(short_description, msg='Short description is not shown')
        if tests.settings.cms_env != 'prd0':
            self.assertEqual(self.promo_short_description, short_description)

    def test_009_tap_more_info_and_verify_promo_details_page(self):
        """
        DESCRIPTION: Verify 'More info' button
        EXPECTED: By clicking/tapping 'More info' button user is navigated to Promotion Details page
        EXPECTED: Promotion Details page consists of two sections:
        EXPECTED: Section with image and full description of promotion entitled with promotion name - expanded by default
        EXPECTED: 'Terms and Conditions' section - expanded by default
        """
        promotion = self.promotion
        promotion.more_info_button.click()
        self.assertFalse(promotion.has_more_info(expected_result=False, timeout=15), msg='More info still displaying')
        self.site.wait_content_state(state_name='PromotionDetails')
        details_section = self.site.promotion_details.tab_content.promotion
        self.assertTrue(details_section, msg='Promotion sections was not found')
        self.assertTrue(details_section.is_expanded(), msg=f'"{details_section.name}" section is not expanded')

        description = details_section.detail_description.text
        self.assertTrue(description, msg='Detail promo description is empty')

        terms = self.site.promotion_details.tab_content.terms_and_conditions
        self.assertTrue(terms, msg='Terms and Conditions sections was not found')
        self.assertTrue(terms.is_expanded(), msg=f'"{terms.name}" section is not expanded')

        terms_details = terms.details
        self.assertTrue(terms_details, msg='Terms are empty')

        self.site.back_button_click()
        self.site.wait_content_state('Promotions', timeout=2)
