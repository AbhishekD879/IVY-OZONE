import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.surface_bets
@pytest.mark.event_details
@vtest
class Test_C9770810_Verify_Surface_Bet_module_displaying_on_the_Racing_Card(BaseFeaturedTest):
    """
    TR_ID: C9770810
    VOL_ID: C12587644
    NAME: Verify Surface Bet module displaying on the Racing Card
    DESCRIPTION: Test case verifies that Surface Bet isn't shown on the Racing card
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. There is a single Surface Bet added to the racing event (Horse/Greyhound racing)
        PRECONDITIONS: 2. Valid Selection Id is set
        PRECONDITIONS: 3. Open this event's racing card
        """
        event = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1)
        event_2 = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.event_id = event.event_id
        self.__class__.event_id_2 = event_2.event_id
        self.cms_config.add_surface_bet(selection_id=list(event.selection_ids.values())[0],
                                        eventIDs=[self.event_id, self.event_id_2], edpOn=True,
                                        categoryIDs=[self.ob_config.horseracing_config.category_id,
                                                     self.ob_config.backend.ti.greyhound_racing.category_id])

    def test_001_verify_the_surface_bet_isnt_displayed_on_the_racing_cards(self):
        """
        DESCRIPTION: Verify the Surface Bet isn't displayed on the Racing cards
        EXPECTED: Surface Bet isn't shown
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='greyhound-racing')
        self.assertFalse(self.site.greyhound_event_details.tab_content.has_surface_bets(expected_result=False),
                         msg='Surface Bet module is shown on the greyhound card')

        self.navigate_to_edp(event_id=self.event_id_2, sport_name='horse-racing')
        self.assertFalse(self.site.racing_event_details.tab_content.has_surface_bets(expected_result=False),
                         msg='Surface Bet module is shown on the racing card')
