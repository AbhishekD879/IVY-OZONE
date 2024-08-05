package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType.*;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.FooterMenusTest;
import com.ladbrokescoral.oxygen.cms.api.dto.SportQuickLinkDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportQuickLink;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportQuickLinkExtendedRepository;
import java.time.Instant;
import java.util.Arrays;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SportQuickLinkPublicServiceTest extends BDDMockito {

  @Mock private SportQuickLinkExtendedRepository sportQuickLinkExtendedRepository;

  @Mock private SegmentRepository segmentRepository;

  @InjectMocks private SportQuickLinkPublicService sportQuickLinkPublicService;

  @Before
  public void setUp() {
    given(segmentRepository.findByBrand("bma"))
        .willReturn(
            Arrays.asList(
                Segment.builder().segmentName(SegmentConstants.UNIVERSAL).build(),
                Segment.builder().segmentName("segment1").build()));
  }

  @Test
  public void findAllTest() {
    // given
    given(sportQuickLinkExtendedRepository.findAll("bma"))
        .willReturn(Arrays.asList(createSportQuickLink()));
    List<SportQuickLinkDto> sportQuickLinkDtos = sportQuickLinkPublicService.findAll("bma");
    Assert.assertNotNull(sportQuickLinkDtos);
    Assert.assertSame(1, sportQuickLinkDtos.size());
  }

  @Test
  public void findAllTestForNonUniversal() {
    // given
    SportQuickLink sportQuickLink = createSportQuickLink();
    sportQuickLink.setUniversalSegment(false);
    sportQuickLink.setSegmentReferences(FooterMenusTest.getSegmentReference("segment1"));

    given(sportQuickLinkExtendedRepository.findAll("bma"))
        .willReturn(Arrays.asList(sportQuickLink));

    List<SportQuickLinkDto> sportQuickLinkDtos = sportQuickLinkPublicService.findAll("bma");
    Assert.assertNotNull(sportQuickLinkDtos);
    Assert.assertSame(1, sportQuickLinkDtos.size());
  }

  @Test
  public void findAllTestForUniversalEmptyExclussionList() {
    // given
    SportQuickLink sportQuickLink = createSportQuickLink();
    sportQuickLink.setExclusionList(null);
    given(sportQuickLinkExtendedRepository.findAll("bma"))
        .willReturn(Arrays.asList(sportQuickLink));

    List<SportQuickLinkDto> sportQuickLinkDtos = sportQuickLinkPublicService.findAll("bma");
    Assert.assertNotNull(sportQuickLinkDtos);
    Assert.assertSame(1, sportQuickLinkDtos.size());
  }

  private SportQuickLink createSportQuickLink() {
    SportQuickLink sportQuickLink = new SportQuickLink();
    sportQuickLink.setId("1");
    sportQuickLink.setSportId(0);
    sportQuickLink.setTitle("sport quicklink1");
    sportQuickLink.setUniversalSegment(true);
    sportQuickLink.setExclusionList(Arrays.asList("segment1"));
    sportQuickLink.setDestination("https://www.google.co.in");
    sportQuickLink.setValidityPeriodEnd(Instant.now());
    sportQuickLink.setValidityPeriodEnd(Instant.now().plusSeconds(60 * 60 * 24));
    sportQuickLink.setBrand("bma");
    sportQuickLink.setMessage("hello");
    sportQuickLink.setPageId("0");
    sportQuickLink.setPageType(PageType.valueOf("sport"));

    return sportQuickLink;
  }
}
