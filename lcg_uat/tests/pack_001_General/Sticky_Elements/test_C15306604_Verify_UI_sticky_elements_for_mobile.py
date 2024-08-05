import datetime
import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C15306604_Verify_UI_sticky_elements_for_mobile(Common):
    """
    TR_ID: C15306604
    NAME: Verify UI sticky elements for mobile
    DESCRIPTION: According to Amit B, Free Bet dialogue should NOT be displayed on Ladbrokes brand only on all platforms (but Free Bet notification should still be shown in the Bet Slip on the yellow background):
    DESCRIPTION: https://jira.egalacoral.com/browse/BMA-50888
    PRECONDITIONS:
    """
    keep_browser_open = True
    username = tests.settings.freebet_user

    def test_001_login_to_oxygen_app_on_mobile(self):
        """
        DESCRIPTION: Login to Oxygen app on mobile
        EXPECTED: User is logged in, homepage is displayed
        """
        self.site.wait_content_state("Homepage")

    def test_002_scroll_down_the_page_and_observe_the_header_component(self):
        """
        DESCRIPTION: Scroll down the page and observe the header component
        EXPECTED: Header component is sticky at the top during the scroll and follows along the cursor
        """
        self.site.contents.scroll_to_bottom()
        self.assertTrue(self.site.header.is_displayed(), msg=f'Main Header is hidden')

    def test_003_scroll_down_the_page_and_observer_carousel_menu_component(self):
        """
        DESCRIPTION: Scroll down the page and observer carousel menu component
        EXPECTED: Carousel menu component is sticky at the top under the header during the scroll and follows along the cursor
        """
        self.assertTrue(self.site.home.menu_carousel.is_displayed(), msg="Carousel is not displayed")

    def test_004_scroll_down_the_page_and_observe_the_footer_component(self):
        """
        DESCRIPTION: Scroll down the page and observe the footer component
        EXPECTED: Footer component remains at the bottom of the page during the scroll and there is padding between footer section with links and footer menu
        """
        self.site.footer.scroll_to()
        self.assertTrue(self.site.footer.is_displayed(), msg=f'Main Header is hidden')
        self.assertTrue(self.site.footer.footer_content_section.is_displayed(), msg=f'Main Header is hidden')

    def test_005_open_football_category_and_click_on_match_result_menu(self):
        """
        DESCRIPTION: Open football category and click on Match Result menu
        EXPECTED: Market selector dropdown is expanded
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('Football')
        self.site.football.tab_content.has_dropdown_market_selector()

    def test_006_scroll_down_the_page_and_observe_the_market_selector_component(self):
        """
        DESCRIPTION: Scroll down the page and observe the Market selector component
        EXPECTED: Market selector component is sticky at the top during the scroll and follows along the cursor
        """
        self.site.contents.scroll_to_bottom()
        self.assertTrue(self.site.football.tab_content.is_market_selector_sticky, msg="Market selector is not sticky")

    def test_007_open_horseracing_and_select_any_event_with_tote____click_on_totepool_tab____click_on_any_selection(self):
        """
        DESCRIPTION: Open HorseRacing and select any event with Tote --> Click on TotePool tab --> Click on any selection.
        EXPECTED: Tote bet builder should be displayed at the bottom of the page.
        """
        # Cannot create totes on qa2 envs

    def test_008_scroll_down_the_page_and_observe_the_tote_builder_component(self):
        """
        DESCRIPTION: Scroll down the page and observe the tote builder component
        EXPECTED: Tote bet builder should be anchored to the bottom while scrolling
        """
        # Cannot create totes on qa2 envs

    def test_009_open_any_football_event_and_click_build_your_bet_link(self):
        """
        DESCRIPTION: Open any football event and click Build your bet link
        EXPECTED: Build your bet page is open for current event and build your bet dashboard appears at the bottom of the page
        """
        # Cannot create banach markets on qa2 envs

    def test_010_scroll_down_the_page_and_observe_the_build_your_bet_component(self):
        """
        DESCRIPTION: Scroll down the page and observe the build your bet component
        EXPECTED: Build your bet component is sticky at the bottom of the page during the scroll and follows along the cursor
        """
        # Cannot create banach markets on qa2 envs

    def test_011_scroll_down_the_page_and_observe_the_smart_banner_the_one_with_green_download_button_component(self):
        """
        DESCRIPTION: Scroll down the page and observe the smart banner (the one with green Download button) component
        EXPECTED: Smart banner component is sticky at the top during the scroll and follows along the cursor
        """
        # NA

    def test_012_open_shop_locator_scroll_down_and_observe_the_componentnote_to_do_that_add_shop_locator_after_the_page_url(self):
        """
        DESCRIPTION: Open Shop Locator, scroll down and observe the component
        DESCRIPTION: Note: to do that, add 'shop-locator' after the page URL
        EXPECTED: Shop Locator occupies the entire app area under the header.
        EXPECTED: Footer remains sticky at the bottom and does not overlap with any part of Shop locator component
        """
        self.navigate_to_page("/shop-locator")
        self.assertTrue(self.site.footer.is_displayed(), msg=f'Main Header is hidden')
        self.assertTrue(self.site.footer.footer_content_section.is_displayed(), msg=f'Main Header is hidden')

    def test_013_add_a_freebet_that_is_about_to_expire_in_2_days_and_reload_the_page(self):
        """
        DESCRIPTION: Add a freebet that is about to expire in 2 days and reload the page
        EXPECTED: Oxygen freebet notification appears at the top saying that the user has a freebet that will soon expire
        EXPECTED: Note: For Ladbrokes brand only, Free Bet dialogue should NOT be displayed at all on all platforms.
        """
        self.navigate_to_page("Homepage")
        exp_date = datetime.datetime.now() + datetime.timedelta(hours=0)
        self.ob_config.grant_freebet(username=self.username,
                                     expiration_date=exp_date)
        self.site.login(username=self.username, close_free_bets_notification=False)
        self.site.contents.free_bets_notification.is_displayed()

    def test_014_scroll_down_the_page_and_observe_the_oxygen_freebet_notifier_component(self):
        """
        DESCRIPTION: Scroll down the page and observe the Oxygen freebet notifier component
        EXPECTED: Oxygen freebet notifier component is sticky at the top during the scroll and follows along the cursor
        """
        self.site.contents.scroll_to_bottom()
        self.site.contents.free_bets_notification.is_displayed()
        self.site.logout()

    def test_015_clear_cache_login_and_open_any_football_event(self):
        """
        DESCRIPTION: Clear cache, login and open any Football event.
        EXPECTED: FootballTutorialOverlay should be sticky
        """
        if self.brand == 'bma':
            self.delete_cookies()
            self.device.driver.execute_script('localStorage.clear();')
            self.device.navigate_to(url=tests.HOSTNAME)
            self.device.driver.implicitly_wait(5)
            self.site.login(username=self.username)
            self.navigate_to_page(name='sport/football')
            self.site.wait_content_state('Football')
            try:
                self.site.wait_for_tutorial_overlay()
                self.site.contents.scroll_to_bottom()
                self.assertTrue(self.site.football_overlay.is_displayed(),
                                msg='"close tutorial" button not displayed')
            except (AttributeError, VoltronException):
                self._logger.info('Tutorial overlay is not displayed')
