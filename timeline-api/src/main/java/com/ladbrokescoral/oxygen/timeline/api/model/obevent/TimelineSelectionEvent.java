package com.ladbrokescoral.oxygen.timeline.api.model.obevent;

import static java.util.stream.Collectors.toList;

import java.util.Collections;
import java.util.List;
import java.util.Optional;
import lombok.Data;
import org.springframework.util.CollectionUtils;

@Data
public class TimelineSelectionEvent {
  private ObEvent obEvent;

  public List<String> queryMarketIds() {
    if (isNoMarkets()) {
      return Collections.emptyList();
    }
    return obEvent.getMarkets().stream().map(ObMarket::getId).collect(toList());
  }

  public Optional<ObMarket> getMarketById(String marketId) {
    if (isNoMarkets()) {
      return Optional.empty();
    }
    return obEvent.getMarkets().stream()
        .filter(obMarket -> obMarket.getId().equals(marketId))
        .findAny();
  }

  public Optional<ObOutcome> getOutcomeById(String outcomeId) {
    if (isNoMarkets()) {
      return Optional.empty();
    }
    return obEvent.getMarkets().stream()
        .flatMap(obMarket -> obMarket.getOutcomes().stream())
        .filter(obOutcome -> obOutcome.getId().equals(outcomeId))
        .findAny();
  }

  private boolean isNoMarkets() {
    return obEvent == null || CollectionUtils.isEmpty(obEvent.getMarkets());
  }
}
