import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl  # we can't trigger live updates on prod and hl
@pytest.mark.desktop
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.liveserv_updates
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C28903_Event_becomes_Suspended_on_Race_Event_Details_Page(BaseRacing):
    """
    TR_ID: C28903
    NAME: Event becomes Suspended on <Race> Event Details Page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Preconditions
        DESCRIPTION: Prepare event for test
        """
        self.__class__.eventID = self.ob_config.add_UK_racing_event(number_of_runners=2, lp_prices={0: '7/8', 1: ''}).event_id

    def test_001_open_race_event_details_page(self):
        """
        DESCRIPTION: Open <Race> Event Details page
        EXPECTED: <Race> Event Details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

    def test_002_suspend_event_in_ti_at_the_same_time_have_edp_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Suspend event in TI:
        DESCRIPTION: **eventStatusCode="S"**
        DESCRIPTION: and at the same time have Event Details page opened to watch for updates
        EXPECTED: All Price/Odds buttons of this event are displayed immediately as greyed out and become disabled, but still displaying the prices or SP value
        """
        self.ob_config.change_event_state(event_id=self.eventID, active=False, displayed=True)

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        self.__class__.outcomes = section.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='No outcomes found')
        # todo: VOL-1970
        for outcome_name, outcome in self.outcomes.items():
            bet_button = outcome.bet_button
            self.assertFalse(bet_button.is_enabled(expected_result=False, timeout=50),
                             msg=f'{outcome_name} is not disabled')
            self.assertTrue(bet_button.name, msg=f'{outcome_name} bet button price is not shown')

    def test_003_make_event_active_again_in_ti_at_the_same_time_have_edp_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Make event Active again in TI:
        DESCRIPTION: **eventStatusCode="A"**
        DESCRIPTION: and at the same time have Event Details page opened to watch for updates
        EXPECTED: All Price/Odds buttons of this event are no more disabled, they become active immediately
        """
        self.ob_config.change_event_state(event_id=self.eventID, active=True, displayed=True)
        for outcome_name, outcome in self.outcomes.items():
            self.assertTrue(outcome.bet_button.is_enabled(timeout=15), msg=f'{outcome_name} is not enabled')
