import pytest

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


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
@pytest.mark.races
@pytest.mark.mobile_only
@pytest.mark.safari
@vtest
class Test_C2592684_Specials_carousel_displaying_depending_on_min_number_of_linked_selections(BaseRacing):
    """
    TR_ID: C2592684
    VOL_ID: C9690172
    NAME: Specials carousel displaying depending on min number of linked selections
    DESCRIPTION: This test case verifies that specials carousel appears only when there is a at least 1 linked selection
    PRECONDITIONS: To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: How to link selections to event: https://confluence.egalacoral.com/display/SPI/How+to+link+selections+to+event
    PRECONDITIONS: You should have a <Race> event WITHOUT linked selections
    PRECONDITIONS: "Racing Specials Carousel" should be enabled in CMS > System Configuration > Structure
    PRECONDITIONS: You should be on a <Race> EDP that selections will be linked to
    """
    keep_browser_open = True

    def verify_specials_carousel(self, is_displayed: bool = True):
        """
        This method verify displayed in Racing Specials Carousel
        :param is_displayed: Expected displaying state
        """
        for b in range(0, 2):
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            result = wait_for_result(lambda: bool(self.site.racing_event_details.tab_content.has_specials_carousel()) == is_displayed,
                                     name='Accordion special carousel',
                                     timeout=0)
            if result:
                break

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
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.eventID = event_params.event_id

        event_params2 = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.selection_name, self.__class__.selection_id = list(event_params2.selection_ids.items())[0]

    def test_001_navigate_to_racing_event_details_page(self):
        """
        DESCRIPTION: Open racing event
        EXPECTED: Racing event details page is loaded
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

    def test_002_verify_specials_carousel_displaying(self):
        """
        DESCRIPTION: Verify Specials carousel displaying
        EXPECTED: Specials carousel is not displayed
        """
        self.assertFalse(self.site.racing_event_details.tab_content.has_specials_carousel(expected_result=False),
                         msg=f'Specials carousel is displayed on EDP for event with id: {self.eventID}')

    def test_003_link_selection_from_horse_race_specials_to_the_horse_race_event(self):
        """
        DESCRIPTION: In TI tool link selection from horse race specials to the horse race event from preconditions
        DESCRIPTION: Refresh the page in application and verify Specials carousel displaying
        EXPECTED: Specials carousel is displayed with the linked selection
        """
        self.ob_config.link_selection_to_event(selection_id=self.selection_id, eventID=self.eventID)
        self.verify_specials_carousel(is_displayed=True)

    def test_004_unlink_the_selection_from_the_event(self):
        """
        DESCRIPTION: In TI tool unlink the selection from the event
        DESCRIPTION: Refresh the page in application and verify Specials carousel displaying
        EXPECTED: Specials carousel is not displayed anymore
        """
        self.ob_config.link_selection_to_event(selection_id=self.selection_id, eventID=self.eventID, linked=False)
        self.verify_specials_carousel(is_displayed=False)
