from datetime import datetime
import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.avtar_menu
@vtest
class Test_C65950091_Validate_Avtar_menu_promotion_pages(Common):
    """
    TR_ID: C65949647
    NAME: Validate Avtar menu promotion pages
    DESCRIPTION: Test case need to Validate Avtar menupromotion pages
    PRECONDITIONS: 1.User should have oxygen cms access
    PRECONDITIONS: 2.configuration for promotion in cms
    PRECONDITIONS: -click on promotion from left menu in the main navigation
    PRECONDITIONS: 3.click on create promotion to create new promtion
    PRECONDITIONS: 4.Enter all the required mandatory fields and click on create promotion
    """
    keep_browser_open = True

    def navigate_to_promotion_page(self):
        avatar = self.site.header.user_panel.my_account_button
        self.assertTrue(avatar, msg='User avatar is not displayed')
        avatar.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Account menu is not opened')
        menu_items = self.site.right_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Right menu items are not available')
        sports_promotions = next((item for item in menu_items if item.upper() == 'SPORTS PROMOTIONS'), None)
        self.assertTrue(sports_promotions, msg='Sports Promotions item is not available in right menu items')
        menu_items.get(sports_promotions).click()
        self.site.wait_content_state(state_name='Promotions')
        self._logger.info(f'=====> Clicked on Sports Promotions and Navigated to Promotions page')

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home page should loaded succesfully
        """
        # ********************* Navigating to Home page ***********************************
        self.site.login()
        self.site.wait_content_state('Homepage')
        self._logger.info(f'=====> Launched application and Home page loaded successfully')

    def test_002_verify_by_click_on_sport__promoation_pages(self):
        """
        DESCRIPTION: verify by click on sport  promoation pages
        EXPECTED: User should be naviagted to the promations page
        """
        # ********************* Navigating to Promotions page ***********************************
        self.navigate_to_promotion_page()
        self._logger.info(f'=====> Navigated to Promotions page successfully')

    def test_003_verify_promotions_page(self):
        """
        DESCRIPTION: verify promotions page
        EXPECTED: promotions page should consits of
        EXPECTED: 1.Back button
        EXPECTED: 2.promotions page title
        EXPECTED: 3.page content
        EXPECTED: 4.section content
        """
        # ********************* Verification of Promotions page ***********************************
        if self.brand == 'ladbrokes' and self.device_type == 'mobile':
            self.assertTrue(self.site.has_back_button,
                            msg='Back button is not available in Promotions page')
        else:
            self.assertTrue(self.site.promotions.header_line.has_back_button,
                            msg='Back button is not available in Promotions page')
        actual_promotions_page_title = self.site.promotions.header_line.page_title.text.upper()
        self.assertEqual("PROMOTIONS", actual_promotions_page_title,
                         msg=f'Promotions page title is displayed as {actual_promotions_page_title}')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No promotions found on page')
        self._logger.info(f'=====> Promotions page verified successfully')

    def test_004_verify_back_button(self):
        """
        DESCRIPTION: Verify back button
        EXPECTED: User should be naviagted to the previous  page
        """
        # ********************* Navigating to Previous page ***********************************
        if self.device_type == 'mobile':
            self.site.back_button_click()
            # Wait for the content state 'avtar-menu' to ensure the page has loaded
            self.site.wait_content_state('avtar-menu')
        else:
            self.site.promotions.header_line.back_button.click()
            # Wait for the content state 'home_page' to ensure the page has loaded
            self.site.wait_content_state('Homepage')
        self._logger.info(f'=====> Clicked on back button then User navigated to previous page')

    def test_005_verify_page_content(self):
        """
        DESCRIPTION: Verify page content
        EXPECTED: List of all active promotions should be shown.
        """
        # ********************* Navigating to Promotions page ***********************************
        if self.device_type == 'mobile':
            menu_items = self.site.right_menu.items_as_ordered_dict
            self.assertTrue(menu_items, msg='Right menu items are not available')
            sports_promotions = next((item for item in menu_items if item.upper() == 'SPORTS PROMOTIONS'), None)
            self.assertTrue(sports_promotions, msg='Sports Promotions item is not available in right menu items')
            menu_items.get(sports_promotions).click()
        else:
            self.navigate_to_promotion_page()
        self.site.wait_content_state(state_name='Promotions')
        self._logger.info(f'=====> Clicked on Sports Promotions and Navigated to Promotions page')
        self.__class__.promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(self.promotions, msg='No promotions found on page')
        self._logger.info(f'=====> Navigated to Promotions page again and Verified Promotions are available')

    def test_006_verify_section_content(self):
        """
        DESCRIPTION: verify section content
        EXPECTED: Section content consits of
        EXPECTED: 1.promotion image
        EXPECTED: 2.section title
        EXPECTED: 3.short description
        EXPECTED: 4.see more button
        """
        # ********************* Verification of Promotion ***********************************
        promotion_name, promotion = next(
            ((promotion_name.upper(), promotion) for promotion_name, promotion in self.promotions.items() if
             promotion is not None), (None, None))
        today_date = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        current_time = self.get_date_time_formatted_string(date_time_obj=today_date, time_format=time_format,
                                                           url_encode=False)[:-3] + 'Z'
        cms_promotions = self.cms_config.get_promotions()
        cms_promotion = next((promotion for promotion in cms_promotions if
                              promotion['validityPeriodStart'] < current_time < promotion['validityPeriodEnd'] and not
                              promotion['disabled'] and promotion['title'].upper() == promotion_name), None)
        # ********************* Verification of Promotion Title ***********************************
        expected_cms_promotion_name = cms_promotion['title'].upper()
        self.assertEqual(expected_cms_promotion_name, promotion_name,
                         msg=f'Expected promotion name is {expected_cms_promotion_name} but actual is {promotion_name}')
        # ********************* Verification of Promotion Short Description ***********************************
        actual_short_description = promotion.short_description.text.upper().strip()
        expected_cms_promotion_short_description = cms_promotion['shortDescription'].upper().strip()
        self.assertEqual(expected_cms_promotion_short_description, actual_short_description,
                         msg=f'Expected short description name is {expected_cms_promotion_short_description} but actual is {actual_short_description}')
        # ********************* Verification of Promotion Image ***********************************
        actual_image_url = promotion.image.get_attribute('src').upper()
        expected_cms_promotion_image_url = cms_promotion['directFileUrl'].upper()
        self.assertEqual(expected_cms_promotion_image_url, actual_image_url,
                         msg=f'Expected image url is {expected_cms_promotion_image_url} but actual is {actual_image_url}')
        # ********************* Verification of Promotion SEE MORE button ***********************************
        self.assertTrue(promotion.has_more_info(), msg='SEE MORE button is not displayed')
        # ********************* Verification of Promotion Details ***********************************
        promotion.more_info_button.click()
        self.assertFalse(promotion.has_more_info(expected_result=False, timeout=15), msg='More info still displaying')
        current_url = self.device.get_current_url()
        self.assertIn('promotions/details', current_url,
                      msg=f'User is not navigated to Promotion details page when clicked on SEE MORE button')
        self._logger.info(f'=====> Verified Promotion Title, Short Description, Image and SEE MORE button successfully')

    def test_007_verify_sections_title(self):
        """
        DESCRIPTION: verify sections title
        EXPECTED: section title should be as per cms configured
        """
        # Covered in test_006_verify_section_content

    def test_008_verify_promotions_image(self):
        """
        DESCRIPTION: verify promotions image
        EXPECTED: promotion image should be as per cms
        """
        # Covered in test_006_verify_section_content

    def test_009_verify_see_more_button(self):
        """
        DESCRIPTION: verify see more button
        EXPECTED: By clicking on user should be naviagted to promotion details page
        """
        # Covered in test_006_verify_section_content
