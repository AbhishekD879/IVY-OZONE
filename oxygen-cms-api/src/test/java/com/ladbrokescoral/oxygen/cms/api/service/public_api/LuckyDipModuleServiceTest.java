package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipMappingPublicDto;
import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipModuleDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipMappingPublicService;
import com.ladbrokescoral.oxygen.cms.api.service.SportModuleService;
import java.util.ArrayList;
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
public class LuckyDipModuleServiceTest extends BDDMockito {
  @Mock private SportModuleService sportModuleService;
  @Mock private SportCategoryRepository sportCategoryRepository;
  @Mock private LuckyDipMappingPublicService luckyDipMappingPublicService;

  @InjectMocks private LuckyDipModuleService luckyDipModuleService;

  private List<SportCategory> sportCategories;

  @Before
  public void setUp() throws Exception {
    sportCategories =
        TestUtil.deserializeListWithJackson(
            "service/public_api/ladbrokes_sportCategories.json", SportCategory.class);
  }

  @Test
  public void getLuckyDipModuleDataTestHappyPath() {
    when(sportCategoryRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(any(), any()))
        .thenReturn(sportCategories);
    when(sportModuleService.findAll(any(), any())).thenReturn(Arrays.asList(createSportModule()));
    List<LuckyDipMappingPublicDto> list = new ArrayList<>();
    LuckyDipMappingPublicDto luckyDipMappingPublicDto = new LuckyDipMappingPublicDto();
    luckyDipMappingPublicDto.setId("65e8179ac315856972632c29");
    luckyDipMappingPublicDto.setCategoryId("Football");
    luckyDipMappingPublicDto.setTypeIds("442,435,25230,25231,682,438");
    luckyDipMappingPublicDto.setCategory(16);
    list.add(luckyDipMappingPublicDto);
    when(luckyDipMappingPublicService.findAllActiveLuckyDipMappingsByBrand(any())).thenReturn(list);
    List<LuckyDipModuleDto> luckyDipModuleDtoList =
        luckyDipModuleService.getLuckyDipModuleData("ladbrokes");
    Assert.assertNotNull(luckyDipModuleDtoList);
  }

  @Test
  public void getLuckyDipModuleDataTestSvgIdNull() {
    SportCategory sportCategory = new SportCategory();
    sportCategory.setSvgId(null);
    when(sportCategoryRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(any(), any()))
        .thenReturn(Arrays.asList(sportCategory));
    when(sportModuleService.findAll(any(), any())).thenReturn(Arrays.asList(createSportModule()));
    List<LuckyDipMappingPublicDto> list = new ArrayList<>();
    LuckyDipMappingPublicDto luckyDipMappingPublicDto = new LuckyDipMappingPublicDto();
    luckyDipMappingPublicDto.setId("65e8179ac315856972632c29");
    luckyDipMappingPublicDto.setCategoryId("Football");
    luckyDipMappingPublicDto.setTypeIds("442,435,25230,25231,682,438");
    luckyDipMappingPublicDto.setCategory(16);
    list.add(luckyDipMappingPublicDto);
    when(luckyDipMappingPublicService.findAllActiveLuckyDipMappingsByBrand(any())).thenReturn(list);
    List<LuckyDipModuleDto> luckyDipModuleDtoList =
        luckyDipModuleService.getLuckyDipModuleData("ladbrokes");
    Assert.assertNotNull(luckyDipModuleDtoList);
  }

  @Test
  public void getLuckyDipModuleDataTestCategoryIdNull() {
    SportCategory sportCategory = new SportCategory();
    sportCategory.setCategoryId(null);
    when(sportCategoryRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(any(), any()))
        .thenReturn(Arrays.asList(sportCategory));
    when(sportModuleService.findAll(any(), any())).thenReturn(Arrays.asList(createSportModule()));
    List<LuckyDipMappingPublicDto> list = new ArrayList<>();
    LuckyDipMappingPublicDto luckyDipMappingPublicDto = new LuckyDipMappingPublicDto();
    luckyDipMappingPublicDto.setId("65e8179ac315856972632c29");
    luckyDipMappingPublicDto.setCategoryId("Football");
    luckyDipMappingPublicDto.setTypeIds("442,435,25230,25231,682,438");
    luckyDipMappingPublicDto.setCategory(16);
    list.add(luckyDipMappingPublicDto);
    when(luckyDipMappingPublicService.findAllActiveLuckyDipMappingsByBrand(any())).thenReturn(list);
    List<LuckyDipModuleDto> luckyDipModuleDtoList =
        luckyDipModuleService.getLuckyDipModuleData("ladbrokes");
    Assert.assertNotNull(luckyDipModuleDtoList);
  }

  private SportModule createSportModule() {
    SportModule sportModule = new SportModule();
    sportModule.setModuleType(SportModuleType.LUCKY_DIP);
    return sportModule;
  }
}
