package com.ladbrokescoral.cashout.service;

import com.ladbrokescoral.cashout.model.context.IndexedSportsData;
import java.math.BigInteger;
import java.util.Collection;
import java.util.HashSet;
import java.util.Set;
import java.util.stream.Collectors;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.ToString;

public class UnknownSelectionData {

  private final IndexedSportsData indexedSportsData;

  private UnknownSelectionData(IndexedSportsData indexedSportsData) {
    this.indexedSportsData = indexedSportsData;
  }

  public static UnknownSelectionData create(IndexedSportsData indexedSportsData) {
    return new UnknownSelectionData(indexedSportsData);
  }

  public UnknownEntities getUnknownEntitiesOnly() {
    return collectUnknownEntities(getWithUnknownStatusesOrPrice());
  }

  public Set<BigInteger> getMarketIdsOfUnknownItems() {
    return getWithUnknownStatusesOrPrice().stream()
        .map(SelectionData::getMarketId)
        .collect(Collectors.toSet());
  }

  private Set<SelectionData> getWithUnknownStatusesOrPrice() {
    return this.indexedSportsData.getAllSelectionData().stream()
        .filter(SelectionData::hasUnknownStatusOrLpPrice)
        .collect(Collectors.toSet());
  }

  public void updateEventStatus(BigInteger eventId, boolean eventActive) {
    indexedSportsData
        .getSelectionDataByEventId(eventId)
        .forEach(sd -> sd.changeEventStatus(eventActive));
  }

  public void updateMarketStatus(BigInteger marketId, boolean marketActive) {
    indexedSportsData
        .getSelectionDataByMarketId(marketId)
        .forEach(sd -> sd.changeMarketStatus(marketActive));
  }

  public void updateSelectionStatus(BigInteger selectionId, boolean selectionActive) {
    indexedSportsData
        .getSelectionDataBySelectionId(selectionId)
        .ifPresent(sd -> sd.changeSelectionStatus(selectionActive));
  }

  private UnknownEntities collectUnknownEntities(
      Collection<SelectionData> selectionDataCollection) {
    return selectionDataCollection.stream()
        .reduce(
            new UnknownEntities(),
            (ue, s) -> {
              if (s.getEventActive() == null) {
                ue.addEventId(s.getEventId());
              }
              if (s.getMarketActive() == null) {
                ue.addMarketId(s.getMarketId());
              }
              if (s.getSelectionActive() == null || !s.getLpPrice().isPresent()) {
                ue.addSelectionId(s.getSelectionId());
              }
              return ue;
            },
            (u1, u2) -> {
              UnknownEntities combined = new UnknownEntities();
              combined.addAllFrom(u1);
              combined.addAllFrom(u2);
              return combined;
            });
  }

  public void updatePrice(BigInteger selectionId, int priceNum, int priceDen) {
    this.indexedSportsData
        .getSelectionDataBySelectionId(selectionId)
        .ifPresent(sd -> sd.changeLpPrice(priceNum, priceDen));
  }

  @Getter
  @ToString
  @EqualsAndHashCode
  static class UnknownEntities {

    private final Set<BigInteger> eventIds = new HashSet<>();
    private final Set<BigInteger> marketIds = new HashSet<>();
    private final Set<BigInteger> selectionIds = new HashSet<>();

    void addEventId(BigInteger eventId) {
      this.eventIds.add(eventId);
    }

    void addMarketId(BigInteger marketId) {
      this.marketIds.add(marketId);
    }

    void addSelectionId(BigInteger selectionId) {
      this.selectionIds.add(selectionId);
    }

    public void addAllFrom(UnknownEntities otherUnknownEntities) {
      this.eventIds.addAll(otherUnknownEntities.getEventIds());
      this.marketIds.addAll(otherUnknownEntities.getMarketIds());
      this.selectionIds.addAll(otherUnknownEntities.getSelectionIds());
    }
  }
}
