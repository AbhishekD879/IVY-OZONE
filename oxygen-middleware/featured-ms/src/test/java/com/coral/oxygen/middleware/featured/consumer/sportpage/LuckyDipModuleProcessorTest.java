package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.coral.oxygen.middleware.featured.service.LuckyDipModuleService;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.featured.*;
import java.util.*;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class LuckyDipModuleProcessorTest extends BDDMockito {
  @Mock private LuckyDipModuleService luckyDipModuleService;

  @InjectMocks private LuckyDipModuleProcessor luckyDipModuleProcessor;

  @Test
  public void processModulesTest() throws SportsModuleProcessException {
    List<LuckyDipCategoryData> luckyDipCategoryDataList = Arrays.asList(getluckyDipCategoryData());
    SportModule sportModule = createSportModule(0);
    SportPageModule sportPageModule =
        new SportPageModule(sportModule, createSportPageModuleDataItem("16"));
    when(luckyDipModuleService.processLuckyDipData(any())).thenReturn(luckyDipCategoryDataList);
    LuckyDipModule luckyDipModule =
        luckyDipModuleProcessor.processModule(
            sportPageModule, new CmsSystemConfig(), new HashSet<>());
    Assert.assertEquals(ModuleType.LUCKY_DIP, luckyDipModule.getModuleType());
    Assert.assertEquals(1, luckyDipModule.getData().size());
  }

  @Test
  public void processModulesWithEmptyLuckyDipTest() throws SportsModuleProcessException {
    SportModule sportModule = createSportModule(0);
    SportPageModule sportPageModule =
        new SportPageModule(sportModule, createSportPageModuleDataItemWithEmptyLuckyDip());
    LuckyDipModule luckyDipModule =
        luckyDipModuleProcessor.processModule(
            sportPageModule, new CmsSystemConfig(), new HashSet<>());
    Assert.assertEquals(ModuleType.LUCKY_DIP, luckyDipModule.getModuleType());
    Assert.assertEquals(0, luckyDipModule.getData().size());
  }

  @Test
  public void processModulesWithEmptyLuckyDipMappingTest() throws SportsModuleProcessException {
    SportModule sportModule = createSportModule(0);
    SportPageModule sportPageModule =
        new SportPageModule(sportModule, createSportPageModuleDataItemWithEmptyLuckyDipMappings());
    LuckyDipModule luckyDipModule =
        luckyDipModuleProcessor.processModule(
            sportPageModule, new CmsSystemConfig(), new HashSet<>());
    Assert.assertEquals(ModuleType.LUCKY_DIP, luckyDipModule.getModuleType());
    Assert.assertEquals(0, luckyDipModule.getData().size());
  }

  @Test
  public void processModulesWithNullLuckyDipMappingTest() throws SportsModuleProcessException {
    SportModule sportModule = createSportModule(0);
    SportPageModule sportPageModule =
        new SportPageModule(sportModule, createSportPageModuleDataItemNullModuleMapping());
    LuckyDipModule luckyDipModule =
        luckyDipModuleProcessor.processModule(
            sportPageModule, new CmsSystemConfig(), new HashSet<>());
    Assert.assertEquals(ModuleType.LUCKY_DIP, luckyDipModule.getModuleType());
    Assert.assertEquals(0, luckyDipModule.getData().size());
  }

  private SportModule createSportModule(Integer sportId) {
    SportModule module = new SportModule();
    module.setSportId(sportId);
    module.setPageId(String.valueOf(sportId));
    module.setId(String.valueOf(sportId) + new Random().nextInt());
    module.setPageType(FeaturedRawIndex.PageType.sport);
    return module;
  }

  private List<SportPageModuleDataItem> createSportPageModuleDataItem(String categoryId) {
    List<SportPageModuleDataItem> sportPageModuleDataItemList = new ArrayList<>();
    LuckyDip luckyDip = new LuckyDip();
    luckyDip.setType("LuckyDipModule");
    LuckyDipMapping luckyDipMapping = new LuckyDipMapping();
    luckyDipMapping.setCategoryId(categoryId);
    luckyDipMapping.setTypeIds("78956,82728");
    luckyDipMapping.setSvgId("SvgId");
    luckyDipMapping.setSortOrder(-1.00);
    luckyDip.setLuckyDipMappings(Arrays.asList(luckyDipMapping));
    sportPageModuleDataItemList.add(luckyDip);
    return sportPageModuleDataItemList;
  }

  private List<SportPageModuleDataItem> createSportPageModuleDataItemWithEmptyLuckyDipMappings() {
    List<SportPageModuleDataItem> sportPageModuleDataItemList = new ArrayList<>();
    LuckyDip luckyDip = new LuckyDip();
    luckyDip.setType("LuckyDipModule");
    luckyDip.setLuckyDipMappings(new ArrayList<>());
    sportPageModuleDataItemList.add(luckyDip);
    return sportPageModuleDataItemList;
  }

  private List<SportPageModuleDataItem> createSportPageModuleDataItemNullModuleMapping() {
    List<SportPageModuleDataItem> sportPageModuleDataItemList = new ArrayList<>();
    LuckyDip luckyDip = new LuckyDip();
    luckyDip.setType("LuckyDipModule");
    luckyDip.setLuckyDipMappings(null);
    sportPageModuleDataItemList.add(luckyDip);
    return sportPageModuleDataItemList;
  }

  private List<SportPageModuleDataItem> createSportPageModuleDataItemWithEmptyLuckyDip() {
    return new ArrayList<>();
  }

  private LuckyDipCategoryData getluckyDipCategoryData() {
    LuckyDipCategoryData luckyDipCategoryData = new LuckyDipCategoryData();
    luckyDipCategoryData.setSportName("|Football|");
    luckyDipCategoryData.setLuckyDipTypeData(getluckyDipTypeData());
    return luckyDipCategoryData;
  }

  private List<LuckyDipTypeData> getluckyDipTypeData() {
    LuckyDipTypeData luckyDipTypeData = new LuckyDipTypeData();
    luckyDipTypeData.setTypeName("|League One|");
    LuckyDipMarketData luckyDipMarketData1 = setLuckyDipMarketData(16, "|League One|");
    LuckyDipMarketData luckyDipMarketData2 = setLuckyDipMarketData(16, "|League One|");
    List<LuckyDipMarketData> list = new ArrayList<>();
    list.add(luckyDipMarketData1);
    list.add(luckyDipMarketData2);
    luckyDipTypeData.setLuckyDipMarketData(list);

    LuckyDipTypeData luckyDipTypeData2 = new LuckyDipTypeData();
    luckyDipTypeData2.setTypeName("|League Two|");
    luckyDipTypeData2.setLuckyDipMarketData(List.of(setLuckyDipMarketData(16, "|League Two|")));
    List<LuckyDipTypeData> l = new ArrayList<>();
    l.add(luckyDipTypeData);
    l.add(luckyDipTypeData2);
    return l;
  }

  private LuckyDipMarketData setLuckyDipMarketData(Integer categoryId, String typeName) {
    LuckyDipMarketData luckyDipMarketData = new LuckyDipMarketData();
    luckyDipMarketData.setCategoryId(categoryId);
    luckyDipMarketData.setTypeName(typeName);
    luckyDipMarketData.setCategoryName("|Football|");
    luckyDipMarketData.setEventId("6905203");
    luckyDipMarketData.setTypeId("95507");
    luckyDipMarketData.setEventName("|Newcastle vs Aston Villa|");
    luckyDipMarketData.setMarketId("57974362");
    luckyDipMarketData.setMarketDescription("|Random horse, Racing selection, 125/1|");
    return luckyDipMarketData;
  }
}
