package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class OrderedOutcomeMarketHelper {

  private SiteServerApi siteServerApi;

  public OrderedOutcomeMarketHelper(SiteServerApi siteServerApi) {
    this.siteServerApi = siteServerApi;
  }

  public void recalculateCorrectedMeaningMinorCode(Event event, OutputMarket outputMarket) {

    List<OutputOutcome> outcomes =
        new ArrayList<>(
            outputMarket.getOutcomes().stream()
                .filter(o -> o.getDisplayOrder() != null)
                .collect(Collectors.toList()));
    outcomes.sort(
        Comparator.comparing(OutputOutcome::getDisplayOrder).thenComparing(OutputOutcome::getId));

    if (outcomes.size() > 2) {

      // set 1 && 2
      for (int i = 0; i < 2 && i < outcomes.size(); i++) {
        outcomes.get(i).setCorrectedOutcomeMeaningMinorCode(i + 1);
      }
      // clear from index 2 to size - 1 if we have more than 3 outcomes
      for (int i = 2; i < outcomes.size() - 1; i++) {
        outcomes.get(i).clearCorrectedOutcomeMeaningMinorCode();
      }
      // set 3 to last one
      if (outcomes.size() > 2) {
        outcomes.get(outcomes.size() - 1).setCorrectedOutcomeMeaningMinorCode(3);
      }
    } else if (event.getName().contains("Perf_")) {
      for (int i = 0; i < outcomes.size(); i++) {
        outcomes.get(i).setCorrectedOutcomeMeaningMinorCode(i + 1);
      }
    } else {
      Optional<List<Market>> markets =
          siteServerApi.getEventToOutcomeForMarket(outputMarket.getId(), true);
      if (markets.isPresent()) {
        List<Outcome> undisplayedOutcomes =
            markets.get().stream()
                .flatMap(s -> s.getOutcomes().stream())
                .collect(Collectors.toList());
        if (undisplayedOutcomes.size() == 3) {
          Set<Integer> displayOrdersSet =
              undisplayedOutcomes.stream()
                  .map(Outcome::getDisplayOrder)
                  .collect(Collectors.toSet());
          if (displayOrdersSet.size()
              < undisplayedOutcomes.size()) { // outcomes contain same order values
            log.warn(
                "Same value for outcomes displayOrder in market {}. Can\'t evaluate CorrectedOutcomeMeaningMinorCode",
                outputMarket.getId());
          } else {
            List<Integer> sortedDisplayOrders =
                displayOrdersSet.stream().sorted().collect(Collectors.toList());
            for (OutputOutcome outcome : outcomes) {
              outcome.clearCorrectedOutcomeMeaningMinorCode();
              outcome.setCorrectedOutcomeMeaningMinorCode(
                  getPositionForDisplayOrder(outcome, sortedDisplayOrders) + 1);
            }
          }
        } else {
          log.warn(
              "Not enough outcomes in market {} for evaluating CorrectedOutcomeMeaningMinorCode",
              outputMarket.getId());
        }
      } else {
        log.warn("Can\'t find outcomes for market {}", outputMarket.getId());
      }
    }
  }

  private Integer getPositionForDisplayOrder(OutputOutcome outcome, List<Integer> displayOrder) {
    for (int i = 0; i < displayOrder.size(); i++) {
      if (displayOrder.get(i).equals(outcome.getDisplayOrder())) {
        return i;
      }
    }
    return -1;
  }
}
