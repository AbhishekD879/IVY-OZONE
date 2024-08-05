package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertEquals;

import com.ladbrokescoral.oxygen.cms.api.dto.PriceDto;
import com.ladbrokescoral.oxygen.cms.api.dto.RelationDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SegmentReferenceDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SurfaceBetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RelationType;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.time.Duration;
import java.time.Instant;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.junit.Test;

public class SurfaceBetSortHelperTest {

  private static final int EXISTS_SELECTION_ID = 907016395;
  private static final String TEST_PAGE_ID = "test";

  @Test
  public void getHomeAndReamingSportPagesSortedOrder() {

    final SurfaceBetDto surfaceBet1 = createValidSurfaceBetDto();
    surfaceBet1.setId("1");
    surfaceBet1.setReference(getRelationDto("0", null));

    final SurfaceBetDto surfaceBet2 = createValidSurfaceBetDto();
    surfaceBet2.setId("2");
    surfaceBet2.setReference(getRelationDto("16", null));

    final SurfaceBetDto surfaceBet3 = createValidSurfaceBetDto();
    surfaceBet3.setId("3");
    surfaceBet3.setReference(getRelationDto("16", 22.0));

    final SurfaceBetDto surfaceBet4 = createValidSurfaceBetDto();
    surfaceBet4.setId("4");
    surfaceBet4.setReference(getRelationDto("16", 2.0));

    final SurfaceBetDto surfaceBet5 = createValidSurfaceBetDto();
    surfaceBet5.setId("5");
    surfaceBet5.setReference(getRelationDto("0", 2.0));

    final SurfaceBetDto surfaceBet6 = createValidSurfaceBetDto();
    surfaceBet6.setId("6");
    surfaceBet6.setReference(getRelationDto("6", 2.0));

    final SurfaceBetDto surfaceBet7 = createValidSurfaceBetDto();
    surfaceBet7.setId("7");
    surfaceBet7.setReference(getRelationDto("16", null));

    final SurfaceBetDto surfaceBet8 = createValidSurfaceBetDto();
    surfaceBet8.setId("8");
    surfaceBet8.setReference(getRelationDto("6", 1.0));

    final SurfaceBetDto surfaceBet9 = createValidSurfaceBetDto();
    surfaceBet9.setId("9");
    surfaceBet9.setReference(getRelationDto("6", null));

    final SurfaceBetDto surfaceBet10 = createValidSurfaceBetDto();
    surfaceBet10.setId("10");
    surfaceBet10.setReference(getEDPRelationDto("647589092"));

    final SurfaceBetDto surfaceBet11 = createValidSurfaceBetDto();
    surfaceBet11.setId("11");
    surfaceBet11.setReference(getEDPRelationDto("56790834"));

    final List<SurfaceBetDto> surfaceBetDtoList =
        Stream.of(
                surfaceBet6,
                surfaceBet2,
                surfaceBet5,
                surfaceBet3,
                surfaceBet1,
                surfaceBet4,
                surfaceBet7,
                surfaceBet8,
                surfaceBet9,
                surfaceBet10,
                surfaceBet11)
            .collect(Collectors.toList());

    final List<SurfaceBetDto> homeAndReamingSportPagesSortedOrder =
        SurfaceBetSortHelper.getHomeAndReamingSportPagesSortedOrder(surfaceBetDtoList);

    assertEquals(
        "surfaceBets size must be match ",
        homeAndReamingSportPagesSortedOrder.size(),
        surfaceBetDtoList.size());
  }

  private RelationDto getRelationDto(final String sportId, final Double sortOrder) {

    final RelationDto relationDto = new RelationDto();
    relationDto.setEnabled(true);
    relationDto.setRelationType(RelationType.sport.name());
    relationDto.setRefId(sportId);
    relationDto.setSortOrder(sortOrder);

    return relationDto;
  }

  private RelationDto getEDPRelationDto(final String sportId) {

    final RelationDto relationDto = new RelationDto();
    relationDto.setEnabled(true);
    relationDto.setRelationType(RelationType.edp.name());
    relationDto.setRefId(sportId);

    return relationDto;
  }

  private static SurfaceBetDto createValidSurfaceBetDto() {

    final RelationDto relationDto = new RelationDto();
    relationDto.setEnabled(true);
    relationDto.setRelationType(RelationType.sport.name());
    relationDto.setRefId(TEST_PAGE_ID);

    final PriceDto priceDto = new PriceDto();
    priceDto.setPriceDec(BigDecimal.valueOf(1.27));
    priceDto.setPriceDen(27);
    priceDto.setPriceNum(10);
    priceDto.setPriceType("LP");

    final SurfaceBetDto result = new SurfaceBetDto();
    result.setDisplayFrom(Instant.now());
    result.setDisplayTo(Instant.now().plus(Duration.ofDays(5)));
    result.setEdpOn(true);
    result.setHighlightsTabOn(true);
    result.setPrice(priceDto);
    result.setSelectionId(BigInteger.valueOf(EXISTS_SELECTION_ID));
    result.setReference(relationDto);
    result.setTitle("test ;:#@&-+()!?'$£");
    result.setContent("content ;:#@&-+()!?'$£");
    result.setSvgBgId("image1");
    result.setSvgBgImgPath("/images/uploads/svg/test1.svg");
    result.setContentHeader("test");
    result.setSegmentReferences(Arrays.asList(getSegmentReferences("segment1")));

    return result;
  }

  private static SegmentReferenceDto getSegmentReferences(String segmentName) {

    final SegmentReferenceDto segmentReferenceDto = new SegmentReferenceDto();
    segmentReferenceDto.setSegment(segmentName);
    segmentReferenceDto.setDisplayOrder(2.0);
    segmentReferenceDto.setPageRefId("0");

    return segmentReferenceDto;
  }
}
