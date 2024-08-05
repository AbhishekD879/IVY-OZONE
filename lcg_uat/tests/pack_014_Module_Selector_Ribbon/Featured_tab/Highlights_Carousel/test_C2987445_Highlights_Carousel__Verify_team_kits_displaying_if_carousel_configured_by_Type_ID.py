import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    BaseHighlightsCarouselTest, generate_highlights_carousel_name
from voltron.utils.helpers import get_featured_structure_changed
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # it's not allowed to create events / highlights carousels on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.featured
@pytest.mark.homepage_featured
@pytest.mark.highlights_carousel
@vtest
class Test_C2987445_Highlights_Carousel__Verify_team_kits_displaying_if_carousel_configured_by_Type_ID(BaseHighlightsCarouselTest):
    """
    TR_ID: C2987445
    VOL_ID: C58693882
    NAME: Highlights Carousel - Verify team kits displaying if carousel configured by Type ID
    DESCRIPTION: This test case verifies displaying of team kits of events cards in Highlights Carousels configured by Type ID
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Homepage
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS:
    PRECONDITIONS: * Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: * Sport Pages > Sport Categories > Sport > Highlights Carousel
    PRECONDITIONS: - You should have active Highlights Carousels with active events in CMS. Make sure that Highlights Carousel configured by TypeID
    PRECONDITIONS: - Team kits are mapped to teams by names (e.g. to show team kit for Manchester United team name should be "Man-United"). Refer to the attached files to see team names for mapping
    PRECONDITIONS: - TypeID must be from Premier League or Champions League to display the team kits
    """
    keep_browser_open = True

    def wait_for_highlights_carousel_to_change_type_id(self, module_name, type_id, delimiter):
        for _ in range(2):
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            result = wait_for_result(lambda: [module for module in
                                     get_featured_structure_changed(delimiter=delimiter).get('modules', [])
                                     if module['@type'] == 'HighlightCarouselModule' and
                                              module['title'] == module_name and
                                              module['typeId'] == type_id] != [],
                                     name=f'"type ID" update for Highlight carousel module '
                                          f'{self.highlights_carousel_name}',
                                     timeout=10)
            if result:
                return result
        return result

    def test_000_preconditions(self):
        """
        DESCRIPTION: "Highlights Carousel" module should be "Active" in CMS and configured by TypeID (Premier League or Champions League))
        DESCRIPTION: Create Premier league football event with teams that have team kits
        DESCRIPTION: Create another competition football event with teams that have team kits
        DESCRIPTION: - Team kits are mapped to teams by names (e.g. to show team kit for Manchester United team name should be "Man-United")
        """
        highlights_carousels_titles = [generate_highlights_carousel_name().title(),
                                       generate_highlights_carousel_name().title()]
        england_premier_league_type_id = self.ob_config.football_config.england.premier_league.type_id
        self.__class__.italy_serie_a_liga = self.ob_config.football_config.italy_serie_a.serie_a.type_id
        football_sport_id = self.ob_config.backend.ti.football.category_id

        event_1 = self.ob_config.add_football_event_to_england_premier_league(team1='Man City', team2='Chelsea')
        event_2 = self.ob_config.add_football_event_to_italy_serie_a(team1='Chelsea', team2='Man City')
        self.__class__.event_name_1 = f'{event_1.team1} v {event_1.team2}'
        self.__class__.event_name_2 = f'{event_2.team1} v {event_2.team2}'

        # highlights carousel on Home page
        self.__class__.highlights_carousel = self.cms_config.create_highlights_carousel(
            title=highlights_carousels_titles[0],
            typeId=str(england_premier_league_type_id))

        self.__class__.highlights_carousel_name = self.convert_highlights_carousel_title(highlights_carousels_titles[0])

        # highlights carousel on Football landing page
        self.__class__.football_highlights_carousel = self.cms_config.create_highlights_carousel(
            title=highlights_carousels_titles[1],
            typeId=str(england_premier_league_type_id),
            sport_id=football_sport_id)

        self.__class__.football_highlights_carousel_name = \
            self.convert_highlights_carousel_title(highlights_carousels_titles[1])

    def test_001_verify_team_kits_displaying_on_events_cards_in_highlights_carousels_from_premier_league_or_champions_league(self):
        """
        DESCRIPTION: Verify team kits displaying on events cards in Highlights Carousels from Premier League or Champions League
        EXPECTED: - Team kits are displayed correctly according to mapped teams in Highlights Carousel configured by TypeID
        EXPECTED: - If team name has no mapped team kit - no team kit is displayed
        """
        self.site.wait_content_state(state_name='HomePage')
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name, timeout=10)

        highlight_carousels = self.site.home.tab_content.highlight_carousels
        self.assertTrue(highlight_carousels, msg='No Highlight carousels on Home Page')
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
        self.assertTrue(highlight_carousel and highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel "{self.highlights_carousel_name}"')

        highlight_carousel_events = highlight_carousel.items_as_ordered_dict
        self.assertTrue(highlight_carousel_events,
                        msg=f'No events in Highlights Carousel "{self.highlights_carousel_name}"')
        self.assertIn(self.event_name_1, highlight_carousel_events,
                      msg=f'Event "{self.event_name_1}" is not displayed in Carousel "{self.highlights_carousel_name}" '
                          f'among events "{highlight_carousel_events}"')

        event = highlight_carousel_events.get(self.event_name_1)
        self.assertTrue(event.has_team_kits, msg=f'Team kits are not displayed for event "{self.event_name_1}"')

    def test_002_in_cms_edit_highlights_carousels_with_typeid_with_teams_that_have_team_kits_but_from_another_competition(
            self,
            highlights_carousel=None,
            highlights_carousel_name=None,
            delimiter=None):
        """
        DESCRIPTION: In CMS edit Highlights Carousels with TypeID with teams that have team kits, but from another competition
        DESCRIPTION: (not from Premier League or Champions League)and save the changes
        EXPECTED: The changes are saved successfully
        """
        highlights_carousel = highlights_carousel if highlights_carousel else self.highlights_carousel
        highlights_carousel_name = highlights_carousel_name if highlights_carousel_name \
            else self.highlights_carousel_name
        self.cms_config.update_highlights_carousel(highlight_carousel=highlights_carousel,
                                                   type_id=self.italy_serie_a_liga)

        delimiter = delimiter if delimiter else '42/0,'
        result = self.wait_for_highlights_carousel_to_change_type_id(module_name=highlights_carousel_name.title(),
                                                                     type_id=self.italy_serie_a_liga,
                                                                     delimiter=delimiter)
        self.assertTrue(result, msg=f'"{highlights_carousel_name.title()}" Highlight carousel module type ID was not '
                                    f'changed to "{self.italy_serie_a_liga}"')

    def test_003_verify_team_kits_displaying_on_events_cards_in_highlights_carousels_not_from_premier_league_or_champions_league(
            self,
            highlights_carousel_name=None,
            sport_page=None):
        """
        DESCRIPTION: Verify team kits displaying on events cards in Highlights Carousels NOT from Premier League or Champions League
        EXPECTED: Team kits are NOT displayed as events are from other competitions
        """
        if sport_page:
            highlight_carousels = self.site.football.tab_content.highlight_carousels
        else:
            highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlights_carousel_name = highlights_carousel_name if highlights_carousel_name \
            else self.highlights_carousel_name
        highlight_carousel = highlight_carousels.get(highlights_carousel_name)
        self.assertTrue(highlight_carousel and highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel "{highlights_carousel_name}"')

        highlight_carousel_events = highlight_carousel.items_as_ordered_dict
        self.assertTrue(highlight_carousel_events,
                        msg=f'No events in Highlights Carousel "{highlights_carousel_name}"')
        self.assertIn(self.event_name_2, highlight_carousel_events,
                      msg=f'Event "{self.event_name_2}" is not displayed in Carousel "{highlights_carousel_name}" '
                          f'among events "{highlight_carousel_events}"')

        event = highlight_carousel_events.get(self.event_name_2)
        self.assertFalse(event.has_team_kits, msg=f'Team kits are displayed for event "{self.event_name_2}"')

    def test_004_navigate_to_the_some_sports_landing_page_and_repeat_the_steps_1_3(self):
        """
        DESCRIPTION: Navigate to the some Sports Landing page and repeat the steps 1-3
        EXPECTED:
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        self.wait_for_highlights_carousels(name=self.football_highlights_carousel_name, timeout=10, delimiter='42/16,')

        highlight_carousels = self.site.football.tab_content.highlight_carousels
        self.assertTrue(highlight_carousels, msg='No Highlight carousels on Football landing page')

        highlight_carousel = highlight_carousels.get(self.football_highlights_carousel_name)
        self.assertTrue(highlight_carousel and highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel "{self.football_highlights_carousel_name}"')

        highlight_carousel_events = highlight_carousel.items_as_ordered_dict
        self.assertTrue(highlight_carousel_events,
                        msg=f'No events in Highlights Carousel "{self.football_highlights_carousel_name}"')
        self.assertIn(self.event_name_1, highlight_carousel_events,
                      msg=f'Event "{self.event_name_1}" is not displayed in Carousel "{self.football_highlights_carousel_name}"'
                          f' among events "{highlight_carousel_events}"')

        event = highlight_carousel_events.get(self.event_name_1)
        self.assertTrue(event.has_team_kits, msg=f'Team kits are not displayed for event "{self.event_name_1}"')

        self.test_002_in_cms_edit_highlights_carousels_with_typeid_with_teams_that_have_team_kits_but_from_another_competition(
            highlights_carousel=self.football_highlights_carousel,
            highlights_carousel_name=self.football_highlights_carousel_name,
            delimiter='42/16,'
        )
        self.test_003_verify_team_kits_displaying_on_events_cards_in_highlights_carousels_not_from_premier_league_or_champions_league(
            highlights_carousel_name=self.football_highlights_carousel_name,
            sport_page=True
        )
