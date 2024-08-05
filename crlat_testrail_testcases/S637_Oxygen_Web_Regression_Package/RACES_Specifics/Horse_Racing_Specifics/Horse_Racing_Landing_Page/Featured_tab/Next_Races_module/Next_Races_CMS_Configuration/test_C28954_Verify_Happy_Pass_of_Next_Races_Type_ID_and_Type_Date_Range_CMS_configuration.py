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
class Test_C28954_Verify_Happy_Pass_of_Next_Races_Type_ID_and_Type_Date_Range_CMS_configuration(Common):
    """
    TR_ID: C28954
    NAME: Verify Happy Pass of Next Races Type ID and Type Date Range CMS configuration
    DESCRIPTION: This test case verifies Happy Pass Next Races CMS configuration via Type ID and Type Date Range
    DESCRIPTION: Story Tickets:
    DESCRIPTION: **BMA-6572 **CMS: Next Races Config Group
    DESCRIPTION: BMA-10828 All devices - Next 4 Races
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/structure
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: 1. In order to get a list of **Next Races** events and check **typeId**
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

    def test_003_type_in_search_field_nextraces(self):
        """
        DESCRIPTION: Type in search field 'NEXTRACES'
        EXPECTED: NEXTRACES section is shown
        """
        pass

    def test_004_in_type_id_field_enter_valid_race_id_and_set_correct_type_date_range___press_submit(self):
        """
        DESCRIPTION: In '**Type ID**' field enter valid <Race> id and set correct '**Type Date Range**' -> Press 'Submit'
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
        EXPECTED: *   <Racе> landing page is opened
        EXPECTED: *   'Next Races' module is displayed
        """
        pass

    def test_007_verify_next_races(self):
        """
        DESCRIPTION: Verify 'Next Races'
        EXPECTED: Events are present in 'Next Races' which:
        EXPECTED: *   have appropriate id (set in CMS)
        EXPECTED: *   date correspond to Type Date Ranges (set in CMS)
        EXPECTED: *   Other inputted filters are taken into consideration (**Number of Selection**, **Number of Events**, **Show prices only**)
        EXPECTED: *    Filters according typeflagcode (**Is In UK**, **Is Irish**, **Is International**) are **NOT **taken into consideration
        """
        pass

    def test_008_go_to_cms___in_type_id_field_enter_valid_multiplerace_ids_by_comma_eg_19871586_and_set_correct_type_date_range___press_submit(self):
        """
        DESCRIPTION: Go to CMS -> In '**Type ID**' field enter valid Multiple <Race> ids by comma (e.g. 1987,1586)  and set correct '**Type Date Range**' -> Press 'Submit'
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_009_repeat_steps_5_6(self):
        """
        DESCRIPTION: Repeat steps #5-6
        EXPECTED: 
        """
        pass

    def test_010_verify_next_races_events(self):
        """
        DESCRIPTION: Verify 'Next Races' events
        EXPECTED: Events are present in 'Next Races' which:
        EXPECTED: *   have appropriate ids (set in CMS)
        EXPECTED: *   date correspond to Type Date Ranges (set in CMS)
        EXPECTED: *   Other inputted filters are taken into consideration (**Number of Selection**, **Number of Events**, **Show prices only**)
        EXPECTED: *    Filters according typeflagcode (**Is In UK**, **Is Irish**, **Is International**) are **NOT **taken into consideration
        """
        pass
