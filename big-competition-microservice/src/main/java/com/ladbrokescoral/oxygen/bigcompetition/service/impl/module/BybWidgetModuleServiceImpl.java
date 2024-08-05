package com.ladbrokescoral.oxygen.bigcompetition.service.impl.module;

import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.BybWidgetData;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.BybWidgetModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.EventDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.MarketDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.SiteServeEventDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.module.BybWidgetModuleDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.service.BybWidgetModuleService;
import com.ladbrokescoral.oxygen.bigcompetition.service.CmsApiService;
import com.ladbrokescoral.oxygen.bigcompetition.service.SiteServeApiService;
import com.ladbrokescoral.oxygen.cms.client.model.BybWidgetDataDto;
import com.ladbrokescoral.oxygen.cms.client.model.BybWidgetDto;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import java.time.Instant;
import java.util.AbstractMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;
import org.jetbrains.annotations.NotNull;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Service
public class BybWidgetModuleServiceImpl implements BybWidgetModuleService {

  private final SiteServeApiService siteServeApiService;

  private final CmsApiService cmsApiService;

  @Value("${cms.brand}")
  private final String brand;

  @Autowired
  public BybWidgetModuleServiceImpl(
      SiteServeApiService siteServeApiService,
      CmsApiService cmsApiService,
      @Value("${cms.brand}") String brand) {
    this.siteServeApiService = siteServeApiService;
    this.cmsApiService = cmsApiService;
    this.brand = brand;
  }

  @Override
  public BybWidgetModuleDto process(CompetitionModule module) {
    BybWidgetModuleDto bybWidgetModuleDto = BybWidgetModuleDtoMapper.INSTANCE.toDto(module);

    Optional<BybWidgetDto> bybWidget = cmsApiService.getBybWidget(brand);

    bybWidget
        .map(
            (BybWidgetDto b) -> {
              bybWidgetModuleDto.setTitle(b.getTitle());
              bybWidgetModuleDto.setShowAll(b.isShowAll());
              bybWidgetModuleDto.setMarketCardVisibleSelections(b.getMarketCardVisibleSelections());
              return b.getData();
            })
        .ifPresent(data -> populateModule(bybWidgetModuleDto, data));

    return bybWidgetModuleDto;
  }

  private void populateModule(BybWidgetModuleDto bybWidgetModuleDto, List<BybWidgetDataDto> data) {
    Instant now = Instant.now();
    List<BybWidgetDataDto> activeData =
        data.stream().filter(d -> !d.getDisplayFrom().isAfter(now)).toList();
    List<String> marketIds = activeData.stream().map(BybWidgetDataDto::getMarketId).toList();
    this.siteServeApiService
        .getEventToOutcomeForMarkets(marketIds)
        .ifPresent(events -> populateWidgetData(bybWidgetModuleDto, activeData, events));
  }

  private void populateWidgetData(
      BybWidgetModuleDto bybWidgetModuleDto, List<BybWidgetDataDto> data, List<Event> events) {
    Map<String, Event> eventsMap =
        events.stream()
            .flatMap(
                event ->
                    event.getMarkets().stream()
                        .map(
                            (Market market) ->
                                new AbstractMap.SimpleEntry<>(market.getId(), event)))
            .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));

    List<BybWidgetData> widgetData =
        data.stream()
            .filter(dto -> eventsMap.containsKey(dto.getMarketId()))
            .map(
                (BybWidgetDataDto dto) ->
                    convertBybWidgetData(dto, eventsMap.get(dto.getMarketId())))
            .filter(d -> !CollectionUtils.isEmpty(d.getEvent().getMarkets()))
            .toList();

    bybWidgetModuleDto.setData(widgetData);
  }

  @NotNull
  private BybWidgetData convertBybWidgetData(BybWidgetDataDto dto, Event event) {
    BybWidgetData bybWidgetData = BybWidgetModuleDtoMapper.INSTANCE.toDto(dto);
    EventDto eventDto = SiteServeEventDtoMapper.INSTANCE.toDto(event);
    List<MarketDto> otherMarkets =
        eventDto.getMarkets().stream()
            .filter(m -> !m.getId().equals(bybWidgetData.getMarketId()) || !isValidMarket(event, m))
            .toList();
    eventDto.getMarkets().removeAll(otherMarkets);
    bybWidgetData.setEvent(eventDto);
    return bybWidgetData;
  }

  private boolean isValidMarket(Event event, MarketDto market) {
    return !Boolean.TRUE.equals(event.getIsLiveNowEvent())
        || Boolean.TRUE.equals(market.getIsMarketBetInRun());
  }
}
