package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.coral.oxygen.middleware.featured.service.PopularBetService;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.popular_bet.PopularAccaResponse;
import com.coral.oxygen.middleware.pojos.model.output.popular_bet.TrendingPosition;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Slf4j
@Service
public class PopularAccaModuleProcessor implements ModuleConsumer<PopularAccaModule> {

  private final PopularBetService popularBetService;

  @Autowired
  public PopularAccaModuleProcessor(PopularBetService popularBetService) {
    this.popularBetService = popularBetService;
  }

  @Override
  public PopularAccaModule processModule(
      SportPageModule sportPageModule,
      CmsSystemConfig cmsSystemConfig,
      Set<Long> excludedEventIds) {
    log.info("popular acca module processing started");
    PopularAccaModule module = new PopularAccaModule();
    SportModule sportModule = sportPageModule.getSportModule();

    sportPageModule.getPageData().stream()
        .filter(PopularAccaWidget.class::isInstance)
        .map(PopularAccaWidget.class::cast)
        .forEach(widget -> populatePopularAccaModule(module, sportModule, widget));
    return module;
  }

  private List<PopularAccaModuleData> toPopularAccaModuleData(List<PopularAccaWidgetData> pageData)
      throws ExecutionException, InterruptedException {

    CompletableFuture[] completableFutures =
        pageData.stream()
            .map(data -> CompletableFuture.supplyAsync(() -> populatePopularAccaModuleData(data)))
            .toArray(CompletableFuture[]::new);
    return CompletableFuture.allOf(completableFutures)
        .thenApply(
            nothing ->
                Arrays.asList(completableFutures).stream()
                    .parallel()
                    .map(CompletableFuture::join)
                    .map(PopularAccaModuleData.class::cast)
                    .filter(data -> !CollectionUtils.isEmpty(data.getPositions()))
                    .sorted(Comparator.comparing(PopularAccaModuleData::getDisplayOrder))
                    .toList())
        .get();
  }

  @SneakyThrows
  protected void populatePopularAccaModule(
      PopularAccaModule module, SportModule sportModule, PopularAccaWidget popularAccaWidget) {
    module.setId(sportModule.getId());
    module.setPageType(sportModule.getPageType());
    module.setSportId(sportModule.getSportId());
    module.setTitle(popularAccaWidget.getTitle());
    module.setCardCta(popularAccaWidget.getCardCta());
    module.setCardCtaAfterAdd(popularAccaWidget.getCardCtaAfterAdd());
    module.setData(toPopularAccaModuleData(popularAccaWidget.getData()));
  }

  private PopularAccaModuleData populatePopularAccaModuleData(PopularAccaWidgetData widgetData) {
    PopularAccaModuleData moduleData = new PopularAccaModuleData();
    try {
      PopularAccaResponse dto = popularBetService.getPopularAccaForData(widgetData);
      if (dto.getPositions() != null) {
        dto.getPositions().forEach(this::mapMetaData);
      }
      moduleData.setId(widgetData.getId());
      moduleData.setTitle(widgetData.getTitle());
      moduleData.setSubTitle(widgetData.getSubTitle());
      moduleData.setSvgId(widgetData.getSvgId());
      moduleData.setDisplayOrder(widgetData.getSortOrder());
      moduleData.setNumberOfTimeBackedLabel(widgetData.getNumberOfTimeBackedLabel());
      moduleData.setNumberOfTimeBackedThreshold(widgetData.getNumberOfTimeBackedThreshold());
      moduleData.setPositions(dto.getPositions());
    } catch (Exception ex) {
      log.error("trending bets ms call failed with reason ", ex);
    }
    return moduleData;
  }

  private PopularBetModuleData mapMetaData(TrendingPosition position) {
    PopularBetModuleData data = position.getEvent();
    data.setNBets(position.getNBets());
    data.setRank(position.getRank());
    data.setPreviousRank(position.getPreviousRank());
    data.setPosition(position.getPosition());
    return data;
  }
}
