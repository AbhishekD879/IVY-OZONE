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
@pytest.mark.racing
@pytest.mark.greyhounds
@pytest.mark.horseracing
@pytest.mark.specials_carousel
@pytest.mark.event_details
@pytest.mark.cms
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.mobile_only
@pytest.mark.safari
@vtest
class Test_C2592683_Adding_and_removing_selections_from_Specials_carousel(BaseRacing):
    """
    TR_ID: C2592683
    VOL_ID: C9690171
    NAME: Adding and removing selections from Specials carousel
    DESCRIPTION: This test case verifies adding and removing selections from Specials carousel
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - How to link selections to event: https://confluence.egalacoral.com/display/SPI/How+to+link+selections+to+event
    PRECONDITIONS: - You should have a linked selection to <Race> event
    PRECONDITIONS: - "Racing Specials Carousel" should be enabled in CMS > System Configuration > Structure
    PRECONDITIONS: - You should be on a <Race> EDP that has linked selections
    """
    keep_browser_open = True
    price = '1/2'

    def verify_selection_in_specials_carousel(self, selection_name: str, is_displayed: bool = True):
        """
        This method verify if specific selection displayed in Racing Specials Carousel
        :param selection_name: Expected selection name
        :param is_displayed: Expected displaying state
        """
        for b in range(0, 2):
            racing_specials = self.site.greyhound_event_details.tab_content.specials_carousel.items_as_ordered_dict
            self.assertTrue(racing_specials, msg='No one selection found in Specials carousel')
            result = wait_for_result(lambda: bool(racing_specials.get(selection_name)) == is_displayed,
                                     name='Accordion special name "%s: ' % selection_name,
                                     timeout=0)
            if result:
                break
            self.device.refresh_page()
            self.site.wait_splash_to_hide()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create racing specials events
        EXPECTED: Events are created in OB
        """
        racing_special_carousel_conf = self.get_initial_data_system_configuration().get('RacingSpecialsCarousel', {})
        if not racing_special_carousel_conf:
            racing_special_carousel_conf = self.cms_config.get_system_configuration_item('RacingSpecialsCarousel')
        if not racing_special_carousel_conf.get('enable'):
            raise CmsClientException('Racing specials carousel is not enabled in CMS')
        if racing_special_carousel_conf.get('label') == '':
            self.__class__.cms_racing_specials_label = vec.racing.RACING_SPECIALS_CAROUSEL_LABEL
        else:
            self.__class__.cms_racing_specials_label = racing_special_carousel_conf.get('label', None)

        event_params = self.ob_config.add_UK_racing_event(number_of_runners=2)
        self.__class__.selection_name, self.__class__.selection_id = list(event_params.selection_ids.items())[0]
        self.__class__.selection_name2, self.__class__.selection_id2 = list(event_params.selection_ids.items())[1]

        event_params2 = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1, lp_prices={0: self.price})
        self.__class__.eventID = event_params2.event_id

        self.ob_config.link_selection_to_event(selection_id=self.selection_id, eventID=self.eventID)

    def test_001_navigate_to_racing_event_details_page(self):
        """
        DESCRIPTION: Open racing event
        EXPECTED: Racing event details page is loaded
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='greyhound-racing')

    def test_002_verify_that_specials_carousel_contains_all_linked_selections(self):
        """
        DESCRIPTION: Verify that Specials carousel contains all linked selections
        EXPECTED: Specials carousel is displayed with all linked selection
        """
        sections = self.site.greyhound_event_details.tab_content.specials_carousel.items_as_ordered_dict
        self.assertTrue(sections, msg=f'Can not find any race card')
        expected_specials_racecard = [f'{self.cms_racing_specials_label.upper()} - {self.selection_name}']
        self.assertEqual(list(sections.keys()), expected_specials_racecard, msg=f'Actual section name "{list(sections.keys())}" '
                                                                                f'is not equal to expected "{expected_specials_racecard}"')

    def test_003_in_ti_tool_link_one_more_selection_to_the_event_refresh_the_page_in_application_and_verify_that_new_selection_appears(self):
        """
        DESCRIPTION: - In TI tool link one more selection to the event
        DESCRIPTION: - Refresh the page in application and verify that new selection appears
        EXPECTED: New selection is present in Specials carousel
        """
        self.ob_config.link_selection_to_event(selection_id=self.selection_id2, eventID=self.eventID)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.__class__.expected_specials_racecard2 = f'{self.cms_racing_specials_label.upper()} - {self.selection_name2}'
        self.verify_selection_in_specials_carousel(selection_name=self.expected_specials_racecard2)

    def test_004_in_ti_tool_unlink_one_of_the_linked_selections__refresh_the_page_in_application_and_verify_that_unlinked_selection_is_no_more_displayed(self):
        """
        DESCRIPTION: - In TI tool unlink one of the linked selections
        DESCRIPTION: - Refresh the page in application and verify that unlinked selection is no more displayed
        EXPECTED: Removed selection is not displayed in Specials carousel anymore
        """
        self.ob_config.link_selection_to_event(selection_id=self.selection_id2, eventID=self.eventID, linked=False)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.verify_selection_in_specials_carousel(selection_name=self.expected_specials_racecard2, is_displayed=False)
