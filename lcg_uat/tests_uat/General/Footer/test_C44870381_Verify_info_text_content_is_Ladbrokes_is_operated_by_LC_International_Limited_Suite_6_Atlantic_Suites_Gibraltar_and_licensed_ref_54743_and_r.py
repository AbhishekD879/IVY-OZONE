import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.p2
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870381_Verify_info_text_content_is_Coral_is_operated_by_LC_International_Limited_Suite_6_Atlantic_Suites_Gibraltar_and_licensed_ref_54743_and_regulated_by_the_British_Gambling_Commission_for_persons_gambling_in_Great_Britain_For_persons_gamblin(Common):
    """
    TR_ID: C44870381
    NAME: "Verify info text content is: Coral is operated by LC International Limited (Suite 6, Atlantic Suites, Gibraltar) and licensed (ref 54743) and regulated by the British Gambling Commission for persons gambling in Great Britain. For persons gamblin
    DESCRIPTION: "Verify info text content is:
    DESCRIPTION: Coral is operated by LC International Limited (Suite 6, Atlantic Suites, Gibraltar) and licensed (ref 54743) and regulated by the British Gambling Commission for persons gambling in Great Britain. For persons gambling outside Great Britain, Coral is licensed (ref 010, 012) by the Government of Gibraltar and regulated by the Gibraltar Gambling Commissioner.
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Application is opened.
        """
        self.site.wait_content_state(state_name="Homepage")

    def test_002_verify_info_text_content_iscoral_is_operated_by_lc_international_limited_suite_6_atlantic_suites_gibraltar_and_licensed_ref_54743_and_regulated_by_the_british_gambling_commission_for_persons_gambling_in_great_britain_for_persons_gambling_outside_great_britain_coral_is_licensed_ref_010_012_by_the_government_of_gibraltar_and_regulated_by_the_gibraltar_gambling_commissioner(self):
        """
        DESCRIPTION: "Verify info text content is:
        DESCRIPTION: Coral is operated by LC International Limited (Suite 6, Atlantic Suites, Gibraltar) and licensed (ref 54743) and regulated by the British Gambling Commission for persons gambling in Great Britain. For persons gambling outside Great Britain, Coral is licensed (ref 010, 012) by the Government of Gibraltar and regulated by the Gibraltar Gambling Commissioner.
        EXPECTED: User is able to see
        EXPECTED: Coral is operated by LC International Limited (Suite 6, Atlantic Suites, Gibraltar) and licensed (ref 54743) and regulated by the British Gambling Commission for persons gambling in Great Britain. For persons gambling outside Great Britain, Coral is licensed (ref 010, 012) by the Government of Gibraltar and regulated by the Gibraltar Gambling Commissioner.
        """
        if self.brand == 'ladbrokes':
            expected_text = vec.gvc.COMPLIANCE_INFORMATION.replace('Coral', self.brand.title())
        else:
            expected_text = vec.gvc.COMPLIANCE_INFORMATION
        actual_text = self.site.footer.footer_content_section.footer_text.text
        self.assertEqual(actual_text, expected_text,
                         msg=f'Actual text: "{actual_text}" is not same as Expected text: "{expected_text}"')
