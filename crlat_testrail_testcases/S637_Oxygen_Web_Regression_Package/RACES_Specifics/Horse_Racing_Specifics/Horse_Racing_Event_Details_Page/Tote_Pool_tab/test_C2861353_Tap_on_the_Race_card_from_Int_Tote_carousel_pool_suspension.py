import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2861353_Tap_on_the_Race_card_from_Int_Tote_carousel_pool_suspension(Common):
    """
    TR_ID: C2861353
    NAME: Tap on the Race card from Int Tote carousel (pool suspension)
    DESCRIPTION: Test case verified the behavior when user tap on the event link and updates about pool suspension are not received yet
    PRECONDITIONS: International Tote Races Carousel is present
    PRECONDITIONS: **Instruction on International Tote events mapping**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+International+Tote+events+with+Regular+Horse+Racing+events
    PRECONDITIONS: **CMS configuration**
    PRECONDITIONS: System configuration > Structure: InternationalTotePool is enabled
    PRECONDITIONS: **Request to retrieve events to be shown in the International Tote carousel:**
    PRECONDITIONS: EventToMarketForClass/16288
    PRECONDITIONS: where class - Horse Racing - Intl Thoroughbred Pools
    PRECONDITIONS: **Request from pool types on EDP**
    PRECONDITIONS: PoolForEvent/event_id
    PRECONDITIONS: **User is on Horse racing landing page.**
    """
    keep_browser_open = True

    def test_001_while_user_stays_on_the_hr_landing_page_go_to_ob_office_and_suspend_the_pool_first_default_pool_for_the_event_to_be_opened(self):
        """
        DESCRIPTION: While user stays on the HR landing page, go to OB office, and suspend the pool (first default pool for the event to be opened)
        EXPECTED: Pool suspended
        """
        pass

    def test_002_tap_on_the_event_from_int_tote_carousel(self):
        """
        DESCRIPTION: Tap on the event from Int Tote carousel
        EXPECTED: - Event card is opened
        EXPECTED: - Totepool tab is selected
        EXPECTED: - Selected pool is greyed out as suspended
        """
        pass

    def test_003_verify_url_path(self):
        """
        DESCRIPTION: Verify url path
        EXPECTED: Path contains /{event_id}/totepool/{actual selected pool type}
        """
        pass
