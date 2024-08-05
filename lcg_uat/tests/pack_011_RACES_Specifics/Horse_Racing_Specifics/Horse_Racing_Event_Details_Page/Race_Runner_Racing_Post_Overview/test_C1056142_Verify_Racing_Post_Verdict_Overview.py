import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2  # coral only
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.desktop
@pytest.mark.race_form
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1056142_Verify_Racing_Post_Verdict_Overview(BaseRacing):
    """
    TR_ID: C1056142
    NAME: Verify Racing Post Verdict Overview
    DESCRIPTION: This test case verifies 'Racing Post' logo and Overview displaying on Event Details page.
    """
    keep_browser_open = True

    def test_001_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the Event details page
        """
        self.__class__.event_info = self.get_racing_event_with_form_details(event_complete_info=True, star_rating=['1', '2', '3', '4', '5'])
        if not self.event_info:
            raise SiteServeException('Racing events not available')
        event_id = list(self.event_info.keys())[0]
        self.navigate_to_edp(event_id=event_id, sport_name='horse-racing')
        self.__class__.is_mobile = True if self.device_type in ['mobile'] else False

    def test_002_verify_racing_post_overview(self):
        """
        DESCRIPTION: Verify Racing Post overview
        EXPECTED: Racing Post overview consists of:
        EXPECTED: **For mobile&tablet:**
        EXPECTED: *   Racing Post | Verdict labels
        EXPECTED: *   100 characters <Race> information for Horse is displayed, followed by 'Show More' link
        EXPECTED: *   Racing Post section is located above Media area
        EXPECTED: **For desktop:**
        EXPECTED: *   Racing Post | Verdict labels
        EXPECTED: *   The whole information text is displayed
        EXPECTED: *   The Racing Post section is located in the second column
        EXPECTED: *   The Racing Post section is expanded by default
        EXPECTED: *   User is able to collapse/expand section by pressing up/down arrow icon
        """
        self.__class__.post_info = self.site.racing_event_details.tab_content.post_info
        self.assertTrue(self.post_info.logo_icon.is_displayed(),
                        msg='"Racing Post | Verdict" logo is not displayed')
        self.assertTrue(self.post_info.has_logo_icon, msg ='"Racing Post | Verdict" has no logo icon')
        if self.is_mobile:
            self.post_info.click()
            racing_post_verdict = self.site.racing_event_details.racing_post_verdict
            self.assertTrue(racing_post_verdict, msg='"Racing Post Verdict overlay" is not shown')
            self.assertTrue(racing_post_verdict.is_at_bottom(),
                            msg='"Racing Post  Verdict" overlay is not shown at the bottom of the page')
            self.__class__.description = racing_post_verdict.summary
            self.assertTrue(self.description.text, msg='Racing Post summary is not displayed')
            # racing_post_verdict.header.close_button.click()
            if self.description.is_truncated():
                self.assertTrue(self.post_info.has_summary_button, msg='"Show more" link is not displayed')
        else:
            self.__class__.description = self.post_info.summary_text
            self.assertFalse(self.description.is_truncated(), msg='Racing Post overview text is truncated')
            self.assertTrue(self.post_info.is_expanded(),
                            msg='Racing Post accordion in not expanded')
            self.post_info.collapse()
            self.assertFalse(self.post_info.is_expanded(),
                             msg='Racing Post accordion in not collapsed')
            self.post_info.expand()
            self.assertTrue(self.post_info.is_expanded(), msg='Racing Post accordion in not expanded')

    def test_003_tap_on_show_more_link(self):
        """
        DESCRIPTION: Tap on 'Show More' link
        EXPECTED: * The whole information text is shown
        EXPECTED: * Link is changed to 'Show Less' link
        """
        if self.is_mobile:
            if self.description.is_truncated():
                self.post_info.show_summary_button.click()
                self.assertFalse(self.site.racing_event_details.tab_content.post_info.summary_text.is_truncated(),
                                 msg='Text is truncated after clicking on "Show More" link')
                self.assertEqual(self.post_info.show_summary_button.name, 'Show Less',
                                 msg=f'Link name "{self.post_info.show_summary_button.name}" '
                                     f'is not the same as expected "Show Less"')

    def test_004_verify_racing_post__verdict_logo(self):
        """
        DESCRIPTION: Verify 'Racing Post | Verdict' logo
        EXPECTED: 'Racing Post | Verdict' logo is NOT hyperlinked
        """
        self.assertFalse(self.post_info.logo_icon.is_hyperlinked, msg='Racing Post logo icon is hyperlinked')

    def test_005_tap_on_show_less_link(self):
        """
        DESCRIPTION: Tap on 'Show Less' link
        EXPECTED: Racing Post section is collapsed
        """
        if self.is_mobile:
            if self.description.is_truncated():
                self.post_info.show_summary_button.click()
                self.assertTrue(self.site.racing_event_details.tab_content.post_info.summary_text.is_truncated(),
                                msg='Text is not truncated after clicking on "Show Less" link')
