package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class SimpleEventMapper implements EventMapper {

  private final MarketMapper marketMapper;

  private static final String EVFLAG_BB = "EVFLAG_BB";

  public SimpleEventMapper(MarketMapper marketMapper) {
    this.marketMapper = marketMapper;
  }

  @Override
  public EventsModuleData map(EventsModuleData result, Event event) {
    result.setId(Long.valueOf(event.getId()));
    result.setName(event.getName());
    result.setNameOverride(result.getNameOverride());
    result.setEventSortCode(event.getEventSortCode());
    result.setStartTime(event.getStartTime());
    result.setLiveServChannels(event.getLiveServChannels());
    result.setLiveServChildrenChannels(event.getLiveServChildrenChannels());
    result.setLiveServLastMsgId(event.getLiveServLastMsgId());
    result.setCategoryId(event.getCategoryId());
    result.setCategoryCode(event.getCategoryCode());
    result.setCategoryName(event.getCategoryName());
    result.setClassId(event.getClassId());
    result.setClassName(event.getClassName());
    result.setTypeName(event.getTypeName());
    result.setCashoutAvail(event.getCashoutAvail());
    result.setDisplayOrder(
        result.getType().equals("SurfaceBetModuleData") || result.getType().equals("BybWidgetData")
            ? result.getDisplayOrder()
            : event.getDisplayOrder());
    result.setStarted(event.getIsStarted());
    result.setFinished(event.getIsFinished());
    result.setResponseCreationTime(event.getResponseCreationTime());
    result.setDrilldownTagNames(event.getDrilldownTagNames());
    result.setTypeId(event.getTypeId());
    result.setEventStatusCode(event.getEventStatusCode());
    result.setTypeFlagCodes(event.getTypeFlagCodes());
    mapMarkets(result, event);
    result.setTeamExtIds(event.getTeamExtIds());
    result.setAwayTeamExtIds(event.getAwayTeamExtIds());
    result.setHomeTeamExtIds(event.getHomeTeamExtIds());
    result.setEffectiveGpStartTime(event.getEffectiveGpStartTime());
    result.setEventFlagCodes(event.getEventFlagCodes());
    if (Objects.nonNull(event.getExtIds()) && getDrillDownBBFlag(event)) {
      result.setBybAvailableEvent(true);
    }
    if (Objects.nonNull(event.getExtIds())) {
      List<String> extId = Arrays.asList(event.getExtIds().split(","));
      result.setBwinId(extId.get(1));
    }
    return result;
  }

  private static boolean getDrillDownBBFlag(Event event) {
    return Objects.nonNull(event.getDrilldownTagNames())
        && event.getDrilldownTagNames().contains(EVFLAG_BB);
  }

  protected void mapMarkets(EventsModuleData result, Event event) {
    result.setMarkets(
        event.getMarkets().parallelStream()
            .filter(Objects::nonNull)
            .map(m -> this.mapMarket(event, m))
            .collect(Collectors.toCollection(ArrayList::new)));
  }

  protected OutputMarket mapMarket(Event event, Market market) {
    return marketMapper.map(event, market);
  }
}
