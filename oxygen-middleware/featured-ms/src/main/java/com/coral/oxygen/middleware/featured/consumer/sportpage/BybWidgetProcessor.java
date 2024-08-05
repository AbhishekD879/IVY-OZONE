package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.coral.oxygen.middleware.common.service.featured.IdsCollector;
import com.coral.oxygen.middleware.featured.service.injector.EventDataInjector;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.featured.BybWidgetModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.BybWidgetModuleData;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Slf4j
@Service
public class BybWidgetProcessor implements ModuleConsumer<BybWidgetModule> {
  private final EventDataInjector eventDataInjector;

  public BybWidgetProcessor(EventDataInjector eventDataInjector) {
    this.eventDataInjector = eventDataInjector;
  }

  @Override
  public BybWidgetModule processModule(
      SportPageModule sportPageModule,
      CmsSystemConfig cmsSystemConfig,
      Set<Long> excludedEventIds) {
    SportModule sportModule = sportPageModule.getSportModule();
    BybWidgetModule module = populateModule(sportPageModule, sportModule);

    IdsCollector idsCollector = new IdsCollector(Collections.emptyList());
    idsCollector.setMarketIds(
        module.getData().stream()
            .map(BybWidgetModuleData::getMarketId)
            .map(String::valueOf)
            .collect(Collectors.toSet()));

    eventDataInjector.injectData(module.getData(), idsCollector);
    module.setData(updateMarketAndSortByOrder(module));
    return module;
  }

  private List<BybWidgetModuleData> updateMarketAndSortByOrder(BybWidgetModule module) {
    return module.getData().stream()
        .sorted(Comparator.comparing(BybWidgetModuleData::getDisplayOrder))
        .map(
            (BybWidgetModuleData data) -> {
              data.setMarkets(
                  data.getPrimaryMarkets().stream()
                      .filter(
                          prMarket -> String.valueOf(data.getMarketId()).equals(prMarket.getId()))
                      .toList());
              return data;
            })
        .filter(data -> !CollectionUtils.isEmpty(data.getMarkets()))
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private BybWidgetModule populateModule(SportPageModule sportPageModule, SportModule sportModule) {
    BybWidgetModule module = new BybWidgetModule();

    sportPageModule.getPageData().stream()
        .filter(BybWidget.class::isInstance)
        .map(BybWidget.class::cast)
        .map(
            (BybWidget bybWidget) -> {
              module.setId(sportModule.getId());
              module.setTitle(bybWidget.getTitle());
              module.setSportId(sportModule.getSportId());
              module.setDisplayOrder(sportModule.getSortOrderOrDefault(null));
              module.setPageType(sportModule.getPageType());
              module.setShowAll(bybWidget.isShowAll());
              module.setMarketCardVisibleSelections(bybWidget.getMarketCardVisibleSelections());
              return bybWidget.getData();
            })
        .forEach(bybWidget -> module.setData(toBybWidgetData(bybWidget)));
    return module;
  }

  private List<BybWidgetModuleData> toBybWidgetData(List<BybWidgetData> pageData) {

    return pageData.stream()
        .filter(BybWidgetData.class::isInstance)
        .map(BybWidgetData.class::cast)
        .map(this::createEventData)
        .collect(Collectors.toCollection(ArrayList::new));
  }

  protected BybWidgetModuleData createEventData(BybWidgetData bybWidgetData) {
    BybWidgetModuleData data = new BybWidgetModuleData();
    data.setMarketId(Long.valueOf(bybWidgetData.getMarketId()));
    data.setDisplayOrder(bybWidgetData.getSortOrder());
    data.setTitle(bybWidgetData.getTitle());
    data.setId(Long.valueOf(bybWidgetData.getEventId()));
    return data;
  }
}
