import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.horseracing
@pytest.mark.races
@vtest
class Test_C60094831_Verify_chevron_display_long_name(BaseRacing):
    """
    TR_ID: C60094831
    NAME: Verify chevron display-long name
    DESCRIPTION: Verify that chevron is not hidden if there is a long name and is displayed as ellipses "..." before
    the chevron and also there is always minimum of 12px between bet filter and the chevron.
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Bet Filter should be enabled in CMS
    PRECONDITIONS: 3: Long Course name
    """
    keep_browser_open = True
    section_skip_list = ['VIRTUAL RACING', 'VIRTUAL RACE CAROUSEL', 'ENHANCED RACES', 'NEXT RACES',
                         'OFFERS & FEATURED RACES', 'INTERNATIONAL TOTE CAROUSEL',
                         'YOURCALL SPECIALS', 'EXTRA PLACE OFFER', 'ENHANCED MULTIPLES', 'EXTRA PLACE RACES']

    def verify_bet_filter_page(self):
        self.site.wait_content_state(state_name='HorseRacingBetFilterPage')
        bet_filter = self.site.horseracing_bet_filter
        self.assertEqual(bet_filter.page_title.text, vec.bet_finder.BF_HEADER_TITLE,
                         msg=f'Bet filter page\'s title is incorrect.\n Expected is "{bet_filter.page_title.text}", '
                             f'Actual is "{vec.bet_finder.BF_HEADER_TITLE}"')
        if self.brand == 'bma':
            self.assertEqual(bet_filter.header_line.page_title.sport_title, vec.bet_finder.BF_HEADER_TITLE,
                             msg=f'Bet filter header line title is incorrect.\n '
                                 f'Expected is "{bet_filter.header_line.page_title.sport_title}",'
                                 f'Actual is "{vec.bet_finder.BF_HEADER_TITLE}"')
        self.assertEqual(bet_filter.description.text, vec.bet_finder.BF_HEADER_TEXT,
                         msg=f'Bet filter page description is incorrect.\n '
                             f'Expected is "{bet_filter.description.text}", '
                             f'Actual is "{vec.bet_finder.BF_HEADER_TEXT}"')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Enable horse racing bet filter
        """
        if tests.settings.backend_env != 'prod':
            hr_bet_filter_status = self.cms_config.verify_and_update_bet_filter_horse_racing_status(status=True)
            self.assertTrue(hr_bet_filter_status, msg='Bet Filter is disabled')

    def test_001_launch_ladbrokes_coral_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral App
        EXPECTED: App should be opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        all_items = self.site.home.menu_carousel.items_as_ordered_dict
        self.assertTrue(all_items, msg='No items on MenuCarousel found')
        if self.brand == 'bma':
            all_items.get(vec.SB.HORSERACING.upper()).click()
        else:
            all_items.get(vec.SB.HORSERACING).click()
        self.site.wait_content_state_changed(timeout=10)
        self.site.wait_content_state('horse-racing')

    def test_003_click_on_race_which_has_a_long_course_name(self):
        """
        DESCRIPTION: Click on race which has a long course name
        EXPECTED: User should be navigated to the Event details page
        """
        max_length = -1
        self.site.wait_splash_to_hide()
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Failed to display any section')
        for section_name, section in sections.items():
            if section_name in self.section_skip_list or self.next_races_title in section_name:
                continue
            else:
                self.meetings = section.items_as_ordered_dict
                self.assertTrue(self.meetings, msg='Failed to display any meeting')
                for meeting_name, meeting in self.meetings.items():
                    self.meetings = section.items_as_ordered_dict
                    if len(meeting_name) > max_length:
                        max_length = len(meeting_name)
                        self.max_len_meeting = meeting
        events = self.max_len_meeting.items_as_ordered_dict
        self.assertTrue(events, msg='Failed to display any event')
        event = list(events.values())[0]
        self.assertTrue(event, msg='Could not find event')
        event.click()
        self.site.wait_content_state_changed()
        self.site.wait_content_state(state_name='RacingEventDetails')

    def test_004_validate_breadcrumbs_contentindexphpattachmentsget118934682indexphpattachmentsget118934683(self):
        """
        DESCRIPTION: Validate breadcrumbs content
        DESCRIPTION: ![](index.php?/attachments/get/118934682)
        DESCRIPTION: ![](index.php?/attachments/get/118934683)
        EXPECTED: 1: User should be displayed "Bet Filter" to the right corner
        EXPECTED: 2: Chevron should not be hidden
        EXPECTED: 3: Ellipses "...." should be displayed before the Chevron when there is a long name
        EXPECTED: 4: 12 px should be there between the Chevron and betfilter
        """
        has_bet_filter_link = self.site.racing_event_details.has_bet_filter_link
        self.assertTrue(has_bet_filter_link, msg='Event details page doesn\'t have back button')
        self.assertTrue(self.site.racing_event_details.breadcrumbs.toggle_icon.is_displayed(),
                        msg='Toggle icon is not displayed')
        breadcrumb_list = list(self.site.racing_event_details.breadcrumbs.items_as_ordered_dict.keys())[-1:]
        dots = ''.join(breadcrumb_list)
        self.assertEqual(dots[-3:], '...', msg=f'Ellipses "..." is not displayed before the '
                                               f'Chevron when there is a long name')
