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
@pytest.mark.issue("https://jira.egalacoral.com/browse/BMA-52604")  # desktop coral only
class Test_C2745929_Verify_behavior_of_Meeting_time_in_International_Tote_Races_Carousel(BaseInternationalTote):
    """
    TR_ID: C2745929
    NAME: Verify behavior of Meeting time in International Tote Races Carousel
    DESCRIPTION: This test case verifies behavior of Meeting time in International Tote Races Carousel
    PRECONDITIONS: **Instruction on Tote events mapping on test environment**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+International+Tote+events+with+Regular+Horse+Racing+events
    PRECONDITIONS: **CMS configuration**
    PRECONDITIONS: System configuration > Structure: InternationalTotePool is enabled
    PRECONDITIONS: International Tote Races are available.
    PRECONDITIONS: International Tote Races Carousel is present below UK Races
    PRECONDITIONS: ***User is on Horse racing landing page.***
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Navigate to Horseracing and get suitable event
        """
        event = self.get_int_tote_event()
        self.__class__.event_name = event.int_tote_typename[:4]

        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        self.site.horse_racing.tab_content.scroll_to_bottom()
        self.__class__.tote_events = self.site.horse_racing.tab_content.tote_events_carousel.items_as_ordered_dict
        self.assertTrue(self.tote_events, msg='No Tote Events found')

    def test_001_tap_on_any_of_the_meeting_time_which_is_not_finished_(self):
        """
        DESCRIPTION: Tap on any of the Meeting time (which is not finished )
        EXPECTED: - User should go to the Race card of respective Meeting
        EXPECTED: - Meeting time is selected
        EXPECTED: - 'Tote Pool' Tab should be selected
        EXPECTED: - First default pool should be selected and content is loaded
        """
        for event_name, event in self.tote_events.items():
            if event_name[:4] == self.event_name:
                event.click()
                break
        self.site.wait_content_state('RacingEventDetails')

        tab_content = self.site.racing_event_details.tab_content
        self.assertTrue(tab_content.event_off_times_list.selected_item, msg='No selected event time')
        tab_opened = tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg=f'"{vec.uk_tote.TOTEPOOL}" tab is not opened')
