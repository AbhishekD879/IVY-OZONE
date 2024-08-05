package com.coral.oxygen.middleware.featured.service;

import com.coral.oxygen.middleware.common.utils.Utils;
import com.coral.oxygen.middleware.featured.service.injector.FeaturedSiteServerService;
import com.coral.oxygen.middleware.pojos.model.cms.featured.LuckyDipMapping;
import com.coral.oxygen.middleware.pojos.model.output.featured.LuckyDipCategoryData;
import com.coral.oxygen.middleware.pojos.model.output.featured.LuckyDipMarketData;
import com.coral.oxygen.middleware.pojos.model.output.featured.LuckyDipTypeData;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import java.time.Duration;
import java.time.Instant;
import java.util.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.jetbrains.annotations.NotNull;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class LuckyDipModuleService {
  private final FeaturedSiteServerService siteServerService;

  public List<LuckyDipCategoryData> processLuckyDipData(List<LuckyDipMapping> luckyDipMappings) {
    Optional<List<Event>> events = getLuckyDipEvents(luckyDipMappings);
    List<Event> eventsList;
    List<LuckyDipMarketData> luckyDipModuleData;
    List<LuckyDipMarketData> luckyDipModuleDataResponse;
    if (events.isEmpty()) {
      log.info("LuckyDip events are empty: {}", true);
      return Collections.emptyList();
    }
    eventsList = events.get();

    List<String> luckyDipValidCategoryIds = new ArrayList<>();
    Map<Integer, String> svgMap = new HashMap<>();
    Map<Integer, Double> orderMap = new HashMap<>();
    List<Event> validEventsList =
        getValidEvents(eventsList, luckyDipMappings, luckyDipValidCategoryIds, svgMap, orderMap);
    luckyDipModuleData = processEventData(validEventsList);
    luckyDipModuleDataResponse = new ArrayList<>(luckyDipModuleData);

    List<LuckyDipCategoryData> luckyDipCategoryDataList =
        processAndFetchEventsByTypeAndCategories(luckyDipModuleDataResponse, svgMap, orderMap);
    luckyDipCategoryDataList.forEach(
        categoryData ->
            categoryData
                .getLuckyDipTypeData()
                .forEach(
                    typeData ->
                        typeData.setLuckyDipMarketData(
                            typeData.getLuckyDipMarketData().stream()
                                .sorted(
                                    Comparator.comparing(LuckyDipMarketData::getEventStartTime)
                                        .thenComparing(LuckyDipMarketData::getEventName)
                                        .thenComparing(LuckyDipMarketData::getMarketDisplayOrder))
                                .toList())));
    log.info("eventInfoByCategory {}", luckyDipCategoryDataList);
    return luckyDipCategoryDataList;
  }

  private Optional<List<Event>> getLuckyDipEvents(List<LuckyDipMapping> luckyDipMappings) {
    Instant startEventToMarketForType = Instant.now();
    List<String> typeIds =
        luckyDipMappings.stream()
            .map(LuckyDipMapping::getTypeIds)
            .flatMap(
                (String typeId) -> {
                  String[] parts = typeId.split(",");
                  return Arrays.stream(parts);
                })
            .toList();

    if (!typeIds.isEmpty()) {
      Optional<List<Event>> events = siteServerService.getEventToMarketForType(typeIds);
      Instant endEventToMarketForType = Instant.now();
      log.info(
          "duration time for processing SS getEventToMarketForType {}",
          Duration.between(startEventToMarketForType, endEventToMarketForType).toMillis());
      return events;
    }
    return Optional.empty();
  }

  @NotNull
  private List<Event> getValidEvents(
      List<Event> eventsList,
      List<LuckyDipMapping> luckyDipMappings,
      List<String> luckyDipValidCategoryIds,
      Map<Integer, String> svgMap,
      Map<Integer, Double> orderMap) {
    luckyDipMappings.forEach(
        (LuckyDipMapping mapping) -> {
          luckyDipValidCategoryIds.add(mapping.getCategoryId());
          svgMap.put(mapping.getCategory(), mapping.getSvgId());
          orderMap.put(mapping.getCategory(), mapping.getSortOrder());
        });
    List<String> luckyDipValidTypeIds = getLuckyDipValidTypeIds(luckyDipMappings);
    return eventsList.stream()
        .filter(event -> "A".equalsIgnoreCase(event.getEventStatusCode()))
        .filter(
            event ->
                luckyDipValidCategoryIds.contains(Utils.trimWithEmpty(event.getCategoryName()))
                    && luckyDipValidTypeIds.contains(event.getTypeId()))
        .toList();
  }

  private List<LuckyDipMarketData> processEventData(List<Event> events) {
    return events.stream()
        .map(
            (Event event) ->
                event.getMarkets().stream()
                    .filter(market -> market.getDrilldownTagNames().contains("MKTFLAG_LD"))
                    .filter(market -> "A".equalsIgnoreCase(market.getMarketStatusCode()))
                    .map(
                        (Market market) -> {
                          LuckyDipMarketData luckyDipMarketData = new LuckyDipMarketData();
                          luckyDipMarketData.setEventId(event.getId());
                          luckyDipMarketData.setMarketDescription(
                              Utils.trimWithEmpty(market.getName()));
                          luckyDipMarketData.setMarketId(market.getId());
                          luckyDipMarketData.setEventName(Utils.trimWithEmpty(event.getName()));
                          luckyDipMarketData.setTypeId(event.getTypeId());
                          luckyDipMarketData.setTypeName(Utils.trimWithEmpty(event.getTypeName()));
                          luckyDipMarketData.setCategoryName(
                              Utils.trimWithEmpty(event.getCategoryName()));
                          luckyDipMarketData.setCategoryId(Integer.parseInt(event.getCategoryId()));
                          luckyDipMarketData.setEventStatus(event.getEventStatusCode());
                          luckyDipMarketData.setMarketStatus(market.getMarketStatusCode());
                          luckyDipMarketData.setEventStartTime(event.getStartTime());
                          luckyDipMarketData.setEventDisplayOrder(event.getDisplayOrder());
                          luckyDipMarketData.setMarketDisplayOrder(market.getDisplayOrder());
                          return luckyDipMarketData;
                        })
                    .toList())
        .flatMap(List::stream)
        .toList();
  }

  @NotNull
  private static List<String> getLuckyDipValidTypeIds(List<LuckyDipMapping> luckyDipMappings) {
    List<String> luckyDipValidTypeIds =
        luckyDipMappings.stream()
            .map(LuckyDipMapping::getTypeIds)
            .map(s -> s.split(","))
            .map(Arrays::asList)
            .flatMap(Collection::stream)
            .toList();
    log.info("Lucky Dip TypeIds {}", luckyDipValidTypeIds);
    return luckyDipValidTypeIds;
  }

  private List<LuckyDipCategoryData> processAndFetchEventsByTypeAndCategories(
      List<LuckyDipMarketData> luckyDipModuleDataResponse,
      Map<Integer, String> svgMap,
      Map<Integer, Double> orderMap) {
    Instant start = Instant.now();
    Map<String, LuckyDipCategoryData> dataByCategory = new HashMap<>();
    List<String> dataList = new ArrayList<>();

    luckyDipModuleDataResponse.forEach(
        (LuckyDipMarketData luckyDipMarketData) -> {
          if (dataList.contains(luckyDipMarketData.getCategoryName())) {
            if (dataList.contains(luckyDipMarketData.getTypeName())) {
              dataByCategory
                  .get(luckyDipMarketData.getCategoryName())
                  .getLuckyDipTypeData()
                  .stream()
                  .filter(
                      luckyDipTypeData ->
                          luckyDipTypeData.getTypeName().equals(luckyDipMarketData.getTypeName()))
                  .findFirst()
                  .ifPresent(
                      luckyDipTypeData ->
                          luckyDipTypeData.getLuckyDipMarketData().add(luckyDipMarketData));
            } else {
              LuckyDipTypeData luckyDipTypeData = new LuckyDipTypeData();
              luckyDipTypeData.setTypeName(luckyDipMarketData.getTypeName());
              List<LuckyDipMarketData> luckyDipMarketDataList = new ArrayList<>();
              luckyDipMarketDataList.add(luckyDipMarketData);
              luckyDipTypeData.setLuckyDipMarketData(luckyDipMarketDataList);
              dataByCategory
                  .get(luckyDipMarketData.getCategoryName())
                  .getLuckyDipTypeData()
                  .add(luckyDipTypeData);
              dataList.add(luckyDipMarketData.getTypeName());
            }
          } else {
            LuckyDipTypeData luckyDipTypeData = new LuckyDipTypeData();
            luckyDipTypeData.setTypeName(luckyDipMarketData.getTypeName());
            List<LuckyDipMarketData> luckyDipMarketDataList = new ArrayList<>();
            luckyDipMarketDataList.add(luckyDipMarketData);
            luckyDipTypeData.setLuckyDipMarketData(luckyDipMarketDataList);
            List<LuckyDipTypeData> luckyDipTypeDataList = new ArrayList<>();
            luckyDipTypeDataList.add(luckyDipTypeData);
            LuckyDipCategoryData luckyDipCategoryData = new LuckyDipCategoryData();
            luckyDipCategoryData.setLuckyDipTypeData(luckyDipTypeDataList);
            luckyDipCategoryData.setSvgId(svgMap.get(luckyDipMarketData.getCategoryId()));
            luckyDipCategoryData.setDisplayOrder(orderMap.get(luckyDipMarketData.getCategoryId()));
            luckyDipCategoryData.setSportName(luckyDipMarketData.getCategoryName());
            dataByCategory.put(luckyDipMarketData.getCategoryName(), luckyDipCategoryData);
            dataList.add(luckyDipMarketData.getCategoryName());
            dataList.add(luckyDipMarketData.getTypeName());
          }
        });

    Instant end = Instant.now();
    log.info(
        "processAndFetchEventsByTypeAndCategories time {}",
        Duration.between(start, end).toMillis());
    return dataByCategory.values().stream()
        .sorted(
            Comparator.nullsLast(
                Comparator.comparingDouble(
                    (LuckyDipCategoryData d) ->
                        d.getDisplayOrder() == null ? Double.MAX_VALUE : d.getDisplayOrder())))
        .toList();
  }
}
