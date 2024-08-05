import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C15306587_Verify_UI_sticky_elements_for_desktop(Common):
    """
    TR_ID: C15306587
    NAME: Verify UI sticky elements for desktop
    DESCRIPTION: According to Amit B, Free Bet dialogue should NOT be displayed on Ladbrokes brand only on all platforms (but Free Bet notification should still be shown in the Bet Slip on the yellow background):
    DESCRIPTION: https://jira.egalacoral.com/browse/BMA-50888
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_login_to_oxygene_app_on_desktop(self):
        """
        DESCRIPTION: Login to Oxygene app on desktop
        EXPECTED: User is logged in, homepage is displayed
        """
        pass

    def test_002_scroll_down_the_page_and_observe_the_header_component(self):
        """
        DESCRIPTION: Scroll down the page and observe the header component
        EXPECTED: Header component is sticky at the top during the scroll and follows along the cursor
        """
        pass

    def test_003_scroll_down_the_page_and_observe_the_footer_component(self):
        """
        DESCRIPTION: Scroll down the page and observe the footer component
        EXPECTED: Footer component remains at the bottom of the page during the scroll and there is padding between footer section with links and footer menu
        """
        pass

    def test_004_open_horseracing_and_select_any_event_with_tote____click_on_totepool_tab____click_on_any_selection(self):
        """
        DESCRIPTION: Open HorseRacing and select any event with Tote --> Click on TotePool tab --> Click on any selection.
        EXPECTED: Tote bet builder should be displayed at the bottom of the page.
        """
        pass

    def test_005_scroll_down_the_page_and_observe_the_tote_builder_component(self):
        """
        DESCRIPTION: Scroll down the page and observe the tote builder component
        EXPECTED: Tote bet builder should be anchored to the bottom while scrolling
        """
        pass

    def test_006_open_any_football_event_and_click_build_your_bet_link(self):
        """
        DESCRIPTION: Open any football event and click Build your bet link
        EXPECTED: Build your bet page is open for current event and build your bet dashboard appears at the bottom of the page
        """
        pass

    def test_007_scroll_down_the_page_and_observe_the_build_your_bet_component(self):
        """
        DESCRIPTION: Scroll down the page and observe the build your bet component
        EXPECTED: Build your bet component is sticky at the bottom of the page during the scroll and follows along the cursor
        """
        pass

    def test_008_open_shop_locator_scroll_down_and_observe_the_componentnote_to_do_that_add_shop_locator_after_the_page_url(self):
        """
        DESCRIPTION: Open Shop Locator, scroll down and observe the component
        DESCRIPTION: Note: to do that, add 'shop-locator' after the page URL
        EXPECTED: Shop Locator occupies the entire app area under the header.
        EXPECTED: Footer remains sticky at the bottom and does not overlap with any part of Shop locator component
        """
        pass

    def test_009_add_a_freebet_that_is_about_to_expire_in_24_hours_and_reload_the_page(self):
        """
        DESCRIPTION: Add a freebet that is about to expire in 24 hours and reload the page
        EXPECTED: Oxygen freebet notification appears at the top saying that the user has a freebet that will soon expire
        EXPECTED: Note: For Ladbrokes brand only, Free Bet dialogue should NOT be displayed at all on all platforms.
        """
        pass

    def test_010_scroll_down_the_page_and_observe_the_oxygen_freebet_notifier_component(self):
        """
        DESCRIPTION: Scroll down the page and observe the Oxygen freebet notifier component
        EXPECTED: Oxygen freebet notifier component is sticky at the top during the scroll and follows along the cursor
        """
        pass
