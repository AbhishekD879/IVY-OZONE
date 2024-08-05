from datetime import datetime
import pytest
from crlat_ob_client.utils.date_time import get_date_time_as_string
import tests
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
@pytest.mark.high
@pytest.mark.consequent
@vtest
class Test_C2987418_Highlights_Carousel_displaying_based_on_date_and_time(BaseHighlightsCarouselTest):
    """
    TR_ID: C2987418
    NAME: Highlights Carousel displaying based on date and time
    DESCRIPTION: This test case verifies Highlights Carousels displaying based on configured display date and time
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    """
    highlights_carousels_titles = ['Past Autotest Highlight Carousel', 'Future Autotest Highlight Carousel',
                                   'Present Autotest Highlight Carousel']
    time_format = '%Y-%m-%dT%H:%M:%S.%f'

    def test_000_preconditions(self):
        """
        DESCRIPTION: "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
        DESCRIPTION: You should have 3 active Highlights Carousels with active events in CMS > Sport Pages > Homepage > Highlights Carousel:
        DESCRIPTION: 1) 1st Highlights Carousel should be configured in past;
        DESCRIPTION: 2) 2nd Highlights Carousel should be configured in future;
        DESCRIPTION: 3) 3rd Highlights Carousel should be configured to include current date and time.
        DESCRIPTION: Home page in application is opened
        """
        if tests.settings.backend_env == 'prod':
            category_id = self.ob_config.football_config.category_id
            events = self.get_active_events_for_category(category_id=category_id,
                                                         number_of_events=3)

            event_id_1 = events[0]['event']['id']
            event_id_2 = events[1]['event']['id']
            event_id_3 = events[2]['event']['id']

            self._logger.info(f'*** First event with id "{event_id_1}"')
            self._logger.info(f'*** Second event with id "{event_id_2}"')
            self._logger.info(f'*** Third event with id "{event_id_3}"')
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            event_2 = self.ob_config.add_autotest_premier_league_football_event()
            event_3 = self.ob_config.add_autotest_premier_league_football_event()

            event_id_1 = event.event_id
            event_id_2 = event_2.event_id
            event_id_3 = event_3.event_id

        now = datetime.now()
        cms = self.cms_config

        date_from = get_date_time_as_string(date_time_obj=now, time_format=self.time_format, url_encode=False, days=-2)[:-3] + 'Z'
        date_to = get_date_time_as_string(date_time_obj=now, time_format=self.time_format, url_encode=False, days=-1)[:-3] + 'Z'
        self.__class__.past_highlights_carousel = cms.create_highlights_carousel(
            title=self.highlights_carousels_titles[0], events=[event_id_1], date_from=date_from, date_to=date_to)

        date_from = get_date_time_as_string(date_time_obj=now, time_format=self.time_format, url_encode=False, minutes=1)[:-3] + 'Z'
        date_to = get_date_time_as_string(date_time_obj=now, time_format=self.time_format, url_encode=False, days=1)[:-3] + 'Z'
        self.__class__.future_highlights_carousel = cms.create_highlights_carousel(
            title=self.highlights_carousels_titles[1], events=[event_id_2], date_from=date_from, date_to=date_to)

        self.__class__.current_highlights_carousel = cms.create_highlights_carousel(
            title=self.highlights_carousels_titles[2], events=[event_id_3])

        self.__class__.past_highlights_carousel_name = self.convert_highlights_carousel_title(self.highlights_carousels_titles[0])
        self.__class__.future_highlights_carousel_name = self.convert_highlights_carousel_title(self.highlights_carousels_titles[1])
        self.__class__.present_highlights_carousel_name = self.convert_highlights_carousel_title(self.highlights_carousels_titles[2])

    def test_001_verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: Verify Highlights Carousel displaying
        EXPECTED: Only Highlights Carousel that includes current date and time is displayed
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_highlights_carousels(name=self.present_highlights_carousel_name)
        highlight_carousels = self.site.home.tab_content.highlight_carousels

        self.assertNotIn(self.past_highlights_carousel_name, highlight_carousels.keys(),
                         msg=f'Highlights Carousel named {self.past_highlights_carousel_name} should be not displayed')
        self.assertNotIn(self.future_highlights_carousel_name, highlight_carousels.keys(),
                         msg=f'Highlights Carousel named {self.future_highlights_carousel_name} should be not displayed')

        highlight_carousel = highlight_carousels.get(self.present_highlights_carousel_name)
        self.assertTrue(highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named {self.present_highlights_carousel_name}')

    def test_002_edit_future_highlights_carousel_to_be_displayed_in_couple_minutes(self):
        """
        DESCRIPTION: - In CMS > Sport Pages > Homepage > Highlights Carousel edit currently displayed Highlights Carousel to be undisplayed in couple minutes
        DESCRIPTION: - In CMS > Sport Pages > Homepage > Highlights Carousel edit future Highlights Carousel to be displayed in couple minutes
        DESCRIPTION: - Wait for the configured time and refresh the page in application
        DESCRIPTION: - Verify Highlights Carousel displaying
        EXPECTED: Only Highlights Carousel that includes current date and time is displayed
        """
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=-2)[:-3] + 'Z'
        self.cms_config.update_highlights_carousel(
            highlight_carousel=self.current_highlights_carousel,
            end_time=end_time)

        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=-2)[:-3] + 'Z'
        self.cms_config.update_highlights_carousel(
            highlight_carousel=self.future_highlights_carousel,
            start_time=start_time)

        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        self.wait_for_highlights_carousels(name=self.future_highlights_carousel_name)

        result1 = wait_for_result(lambda: self.past_highlights_carousel_name in self.site.home.tab_content.highlight_carousels.keys(),
                                  name=f'Highlight carousel "{self.past_highlights_carousel_name}" to dissappear',
                                  timeout=2,
                                  bypass_exceptions=(KeyError, AttributeError),
                                  expected_result=False)
        self.assertFalse(result1,
                         msg=f'Highlights Carousel named {self.past_highlights_carousel_name} should disappear')

        result2 = wait_for_result(lambda: self.present_highlights_carousel_name in self.site.home.tab_content.highlight_carousels.keys(),
                                  name=f'Highlight carousel "{self.present_highlights_carousel_name}" to disappear',
                                  timeout=2,
                                  bypass_exceptions=(KeyError, AttributeError),
                                  expected_result=False)
        self.assertFalse(result2,
                         msg=f'Highlights Carousel named {self.present_highlights_carousel_name} should disappear')

        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.future_highlights_carousel_name)
        self.assertTrue(highlight_carousel and highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named {self.future_highlights_carousel_name}')
