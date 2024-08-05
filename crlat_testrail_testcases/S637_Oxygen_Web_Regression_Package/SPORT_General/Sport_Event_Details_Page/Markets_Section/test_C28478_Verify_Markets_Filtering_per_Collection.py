import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28478_Verify_Markets_Filtering_per_Collection(Common):
    """
    TR_ID: C28478
    NAME: Verify Market's Filtering per Collection
    DESCRIPTION: This test case verifies Market's Filtering per Collection.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1. http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/SportToCollection?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: NOTE: For **combined markets** (e.g. Popular Goalscorer Markets, Over/Under Total Goals, etc) if one of the markets within combined markets section contains an **id **of collection from collection ribbon -> whole combined markets section is shown under this collection.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sport> Landing Page
        EXPECTED: <Sport> Landing Page is opened
        """
        pass

    def test_003_clicktap_on_event_name_or_more_link_on_the_event_section(self):
        """
        DESCRIPTION: Click/Tap on Event Name or 'More' link on the event section
        EXPECTED: <Sport> Event Details page is opened
        """
        pass

    def test_004_clicktap_on_name_of_verified_collection(self):
        """
        DESCRIPTION: Click/Tap on name of verified collection
        EXPECTED: *   The first **two** Market sections are expanded by default **For Mobile/Tablet**
        EXPECTED: *   The first **four** Market sections are expanded by default **For Desktop**
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand Market sections by tapping the section's header
        """
        pass

    def test_005_check_collection_id_use_link_2_from_preconditions_of_collection_from_step_4(self):
        """
        DESCRIPTION: Check collection **id **(use link 2 from preconditions) of collection from step №4
        EXPECTED: 
        """
        pass

    def test_006_verifycollectionids_attribute_of_each_market(self):
        """
        DESCRIPTION: Verify **collectionIds **attribute of each Market
        EXPECTED: Market's **collectionIds **contains **id **of collection from step №5
        """
        pass

    def test_007_please_repeat_steps_4_6_for_all_available_collections_on_event_details_page(self):
        """
        DESCRIPTION: Please repeat steps №4-6 for all available Collections on Event Details Page
        EXPECTED: 
        """
        pass
