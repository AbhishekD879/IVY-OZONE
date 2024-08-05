package com.coral.oxygen.middleware.featured.service;

import com.coral.oxygen.middleware.featured.service.injector.FeaturedSiteServerService;
import com.coral.oxygen.middleware.featured.utils.TestUtils;
import com.coral.oxygen.middleware.pojos.model.cms.featured.LuckyDipMapping;
import com.coral.oxygen.middleware.pojos.model.output.featured.LuckyDipCategoryData;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class LuckyDipModuleServiceTest extends BDDMockito {

  @Mock private FeaturedSiteServerService siteServerService;
  @InjectMocks LuckyDipModuleService luckyDipModuleService;

  @Test
  public void processModulesTest() {
    Gson gson = new GsonBuilder().create();
    Type ssResponseType = new TypeToken<List<Children>>() {}.getType();
    Optional<List<Children>> response =
        Optional.of(gson.fromJson(TestUtils.getResourse("luckyDipEvents.json"), ssResponseType));
    Optional<List<Event>> event =
        response.map(
            resp -> resp.stream().map(Children::getEvent).filter(Objects::nonNull).toList());
    LuckyDipMapping footballLuckyDipMapping = new LuckyDipMapping();
    footballLuckyDipMapping.setCategoryId("Football");
    footballLuckyDipMapping.setCategory(16);
    footballLuckyDipMapping.setTypeIds("442,95507,441");
    footballLuckyDipMapping.setSvgId("football2");
    footballLuckyDipMapping.setSortOrder(-2.00);

    LuckyDipMapping cricketLuckyDipMapping = new LuckyDipMapping();
    cricketLuckyDipMapping.setCategoryId("Cricket");
    cricketLuckyDipMapping.setCategory(10);
    cricketLuckyDipMapping.setTypeIds("157");
    cricketLuckyDipMapping.setSvgId("cricket");
    cricketLuckyDipMapping.setSortOrder(-1.00);

    List<LuckyDipMapping> luckyDipMappings = new ArrayList<>();
    luckyDipMappings.add(footballLuckyDipMapping);
    luckyDipMappings.add(cricketLuckyDipMapping);
    when(siteServerService.getEventToMarketForType(any())).thenReturn(event);
    List<LuckyDipCategoryData> luckyDipCategoryData =
        luckyDipModuleService.processLuckyDipData(luckyDipMappings);
    Assert.assertEquals(2, luckyDipCategoryData.size());
    Assert.assertEquals("Football", luckyDipCategoryData.get(0).getSportName());
    Assert.assertEquals("football2", luckyDipCategoryData.get(0).getSvgId());
    Assert.assertEquals(3, luckyDipCategoryData.get(0).getLuckyDipTypeData().size());
    Assert.assertEquals(
        5, luckyDipCategoryData.get(0).getLuckyDipTypeData().get(0).getLuckyDipMarketData().size());
    Assert.assertEquals("Cricket", luckyDipCategoryData.get(1).getSportName());
    Assert.assertEquals("cricket", luckyDipCategoryData.get(1).getSvgId());
    Assert.assertEquals(1, luckyDipCategoryData.get(1).getLuckyDipTypeData().size());
    Assert.assertEquals(
        1, luckyDipCategoryData.get(1).getLuckyDipTypeData().get(0).getLuckyDipMarketData().size());
  }

  @Test
  public void processModulesTestWithNullDisplayOrder() {
    Gson gson = new GsonBuilder().create();
    Type ssResponseType = new TypeToken<List<Children>>() {}.getType();
    Optional<List<Children>> response =
        Optional.of(gson.fromJson(TestUtils.getResourse("luckyDipEvents.json"), ssResponseType));
    Optional<List<Event>> event =
        response.map(
            resp -> resp.stream().map(Children::getEvent).filter(Objects::nonNull).toList());
    LuckyDipMapping footballLuckyDipMapping = new LuckyDipMapping();
    footballLuckyDipMapping.setCategoryId("Football");
    footballLuckyDipMapping.setCategory(16);
    footballLuckyDipMapping.setTypeIds("442,95507,441");
    footballLuckyDipMapping.setSvgId("football2");
    footballLuckyDipMapping.setSortOrder(-2.00);

    LuckyDipMapping cricketLuckyDipMapping = new LuckyDipMapping();
    cricketLuckyDipMapping.setCategoryId("Cricket");
    cricketLuckyDipMapping.setCategory(10);
    cricketLuckyDipMapping.setTypeIds("157");
    cricketLuckyDipMapping.setSvgId("cricket");
    cricketLuckyDipMapping.setSortOrder(-1.00);

    LuckyDipMapping rugbyLeagueLuckyDipMapping = new LuckyDipMapping();
    rugbyLeagueLuckyDipMapping.setCategoryId("Rugby League");
    rugbyLeagueLuckyDipMapping.setCategory(30);
    rugbyLeagueLuckyDipMapping.setTypeIds("1491");
    rugbyLeagueLuckyDipMapping.setSvgId("rugby");
    rugbyLeagueLuckyDipMapping.setSortOrder(null);

    List<LuckyDipMapping> luckyDipMappings = new ArrayList<>();
    luckyDipMappings.add(footballLuckyDipMapping);
    luckyDipMappings.add(rugbyLeagueLuckyDipMapping);
    luckyDipMappings.add(cricketLuckyDipMapping);
    when(siteServerService.getEventToMarketForType(any())).thenReturn(event);
    List<LuckyDipCategoryData> luckyDipCategoryData =
        luckyDipModuleService.processLuckyDipData(luckyDipMappings);
    Assert.assertEquals(3, luckyDipCategoryData.size());
    Assert.assertEquals("Football", luckyDipCategoryData.get(0).getSportName());
    Assert.assertEquals("football2", luckyDipCategoryData.get(0).getSvgId());
    Assert.assertEquals(3, luckyDipCategoryData.get(0).getLuckyDipTypeData().size());
    Assert.assertEquals(
        5, luckyDipCategoryData.get(0).getLuckyDipTypeData().get(0).getLuckyDipMarketData().size());
    Assert.assertEquals("Cricket", luckyDipCategoryData.get(1).getSportName());
    Assert.assertEquals("cricket", luckyDipCategoryData.get(1).getSvgId());
    Assert.assertEquals(1, luckyDipCategoryData.get(1).getLuckyDipTypeData().size());
    Assert.assertEquals(
        1, luckyDipCategoryData.get(1).getLuckyDipTypeData().get(0).getLuckyDipMarketData().size());
  }

  @Test
  public void processLuckyDipDataTestWithEmptyTypeId() {
    LuckyDipMapping footballLuckyDipMapping = new LuckyDipMapping();
    footballLuckyDipMapping.setCategoryId("Football");
    footballLuckyDipMapping.setCategory(16);
    footballLuckyDipMapping.setTypeIds(",");
    footballLuckyDipMapping.setSvgId("football2");
    footballLuckyDipMapping.setSortOrder(-2.00);

    List<LuckyDipMapping> luckyDipMappings = new ArrayList<>();
    luckyDipMappings.add(footballLuckyDipMapping);

    List<LuckyDipCategoryData> luckyDipCategoryData =
        luckyDipModuleService.processLuckyDipData(luckyDipMappings);
    Assert.assertEquals(0, luckyDipCategoryData.size());
  }
}
