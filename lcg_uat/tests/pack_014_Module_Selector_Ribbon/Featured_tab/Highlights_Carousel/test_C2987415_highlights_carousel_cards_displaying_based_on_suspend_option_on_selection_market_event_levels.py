import pytest
from selenium.common.exceptions import StaleElementReferenceException

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    BaseHighlightsCarouselTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl - can't suspend event on HL
# @pytest.mark.prod - it's not allowed to create events / highlights carousels on prod
@pytest.mark.tablet
@pytest.mark.featured
@pytest.mark.liveserv_updates
@pytest.mark.highlights_carousel
@pytest.mark.medium
@pytest.mark.consequent
@vtest
class Test_C2987415_Highlights_Carousel_cards_displaying_based_on_suspend_option_on_selection_market_event_levels(BaseHighlightsCarouselTest):
    """
    TR_ID: C2987415
    VOL_ID: C9698725
    NAME: Highlights Carousel - cards' displaying based on "suspend" option on selection/market/event levels
    DESCRIPTION: This test case verifies displaying of cards based on "suspend" option on selection/market/event levels
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have an active Highlights Carousel with active events in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should be on a home page in application
    """
    def check_all_selections_from_event_card(self, selections_suspended: bool) -> None:
        """
        This method verifies whether all selections represented within single event odds card are suspended or not
        depending on single input parameter `selections_suspended`
        """
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name)
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        self.assertIn(self.highlights_carousel_name, highlight_carousels,
                      msg=f'"{self.highlights_carousel_name}" carousel is not shown')
        highlight_carousel_cards = highlight_carousels[self.highlights_carousel_name].items_as_ordered_dict
        self.assertTrue(highlight_carousel_cards,
                        msg=f'"{self.highlights_carousel_name}" carousel contains no odds cards')
        event_odds_card = highlight_carousel_cards.get(self.event_name)
        self.assertTrue(event_odds_card,
                        msg=f'"{self.event_name}" odds card is not shown '
                        f'within "{self.highlights_carousel_name}" carousel')
        if selections_suspended:
            self.assertFalse(event_odds_card.first_player_bet_button.is_enabled(expected_result=False, timeout=60),
                             msg=f'Bet button for "{event_odds_card.first_player}" selection is not disabled')

            self.assertFalse(event_odds_card.draw_bet_button.is_enabled(expected_result=False, timeout=3),
                             msg=f'Bet button for "{vec.sb.DRAW}" selection is not disabled')

            self.assertFalse(event_odds_card.second_player_bet_button.is_enabled(expected_result=False, timeout=3),
                             msg=f'Bet button for "{event_odds_card.second_player}" selection is not disabled')
        else:
            self.assertTrue(event_odds_card.first_player_bet_button.is_enabled(timeout=10),
                            msg=f'Bet button for "{event_odds_card.first_player}" selection is not enabled')

            self.assertTrue(event_odds_card.draw_bet_button.is_enabled(timeout=3),
                            msg=f'Bet button for "{vec.sb.DRAW}" selection is not enabled')

            self.assertTrue(event_odds_card.second_player_bet_button.is_enabled(timeout=3),
                            msg=f'Bet button for "{event_odds_card.second_player}" selection is not enabled')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test football event and add it to Highlights Carousel
        DESCRIPTION: Navigate to the Home page.
        EXPECTED: Highlights Carousel is shown with test event in it.
        """
        cms = self.cms_config
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = event_params.event_id
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.marketID = self.ob_config.market_ids[event_params.event_id][market_short_name]
        team1, self.__class__.team1_selection_id = list(event_params.selection_ids.items())[0]
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'

        self.__class__.highlights_carousel = cms.create_highlights_carousel(
            title=self.highlights_carousels_titles[0], events=[self.eventID])

        self.__class__.highlights_carousel_name = self.convert_highlights_carousel_title(self.highlights_carousels_titles[0])

        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name)

    def test_001_in_ti_tool_suspend_one_of_the_selection_of_one_of_the_events_cards_displayed_in_highlights_carousel_verify_live_update_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool suspend one of the selection of one of the events' cards displayed in Highlights Carousel
        DESCRIPTION: - Verify live update in Highlights Carousel
        EXPECTED: Respective selection is suspended (disabled)
        """
        self.ob_config.change_selection_state(selection_id=self.team1_selection_id, displayed=True, active=False)
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        self.assertIn(self.highlights_carousel_name, highlight_carousels,
                      msg=f'"{self.highlights_carousel_name}" carousel is not shown')
        highlight_carousel_cards = highlight_carousels[self.highlights_carousel_name].items_as_ordered_dict
        self.assertTrue(highlight_carousel_cards,
                        msg=f'"{self.highlights_carousel_name}" carousel contains no odds cards')
        event_odds_card = highlight_carousel_cards[self.event_name]
        self.assertTrue(event_odds_card,
                        msg=f'"{self.event_name}" odds card is not shown within "{self.highlights_carousel_name}" carousel')
        try:
            self.assertFalse(event_odds_card.first_player_bet_button.is_enabled(expected_result=False, timeout=60),
                             msg=f'Bet button for "{event_odds_card.first_player}" selection is not disabled')
        except StaleElementReferenceException:
            highlight_carousels = self.site.home.tab_content.highlight_carousels
            self.assertIn(self.highlights_carousel_name, highlight_carousels,
                          msg=f'"{self.highlights_carousel_name}" carousel is not shown')
            highlight_carousel_cards = highlight_carousels[self.highlights_carousel_name].items_as_ordered_dict
            self.assertTrue(highlight_carousel_cards,
                            msg=f'"{self.highlights_carousel_name}" carousel contains no odds cards')
            event_odds_card = highlight_carousel_cards[self.event_name]
            self.assertTrue(event_odds_card,
                            msg=f'"{self.event_name}" odds card is not shown '
                                f'within "{self.highlights_carousel_name}" carousel')

    def test_002_in_ti_tool_unsuspend_the_selection_from_step_1_verify_live_update_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool unsuspend the selection from step 1
        DESCRIPTION: - Verify live update in Highlights Carousel
        EXPECTED: Selection is unsuspended (enabled)
        """
        self.ob_config.change_selection_state(selection_id=self.team1_selection_id, displayed=True, active=True)
        self.check_all_selections_from_event_card(selections_suspended=False)

    def test_003_in_ti_tool_suspend_a_primary_market_of_one_of_the_events_cards_displayed_in_highlights_carousel_verify_live_update_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool suspend a primary market of one of the events' cards displayed in Highlights Carousel
        DESCRIPTION: - Verify live update in Highlights Carousel
        EXPECTED: All selection from respective event's card are suspended (disabled)
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=False)
        self.check_all_selections_from_event_card(selections_suspended=True)

    def test_004_in_ti_tool_unsuspend_a_primary_market_from_step_3_verify_live_update_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool unsuspend a primary market from step 3
        DESCRIPTION: - Verify live update in Highlights Carousel
        EXPECTED: All selection from respective event's card are unsuspended (enabled)
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)
        self.check_all_selections_from_event_card(selections_suspended=False)

    def test_005_in_ti_tool_suspend_one_of_the_events_displayed_in_highlights_carousel_verify_live_update_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool suspend one of the events displayed in Highlights Carousel
        DESCRIPTION: - Verify live update in Highlights Carousel
        EXPECTED: All selection from respective event's card are suspended (disabled)
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
        self.check_all_selections_from_event_card(selections_suspended=True)

    def test_006_in_ti_tool_unsuspend_the_event_from_step_5_verify_live_update_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool unsuspend the event from step 5
        DESCRIPTION: - Verify live update in Highlights Carousel
        EXPECTED: All selection from respective event's card are unsuspended (enabled)
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        self.check_all_selections_from_event_card(selections_suspended=False)
