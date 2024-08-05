import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.homepage_featured
@vtest
class Test_C29417_Verify_More_Link(BaseRacing):
    """
    TR_ID: C29417
    NAME: Verify 'More' Link.
    DESCRIPTION: This test case is for checking of 'View Full Race Card' link ('More' for Mobile)
    DESCRIPTION: **Jira tickets:** BMA-6571 CMS: Featured Tab Module - Horse Racing
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) Make sure events are available within module created by <Race> type ID for current day
    PRECONDITIONS: 3) In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE**: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        """
        self.site.wait_content_state("Homepage")

    def test_002_for_mobiletabletgo_to_module_selector_ribbon___module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Go to Module Selector Ribbon -> Module created by <Race> type ID
        EXPECTED: *   'Feature' tab is selected by default
        EXPECTED: *   Module created by <Race> type ID is shown
        """
        if self.device_type == 'mobile':
            self.site.home.tabs_menu.click_button(button_name=vec.sb.TABS_NAME_NEXT.upper())
            # used sleep because Next race tab is taking time to reflect, other synchronization method is not working
            sleep(2)
            next_races_tab = self.site.home.tabs_menu.current
            self.assertTrue(next_races_tab, msg=f'"{vec.sb.TABS_NAME_NEXT.upper()}" tab is not selected after click')
            self.meetings = self.site.home.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(self.meetings, msg='No race sections are found in next races')
            event = list(self.meetings.values())[0]
            event.full_race_card.click()
            self.site.wait_content_state(state_name='RacingEventDetails')

    def test_003_for_desktopscroll_the_page_down_to_featured_section____module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Scroll the page down to 'Featured' section ->-> Module created by <Race> type ID
        EXPECTED: * 'Featured' section is displayed below the following sections: Enhanced/ Sports offer carousel, In-Play & Live Stream, Next Races Carousel (if applicable)
        EXPECTED: * Module created by <Race> type ID is shown
        """
        if self.device_type == 'desktop':
            featured_module = self.site.home.desktop_modules.featured_module
            self.assertTrue(featured_module, msg='"Featured" module is not displayed')
            featured_content = featured_module.tab_content
            self.assertTrue(featured_content.accordions_list, msg='"Featured" module does not contain any accordions')
            self.module_name = 'NEXT RACES: UK & IRELAND' if self.brand == 'bma' else 'HORSE RACING - UK & IRELAND'
            module1 = featured_content.accordions_list.items_as_ordered_dict
            list(module1.get(self.module_name).items_as_ordered_dict.values())[0].full_race_card.click()
            self.site.wait_content_state("HorseRacing")

    def test_004_on_race_events_carousel_find_view_full_race_card_link(self):
        """
        DESCRIPTION: On <Race> events carousel find 'View Full Race Card' link
        EXPECTED: 1.  'View Full Race Card' ('More' for Mobile)
        EXPECTED: is displayed for each event in <Race> events carousel
        EXPECTED: 2.  Link is displayed at the bottom of section
        EXPECTED: 3.  Both text and icon are hyperlinked
        EXPECTED: 4.  Link is internationalised
        """
        # Covered in step 2

    def test_005_tap_more_link_more_also_mobile(self):
        """
        DESCRIPTION: Tap 'More' link ('More' also Mobile)
        EXPECTED: User is redirected to event details page
        """
        # Covered step 3

    def test_006_tap_back_button(self):
        """
        DESCRIPTION: Tap back button
        EXPECTED: User is redirected to the page he navigated from
        """
        self.device.go_back()
        self.site.wait_content_state("Homepage")
