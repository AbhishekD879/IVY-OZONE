package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportCategoryArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.HomeInplaySportsTest;
import com.ladbrokescoral.oxygen.cms.api.dto.SportNameDto;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import com.ladbrokescoral.oxygen.cms.api.repository.HomeInplaySportRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig;
import java.util.*;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.mock.mockito.MockBean;

public class SportCategoryServiceTest {
  private SportCategoryService sportCategoryService;
  @MockBean SportCategoryRepository sportCategoryRepository;
  @MockBean private SportTabService sportTabService;
  @MockBean private SportModuleService sportModuleService;
  @MockBean private ImageEntityService<SportCategory> imageEntityService;
  @MockBean private IconEntityService<SportCategory> iconEntityService;
  @MockBean private SvgEntityService<SportCategory> svgEntityService;
  @MockBean private SiteServeService siteServeService;
  @MockBean private ScheduledTaskExecutor scheduledTaskExecutor;
  @MockBean private ImageConfig.ImagePath sportCategoryIcon;
  @MockBean SportCategoryArchivalRepository sportCategoryArchivalRepository;
  @MockBean private ImageConfig.ImagePath sportCategoryMenuImagePath;
  @MockBean private SegmentService segmentService;
  @MockBean private ModelMapper modelMapper;
  @MockBean private HomeInplaySportRepository homeInplaySportRepository;
  private String segmentName;

  @Before
  public void init() throws Exception {
    sportCategoryRepository = Mockito.mock(SportCategoryRepository.class);
    homeInplaySportRepository = Mockito.mock(HomeInplaySportRepository.class);

    sportCategoryService =
        new SportCategoryService(
            sportCategoryRepository,
            sportTabService,
            sportModuleService,
            imageEntityService,
            iconEntityService,
            svgEntityService,
            siteServeService,
            scheduledTaskExecutor,
            sportCategoryIcon,
            sportCategoryMenuImagePath,
            sportCategoryArchivalRepository,
            segmentService,
            modelMapper,
            homeInplaySportRepository);
  }

  @Test
  public void testSportCategoryTest() {
    Mockito.when(
            sportCategoryRepository.findUniversalRecordsByBrand(
                "bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(findSportCategories());
    List<SportCategory> categories =
        sportCategoryService.findByBrandAndSegmentName("bma", SegmentConstants.UNIVERSAL);
    Assert.assertEquals(SportTier.UNTIED, categories.get(0).getTier());
  }

  @Test
  public void testSportCategory() {
    Mockito.when(
            sportCategoryRepository.findAllByBrandAndSegmentName(
                "bma", Arrays.asList("falcons", "s1")))
        .thenReturn(findSportCategoriesWithSegmentReferences());
    Mockito.when(
            sportCategoryRepository
                .findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
                    anyString(), anyList(), anyList(), any()))
        .thenReturn(findSportCategoriesWithSegmentReferences());

    List<SportCategory> categories =
        sportCategoryService.findByBrandAndSegmentName("bma", "falcons");
    Assert.assertEquals("2", categories.get(1).getId());
  }

  @Test
  public void testreadSportNameByBrand() {
    when(sportCategoryRepository.findByBrandAndCategoryIdNotNullAndIsActiveAndInTier("bma"))
        .thenReturn(findSportCategories());
    when(homeInplaySportRepository.findByBrand("bma"))
        .thenReturn(HomeInplaySportsTest.findAllEntites());
    List<SportNameDto> sportdto = sportCategoryService.readSportNameByBrand("bma");
    Assert.assertNotNull(sportdto);
  }

  @Test
  public void testSportCategoryByBrandAndImage() {
    SportCategory sportCategory = new SportCategory();
    sportCategory.setId("11");
    sportCategory.setImageTitle("football");
    sportCategory.setBrand("bma");
    when(sportCategoryRepository.findByBrandAndImageTitle(any(), any()))
        .thenReturn(Collections.singletonList(sportCategory));
    List<SportCategory> sportCategories =
        this.sportCategoryService.findSportCategoryByBrandAndImageTitle("bma", "football");
    verify(sportCategoryRepository, times(1)).findByBrandAndImageTitle(any(), any());
    Assert.assertEquals("football", sportCategories.get(0).getImageTitle());
  }

  public List<SportCategory> findSportCategories() {
    List<SportCategory> sCategories = new ArrayList<>();
    sCategories.add(createSportCategoryWithIdNull(null, SportTier.UNTIED));
    sCategories.add(createSportCategory(1, SportTier.TIER_1));
    sCategories.add(createSportCategory(2, SportTier.TIER_2));
    sCategories.add(createSportCategory(3, SportTier.TIER_1));
    sCategories.add(createSportCategory(4, SportTier.TIER_2));
    return sCategories;
  }

  public List<SportCategory> findSportCategoriesWithSegmentReferences() {
    List<SportCategory> sCategories = new ArrayList<>();
    sCategories.add(createSportCategoryWithIdNull(null, SportTier.UNTIED));
    sCategories.add(createSportCategory(1, SportTier.TIER_1, "1", 0.2));
    sCategories.add(createSportCategory(2, SportTier.TIER_2, "2", 0.3));
    sCategories.add(createSportCategory(3, SportTier.TIER_1, "3", 0.4));
    sCategories.add(createSportCategory(4, SportTier.TIER_2, "4", 0.5));
    sCategories.add(createSportCategory(4, SportTier.TIER_2, "5", -1.2));
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

  private static SportCategory createSportCategoryWithIdNull(Integer categoryId, SportTier tier) {
    SportCategory sport = new SportCategory();
    sport.setCategoryId(categoryId);
    sport.setTier(tier);
    sport.setBrand("bma");
    return sport;
  }

  private SportCategory createSportCategory(
      Integer categoryId, SportTier tier, String id, Double sortOrder) {
    SportCategory s1 = createSportCategory(categoryId, tier);
    s1.setId(id);

    List<SegmentReference> segmentReferences1 = new ArrayList<>();
    SegmentReference reference1 = new SegmentReference();
    reference1.setSegmentName(SegmentConstants.UNIVERSAL);
    reference1.setSortOrder(sortOrder);
    segmentReferences1.add(reference1);
    SegmentReference reference2 = new SegmentReference();
    reference2.setSegmentName("falcons");
    reference2.setSortOrder(sortOrder);
    segmentReferences1.add(reference2);
    s1.setSegmentReferences(segmentReferences1);
    return s1;
  }
}
