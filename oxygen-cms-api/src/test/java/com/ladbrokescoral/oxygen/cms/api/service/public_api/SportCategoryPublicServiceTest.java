package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.dto.InitialDataSportCategoryDto;
import com.ladbrokescoral.oxygen.cms.api.dto.InitialDataSportCategorySegmentedDto;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import com.ladbrokescoral.oxygen.cms.api.repository.InplayStatsDisplayRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.InplayStatsSortingRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportTabRepository;
import com.ladbrokescoral.oxygen.cms.api.service.InplayStatsDisplayService;
import com.ladbrokescoral.oxygen.cms.api.service.InplayStatsSortingService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentService;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.util.CollectionUtils;

@RunWith(MockitoJUnitRunner.class)
public class SportCategoryPublicServiceTest {

  private static final String CORAL_BRAND = "bma";

  @Mock SportCategoryRepository categoryRepository;
  @Mock private SportTabRepository tabRepository;
  @InjectMocks SportCategoryPublicService service;
  @Mock private SegmentService segmentService;

  @Mock private InplayStatsDisplayRepository statsDisplayRepository;
  @Mock private InplayStatsSortingRepository statsSortingRepository;

  @Before
  public void setup() {
    InplayStatsDisplayService statsDisplayService =
        new InplayStatsDisplayService(statsDisplayRepository);
    InplayStatsSortingService statsSortingService =
        new InplayStatsSortingService(statsSortingRepository);
    service =
        new SportCategoryPublicService(
            categoryRepository,
            tabRepository,
            segmentService,
            statsDisplayService,
            statsSortingService);
  }

  @Test
  public void testMappingInplayStatsConfig() {
    InplayStatsConfig config = new InplayStatsConfig();
    config.setNote("note");
    config.setReorderDisplayIn(11);
    SportCategory category1 = createSportCategory(16, SportTier.TIER_1);
    category1.setInplayStatsConfig(config);
    category1.setDisabled(false);
    SportCategory category2 = createSportCategory(4, SportTier.TIER_2);
    category2.setDisabled(false);
    category2.setInplayStatsConfig(null);
    when(categoryRepository.findUniversalRecordsByBrand(
            "bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(Collections.singletonList(category1));
    when(categoryRepository.findByDisableFalseAndIdNotIn(Mockito.anyList(), Mockito.any()))
        .thenReturn(Collections.singletonList(category2));
    when(this.statsDisplayRepository.findAllByBrandAndCategoryIdOrderBySortOrderAsc(
            Mockito.anyString(), Mockito.any()))
        .thenReturn(Collections.singletonList(buildInplayStatsDisplay()));
    when(this.statsSortingRepository.findAllByBrandAndCategoryIdOrderBySortOrderAsc(
            Mockito.anyString(), Mockito.any()))
        .thenReturn(Collections.singletonList(buildInplayStatsSorting()));
    List<InitialDataSportCategoryDto> result =
        service.findSportCategoriesInitialData("bma", SegmentConstants.UNIVERSAL);
    Assert.assertTrue(!CollectionUtils.isEmpty(result) && 2 == result.size());
  }

  @Test
  public void testFindSportCategoriesInitialDataUniversalTest() {

    when(categoryRepository.findUniversalRecordsByBrand(
            "bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(findUniversalRecords());

    when(categoryRepository.findByDisableFalseAndIdNotIn(Mockito.anyList(), Mockito.any()))
        .thenReturn(findSegmentsSportCategories());

    List<InitialDataSportCategoryDto> result =
        service.findSportCategoriesInitialData("bma", SegmentConstants.UNIVERSAL);

    Assert.assertTrue(!CollectionUtils.isEmpty(result) && 12 == result.size());
  }

  @Test
  public void testFindSportCategoriesInitialDataSegmentTest() {

    when(categoryRepository.findAllByBrandAndSegmentName("bma", Arrays.asList("segment1")))
        .thenReturn(findSegmentsSportCategories());
    when(categoryRepository
            .findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
                Mockito.anyString(), Mockito.anyList(), Mockito.anyList(), Mockito.any()))
        .thenReturn(findUniversalRecords());

    List<InitialDataSportCategoryDto> result =
        service.findSportCategoriesInitialData("bma", "segment1");

    Assert.assertTrue(!CollectionUtils.isEmpty(result) && 11 == result.size());
  }

  @Test
  public void testFindSportCategoriesInitialDataSegmentTestWithEmptysegmentList() {

    when(categoryRepository.findAllByBrandAndSegmentName("bma", Arrays.asList("segment1")))
        .thenReturn(new ArrayList<>());
    when(categoryRepository
            .findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
                Mockito.anyString(), Mockito.anyList(), Mockito.anyList(), Mockito.any()))
        .thenReturn(findUniversalRecords());

    List<InitialDataSportCategoryDto> result =
        service.findSportCategoriesInitialData("bma", "segment1");

    Assert.assertTrue(!CollectionUtils.isEmpty(result) && 6 == result.size());
  }

  @Test
  public void testFindAllActiveByBrand() {

    when(categoryRepository.findAllByBrandAndDisabledOrderBySortOrderAsc("bma", Boolean.FALSE))
        .thenReturn(findAllEntites());
    when(segmentService.getSegmentsForSegmentedViews("bma")).thenReturn(Arrays.asList("s1", "s2"));
    List<InitialDataSportCategorySegmentedDto> result = service.findAllActiveByBrand("bma");
    Assert.assertTrue(!CollectionUtils.isEmpty(result) && 13 == result.size());
  }

  @Test
  public void testInplayStatsConfigForCF() {
    InplayStatsConfig config = new InplayStatsConfig();
    config.setNote("note");
    config.setReorderDisplayIn(11);
    SportCategory category = createSportCategory(16, SportTier.TIER_1);
    category.setInplayStatsConfig(config);
    when(categoryRepository.findAllByBrandAndDisabledOrderBySortOrderAsc("bma", Boolean.FALSE))
        .thenReturn(Collections.singletonList(category));
    when(segmentService.getSegmentsForSegmentedViews("bma")).thenReturn(Arrays.asList("s1", "s2"));
    when(this.statsDisplayRepository.findAllByBrandAndCategoryIdOrderBySortOrderAsc(
            Mockito.anyString(), Mockito.any()))
        .thenReturn(Collections.singletonList(buildInplayStatsDisplay()));
    when(this.statsSortingRepository.findAllByBrandAndCategoryIdOrderBySortOrderAsc(
            Mockito.anyString(), Mockito.any()))
        .thenReturn(Collections.singletonList(buildInplayStatsSorting()));
    List<InitialDataSportCategorySegmentedDto> result = service.findAllActiveByBrand("bma");
    Assert.assertTrue(!CollectionUtils.isEmpty(result) && 1 == result.size());
  }

  @Test
  public void testFindInitialData() {

    when(categoryRepository.findAllByBrandAndDisabledOrderBySortOrderAsc("bma", Boolean.FALSE))
        .thenReturn(findAllEntites());
    List<InitialDataSportCategoryDto> result = service.findInitialData("bma");
    Assert.assertTrue(!CollectionUtils.isEmpty(result) && 13 == result.size());
  }

  private InplayStatsDisplay buildInplayStatsDisplay() {
    InplayStatsDisplay display = new InplayStatsDisplay();
    display.setId("1122");
    display.setBrand("bma");
    return display;
  }

  private InplayStatsSorting buildInplayStatsSorting() {
    InplayStatsSorting sorting = new InplayStatsSorting();
    sorting.setId("3344");
    sorting.setBrand("bma");
    return sorting;
  }

  public List<SportCategory> findAllEntites() {

    List<SportCategory> sCategories = new ArrayList<>();
    sCategories.addAll(findSegmentsSportCategories());
    sCategories.addAll(findUniversalRecords());

    return sCategories;
  }

  public List<SportCategory> findSegmentsSportCategories() {
    List<SportCategory> sCategories = new ArrayList<>();
    sCategories.add(createSportCategory(1, SportTier.TIER_1, "1", 3.0, "segment1", false));
    sCategories.add(createSportCategory(2, SportTier.TIER_2, "2", 0.3, "segment1", false));
    sCategories.add(createSportCategory(3, SportTier.TIER_1, "3", 5.0, "segment1", false));
    sCategories.add(createSportCategory(4, SportTier.TIER_2, "4", 0.3, "segment1", false));
    sCategories.add(createSportCategory(4, SportTier.TIER_2, "5", -1.0, "segment1", false));
    SportCategory category = createSportCategory(4, SportTier.TIER_2, "6", -1.2, "segment1", false);
    category.setDisabled(true);
    sCategories.add(category);
    return sCategories;
  }

  public List<SportCategory> findUniversalRecords() {
    List<SportCategory> sCategories = new ArrayList<>();
    sCategories.add(
        createSportCategory(1, SportTier.TIER_1, "11", 0.2, SegmentConstants.UNIVERSAL, true));
    sCategories.add(
        createSportCategory(2, SportTier.TIER_2, "16", 0.3, SegmentConstants.UNIVERSAL, true));
    sCategories.add(
        createSportCategory(3, SportTier.TIER_1, "7", 0.4, SegmentConstants.UNIVERSAL, true));
    sCategories.add(
        createSportCategory(4, SportTier.TIER_2, "8", 0.5, SegmentConstants.UNIVERSAL, true));
    sCategories.add(
        createSportCategory(4, SportTier.TIER_2, "9", -1.2, SegmentConstants.UNIVERSAL, true));

    SportCategory category =
        createSportCategory(4, SportTier.TIER_2, "10", -1.2, SegmentConstants.UNIVERSAL, true);
    SportCategory categorynoSegRef =
        createSportCategory(4, SportTier.TIER_2, "33", -1.2, SegmentConstants.UNIVERSAL, true);
    categorynoSegRef.setSegmentReferences(new ArrayList<>());
    category.setDisabled(true);
    sCategories.add(category);
    sCategories.add(categorynoSegRef);
    return sCategories;
  }

  private SportCategory createSportCategory(Integer categoryId, SportTier tier) {
    SportCategory sport = new SportCategory();
    sport.setCategoryId(categoryId);
    sport.setTier(tier);
    sport.setBrand("bma");
    sport.setId("121");
    return sport;
  }

  private SportCategory createSportCategory(
      Integer categoryId,
      SportTier tier,
      String id,
      Double sortOrder,
      String segmentName,
      boolean isuniversal) {
    SportCategory sportCategory = createSportCategory(categoryId, tier);
    sportCategory.setId(id);
    sportCategory.setCreatedAt(Instant.now());
    sportCategory.setUniversalSegment(isuniversal);

    List<SegmentReference> segmentReferences = new ArrayList<>();

    SegmentReference reference = new SegmentReference();
    reference.setSegmentName(segmentName);
    reference.setSortOrder(sortOrder);
    segmentReferences.add(reference);
    sportCategory.setSegmentReferences(segmentReferences);
    if (!isuniversal) sportCategory.setInclusionList(Arrays.asList(segmentName));

    return sportCategory;
  }
}
