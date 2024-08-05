package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertEquals;
import static org.mockito.Matchers.any;
import static org.mockito.Matchers.anyString;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import com.ladbrokescoral.oxygen.cms.api.entity.PromotionSection;
import com.ladbrokescoral.oxygen.cms.api.exception.PromotionNotFound;
import com.ladbrokescoral.oxygen.cms.api.repository.PromotionSectionRepository;
import java.util.List;
import java.util.Optional;
import org.assertj.core.api.Assertions;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class PromotionSectionServiceTest {
  @Mock private PromotionSectionRepository repository;
  @Mock private PromotionService promotionService;

  private PromotionSectionService sectionService;

  @Before
  public void setUp() {
    sectionService = new PromotionSectionService(repository, promotionService);
  }

  @Test(expected = PromotionNotFound.class)
  public void testSaveWhenPromotionIdsAreNotFound() {
    PromotionSection section = new PromotionSection();
    section.setBrand("bma");
    section.setDisabled(false);
    section.setName("championship");
    section.setPromotionIds("1,2,3");
    when(promotionService.findByBrandAndPromotionId(anyString(), anyString()))
        .thenReturn(Optional.empty());

    sectionService.save(section);

    verify(promotionService, times(1)).findByBrandAndPromotionId(anyString(), anyString());
  }

  @Test
  public void testFindByBrandWithDefaultSection() throws Exception {

    when(promotionService.findAllExceptPromotionIds(any()))
        .thenReturn(
            TestUtil.deserializeListWithJackson(
                "service/promotion_section/promotion.json", Promotion.class));
    when(repository.findByBrand(any(), any()))
        .thenReturn(
            TestUtil.deserializeListWithJackson(
                "service/promotion_section/sections.json", PromotionSection.class));

    final List<PromotionSection> expected =
        TestUtil.deserializeListWithJackson(
            "service/promotion_section/sections_with_default_section.json", PromotionSection.class);

    final List<PromotionSection> actual = sectionService.findByBrandWithDefaultSection("bma");

    Assertions.assertThat(actual).isEqualTo(expected);
  }

  @Test
  public void testDeletePromotionIdInSections() throws Exception {
    when(promotionService.findByBrandAndPromotionId(anyString(), any()))
        .thenReturn(Optional.of(new Promotion()));
    when(repository.findByBrand(any(), any()))
        .thenReturn(
            TestUtil.deserializeListWithJackson(
                "service/promotion_section/sections.json", PromotionSection.class));
    when(repository.save(any(PromotionSection.class))).thenReturn(new PromotionSection());

    sectionService.deletePromotionIdInSections("bma", "123");

    ArgumentCaptor<PromotionSection> sectionArgumentCaptor =
        ArgumentCaptor.forClass(PromotionSection.class);
    verify(repository, times(1)).save(sectionArgumentCaptor.capture());
    PromotionSection capturedArgument = sectionArgumentCaptor.getValue();
    assertEquals("125", capturedArgument.getPromotionIds());
  }

  @Test
  public void testUpdatePromotionIdInSections() throws Exception {
    when(promotionService.findByBrandAndPromotionId(anyString(), any()))
        .thenReturn(Optional.of(new Promotion()));
    when(repository.findByBrand(any(), any()))
        .thenReturn(
            TestUtil.deserializeListWithJackson(
                "service/promotion_section/sections.json", PromotionSection.class));
    when(repository.save(any(PromotionSection.class))).thenReturn(new PromotionSection());

    sectionService.updatePromotionIdInSections("bma", "123", "124");

    ArgumentCaptor<PromotionSection> sectionArgumentCaptor =
        ArgumentCaptor.forClass(PromotionSection.class);
    verify(repository, times(1)).save(sectionArgumentCaptor.capture());
    PromotionSection capturedArgument = sectionArgumentCaptor.getValue();
    assertEquals("124,125", capturedArgument.getPromotionIds());
  }
}
