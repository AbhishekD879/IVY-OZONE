package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.junit.Assert.assertEquals;

import com.fasterxml.jackson.core.type.TypeReference;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionContainerDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionV2Dto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionWithSectionContainerDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import com.ladbrokescoral.oxygen.cms.api.entity.PromotionSection;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import com.ladbrokescoral.oxygen.cms.api.service.PromotionSectionService;
import com.ladbrokescoral.oxygen.cms.api.service.PromotionService;
import com.ladbrokescoral.oxygen.cms.api.service.StructureService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.PromotionPublicService;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.skyscreamer.jsonassert.JSONAssert;
import org.skyscreamer.jsonassert.JSONCompareMode;

@RunWith(MockitoJUnitRunner.class)
public class PromotionsApiTest extends BDDMockito {

  @Mock private PromotionService promotionServiceMock;
  @Mock private StructureService structureServiceMock;
  @Mock private PromotionSectionService sectionService;
  @Mock private SportCategoryRepository sportCategoryRepository;

  @InjectMocks private PromotionPublicService service;
  private PromotionsApi promotionsApi;

  @Before
  public void init() throws Exception {

    promotionsApi = new PromotionsApi(service);

    when(structureServiceMock.findByBrandAndConfigName("bma", "Promotions"))
        .thenReturn(Optional.of(Collections.singletonMap("expandedAmount", 20)));

    List<Promotion> promotions =
        TestUtil.deserializeListWithJackson(
            "controller/public_api/promotions.json", Promotion.class);
    when(promotionServiceMock.findAllByBrandSorted("bma")).thenReturn(promotions);
    when(promotionServiceMock.findAllByBrandSortedAndCompetitionId("bma", "1"))
        .thenReturn(promotions);
  }

  @Test
  public void findByBrandTest() throws Exception {
    PromotionContainerDto<PromotionDto> result = promotionsApi.findByBrand("bma");

    PromotionContainerDto<PromotionDto> expected =
        TestUtil.deserializeWithJacksonToType(
            "controller/public_api/promotionContainer.json",
            new TypeReference<PromotionContainerDto<PromotionDto>>() {});

    JSONAssert.assertEquals(
        TestUtil.serializeWithJackson(expected),
        TestUtil.serializeWithJackson(result),
        JSONCompareMode.STRICT);
  }

  @Test
  public void findByBrandGroupedBySectionTest() throws Exception {

    when(promotionServiceMock.findByIds(any(), any()))
        .thenReturn(
            TestUtil.deserializeListWithJackson(
                "controller/public_api/promotions/unassigned.json", Promotion.class));
    when(promotionServiceMock.findByPromotionIdsSorted("bma", Collections.singletonList("123")))
        .thenReturn(
            TestUtil.deserializeListWithJackson(
                "controller/public_api/promotions/123.json", Promotion.class));
    when(promotionServiceMock.findByPromotionIdsSorted("bma", Arrays.asList("124", "125")))
        .thenReturn(
            TestUtil.deserializeListWithJackson(
                "controller/public_api/promotions/124-125.json", Promotion.class));
    when(promotionServiceMock.findByPromotionIdsSorted("bma", Arrays.asList("126", "127")))
        .thenReturn(
            TestUtil.deserializeListWithJackson(
                "controller/public_api/promotions/126-127.json", Promotion.class));

    List<PromotionSection> sections =
        TestUtil.deserializeListWithJackson(
            "controller/public_api/sections.json", PromotionSection.class);
    when(sectionService.findByBrandWithDefaultSectionSorted("bma")).thenReturn(sections);

    PromotionWithSectionContainerDto result = promotionsApi.findByBrandAndGroupedBySection("bma");

    PromotionWithSectionContainerDto expected =
        TestUtil.deserializeWithJackson(
            "controller/public_api/promotionBySectionsContainer.json",
            PromotionWithSectionContainerDto.class);
    JSONAssert.assertEquals(
        TestUtil.serializeWithJackson(expected),
        TestUtil.serializeWithJackson(result),
        JSONCompareMode.STRICT);
  }

  @Test
  public void findByBrandWithDefaultExpandedAmountTest() {
    when(structureServiceMock.findByBrandAndConfigName("bma", "Promotions"))
        .thenReturn(Optional.empty());

    PromotionContainerDto<PromotionDto> result = promotionsApi.findByBrand("bma");

    assertEquals("2", result.getExpandedAmount());
  }

  @Test
  public void findByBrandAndCompetitionId() throws Exception {
    PromotionContainerDto<PromotionV2Dto> actual =
        promotionsApi.findByBrandAndCompetitions("bma", "1");
    PromotionContainerDto<PromotionV2Dto> expected =
        TestUtil.deserializeWithJacksonToType(
            "controller/public_api/promotionsExpected.json",
            new TypeReference<PromotionContainerDto<PromotionV2Dto>>() {});
    Assert.assertEquals("Objects are not equals", expected, actual);
  }
}
