import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@vtest
class Test_C10786276_Verify_displaying_of_events_in_In_Play_module_on_Featured_tab_based_on_CMS_configs(Common):
    """
    TR_ID: C10786276
    NAME: Verify displaying of events in 'In-Play' module on 'Featured' tab based on CMS configs
    DESCRIPTION: This test case verifies events displaying in 'In-Play' module on 'Featured' tab based on CMS configs
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. The homepage is opened and 'Featured' tab is selected
    PRECONDITIONS: 3. 'In-Play' module with live events is displayed in 'Featured' tab
    PRECONDITIONS: **Notes:**
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - 'In-Play' module should be enabled in CMS > Sports Configs > Structure > In-Play module
    PRECONDITIONS: - 'In-Play' module should be 'Active' in CMS > Sports Pages > Homepage > In-Play module
    PRECONDITIONS: - To verify data for created 'In-Play' module use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket (featured-sports...) -> response with type: "FEATURED_STRUCTURE_CHANGED" -> modules -> @type: "InplayModule" and choose the appropriate module.
    PRECONDITIONS: ![](index.php?/attachments/get/37874755)
    PRECONDITIONS: **- Next configurations are set up in CMS > Sports Pages > Homepage > In Play module > Add Sport > Set number of events for Sport:**
    PRECONDITIONS: * Several Sports are added (Sport1, Sport2, Sport3, etc.)
    PRECONDITIONS: * 'In Play Event Count' is set to e.g. 10
    PRECONDITIONS: * Several Sports with more than 10 live events available in OB (e.g. Football, Tennis, Horse Racing, Greyhounds etc)
    """
    keep_browser_open = True

    def test_001_in_cms__sports_pages__homepage__in_play_moduleset_sport_1__eg_10_same_value_as_in_in_play_event_count_and_save_changesverify_events_displaying_in_in_play_module(self):
        """
        DESCRIPTION: In CMS > Sports Pages > Homepage > 'In-Play' module:
        DESCRIPTION: Set Sport 1 = e.g. 10 (same value as in 'In-Play Event Count') and save changes
        DESCRIPTION: Verify events displaying in 'In-Play' module
        EXPECTED: * Changes for In-Play module are saved
        EXPECTED: * 10 events are displayed for Sport 1
        EXPECTED: * '10' value is taken from CMS (step 1 -> value set for Sport 1)
        """
        pass

    def test_002_in_cms__sports_pages__homepage__in_play_moduleset_sport_1__eg_15_higher_value_than_in_in_play_event_count_and_save_changesverify_events_displaying_in_in_play_module(self):
        """
        DESCRIPTION: In CMS > Sports Pages > Homepage > 'In-Play' module:
        DESCRIPTION: Set Sport 1 = e.g. 15 (higher value than in 'In-Play Event Count') and save changes
        DESCRIPTION: Verify events displaying in 'In-Play' module
        EXPECTED: * Changes for In-Play module are saved
        EXPECTED: * 10 events are displayed for Sport 1
        EXPECTED: * '10' value is taken from CMS (step 1 -> value set for 'In-Play Event Count' < Sport 1)
        """
        pass

    def test_003_in_cms__sports_pages__homepage__in_play_moduleset__sport_1__eg_6__sport_2__eg_2__sport_3__eg_2__sport_4__eg_2and_save_changesverify_events_displaying_in_in_play_module(self):
        """
        DESCRIPTION: In CMS > Sports Pages > Homepage > 'In-Play' module:
        DESCRIPTION: Set:
        DESCRIPTION: - Sport 1 = e.g. 6
        DESCRIPTION: - Sport 2 = e.g. 2
        DESCRIPTION: - Sport 3 = e.g. 2
        DESCRIPTION: - Sport 4 = e.g. 2
        DESCRIPTION: and save changes
        DESCRIPTION: Verify events displaying in 'In-Play' module
        EXPECTED: * Changes for In-Play module are saved
        EXPECTED: * General number of events that are displaying on 'In-Play' module is 10 according to the value taken in CMS (step 1 > value set for 'In-Play Event Count')
        EXPECTED: * 6 events are displayed for Sport 1
        EXPECTED: * 2 events are displayed for Sport 2
        EXPECTED: * 2 events are displayed for Sport 3
        EXPECTED: * 0 events are displayed for Sport 4 (because the Sum of values set fo Sport 1 + Sport 2 + Sport 3 = 'In-Play Event Count')
        """
        pass

    def test_004_in_cms__sports_pages__homepage__in_play_moduleset__sport_1__eg_2__sport_2__eg_2__sport_3__eg_2__sport_4__eg_8and_save_changesverify_events_displaying_in_in_play_module(self):
        """
        DESCRIPTION: In CMS > Sports Pages > Homepage > 'In-Play' module:
        DESCRIPTION: Set:
        DESCRIPTION: - Sport 1 = e.g. 2
        DESCRIPTION: - Sport 2 = e.g. 2
        DESCRIPTION: - Sport 3 = e.g. 2
        DESCRIPTION: - Sport 4 = e.g. 8
        DESCRIPTION: and save changes
        DESCRIPTION: Verify events displaying in 'In-Play' module
        EXPECTED: * Changes for In-Play module are saved
        EXPECTED: * General number of events that are displaying on 'In-Play' module is 10 according to the value taken in CMS (step 1 > value set for 'In-Play Event Count')
        EXPECTED: * 2 events are displayed for Sport 1
        EXPECTED: * 2 events are displayed for Sport 2
        EXPECTED: * 2 events are displayed for Sport 3
        EXPECTED: * 4 events are displayed for Sport 4 (because the Sum of values set fo Sport 1 + Sport 2 + Sport 3 + Sport 4 =  'In-Play Event Count')
        """
        pass

    def test_005_in_cms__sports_pages__homepage__in_play_moduleset__sport_1__eg_6__sport_2__eg_0__sport_3__eg_1__sport_4__eg_1and_save_changesverify_events_displaying_in_in_play_module(self):
        """
        DESCRIPTION: In CMS > Sports Pages > Homepage > 'In-Play' module:
        DESCRIPTION: Set:
        DESCRIPTION: - Sport 1 = e.g. 6
        DESCRIPTION: - Sport 2 = e.g. 0
        DESCRIPTION: - Sport 3 = e.g. 1
        DESCRIPTION: - Sport 4 = e.g. 1
        DESCRIPTION: and save changes
        DESCRIPTION: Verify events displaying in 'In-Play' module
        EXPECTED: * Changes for In-Play module are saved
        EXPECTED: * General number of events that are displaying on 'In-Play' module is 10 according to the value taken in CMS (step 1 > value set for 'In-Play Event Count')
        EXPECTED: * 6 events are displayed for Sport 1
        EXPECTED: * 0 events are displayed for Sport 2 but Sport 3 with 1 event is displayed instead as the next Sport by display order with available live events
        EXPECTED: * 1 event is displayed for Sport 4 that replaces Sport 3
        EXPECTED: * 1 event is displayed for Sport 5 that replaces Sport 4 (because the Sum of values set fo Sport 1 + Sport 3 + Sport 4 + Sport 5 = 'In-Play Event Count')
        """
        pass
