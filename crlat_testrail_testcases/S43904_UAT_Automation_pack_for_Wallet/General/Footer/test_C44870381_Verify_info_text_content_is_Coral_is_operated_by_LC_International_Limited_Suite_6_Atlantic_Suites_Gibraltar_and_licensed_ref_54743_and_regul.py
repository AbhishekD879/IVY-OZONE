import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870381_Verify_info_text_content_is_Coral_is_operated_by_LC_International_Limited_Suite_6_Atlantic_Suites_Gibraltar_and_licensed_ref_54743_and_regulated_by_the_British_Gambling_Commission_for_persons_gambling_in_Great_Britain_For_persons_gamblin(Common):
    """
    TR_ID: C44870381
    NAME: "Verify info text content is: Coral is operated by LC International Limited (Suite 6, Atlantic Suites, Gibraltar) and licensed (ref 54743) and regulated by the British Gambling Commission for persons gambling in Great Britain. For persons gamblin
    DESCRIPTION: "Verify info text content is:
    DESCRIPTION: Coral is operated by LC International Limited who are licensed and regulated in Great Britain by the Gambling Commission under account number 54743
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Application is opened and scroll to the bottom of the Homepage
        """
        pass

    def test_002_verify_info_text_content_iscoral_is_operated_by_lc_international_limited_who_are_licensed_and_regulated_in_great_britain_by_the_gambling_commission_under_account_number_54743(self):
        """
        DESCRIPTION: "Verify info text content is:
        DESCRIPTION: Coral is operated by LC International Limited who are licensed and regulated in Great Britain by the Gambling Commission under account number 54743
        EXPECTED: User is able to see
        EXPECTED: Coral is operated by LC International Limited who are licensed and regulated in Great Britain by the Gambling Commission under account number 54743
        """
        pass
