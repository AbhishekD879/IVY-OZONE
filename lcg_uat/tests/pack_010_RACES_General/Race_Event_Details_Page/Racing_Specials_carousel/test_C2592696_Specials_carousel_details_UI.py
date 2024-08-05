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
@pytest.mark.specials_carousel
@pytest.mark.cms
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C2592696_Specials_carousel_details_UI(BaseRacing):
    """
    TR_ID: C2592696
    VOL_ID: C9690177
    NAME: Specials carousel details UI
    DESCRIPTION: This test case verifies the selection displaying in Specials carousel
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - How to link selections to event: https://confluence.egalacoral.com/display/SPI/How+to+link+selections+to+event
    PRECONDITIONS: - You should have a linked selection to <Race> event
    PRECONDITIONS: - "Racing Specials Carousel" should be enabled in CMS > System Configuration > Structure
    PRECONDITIONS: - You should be on a <Race> EDP that has linked selections
    """
    keep_browser_open = True
    price = '1/2'

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
            self.__class__.cms_racing_specials_label = cms_config.get('label')

        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices={0: self.price})
        self.__class__.selection_name, self.__class__.selection_id = list(event_params.selection_ids.items())[0]

        event_params2 = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices={0: self.price})
        self.__class__.eventID = event_params2.event_id

        self.ob_config.link_selection_to_event(selection_id=self.selection_id, eventID=self.eventID)

    def test_001_verify_that_ui_elements_are_present(self):
        """
        DESCRIPTION: Verify that UI elements are present:
        EXPECTED: - Specials carousel is placed below the video streaming buttons and above Markets tab
        EXPECTED: - Cards label name in Specials carousel is the same as in CMS > System Configuration > Structure > Racing Specials carousel section > label field
        EXPECTED: - The selection's name is the same as selection's name in TI tool
        EXPECTED: - The price of the selection button is the same as in TI tool
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        for outcome_name, self.__class__.outcome in self.site.racing_event_details.tab_content.specials_carousel.items_as_ordered_dict.items():
            self.assertTrue(self.outcome, msg=f'Can not find any race card')
            expected_specials_racecard = f'{self.cms_racing_specials_label.upper()} - {self.selection_name}'
            self.assertEqual(outcome_name, expected_specials_racecard,
                             msg=f'Actual section name "{outcome_name}" '
                             f'is not equal to expected "{expected_specials_racecard}"')

            self.assertEqual(self.outcome.bet_button.outcome_price_text, self.price,
                             msg=f'Outcome price text "{self.outcome.bet_button.outcome_price_text}" is not equal to'
                                 f'expected "{self.price}"')
