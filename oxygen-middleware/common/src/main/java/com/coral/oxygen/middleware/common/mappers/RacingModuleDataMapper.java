package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.InternationalToteRaceData;
import com.coral.oxygen.middleware.pojos.model.output.RacingEventData;
import com.coral.oxygen.middleware.pojos.model.output.RacingEventMarket;
import com.coral.oxygen.middleware.pojos.model.output.VirtualRaceModuleData;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.ReferenceEachWayTerms;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

@Component
public class RacingModuleDataMapper {

  public InternationalToteRaceData mapInternationalToteData(
      Event event, String externalKeyType, String externalKeyEventId) {
    InternationalToteRaceData toteEvent = new InternationalToteRaceData();
    BeanUtils.copyProperties(event, toteEvent);
    toteEvent.setExternalKeys(Collections.singletonMap(externalKeyType, externalKeyEventId));
    toteEvent.setResulted(event.getIsResulted());
    toteEvent.setStarted(event.getIsStarted());
    toteEvent.setLiveNowEvent(event.getIsLiveNowEvent());
    toteEvent.setEffectiveGpStartTime(event.getEffectiveGpStartTime());
    return toteEvent;
  }

  public VirtualRaceModuleData mapVirtualCarouselData(Event event) {
    VirtualRaceModuleData moduleData = new VirtualRaceModuleData();
    moduleData.setId(event.getId());
    moduleData.setName(event.getName());
    moduleData.setStartTime(event.getStartTime());
    moduleData.setClassId(event.getClassId());
    moduleData.setEffectiveGpStartTime(event.getEffectiveGpStartTime());
    return moduleData;
  }

  public RacingEventData mapRacingEventData(Event event, List<String> poolTypes) {
    RacingEventData eventData = new RacingEventData();
    eventData.setId(event.getId());
    eventData.setName(event.getName());
    eventData.setCategoryId(event.getCategoryId());
    eventData.setCategoryName(event.getCategoryName());
    eventData.setClassId(event.getClassId());
    eventData.setClassName(event.getClassName());
    eventData.setTypeName(event.getTypeName());
    eventData.setStartTime(event.getStartTime());
    eventData.setCashoutAvail(event.getCashoutAvail());
    eventData.setDisplayOrder(event.getDisplayOrder());
    eventData.setClassDisplayOrder(event.getClassDisplayOrder());
    eventData.setTypeDisplayOrder(event.getTypeDisplayOrder());
    eventData.setIsStarted(event.getIsStarted());
    eventData.setIsLiveNowEvent(event.getIsLiveNowEvent());
    eventData.setIsFinished(event.getIsFinished());
    eventData.setIsResulted(event.getIsResulted());
    eventData.setRawIsOffCode(event.getRawIsOffCode());
    eventData.setTypeFlagCodes(event.getTypeFlagCodes());
    eventData.setDrilldownTagNames(event.getDrilldownTagNames());
    eventData.setPoolTypes(poolTypes);
    eventData.setEventStatusCode(event.getEventStatusCode());
    eventData.setLiveServChannels(event.getLiveServChannels());
    eventData.setLiveServChildrenChannels(event.getLiveServChildrenChannels());
    eventData.setMarkets(
        event.getMarkets().stream()
            .filter(m -> !CollectionUtils.isEmpty(m.getOutcomes()))
            .map(this::mapRacingEventMarket)
            .collect(Collectors.toCollection(ArrayList::new)));
    eventData.setEffectiveGpStartTime(event.getEffectiveGpStartTime());
    return eventData;
  }

  private RacingEventMarket mapRacingEventMarket(Market market) {
    RacingEventMarket racingMarket = new RacingEventMarket();
    racingMarket.setId(market.getId());
    racingMarket.setName(market.getName());
    racingMarket.setDrilldownTagNames(market.getDrilldownTagNames());
    racingMarket.setEachWayFactorDen(market.getEachWayFactorDen());
    racingMarket.setEachWayFactorNum(market.getEachWayFactorNum());
    racingMarket.setEachWayPlaces(market.getEachWayPlaces());
    racingMarket.setIsEachWayAvailable(market.getIsEachWayAvailable());
    racingMarket.setIsSpAvailable(market.getIsSpAvailable());
    racingMarket.setIsLpAvailable(market.getIsLpAvailable());
    racingMarket.setIsGpAvailable(market.getIsGpAvailable());
    racingMarket.setIsResulted(market.getIsResulted());
    racingMarket.setMarketStatusCode(market.getMarketStatusCode());
    racingMarket.setLiveServChannels(market.getLiveServChannels());
    racingMarket.setLiveServChildrenChannels(market.getLiveServChildrenChannels());
    racingMarket.setReferenceEachWayTerms(
        market.getReferenceEachWayTerms().stream()
            .map(this::mapReferenceEachWayTerms)
            .collect(Collectors.toCollection(ArrayList::new)));
    return racingMarket;
  }

  // mapping ReferenceEachWayTerms for extraplacesignposting
  private com.coral.oxygen.middleware.pojos.model.output.ReferenceEachWayTerms
      mapReferenceEachWayTerms(ReferenceEachWayTerms referenceEachWayTerms) {
    com.coral.oxygen.middleware.pojos.model.output.ReferenceEachWayTerms referenceEachWayTerms1 =
        new com.coral.oxygen.middleware.pojos.model.output.ReferenceEachWayTerms();
    referenceEachWayTerms1.setId(referenceEachWayTerms.getId());
    referenceEachWayTerms1.setPlaces(referenceEachWayTerms.getPlaces());
    return referenceEachWayTerms1;
  }
}
