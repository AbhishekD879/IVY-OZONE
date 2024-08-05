import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.exceptions.precondition_not_met_exception import PreconditionNotMetException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C24623576_Verify_data_filtering_on_In_Play_and_Live_Stream_section_on_Desktop(Common):
    """
    TR_ID: C24623576
    NAME: Verify data filtering on 'In-Play and Live Stream' section on Desktop
    DESCRIPTION: This test case verifies in-play and live streaming events filtering on 'In-Play and Live Stream' section on Desktop
    PRECONDITIONS: 1. Load Oxygen app on Desktop
    PRECONDITIONS: 2. On Homepage scroll down to 'In-Play and Live Stream' section
    PRECONDITIONS: 3. Make sure that in-play and live streaming events are configured
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: * To verify received data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX" for 'In-play' switcher and "IN_PLAY_SPORT_TYPE::XX::STREAM_EVENT::XXX" for 'Live stream' switcher
    PRECONDITIONS: where:
    PRECONDITIONS: XX - Sport/Category Id
    PRECONDITIONS: XXX - Type Id
    PRECONDITIONS: ![](index.php?/attachments/get/40725)      ![](index.php?/attachments/get/40724)
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/Get live events
        """
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_autotest_premier_league_football_event(is_live=True, img_stream=True)
        self.__class__.leagues = self.site.home.desktop_modules.inplay_live_stream_module.tab_content.accordions_list.items_as_ordered_dict

    def test_001_verify_events_when_in_play_switcher_is_selected(self, drilldowntagnames=['EVFLAG_BL'], livestream=False):
        """
        DESCRIPTION: Verify events when 'In-play' switcher is selected
        EXPECTED: Events with the following attributes are present:
        EXPECTED: * Event's/market's/outcome's attribute 'siteChannels' contains 'M'
        EXPECTED: * Attribute 'isStarted="true"' is present
        EXPECTED: * Event's attribute 'drilldownTagNames' contains
        EXPECTED: "EVFLAG_BL"
        EXPECTED: * Attribute 'isLiveNowEvent="true"' is present
        EXPECTED: * Time in 'suspendAtTime' attribute of the event is NOT in the past or it is not present
        EXPECTED: * At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: * At least one market is not resulted (there is no attribute 'isResulted="true")
        EXPECTED: * At least one market is displayed (available in the response)
        """
        if self.leagues:
            for league in self.leagues.values():
                events = league.items_as_ordered_dict
                for event in events.values():
                    event_id = event.template.event_id
                    event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)[0]['event']
                    self.assertIn('M', event_details['siteChannels'], msg='Event attribute siteChannels does not contain "M".')
                    self.assertEqual(event_details['isStarted'], 'true', msg='Event attribute isStarted does not contain "true".')
                    self.assertEqual(event_details['isLiveNowEvent'], 'true', msg='Event attribute isLiveNowEvent does not contain "true".')
                    if livestream:
                        self.assertTrue(drilldowntagnames[0] or drilldowntagnames[1] or drilldowntagnames[2] in event_details['drilldownTagNames'], msg=f'Event attribute drilldownTagNames does not contain "{drilldowntagnames}"')
                        self.assertTrue('IVA,' or 'PVA,' or 'GVA,' in event_details['typeFlagCodes'], msg='"IVA" or "PVA" or "GVA" not present in "typeFlagCodes" attribute')
                    else:
                        self.assertIn(drilldowntagnames[0], event_details['drilldownTagNames'], msg=f'Event attribute drilldownTagNames does not contain "{drilldowntagnames}"')
                    for market in event_details['children']:
                        market_details = market['market']
                        if market_details['isMarketBetInRun'] == 'true' and 'isResulted' not in event_details:
                            break
                    else:
                        raise VoltronException('Not even one market contains attribute "isMarketBetInRun=true" and "isResulted!=true"')
        else:
            raise PreconditionNotMetException('No live events found to verify')
        if not livestream:
            self.site.home.desktop_modules.inplay_live_stream_module.tabs_menu.click_item(vec.sb.LIVE_STREAM.upper())

    def test_002_verify_events_when_live_stream_switcher_is_selected(self):
        """
        DESCRIPTION: Verify events when 'Live Stream' switcher is selected
        EXPECTED: Events with the following attributes are present:
        EXPECTED: * Event's/market's/outcome's attribute 'siteChannels' contains 'M'
        EXPECTED: * Attribute 'isStarted="true"' is present
        EXPECTED: * Event's attribute 'drilldownTagNames' contains
        EXPECTED: {"EVFLAG_BL" AND "EVFLAG_IVM"} OR {"EVFLAG_BL" AND "EVFLAG_PVM"} OR {"EVFLAG_BL" AND "EVFLAG_GVM"}
        EXPECTED: * Type's attribute contains 'typeFlagCodes' contains "IVA" OR "PVA" OR "GVA"
        EXPECTED: * Attribute 'isLiveNowEvent="true"' is present
        EXPECTED: * Time in 'suspendAtTime' attribute of the event is NOT in the past or it is not present
        EXPECTED: * At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: * At least one market is not resulted (there is no attribute 'isResulted="true")
        EXPECTED: * At least one market is displayed (available in the response)
        """
        try:
            self.leagues = self.site.home.desktop_modules.inplay_live_stream_module.tab_content.accordions_list.items_as_ordered_dict
        except VoltronException:
            raise PreconditionNotMetException('No live stream events found to verify')
        self.test_001_verify_events_when_in_play_switcher_is_selected(livestream=True, drilldowntagnames=['EVFLAG_BL,EVFLAG_IVM', 'EVFLAG_BL,EVFLAG_PVM', 'EVFLAG_BL,EVFLAG_GVM'])
