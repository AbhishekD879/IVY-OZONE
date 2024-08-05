import pytest
from tests.base_test import vtest
from tests.pack_011_RACES_Specifics.Horse_Racing_Specifics.Horse_Racing_Event_Details_Page.Tote_Pool_tab.BaseInternationalTote import \
    BaseInternationalTote
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.international_tote
@pytest.mark.frequent_blocker
@vtest
class Test_C2727621_Verify_International_Tote_Races_Carousel(BaseInternationalTote):
    """
    TR_ID: C2727621
    NAME: Verify International Tote Races Carousel
    DESCRIPTION: This test case verifies International Tote Races Carousel
    PRECONDITIONS: **Instruction on Tote events mapping on test environment**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+International+Tote+events+with+Regular+Horse+Racing+events
    PRECONDITIONS: **CMS configuration**
    PRECONDITIONS: System configuration > Structure: InternationalTotePool is enabled
    PRECONDITIONS: International Tote Races are available.
    PRECONDITIONS: International Tote Races Carousel is present below UK Races
    PRECONDITIONS: To get all available 'Events' on HR Landing page use the link:
    PRECONDITIONS: EventToMarketForEvent/{event-id1},{event-id2}
    PRECONDITIONS: **Note:** NOT showing International Tote Races Carousel when NO Tote races are available
    PRECONDITIONS: ***User is on Horse racing landing page.***
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Check if int pools are available
        """
        self.get_int_tote_event()

    def test_001_verify_content_of_international_tote_races_carousel(self):
        """
        DESCRIPTION: Verify content of International Tote Races Carousel
        EXPECTED: International Tote Races Carousel should contain:
        EXPECTED: - Text "TOTE EVENTS" (for Ladbrokes)
        EXPECTED: - Meeting Timing
        EXPECTED: - Meeting Venue (if it is more than five characters it should be truncated to 5 characters)
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

        self.__class__.tote_events = self.site.horse_racing.tab_content.tote_events_carousel

        if self.brand == 'ladbrokes':
            self.assertEqual(self.tote_events.meeting_name, vec.tote.TOTE_EVENTS,
                             msg=f'Carousel header "{self.tote_events.meeting_name}" is '
                                 f'not the same as expected "{vec.tote.TOTE_EVENTS}"')
        tote_events = self.tote_events.items
        self.assertTrue(tote_events, msg='No Tote Events found')
        for event in tote_events:
            self.assertTrue(event.event_time, msg='Event does not have time')
            self.assertTrue(len(event.name) <= 5,
                            msg=f'Event name "{event.name}" is longer than 5 characters')

    def test_002_verify_order_of_meetings(self):
        """
        DESCRIPTION: Verify order of Meetings
        EXPECTED: - Events are ordered by Meeting time
        EXPECTED: - Finished Races should shown in Meeting time order on the left side before unfinished ones.
        EXPECTED: - Unfinished Meetings should be shown in order after finished Races.
        EXPECTED: - if Meeting times are same for 2 or more meetings than it should be shown as per OB event ID order
        """
        all_event_times = []
        event_times_resulted = []
        event_times_not_resulted = []
        for event in self.tote_events.items:
            all_event_times.append(event.event_time)
            if event.is_resulted:
                event_times_resulted.append(event.event_time)
            else:
                event_times_not_resulted.append(event.event_time)

        expected_event_times = sorted(event_times_resulted) + sorted(event_times_not_resulted)

        self.assertEqual(all_event_times, expected_event_times,
                         msg=f'Events are not ordered by meeting time. Expected event times are: "{expected_event_times}",'
                             f' while actual times are: "{all_event_times}"')

        # the rest expected results can not be checked

    def test_003_verify_ability_to_swipe_the_carousel_right_to_left_and_vice_versa(self):
        """
        DESCRIPTION: Verify ability to swipe the carousel right to left and vice versa
        EXPECTED: User should be able to move the carousel right to left and vice versa
        """
        last_event = self.tote_events.items[-1]
        first_event = self.tote_events.items[0]
        self.assertTrue(last_event.is_displayed(), msg=f'Last event "{last_event.name}" is not displayed')
        self.assertTrue(first_event.is_displayed(), msg=f'First event "{first_event.name}" is not displayed')
