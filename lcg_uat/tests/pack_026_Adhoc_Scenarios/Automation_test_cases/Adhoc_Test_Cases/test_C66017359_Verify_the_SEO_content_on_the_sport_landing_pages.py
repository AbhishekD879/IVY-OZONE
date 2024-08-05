import pytest

import tests
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.adhoc_suite
@pytest.mark.back_button
@pytest.mark.navigation
@pytest.mark.desktop
@pytest.mark.adhoc24thJan24
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66017359_Verify_the_SEO_content_on_the_sport_landing_pages(Common):
    """
    TR_ID: C66017359
    NAME: Verify the SEO content on the sport landing pages
    DESCRIPTION: Verify the SEO content on the sport landing pages for both tier-1 & tier-2 sports
    PRECONDITIONS: In CMS SEO-&gt;Manual-&gt;Configure SEO content for this URL(Example): /sport/football
    PRECONDITIONS: In CMS Sports Category-&gt;Football-&gt;Target Uri-&gt;'sport/football'
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: In CMS SEO-&gt;Manual-&gt;Configure SEO content for this URL(Example): /sport/football
        PRECONDITIONS: In CMS Sports Category-&gt;Football-&gt;Target Uri-&gt;'sport/football'
        """
        # Retrieve SEO pages configuration from the CMS (Content Management System)
        seo_pages = self.cms_config.get_seo_pages()

        # Find the SEO page related to football in the configuration
        football_seo_page = next((seo_page for seo_page in seo_pages if seo_page.get('url') == '/sport/football'), None)

        # If the football SEO page is not found, create a new one with default values
        if not football_seo_page:
            football_seo_page = self.cms_config.create_seo_page(title="Auto_test_C66017359", url="/sport/football")

        # Check if the 'disabled' attribute of the football SEO page is True
        if football_seo_page.get('disabled'):
            # If disabled, update the SEO page by setting 'disabled' to False
            self.cms_config.update_seo_page(url='/sport/football', disabled=False)

        # Store relevant information about the football SEO page in class attributes
        self.__class__.football_seo_page_title = football_seo_page.get('staticBlockTitle')
        self.__class__.football_seo_page_url = football_seo_page.get('url')

    def test_001_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football landing page
        EXPECTED: Football landing page is successfully loaded
        """
        self.site.go_to_home_page()
        self.site.open_sport(name='FOOTBALL')
        self.site.wait_content_state(state_name="football")

    def test_002_verify_the_football_landing_page_url(self):
        """
        DESCRIPTION: Verify the football landing page URL
        EXPECTED: Football URL is displayed in this format:
        EXPECTED: https://sports.ladbrokes.com/sport/football
        """
        expected_url = f'https://{tests.HOSTNAME}{self.football_seo_page_url}'
        actual_url = self.device.get_current_url()
        self.assertEqual(expected_url, actual_url, msg=f'expected url {expected_url} is not equal to '
                                                       f'actual url {actual_url}')

    def test_003_verify_the_seo_content_by_scrolling_down_the_page(self):
        """
        DESCRIPTION: Verify the SEO content by scrolling down the page
        EXPECTED: SEO content should be displayed as CMS configuration
        """
        # Get the SEO static block section related to football on the current page
        seo_block = self.site.football.seo_static_block_section

        self.assertTrue(seo_block, "seo_static_block_section not found")

        # Scroll to the SEO static block section to ensure it's visible on the page
        # seo_block.scroll_to_we()

        # If the SEO static block section is not expanded, expand it
        if not seo_block.is_expanded(brand=self.brand):
            seo_block.expand()

        # Retrieve the name of the expanded SEO static block
        seo_block_name = seo_block.name

        # Check if the retrieved SEO block name matches the expected SEO page title
        self.assertEqual(seo_block_name.upper(), self.football_seo_page_title.upper(),
                         msg=f'Actual SEO block name "{seo_block_name.upper()}" is not equal to '
                             f'expected SEO page title "{self.football_seo_page_title.upper()}"')

        # Retrieve the content of the SEO static block
        seo_block_content = seo_block.content

        # Assert that the SEO block content is present (not empty)
        self.assertTrue(seo_block_content, msg='SEO block content not found')

