from time import sleep
import pytest

import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import BaseHighlightsCarouselTest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import generate_highlights_carousel_name
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.featured
@pytest.mark.highlights_carousel
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.consequent
@vtest
class Test_C2986717_Highlights_Carousel_cards_displaying_with_and_without_limitation_of_cards_to_be_displayed(BaseHighlightsCarouselTest):
    """
    TR_ID: C2986717
    VOL_ID: C9698521
    NAME: Highlights Carousel - cards displaying with and without limitation of cards to be displayed
    DESCRIPTION: This test case verifies cards displaying when limitation of cards to be displayed is set and not
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    highlights_carousels_titles = [generate_highlights_carousel_name(), generate_highlights_carousel_name()]

    def check_events(self, highlight_carousels, title):
        """
        Checks events within Highlights carousel
        :param highlight_carousels: self.site.home.tab_content.highlight_carousels
        :param title: title of carousel to verify
        """
        highlight_carousel = highlight_carousels.get(title)
        self.assertTrue(highlight_carousel and highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named {title}')
        displayed_events_names = sorted(list(highlight_carousel.items_as_ordered_dict.keys()))
        self.assertEqual(displayed_events_names, sorted([self.event_name, self.event_2_name]),
                         msg=f'Incorrect events are displayed in Highlights Carousel '
                             f'{title}\n'
                             f'Actual: {displayed_events_names}\n'
                             f'Expected: {sorted([self.event_name, self.event_2_name])}')

    def test_000_preconditions(self):
        """
        DESCRIPTION: "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
        DESCRIPTION: 2 active Highlights Carousels with active events in CMS > Sport Pages > Homepage > Highlights Carousel
        DESCRIPTION: 1) 1st Highlights Carousel should be configured by EventIDs
        DESCRIPTION: 2) 2nd Highlight Carousel is configured by TypeID
        DESCRIPTION: Both Highlights Carousels above should be without any limitation of cards to be displayed ("No. of Events" option in CMS)
        DESCRIPTION: Home page in application is opened
        """
        if tests.settings.backend_env == 'prod':
            category_id = self.ob_config.football_config.category_id
            events = self.get_active_events_for_category(category_id=category_id,
                                                         number_of_events=2)

            event_id_1 = events[0]['event']['id']
            event_id_2 = events[1]['event']['id']

            self.__class__.event_name = normalize_name(events[0]['event']['name'])
            self.__class__.event_2_name = normalize_name(events[1]['event']['name'])

            self._logger.info(f'*** First event with id "{event_id_1}" and name "{self.event_name}"')
            self._logger.info(f'*** Second event with id "{event_id_2}" and name "{self.event_2_name}"')
            self.__class__.type_id = events[0]['event']['typeId']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            event_2 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_name = event.team1 + ' v ' + event.team2
            self.__class__.event_2_name = event_2.team1 + ' v ' + event_2.team2
            event_id_1 = event.event_id
            event_id_2 = event_2.event_id

            self.__class__.type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id

        self.__class__.highlights_carousel = self.cms_config.create_highlights_carousel(title=self.highlights_carousels_titles[0],
                                                                                        events=[event_id_1, event_id_2])
        self.__class__.highlights_carousel_name_1 = self.convert_highlights_carousel_title(self.highlights_carousels_titles[0])
        self.__class__.highlights_carousel_name_2 = self.convert_highlights_carousel_title(self.highlights_carousels_titles[1])

    def test_001_verify_cards_displaying_within_highlights_carousels(self):
        """
        DESCRIPTION: Verify cards displaying within Highlights Carousel configured by event ids
        EXPECTED: All cards of available events are displayed
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name_1)

        highlight_carousels = self.site.home.tab_content.highlight_carousels

        self.check_events(highlight_carousels=highlight_carousels, title=self.highlights_carousel_name_1)

    def test_002_set_displayed_events_number_limit_in_cms(self):
        """
        DESCRIPTION: - In CMS > Sport Pages > Homepage > Highlights Carousel set some limitation "X" of events to be displayed for both Highlights Carousels from preconditions
        DESCRIPTION: - Verify cards displaying within Highlights Carousels
        EXPECTED: Highlights Carousels contain only "X" amount of cards
        """
        self.cms_config.update_highlights_carousel(self.highlights_carousel, limit=1)
        sleep(30)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        self.wait_for_highlights_carousels(name=self.highlights_carousel_name_1)

        highlight_carousels = self.site.home.tab_content.highlight_carousels

        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_1)
        self.assertTrue(highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name_1}')
        result = wait_for_result(lambda: len(highlight_carousel.items_as_ordered_dict) == 1,
                                 name=f'1 event to be displayed in Highlights carousel "{self.highlights_carousel_name_1}"',
                                 timeout=5)

        self.assertTrue(result,
                        msg=f'Only one event should be displayed after setting limit in CMS. '
                            f'Now {len(highlight_carousel.items_as_ordered_dict)} events are found')

        for highlights_carousel_id in self.cms_config._created_highlights_carousels:
            self.cms_config.delete_highlights_carousel(highlights_carousel_id)
        self.cms_config._created_highlights_carousels.clear()

        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        self.wait_for_featured_module(name=self.highlights_carousel_name_1, timeout=30,
                                      expected_result=False)

    def test_003_repeat_steps_1_2_for_highlights_carousel_configured_by_type_ID(self):
        """
        DESCRIPTION: Repeat steps 1-2 for Highlighs Carousel configured by type ID
        """
        self.__class__.type_highlights_carousel = self.cms_config.create_highlights_carousel(title=self.highlights_carousels_titles[1],
                                                                                             events=[], typeId=self.type_id, limit=1)
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name_2)

        highlight_carousels = self.site.home.tab_content.highlight_carousels

        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_2)
        self.assertTrue(highlight_carousel and highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name_2}')
        self.assertEqual(len(highlight_carousel.items_as_ordered_dict), 1,
                         msg=f'Only one event should be displayed after setting limit in CMS. '
                             f'Now {len(highlight_carousel.items_as_ordered_dict)} events are found')
