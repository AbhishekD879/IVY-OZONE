import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.cash_out
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.safari
@vtest
class Test_C650618_Cash_Out_icon(BaseRacing):
    """
    TR_ID: C650618
    NAME: Verify 'Cash Out' icon displaying for Racing events with available cash out
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add Horse Racing test event with available cash out
        EXPECTED: Test events with available Cash Out was created
        """
        event = self.ob_config.add_UK_racing_event(time_to_start=2, number_of_runners=1)
        self.__class__.racing_event_off_time = event.event_off_time
        self.__class__.eventID = event.event_id

    def test_001_navigate_to_event_details_page_of_event_with_cashoutavaily_attribute_on_market_level(self):
        """
        DESCRIPTION: Navigate to Event details page of event with **cashoutAvail="Y"** attribute on Market level
        EXPECTED: 'CASH OUT' icon is displayed in the same line as the Each-way terms from the right side (next to BPG icon if available)
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        markets = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = list(markets.values())[0]

        self.assertTrue(market.section_header, msg='Racing terms section was not found')
        self.assertTrue(market.section_header.cash_out_label.is_displayed(),
                        msg=f'Cash out label not displayed on event: "{self.racing_event_off_time}" details page')
