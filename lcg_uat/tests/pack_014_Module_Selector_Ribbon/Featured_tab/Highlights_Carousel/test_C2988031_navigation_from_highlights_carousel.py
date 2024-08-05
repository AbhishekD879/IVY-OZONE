import pytest
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    BaseHighlightsCarouselTest
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
class Test_C2988031_Navigation_from_Highlights_Carousel(BaseHighlightsCarouselTest):
    """
    TR_ID: C2988031
    VOL_ID: C9698537
    NAME: Navigation from Highlights Carousel
    DESCRIPTION: This test case verifies navigation from Highlights Carousel
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    highlights_carousels_titles = ['Autotest Highlight Carousel with Event', 'Autotest Highlight Carousel with Type ID',
                                   'Autotest Highlight Carousel with Tennis']

    def test_000_preconditions(self):
        """
        DESCRIPTION: "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
        DESCRIPTION: 2 active Highlights Carousels with active events in CMS > Sport Pages > Homepage > Highlights Carousel
        DESCRIPTION: Home page in application is opened
        """
        if tests.settings.backend_env == 'prod':
            category_id = self.ob_config.football_config.category_id
            event = self.get_active_events_for_category(category_id=category_id)[0]

            event_id_1 = event['event']['id']
            self.__class__.event_name = event['event']['name']
            self._logger.info(f'*** First football event with id "{event_id_1}" and name "{self.event_name}"')

            self.__class__.type_id = event['event']['typeId']

            category_id = self.ob_config.tennis_config.category_id
            tennis_event = self.get_active_events_for_category(category_id=category_id)[0]
            self.__class__.tennis_event_name = tennis_event['event']['name']
            self._logger.info(f'*** First tennis event with name "{self.tennis_event_name}"')
            self.__class__.tennis_type_id = tennis_event['event']['typeId']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            event_id_1 = event.event_id
            self.__class__.event_name = event.team1 + ' v ' + event.team2

            tennis_event = self.ob_config.add_tennis_event_to_autotest_trophy()
            self.__class__.tennis_event_name = tennis_event.team1 + ' v ' + tennis_event.team2

            self.__class__.type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
            self.__class__.tennis_type_id = self.ob_config.tennis_config.tennis_autotest.autotest_trophy.type_id

        self.__class__.highlights_carousel = self.cms_config.create_highlights_carousel(
            title=self.highlights_carousels_titles[0], events=[event_id_1])

        self.__class__.type_highlights_carousel = self.cms_config.create_highlights_carousel(
            title=self.highlights_carousels_titles[1], events=None, typeId=self.type_id)

        self.__class__.highlights_carousel_name_event = self.convert_highlights_carousel_title(self.highlights_carousels_titles[0])
        self.__class__.highlights_carousel_name_type_id = self.convert_highlights_carousel_title(self.highlights_carousels_titles[1])
        self.__class__.highlights_carousel_name_tennis = self.convert_highlights_carousel_title(self.highlights_carousels_titles[2])

    def test_001_tap_any_events_card_from_both_highlights_carousels_and_verify_navigation(self):
        """
        DESCRIPTION: Tap any events' card from both Highlights Carousels and verify navigation
        EXPECTED: User is navigated to event details page of the respective event
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name_event)

        highlight_carousels = self.site.home.tab_content.highlight_carousels

        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_event)
        self.assertTrue(highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name_event}')
        highlight_carousel_events = highlight_carousel.items_as_ordered_dict
        self.assertTrue(highlight_carousel_events,
                        msg=f'No events in Highlights Carousel named "{self.highlights_carousel_name_event}"')
        highlight_carousel_events[self.event_name].event_name_we.click()
        self.site.wait_content_state(state_name='EventDetails')
        actual_event_name = self.site.sport_event_details.event_title_bar.event_name
        self.assertEqual(actual_event_name, self.event_name,
                         msg=f'Incorrect EDPis opened.\n'
                             f'Actual event name is "{actual_event_name}"\n'
                             f'Expected event name is "{self.event_name}"')

        self.device.open_url(tests.HOSTNAME)
        self.site.wait_content_state(state_name='Home')
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name_type_id)

        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_type_id)
        self.assertTrue(highlight_carousel and highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name_type_id}')
        highlight_carousel_events = highlight_carousel.items_as_ordered_dict
        self.assertTrue(highlight_carousel_events,
                        msg=f'No events in Highlights Carousel named "{self.highlights_carousel_name_type_id}"')

        event_name = list(highlight_carousel.items_as_ordered_dict.keys())[0]
        highlight_carousel.items_as_ordered_dict[event_name].event_name_we.click()
        self.site.wait_content_state(state_name='EventDetails')
        actual_event_name = self.site.sport_event_details.event_title_bar.event_name
        self.assertEqual(actual_event_name, event_name,
                         msg=f'Incorrect EDPis opened.\n'
                             f'Actual event name is "{actual_event_name}"\n'
                             f'Expected event name is "{event_name}"')

    def test_002_tap_see_all_link_on_highlights_carousel_configured_by_typeid(self):
        """
        DESCRIPTION: - Go back to home page
        DESCRIPTION: - Tap "See All" link on Highlights Carousel configured by TypeID
        EXPECTED: - User is navigated to Competitions page of the Type that the Highlights Carousel is configured and can see all events from that type
        EXPECTED: - If sport or type doesn't have corresponding Competitions page then empty Competitions page is shown with a message "No events found"
        """
        self.device.open_url(tests.HOSTNAME)
        self.site.wait_content_state(state_name='Homepage')

        query_builder = self.ss_query_builder\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_SORT_CODE, OPERATORS.NOT_INTERSECTS,
                                      vec.siteserve.OUTRIGHT_EVENT_SORT_CODES))
        ss_events = self.ss_req.ss_event_to_outcome_for_type(type_id=self.type_id, query_builder=query_builder)

        ss_events_names = []
        for ss_event in ss_events:
            if 'event' in ss_event and 'children' in ss_event['event']:
                markets = ss_event['event']['children']
            else:
                continue
            for market in markets:
                if 'market' in market and 'children' in market['market'] and market['market']['children'] != []:
                    ss_events_names.append(ss_event['event']['name'])

        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_type_id)
        self.assertTrue(highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name_type_id}')
        self.assertTrue(highlight_carousel.has_see_all_link(),
                        msg='"See all" link should be displayed for highlights carousel configured by TypeID')

        highlight_carousel.see_all_link.click()
        self.site.wait_content_state(state_name='CompetitionLeaguePage')
        sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Competitions page appears to be empty')
        competition_events_names = []
        for section in sections.values():
            events_names = list(section.items_as_ordered_dict.keys())
            competition_events_names.append(events_names)
        competition_event_names_flat_list = [item for inner in competition_events_names for item in inner]
        for event in competition_event_names_flat_list:
            self.assertIn(event, sorted(list(set(ss_events_names))),
                          msg=f'Events displayed in Highlights Carousel "{self.highlights_carousel_name_type_id}" '
                              f'and Competitions page are not the same\n'
                              f'Actual (displayed on the page): {sorted(competition_event_names_flat_list)}\n'
                              f'Expected (SiteServe): {sorted(list(set(ss_events_names)))}')

        for highlights_carousel_id in self.cms_config._created_highlights_carousels:
            self.cms_config.delete_highlights_carousel(highlights_carousel_id)
        self.cms_config._created_highlights_carousels.clear()
        self.highlights_carousels.clear()

        highlights_carousel = self.cms_config.create_highlights_carousel(
            title=self.highlights_carousels_titles[2], events=None, typeId=self.tennis_type_id, inPlay=True)

        self.device.open_url(tests.HOSTNAME)
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name_tennis, timeout=30)
        self.highlights_carousels.append(highlights_carousel)
        wait_for_result(lambda: self.site.home.tab_content.has_highlight_carousels,
                        name='Highlights Carousel section to appear', timeout=10)

        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_tennis)
        self.assertTrue(highlight_carousel and highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name_tennis}')
        self.assertTrue(highlight_carousel.has_see_all_link(),
                        msg='"See all" link should be displayed for highlights carousel configured by TypeID')

        highlight_carousel.see_all_link.click()
        self.site.wait_content_state(state_name='CompetitionLeaguePage')

        if not self.site.competition_league.tab_content.accordions_list.items:
            self.assertTrue(self.site.competition_league.tab_content.has_no_events_label(),
                            msg='"No events found" message should be displayed')
        else:
            items = self.site.competition_league.tab_content.accordions_list.items
            events = []
            for item in items:
                for event in item.items_as_ordered_dict.keys():
                    events.append(event)
            self.assertIn(self.tennis_event_name, events,
                          msg=f'Event "{self.tennis_event_name}" was not found in "{events}"')
