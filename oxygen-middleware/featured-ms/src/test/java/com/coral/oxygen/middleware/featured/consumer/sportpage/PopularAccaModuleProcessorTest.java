package com.coral.oxygen.middleware.featured.consumer.sportpage;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.featured.exception.TrendingBetDataException;
import com.coral.oxygen.middleware.featured.service.PopularBetService;
import com.coral.oxygen.middleware.featured.utils.TestUtils;
import com.coral.oxygen.middleware.pojos.model.cms.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex;
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType;
import com.coral.oxygen.middleware.pojos.model.output.featured.PopularAccaModule;
import com.coral.oxygen.middleware.pojos.model.output.popular_bet.PopularAccaResponse;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class PopularAccaModuleProcessorTest {

  private PopularAccaModuleProcessor popularAccaModuleProcessor;

  private PopularBetService popularBetService;

  @BeforeEach
  public void setup() {
    popularBetService = mock(PopularBetService.class);
    popularAccaModuleProcessor = new PopularAccaModuleProcessor(popularBetService);
  }

  @Test
  void testProcessModules() {
    when(popularBetService.getPopularAccaForData(any())).thenReturn(popularBetsData());

    PopularAccaModule module =
        popularAccaModuleProcessor.processModule(createSportModule(), null, null);
    Assertions.assertNotNull(module);
  }

  @Test
  void testProcessModulesWithEmptyPositions() {
    when(popularBetService.getPopularAccaForData(any()))
        .thenReturn(PopularAccaResponse.builder().build());

    PopularAccaModule module =
        popularAccaModuleProcessor.processModule(createSportModule(), null, null);
    Assertions.assertNotNull(module);
  }

  @Test
  void processModulesForTrendingException() {
    when(popularBetService.getPopularAccaForData(any()))
        .thenThrow(new TrendingBetDataException(""));

    PopularAccaModule module =
        popularAccaModuleProcessor.processModule(createSportModule(), null, null);
    Assertions.assertNotNull(module);
  }

  @Test
  void testProcessModulesWithEmptyPageData() {
    SportPageModule sportPageModule = createSportModule();
    PopularAccaWidget widget = (PopularAccaWidget) sportPageModule.getPageData().get(0);
    widget.setData(null);
    Assertions.assertThrows(
        Exception.class,
        () -> popularAccaModuleProcessor.processModule(sportPageModule, null, null));
  }

  private PopularAccaResponse popularBetsData() {
    return TestUtils.deserializeWithGson(
        "trendinbBetResponse/response.json", PopularAccaResponse.class);
  }

  private SportPageModule createSportModule() {
    SportModule module =
        new SportModule(
            FeaturedRawIndex.PageType.sport,
            "123",
            0,
            0.0,
            true,
            "0",
            "title",
            "ladbrokes",
            ModuleType.POPULAR_ACCA,
            new ArrayList<>());
    List<SportPageModuleDataItem> widgetModule = createPopularAccaWwidget();
    return new SportPageModule(module, widgetModule);
  }

  private List<SportPageModuleDataItem> createPopularAccaWwidget() {
    PopularAccaWidget widget = new PopularAccaWidget();

    widget.setTitle("title");
    widget.setPageType(FeaturedRawIndex.PageType.sport);
    widget.setData(prepareWidgetData());
    List<SportPageModuleDataItem> list = new ArrayList<>();
    list.add(widget);
    return list;
  }

  private List<PopularAccaWidgetData> prepareWidgetData() {
    List<PopularAccaWidgetData> widgets = new ArrayList<>();
    widgets.add(createWidgetData("title-2", 2));
    widgets.add(createWidgetData("title-3", 3));
    widgets.add(createWidgetData("title-4", 4));
    widgets.add(createWidgetData("title-5", 5));

    return widgets;
  }

  private PopularAccaWidgetData createWidgetData(String title, int sortOrder) {
    PopularAccaWidgetData data = new PopularAccaWidgetData();
    data.setTitle(title);
    data.setSortOrder(sortOrder);
    return data;
  }
}
