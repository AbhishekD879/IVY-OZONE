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
@pytest.mark.horseracing
@pytest.mark.specials_carousel
@pytest.mark.event_details
@pytest.mark.cms
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C2592691_Displaying_of_selection_in_Specials_carousel_based_on_Display_option(BaseRacing):
    """
    TR_ID: C2592691
    VOL_ID: C9690175
    NAME: Displaying of selection in Specials carousel based on "Display" option
    DESCRIPTION: This test case verifies displaying of the selection in Specials carousel on the "Display" option on event/market/selection levels
    PRECONDITIONS: To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: How to link selections to event: https://confluence.egalacoral.com/display/SPI/How+to+link+selections+to+event
    PRECONDITIONS: You should have a <Race> event WITHOUT linked selections
    PRECONDITIONS: "Racing Specials Carousel" should be enabled in CMS > System Configuration > Structure
    PRECONDITIONS: You should be on a <Race> EDP that selections will be linked to
    """
    keep_browser_open = True

    def verify_selection_in_specials_carousel(self, selection_name: str, is_displayed: bool = True):
        """
        This method verify if specific selection displayed in Racing Specials Carousel
        :param selection_name: Expected selection name
        :param is_displayed: Expected displaying state
        """
        for b in range(0, 2):
            racing_specials = self.site.racing_event_details.tab_content.specials_carousel.items_as_ordered_dict
            self.assertTrue(racing_specials, msg='No one selection found in Specials carousel')
            racing_special_name = f'{self.racing_specials_label} - {selection_name}'
            result = wait_for_result(lambda: bool(racing_specials.get(racing_special_name)) == is_displayed,
                                     name='Accordion special name "%s: ' % racing_special_name,
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
        cms_config = self.get_initial_data_system_configuration().get('RacingSpecialsCarousel', {})
        if not cms_config:
            cms_config = self.cms_config.get_system_configuration_item('RacingSpecialsCarousel')
        is_racing_specials_carousel_enabled = cms_config.get('enable')
        if not is_racing_specials_carousel_enabled:
            raise CmsClientException('Racing specials carousel is not enabled in CMS')
        self.__class__.racing_specials_label = cms_config.get('label', None)
        if self.racing_specials_label == '':
            self.__class__.racing_specials_label = vec.racing.RACING_SPECIALS_CAROUSEL_LABEL
        else:
            self.__class__.racing_specials_label = self.racing_specials_label.upper()
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.eventID = event_params.event_id

        event_params2 = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.first_event_id = event_params2.event_id
        self.__class__.first_market_id = self.ob_config.market_ids.get(self.first_event_id)
        self.__class__.first_selection_name, self.__class__.first_selection_id = \
            list(event_params2.selection_ids.items())[0]

        event_params3 = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.second_selection_name, self.__class__.second_selection_id = \
            list(event_params3.selection_ids.items())[0]
        self.ob_config.link_selection_to_event(selection_id=self.first_selection_id, eventID=self.eventID)
        self.ob_config.link_selection_to_event(selection_id=self.second_selection_id, eventID=self.eventID)

    def test_001_navigate_to_racing_event_details_page(self):
        """
        DESCRIPTION: Open racing event
        EXPECTED: Racing event details page is loaded
        EXPECTED: Specials carousel is displayed with the linked selection
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.assertTrue(self.site.racing_event_details.tab_content.has_specials_carousel(),
                        msg=f'Specials carousel not displayed on EDP for event with id: {self.eventID}')
        racing_specials = self.site.racing_event_details.tab_content.specials_carousel.items_as_ordered_dict
        self.assertTrue(racing_specials, msg='No one selection found in Specials carousel')
        self.verify_selection_in_specials_carousel(selection_name=self.first_selection_name)
        self.verify_selection_in_specials_carousel(selection_name=self.second_selection_name)

    def test_002_undisplay_the_selection_from_preconditions(self):
        """
        DESCRIPTION: In TI tool undisplay the selection from preconditions
        DESCRIPTION: In application refresh the page and verify the selection is no more displayed
        EXPECTED: Corresponding selection in Specials carousel is no more displayed
        """
        self.ob_config.change_selection_state(selection_id=self.first_selection_id, displayed=False, active=True)
        self.verify_selection_in_specials_carousel(selection_name=self.first_selection_name, is_displayed=False)

    def test_003_display_the_selection_from_preconditions(self):
        """
        DESCRIPTION: In TI tool display the selection from preconditions
        DESCRIPTION: In application refresh the page and verify the selection is displayed
        EXPECTED: Corresponding selection in Specials carousel is displayed
        """
        self.ob_config.change_selection_state(selection_id=self.first_selection_id, displayed=True, active=True)
        self.verify_selection_in_specials_carousel(selection_name=self.first_selection_name, is_displayed=True)

    def test_004_undisplay_the_market_of_the_selection_from_preconditions(self):
        """
        DESCRIPTION: In TI tool undisplay the market of the selection from preconditions
        DESCRIPTION: In application refresh the page and verify the selection is no more displayed
        EXPECTED: Corresponding selection in Specials carousel is no more displayed
        """
        self.ob_config.change_market_state(event_id=self.first_event_id,
                                           market_id=self.first_market_id, displayed=False, active=True)
        self.verify_selection_in_specials_carousel(selection_name=self.first_selection_name, is_displayed=False)

    def test_005_display_the_market_of_the_selection_from_preconditions(self):
        """
        DESCRIPTION: In TI tool display the market of the selection from preconditions
        DESCRIPTION: In application refresh the page and verify the selection is no more displayed
        EXPECTED: Corresponding selection in Specials carousel is displayed
        """
        self.ob_config.change_market_state(event_id=self.first_event_id,
                                           market_id=self.first_market_id, displayed=True, active=True)
        self.verify_selection_in_specials_carousel(selection_name=self.first_selection_name, is_displayed=True)

    def test_006_undisplay_the_event_of_the_selection_from_preconditions(self):
        """
        DESCRIPTION: In TI tool undisplay the event of the selection from preconditions
        DESCRIPTION: In application refresh the page and verify the selection is no more displayed
        EXPECTED: Corresponding selection in Specials carousel is no more displayed
        """
        self.ob_config.change_event_state(event_id=self.first_event_id, displayed=False, active=True)
        self.verify_selection_in_specials_carousel(selection_name=self.first_selection_name, is_displayed=False)

    def test_007_display_the_event_of_the_selection_from_preconditions(self):
        """
        DESCRIPTION: In TI tool display the event of the selection from preconditions
        DESCRIPTION: In application refresh the page and verify the selection is no more displayed
        EXPECTED: Corresponding selection in Specials carousel is displayed
        """
        self.ob_config.change_event_state(event_id=self.first_event_id, displayed=True, active=True)
        self.verify_selection_in_specials_carousel(selection_name=self.first_selection_name, is_displayed=True)
