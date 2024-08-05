import pytest
from tests.base_test import vtest
from time import sleep
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import BaseHighlightsCarouselTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Cannot create event on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@pytest.mark.mobile_only
@vtest
class Test_C2987414_Highlights_Carousel__cards_displaying_based_on_undisplay_option_on_selection_market_event_levels(BaseHighlightsCarouselTest):
    """
    TR_ID: C2987414
    NAME: Highlights Carousel - cards' displaying based on "undisplay" option on selection/market/event levels
    DESCRIPTION: This test case verifies displaying of cards based on "undisplay" option on selection/market/event levels
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have an active Highlights Carousel with active events in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True
    highlights_carousels_titles = ['Autotest Highlight Carousel with Event']

    def get_highlight_carousel_section(self):
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name)
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        self.assertIn(self.highlights_carousel_name, highlight_carousels,
                      msg=f'"{self.highlights_carousel_name}" carousel is not shown')
        self.__class__.highlight_carousel_cards = highlight_carousels[
            self.highlights_carousel_name].items_as_ordered_dict
        self.assertTrue(self.highlight_carousel_cards,
                        msg=f'"{self.highlights_carousel_name}" carousel contains no odds cards')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test football event and add it to Highlights Carousel
        DESCRIPTION: Navigate to the Home page.
        EXPECTED: Highlights Carousel is shown with test event in it.
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.event_id = event.event_id
        self.__class__.event_name = event.team1 + ' v ' + event.team2
        self.__class__.market_id = event.default_market_id
        self.__class__.selection_ids = list(event.selection_ids.values())
        self.__class__.prices = []
        for outcome in event.ss_response['event']['children'][0]['market']['children']:
            price = outcome['outcome']['children'][0]['price']['priceNum'] + '/' + outcome['outcome']['children'][0]['price']['priceDen']
            self.prices.append(price)

        event_2 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.event_id_2 = event_2.event_id

        self.cms_config.create_highlights_carousel(
            title=self.highlights_carousels_titles[0], events=[self.event_id, self.event_id_2])

        self.__class__.highlights_carousel_name = self.convert_highlights_carousel_title(
            self.highlights_carousels_titles[0])
        self.site.wait_content_state('Homepage')

    def test_001___in_ti_tool_disable_display_option_for_one_of_the_selection_of_one_of_the_events_cards_displayed_in_highlights_carousel__verify_live_update_in_highlights_carousel(
            self):
        """
        DESCRIPTION: - In TI tool disable "display" option for one of the selection of one of the events' cards displayed in Highlights Carousel
        DESCRIPTION: - Verify live update in Highlights Carousel
        EXPECTED: Respective selection is undisplayed in live
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[0], displayed=False, active=True)
        self.get_highlight_carousel_section()
        event_odds_card = self.highlight_carousel_cards.get(self.event_name)
        self.assertTrue(event_odds_card,
                        msg=f'"{self.event_name}" odds card is not shown '
                            f'within "{self.highlights_carousel_name}" carousel')
        outcomes = [outcome.outcome_price_text for outcome in event_odds_card.items_as_ordered_dict.values()]
        self.assertEqual(sorted(outcomes), sorted([self.prices[1], self.prices[2]]),
                         msg=f'Un-displayed selection is still appearing for event-name "{self.event_name}"')
        self.assertEqual(len(event_odds_card.items_as_ordered_dict), 2,
                         msg=f'Un-displayed selection is still appearing for event-name "{self.event_name}"')

    def test_002___in_ti_tool_enable_display_option_for_the_selection_from_step_1__refresh_the_page_and_verify_selections_displaying_in_highlights_carousel(
            self):
        """
        DESCRIPTION: - In TI tool enable "display" option for the selection from step 1
        DESCRIPTION: - Refresh the page and verify selection's displaying in Highlights Carousel
        EXPECTED: Selection is displayed again
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[0], displayed=True, active=True)
        sleep(5)
        self.device.refresh_page()
        self.site.wait_content_state('Homepage', timeout=30)
        self.get_highlight_carousel_section()

        event_odds_card = self.highlight_carousel_cards.get(self.event_name)
        self.assertTrue(event_odds_card,
                        msg=f'"{self.event_name}" odds card is not shown '
                            f'within "{self.highlights_carousel_name}" carousel')
        outcomes = [outcome.outcome_price_text for outcome in event_odds_card.items_as_ordered_dict.values()]
        self.assertEqual(sorted(outcomes), sorted(self.prices),
                         msg=f'Displayed selection is not appearing for event-name "{self.event_name}"')
        self.assertEqual(len(event_odds_card.items_as_ordered_dict), 3,
                         msg=f'Displayed selection is not appearing for event-name "{self.event_name}"')

    def test_003___in_ti_tool_disable_display_option_for_primary_market_of_one_of_the_events_cards_displayed_in_highlights_carousel__verify_live_update_in_highlights_carousel(
            self):
        """
        DESCRIPTION: - In TI tool disable "display" option for primary market of one of the events' cards displayed in Highlights Carousel
        DESCRIPTION: - Verify live update in Highlights Carousel
        EXPECTED: Respective card is undisplayed in live
        """
        self.ob_config.change_market_state(event_id=self.event_id, market_id=self.market_id, displayed=False,
                                           active=True)
        sleep(5)
        self.get_highlight_carousel_section()
        event_odds_card = self.highlight_carousel_cards.get(self.event_name)
        self.assertFalse(event_odds_card,
                         msg=f'Un-displayed market is still appearing for event-name "{self.event_name}"')

    def test_004___in_ti_tool_enable_display_option_for_primary_market_from_step_3__refresh_the_page_and_verify_cards_displaying_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool enable "display" option for primary market from step 3
        DESCRIPTION: - Refresh the page and verify card's displaying in Highlights Carousel
        EXPECTED: Card is displayed
        """
        self.ob_config.change_market_state(event_id=self.event_id, market_id=self.market_id, displayed=True,
                                           active=True)
        sleep(5)
        self.device.refresh_page()
        self.site.wait_content_state('Homepage', timeout=30)
        self.get_highlight_carousel_section()
        event_odds_card = self.highlight_carousel_cards.get(self.event_name)
        self.assertTrue(event_odds_card, msg=f'Displayed market is not appearing for event-name "{self.event_name}"')

    def test_005___in_ti_tool_disable_display_option_for_one_of_the_events_cards_displayed_in_highlights_carousel__verify_live_update_in_highlights_carousel(
            self):
        """
        DESCRIPTION: - In TI tool disable "display" option for one of the events' cards displayed in Highlights Carousel
        DESCRIPTION: - Verify live update in Highlights Carousel
        EXPECTED: Respective card is undisplayed in live
        """
        self.ob_config.change_event_state(event_id=self.event_id, displayed=False, active=True)
        sleep(5)
        self.get_highlight_carousel_section()
        event_odds_card = self.highlight_carousel_cards.get(self.event_name)
        self.assertFalse(event_odds_card,
                         msg=f'Un-displayed Event is still appearing for event-name "{self.event_name}"')

    def test_006___in_ti_tool_enable_display_option_for_event_from_step_5__refresh_the_page_and_verify_cards_displaying_in_highlights_carousel(
            self):
        """
        DESCRIPTION: - In TI tool enable "display" option for event from step 5
        DESCRIPTION: - Refresh the page and verify card's displaying in Highlights Carousel
        EXPECTED: Card is displayed
        """
        self.ob_config.change_event_state(event_id=self.event_id, displayed=True, active=True)
        sleep(5)
        self.device.refresh_page()
        self.site.wait_content_state('Homepage', timeout=30)
        self.get_highlight_carousel_section()
        event_odds_card = self.highlight_carousel_cards.get(self.event_name)
        self.assertTrue(event_odds_card, msg=f'Displayed Event is not appearing for event-name "{self.event_name}"')
