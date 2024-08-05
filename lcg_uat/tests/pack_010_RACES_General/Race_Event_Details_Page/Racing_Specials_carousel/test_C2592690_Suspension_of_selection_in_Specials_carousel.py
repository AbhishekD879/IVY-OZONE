import pytest

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.cms
@pytest.mark.specials_carousel
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C2592690_Suspension_of_selection_in_Specials_carousel(BaseRacing):
    """
    TR_ID: C2592690
    VOL_ID: C9690174
    NAME: Suspension of selection in Specials carousel
    DESCRIPTION: This test case verifies suspension of the selection in Specials carousel on the event/market/selection levels
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - How to link selections to event: https://confluence.egalacoral.com/display/SPI/How+to+link+selections+to+event
    PRECONDITIONS: - You should have a linked selection to <Race> event
    PRECONDITIONS: - "Racing Specials Carousel" should be enabled in CMS > System Configuration > Structure
    PRECONDITIONS: - You should be on a <Race> EDP that has linked selections
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create racing specials events
        EXPECTED: Events are created in OB
        """
        cms_config = self.get_initial_data_system_configuration().get('RacingSpecialsCarousel', {})
        if not cms_config:
            cms_config = self.cms_config.get_system_configuration_item('RacingSpecialsCarousel')
        is_racing_specials_carousel_enabled = cms_config.get('enable')
        if not is_racing_specials_carousel_enabled:
            raise CmsClientException('Racing specials carousel is not enabled in CMS')
        if cms_config.get('label') == '':
            self.__class__.cms_racing_specials_label = vec.racing.RACING_SPECIALS_CAROUSEL_LABEL
        else:
            self.__class__.cms_racing_specials_label = cms_config.get('label', None)

        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.selection_name, self.__class__.selection_id = list(event_params.selection_ids.items())[0]
        self.__class__.marketID = event_params.market_id
        self.__class__.eventID1 = event_params.event_id

        event_params2 = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.eventID2 = event_params2.event_id

        self.ob_config.link_selection_to_event(selection_id=self.selection_id, eventID=self.eventID2)
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=False)

    def test_001_in_ti_tool_suspend_the_linked_selection_in_application_verify_the_selection_is_suspended_in_live(self):
        """
        DESCRIPTION: - In TI tool suspend the linked selection
        DESCRIPTION: - In application verify the selection is suspended in live
        EXPECTED: Suspended selection in Specials carousel is suspended in live
        """
        self.navigate_to_edp(event_id=self.eventID2, sport_name='horse-racing')
        for self.__class__.outcome in self.site.racing_event_details.tab_content.specials_carousel.items_as_ordered_dict.values():
            self.assertTrue(self.outcome, msg=f'Can not find any race card')
            self.assertFalse(self.outcome.bet_button.is_enabled(expected_result=False, timeout=40), msg='Bet button is enabled')

    def test_002_in_ti_tool_enable_the_linked_selection_in_application_verify_the_selection_is_enabled_in_live(self):
        """
        DESCRIPTION: - In TI tool enable the linked selection
        DESCRIPTION: - In application verify the selection is enabled in live
        EXPECTED: Unsuspended selection in Specials carousel is enabled in live
        """
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=True)
        self.assertTrue(self.outcome.bet_button.is_enabled(timeout=40), msg='Bet button is not enabled')

    def test_003_in_ti_tool_suspend_the_market_of_the_linked_selections_in_application_verify_the_selections_are_suspended_in_live(self):
        """
        DESCRIPTION: - In TI tool suspend the market of the linked selections
        DESCRIPTION: - In application verify the selections are suspended in live
        EXPECTED: Selections from the market are suspended in live in Special carousel
        """
        self.ob_config.change_market_state(event_id=self.eventID2, market_id=self.marketID, displayed=True, active=False)
        self.assertFalse(self.outcome.bet_button.is_enabled(expected_result=False, timeout=40), msg='Bet button is enabled')

    def test_004_in_ti_tool_enable_the_market_of_the_linked_selections_in_application_verify_the_selections_are_enabled_in_live(self):
        """
        DESCRIPTION: - In TI tool enable the market of the linked selections
        DESCRIPTION: - In application verify the selections are enabled in live
        EXPECTED: Selections from the market are enabled in live in Special carousel
        """
        self.ob_config.change_market_state(event_id=self.eventID2, market_id=self.marketID, displayed=True, active=True)
        self.assertTrue(self.outcome.bet_button.is_enabled(timeout=40), msg='Bet button is not enabled')

    def test_005_in_ti_tool_suspend_the_event_of_the_linked_selections_in_application_verify_the_selections_are_suspended_in_live(self):
        """
        DESCRIPTION: - In TI tool suspend the event of the linked selections
        DESCRIPTION: - In application verify the selections are suspended in live
        EXPECTED: Selections from different markets from the suspended event are suspended in live in Special carousel
        """
        self.ob_config.change_event_state(event_id=self.eventID1, displayed=True, active=False)
        self.assertFalse(self.outcome.bet_button.is_enabled(expected_result=False, timeout=40), msg='Bet button is enabled')

    def test_006_in_ti_tool_enable_the_event_of_the_linked_selections_in_application_verify_the_selection_are_enabled_in_live(self):
        """
        DESCRIPTION: - In TI tool enable the event of the linked selections
        DESCRIPTION: - In application verify the selection are enabled in live
        EXPECTED: Selections from different markets from the enabled event are enabled in live in Special carousel
        """
        self.ob_config.change_event_state(event_id=self.eventID1, displayed=True, active=True)
        self.assertTrue(self.outcome.bet_button.is_enabled(timeout=40), msg='Bet button is not enabled')
