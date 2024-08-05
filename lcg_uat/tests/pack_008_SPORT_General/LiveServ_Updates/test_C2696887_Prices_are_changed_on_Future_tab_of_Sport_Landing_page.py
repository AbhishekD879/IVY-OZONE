import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.handball
@pytest.mark.liveserv_updates
@pytest.mark.medium
@pytest.mark.desktop  # Today / Tomorrow / Future tabs are present only on desktop
@pytest.mark.sports
@pytest.mark.safari
@vtest
class Test_C2696887_Prices_are_changed_on_Future_tab_of_Sport_Landing_page(BaseSportTest):
    """
    TR_ID: C2696887
    VOL_ID: C9698406
    NAME: Prices are changed on Future tab of <Sport> Landing page
    DESCRIPTION: This test case verifies Prices changes on Future tab of <Sport> Landing page
    PRECONDITIONS: There are <Sport> Future's events
    PRECONDITIONS: LiveServer is available only for In-Play <Sport> events with the following attributes:
    PRECONDITIONS:  - drilldownTagNames="EVFLAG_BL"
    PRECONDITIONS:  - isMarketBetInRun = "true"
    """
    keep_browser_open = True
    handball_section_name = f'CROATIA - {tests.settings.handball_croatia_dukat_premijer_liga}'
    increased_price = '5/2'
    decreased_price = '1/8'
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        start_time = self.get_date_time_formatted_string(days=3)
        event_params = self.ob_config.add_handball_event_to_croatian_premijer_liga(start_time=start_time)
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
        self.__class__.first_selection_name = event_params.team1
        self.__class__.first_selection_id = event_params.selection_ids[event_params.team1]

    def test_001_open_future_tab_of_sport_landing_page(self):
        """
        DESCRIPTION: Open Future tab of <Sport> Landing page
        EXPECTED: Future tab is selected
        """
        self.navigate_to_page('sport/handball')
        self.site.wait_content_state(state_name='Handball')

        self.site.handball.date_tab.future.click()
        self.assertEqual(self.site.handball.date_tab.current_date_tab, vec.sb.SPORT_DAY_TABS.future,
                         msg=f'Current active date tab: "{self.site.sports_page.date_tab.current_date_tab}", '
                             f'expected: "{vec.sb.SPORT_DAY_TABS.future}"')

    def test_002_trigger_price_change_for_outcome_from_primary_market(self):
        """
        DESCRIPTION: Trigger price change for outcome from <Primary market> for one of events from the current page
        EXPECTED: Corresponding 'Price/Odds' button immediately displays new price and for a few seconds it changes its colour to:
        EXPECTED:  - blue colour if price has decreased
        EXPECTED:  - pink colour if price has increased
        EXPECTED: Note: colours flashing is not automated
        """
        self.ob_config.change_price(selection_id=self.first_selection_id, price=self.increased_price)
        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.first_selection_id,
                                                                 price=self.increased_price)
        self.assertTrue(price_update,
                        msg=f'Price update for selection "{self.event_name}" with id '
                            f'"{self.first_selection_id}" is not received')
        self.__class__.handball_section = self.get_section(section_name=self.handball_section_name)
        self.assertTrue(self.handball_section, msg=f'Section: "{self.handball_section_name}" not found')
        price_button = self.handball_section.get_bet_button_by_selection_id(selection_id=self.first_selection_id)
        self.assertTrue(price_button, msg=f'Selection: "{self.first_selection_name}" bet button not found')
        self.assertTrue(price_button.is_price_changed(self.increased_price, timeout=20),
                        msg=f'Actual selection: "{self.first_selection_name}" '
                            f'price: "{price_button.outcome_price_text}", '
                            f'expected: "{self.increased_price}"')

        self.ob_config.change_price(selection_id=self.first_selection_id, price=self.decreased_price)
        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.first_selection_id,
                                                                 price=self.decreased_price)
        self.assertTrue(price_update,
                        msg=f'Price update for selection "{self.event_name}" with id '
                            f'"{self.first_selection_id}" is not received')
        price_button = self.handball_section.get_bet_button_by_selection_id(selection_id=self.first_selection_id)
        self.assertTrue(price_button, msg=f'Selection: "{self.first_selection_name}" price button not found')
        self.assertTrue(price_button.is_price_changed(self.decreased_price, timeout=20),
                        msg=f'Actual selection: "{self.first_selection_name}" '
                            f'price: "{price_button.outcome_price_text}", '
                            f'expected: "{self.decreased_price}"')

    def test_003_verify_prices_changes_for_sections_in_a_collapsed_state(self):
        """
        DESCRIPTION: Verify prices changes for sections in a collapsed state
        EXPECTED: If section is collapsed and price was changed, after expanding the section - updated price will be shown there
        """
        self.handball_section.collapse()
        self.ob_config.change_price(selection_id=self.first_selection_id, price=self.increased_price)
        handball_section = self.get_section(section_name=self.handball_section_name)
        handball_section.expand()
        handball_section = self.get_section(section_name=self.handball_section_name)
        price_button = handball_section.get_bet_button_by_selection_id(selection_id=self.first_selection_id)
        self.assertTrue(price_button, msg=f'Selection: "{self.first_selection_name}" bet button not found')
        self.assertTrue(price_button.is_price_changed(self.increased_price, timeout=20),
                        msg=f'Actual selection: "{self.first_selection_name}" '
                            f'price: "{price_button.outcome_price_text}", '
                            f'expected: "{self.increased_price}"')

        handball_section.collapse()
        self.ob_config.change_price(selection_id=self.first_selection_id, price=self.decreased_price)
        handball_section = self.get_section(section_name=self.handball_section_name)
        handball_section.expand()
        handball_section = self.get_section(section_name=self.handball_section_name)
        price_button = handball_section.get_bet_button_by_selection_id(selection_id=self.first_selection_id)
        self.assertTrue(price_button, msg=f'Selection: "{self.first_selection_name}" price button not found')
        self.assertTrue(price_button.is_price_changed(self.decreased_price, timeout=20),
                        msg=f'Actual selection: "{self.first_selection_name}" '
                            f'price: "{price_button.outcome_price_text}", '
                            f'expected: "{self.decreased_price}"')
