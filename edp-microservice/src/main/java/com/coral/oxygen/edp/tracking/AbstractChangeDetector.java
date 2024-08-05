package com.coral.oxygen.edp.tracking;

import com.coral.oxygen.edp.model.output.OutputMarket;
import com.coral.oxygen.edp.model.output.OutputOutcome;
import com.coral.oxygen.edp.tracking.model.EventData;
import java.util.Collection;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;

public abstract class AbstractChangeDetector {

  protected boolean isChanged(EventData newData, EventData oldData) {
    return Objects.isNull(oldData)
        || extractMarketsCount(newData) != extractMarketsCount(oldData)
        || !extractMarketsId(newData).equals(extractMarketsId(oldData))
        || !extractMarketDisporder(newData).equals(extractMarketDisporder(oldData))
        || !extractOutcomesId(newData).equals(extractOutcomesId(oldData));
  }

  private int extractMarketsCount(EventData data) {
    Integer marketsCount = data.getEvent().getMarketsCount();
    return Objects.isNull(marketsCount) ? 0 : marketsCount;
  }

  private Set<String> extractMarketsId(EventData data) {
    return data.getEvent().getMarkets().stream()
        .map(OutputMarket::getId)
        .collect(Collectors.toSet());
  }

  private Set<String> extractOutcomesId(EventData data) {

    return data.getEvent().getMarkets().stream()
        .map(OutputMarket::getOutcomes)
        .flatMap(Collection::stream)
        .map(OutputOutcome::getId)
        .collect(Collectors.toSet());
  }

  private Set<Integer> extractMarketDisporder(EventData data) {
    return data.getEvent().getMarkets().stream()
        .map(OutputMarket::getDisplayOrder)
        .collect(Collectors.toSet());
  }
}
