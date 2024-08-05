import pytest

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.tablet
@pytest.mark.racing
@pytest.mark.greyhounds
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.specials_carousel
@pytest.mark.cms
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C2592695_Undisplaying_of_the_selection_of_the_resulted_event_in_Specials_carousel(BaseRacing):
    """
    TR_ID: C2592695
    VOL_ID: C9690176
    NAME: Undisplaying of the selection of the resulted event in Specials carousel
    DESCRIPTION: This test case verifies reflection of the selection of the resulted event
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - How to link selections to event: https://confluence.egalacoral.com/display/SPI/How+to+link+selections+to+event
    PRECONDITIONS: - You should have a linked selection to <Race> event
    PRECONDITIONS: - "Racing Specials Carousel" should be enabled in CMS > System Configuration > Structure
    PRECONDITIONS: - You should be on a <Race> EDP that has linked selections
    """
    keep_browser_open = True

    def verify_selection_in_specials_carousel(self, selection_name: str, is_displayed: bool = True) -> None:
        """
        This method verify if specific selection displayed within Racing Specials Carousel
        :param selection_name: Expected selection name
        :param is_displayed: Expected displaying state
        """
        racing_specials_carousel = self.site.greyhound_event_details.tab_content.specials_carousel
        self.assertTrue(racing_specials_carousel, msg='Specials carousel is not shown')
        racing_special_name = f'{self.racing_specials_label} - {selection_name}'

        expected_state = '' if is_displayed else 'not'
        result = wait_for_result(
            lambda: bool(racing_specials_carousel.items_as_ordered_dict.get(racing_special_name, False)),
            expected_result=is_displayed,
            name=f'"{selection_name}" selection {expected_state} to be shown within carousel',
            timeout=15)
        self.assertEqual(result, is_displayed, msg=f'Actual selection: "{selection_name}" displaying state: '
                                                   f'{result}, expected: {is_displayed}')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create racing events, link selection to the <Race> event
        """
        cms_config = self.get_initial_data_system_configuration().get('RacingSpecialsCarousel', {})
        if not cms_config:
            cms_config = self.cms_config.get_system_configuration_item('RacingSpecialsCarousel')
        is_racing_specials_carousel_enabled = cms_config.get('enable')
        if not is_racing_specials_carousel_enabled:
            raise CmsClientException('Racing specials carousel is not enabled in CMS')
        if cms_config.get('label') == '':
            self.__class__.racing_specials_label = vec.racing.RACING_SPECIALS_CAROUSEL_LABEL
        else:
            racing_specials = cms_config.get('label', None)
            self.__class__.racing_specials_label = racing_specials.upper()
        first_race_event = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1)
        first_event_id = first_race_event.event_id

        second_race_event = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.second_event_id = second_race_event.event_id
        self.__class__.second_market_id = second_race_event.market_id
        self.__class__.second_selection_name, self.__class__.second_selection_id = \
            list(second_race_event.selection_ids.items())[0]

        third_race_event = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.third_selection_name, self.__class__.third_selection_id = \
            list(third_race_event.selection_ids.items())[0]

        self.ob_config.link_selection_to_event(selection_id=self.second_selection_id, eventID=first_event_id)
        self.ob_config.link_selection_to_event(selection_id=self.third_selection_id, eventID=first_event_id)
        self.navigate_to_edp(event_id=first_event_id, sport_name='greyhound-racing')

    def test_001_in_ti_tool_result_the_event_of_the_linked_selection_in_application_verify_the_selection_is_undisplayed_in_live(self):
        """
        DESCRIPTION: - In TI tool result the event of the linked selection
        DESCRIPTION: - In application verify the selection is undisplayed in live
        EXPECTED: The selection of the resulted event is undisplayed in live
        """
        self.assertTrue(self.site.greyhound_event_details.tab_content.has_specials_carousel(),
                        msg=f'Specials carousel is not shown')
        racing_specials = self.site.greyhound_event_details.tab_content.specials_carousel.items_as_ordered_dict
        self.assertTrue(all(racing_specials), msg='No one selection found in Specials carousel')

        self.verify_selection_in_specials_carousel(selection_name=self.second_selection_name)
        self.verify_selection_in_specials_carousel(selection_name=self.third_selection_name)

        self.ob_config.result_selection(selection_id=self.second_selection_id, market_id=self.second_market_id,
                                        event_id=self.second_event_id)
        self.ob_config.confirm_result(selection_id=self.second_selection_id, market_id=self.second_market_id,
                                      event_id=self.second_event_id)

        self.verify_selection_in_specials_carousel(selection_name=self.second_selection_name, is_displayed=False)
        self.verify_selection_in_specials_carousel(selection_name=self.third_selection_name)
