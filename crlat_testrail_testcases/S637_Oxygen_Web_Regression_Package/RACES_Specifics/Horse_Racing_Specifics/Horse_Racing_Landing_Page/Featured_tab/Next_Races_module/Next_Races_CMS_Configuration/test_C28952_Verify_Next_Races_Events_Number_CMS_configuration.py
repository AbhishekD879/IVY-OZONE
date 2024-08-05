import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28952_Verify_Next_Races_Events_Number_CMS_configuration(Common):
    """
    TR_ID: C28952
    NAME: Verify 'Next Races' Events Number CMS configuration
    DESCRIPTION: This test case verifies Events number configuration in CMS within Next Races
    DESCRIPTION: Story Tickets:
    DESCRIPTION: **BMA-6572 **CMS: Next Races Config Group
    DESCRIPTION: BMA-10828 All devices - Next 4 Races
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/structure
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: 1. In order to get a list of **Next Races**e vents:
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_tap_system_configuration_section(self):
        """
        DESCRIPTION: Tap 'System-configuration' section
        EXPECTED: 'System-configuration' section is opened
        """
        pass

    def test_003_type_in_serach_field_nextraces(self):
        """
        DESCRIPTION: Type in serach field 'NEXTRACES'
        EXPECTED: NEXTRACES section is shown
        """
        pass

    def test_004_in_number_of_events_drop_down_choose_some_number_from_1_12___press_submit5_option_should_be_set_by_default(self):
        """
        DESCRIPTION: In '**Number of Events**' drop-down choose some number from 1-12 -> Press 'Submit'
        DESCRIPTION: ('5' option should be set by default)
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_005_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_006_tap_horse_racing_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Horse Racing> icon from the Sports Menu Ribbon
        EXPECTED: *   <Horse Racing> landing page is opened
        EXPECTED: *   'Next Races' module is displayed
        """
        pass

    def test_007_verify_next_races_events_number(self):
        """
        DESCRIPTION: Verify 'Next Races' Events number
        EXPECTED: Number of events could differs from number which was set in CMS
        EXPECTED: This happens because some events may be empty
        EXPECTED: To check number of events check Networks -> **NextNEventToOutcomeForClass** response
        """
        pass

    def test_008_go_to_cms___in_number_of_events_drop_down_choose_some_other_number_from_1_12___press_submit5_option_should_be_set_by_default(self):
        """
        DESCRIPTION: Go to CMS -> In '**Number of Events**' drop-down choose some other number from 1-12 -> Press 'Submit'
        DESCRIPTION: ('5' option should be set by default)
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_009_repeat_steps_5_7(self):
        """
        DESCRIPTION: Repeat steps #5-7
        EXPECTED: 
        """
        pass
