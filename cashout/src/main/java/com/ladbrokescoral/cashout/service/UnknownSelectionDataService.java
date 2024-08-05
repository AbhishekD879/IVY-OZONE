package com.ladbrokescoral.cashout.service;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.egalacoral.spark.siteserver.model.Price;
import com.ladbrokescoral.cashout.model.context.SelectionPrice;
import com.ladbrokescoral.cashout.repository.EntityStatus;
import com.ladbrokescoral.cashout.repository.ReactiveRepository;
import com.ladbrokescoral.cashout.repository.SelectionHierarchyStatusRepository;
import com.ladbrokescoral.cashout.service.UnknownSelectionData.UnknownEntities;
import java.math.BigInteger;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import java.util.function.BiConsumer;
import java.util.logging.Level;
import java.util.stream.Collectors;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.publisher.SignalType;
import reactor.core.scheduler.Scheduler;

public class UnknownSelectionDataService {

  private final ReactiveRepository<SelectionPrice> priceRepo;
  private final SelectionHierarchyStatusRepository statusRepository;
  private final SiteServerApi siteServerApi;
  private final UnknownSelectionData unknownSelectionData;
  private final Scheduler schedulerForSiteServeResolver;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  public UnknownSelectionDataService(
      ReactiveRepository<SelectionPrice> priceRepo,
      SelectionHierarchyStatusRepository statusRepository,
      SiteServerApi siteServerApi,
      UnknownSelectionData unknownSelectionData,
      Scheduler schedulerForSiteServeResolver) {
    this.priceRepo = priceRepo;
    this.statusRepository = statusRepository;
    this.siteServerApi = siteServerApi;
    this.unknownSelectionData = unknownSelectionData;
    this.schedulerForSiteServeResolver = schedulerForSiteServeResolver;
  }

  public UnknownEntities getUnknownEntitiesOnly() {
    return unknownSelectionData.getUnknownEntitiesOnly();
  }

  public Set<BigInteger> getMarketIdsOfUnknownItems() {
    return unknownSelectionData.getMarketIdsOfUnknownItems();
  }

  public void updatePrices(List<SelectionPrice> prices) {
    if (prices != null && !prices.isEmpty()) {
      prices.stream()
          .filter(Objects::nonNull)
          .forEach(
              p ->
                  unknownSelectionData.updatePrice(
                      new BigInteger(p.getOutcomeId()),
                      Integer.parseInt(p.getPriceNum()),
                      Integer.parseInt(p.getPriceDen())));
    }
  }

  public void resolveUnknowns() {
    UnknownEntities unknownEntitiesOnly = getUnknownEntitiesOnly();

    String unknownEntitiesHashcode = String.valueOf(unknownEntitiesOnly.hashCode());
    ASYNC_LOGGER.info(
        "Trying to resolve {} [hashcode={}]", unknownEntitiesOnly, unknownEntitiesHashcode);

    Mono<List<EntityStatus>> eventStatusesMono =
        statusRepository
            .fetchEventStatuses(unknownEntitiesOnly.getEventIds())
            .log("eventStatuses#" + unknownEntitiesHashcode, Level.INFO, SignalType.ON_NEXT)
            .doOnNext(ids -> resolveStatuses(ids, unknownSelectionData::updateEventStatus));

    Mono<List<EntityStatus>> marketStatusesMono =
        statusRepository
            .fetchMarketStatuses(unknownEntitiesOnly.getMarketIds())
            .log("marketStatuses#" + unknownEntitiesHashcode, Level.INFO, SignalType.ON_NEXT)
            .doOnNext(ids -> resolveStatuses(ids, unknownSelectionData::updateMarketStatus));

    Mono<List<EntityStatus>> selectionStatusesMono =
        statusRepository
            .fetchSelectionStatuses(unknownEntitiesOnly.getSelectionIds())
            .log("selectionStatuses#" + unknownEntitiesHashcode, Level.INFO, SignalType.ON_NEXT)
            .doOnNext(ids -> resolveStatuses(ids, unknownSelectionData::updateSelectionStatus));

    Mono<List<SelectionPrice>> pricesMono =
        priceRepo
            .multiGet(toStringSet(unknownEntitiesOnly.getSelectionIds()))
            .log("prices#" + unknownEntitiesHashcode, Level.INFO, SignalType.ON_NEXT)
            .doOnNext(this::updatePrices);

    // we need to know it's completion only, so type info not needed.
    Flux<Object> statusesAndPricesResolveFlux =
        eventStatusesMono
            .mergeWith(marketStatusesMono)
            .mergeWith(selectionStatusesMono)
            .map(e -> (Object) e) // so that we can merge with different type of mono
            .mergeWith(pricesMono);

    statusesAndPricesResolveFlux
        .publishOn(schedulerForSiteServeResolver)
        .doFinally(sig -> resolveWithSiteServer())
        .subscribe();
  }

  private Collection<String> toStringSet(Set<BigInteger> selectionIds) {
    return selectionIds.stream().map(String::valueOf).collect(Collectors.toSet());
  }

  private boolean isActive(String eventStatusCode) {
    return "A".equalsIgnoreCase(eventStatusCode);
  }

  private List<Event> fetchEventsByMarketIds(Set<BigInteger> marketIdsOfUnknownItems) {
    return siteServerApi
        .getWholeEventToOutcomeForMarket(
            marketIdsOfUnknownItems.stream().map(String::valueOf).collect(Collectors.toList()),
            true)
        .orElseGet(Collections::emptyList);
  }

  private void resolveStatuses(
      List<EntityStatus> entityStatuses, BiConsumer<BigInteger, Boolean> statusUpdater) {
    if (entityStatuses != null) {
      entityStatuses.stream()
          .filter(Objects::nonNull)
          .forEach(st -> statusUpdater.accept(st.getEntityId(), st.isActive()));
    }
  }

  private void resolveWithSiteServer() {
    Set<BigInteger> marketIdsOfUnknownItems = getMarketIdsOfUnknownItems();
    List<Event> events = fetchEventsByMarketIds(marketIdsOfUnknownItems);

    for (Event event : events) {
      BigInteger eventId = new BigInteger(event.getId());
      boolean eventActive = isActive(event.getEventStatusCode());
      unknownSelectionData.updateEventStatus(eventId, eventActive);
      statusRepository.updateEventStatus(new EntityStatus(eventId, eventActive));

      for (Market market : event.getMarkets()) {
        BigInteger marketId = new BigInteger(market.getId());
        boolean marketActive = isActive(market.getMarketStatusCode());

        unknownSelectionData.updateMarketStatus(marketId, marketActive);
        statusRepository.updateMarketStatus(new EntityStatus(marketId, marketActive));

        for (Outcome outcome : market.getOutcomes()) {
          BigInteger selectionId = new BigInteger(outcome.getId());
          boolean selectionActive = isActive(outcome.getOutcomeStatusCode());

          unknownSelectionData.updateSelectionStatus(selectionId, selectionActive);
          getLpPrice(outcome)
              .ifPresent(
                  p -> {
                    unknownSelectionData.updatePrice(selectionId, p.getPriceNum(), p.getPriceDen());
                    priceRepo
                        .save(
                            SelectionPrice.builder()
                                .outcomeId(String.valueOf(selectionId))
                                .priceNum(String.valueOf(p.getPriceNum()))
                                .priceDen(String.valueOf(p.getPriceDen()))
                                .build())
                        .subscribe();
                  });
          statusRepository.updateSelectionStatus(new EntityStatus(selectionId, selectionActive));
        }
      }
    }
  }

  private Optional<Price> getLpPrice(Outcome outcome) {
    return outcome.getPrices().stream().filter(p -> "LP".equals(p.getPriceType())).findFirst();
  }
}
