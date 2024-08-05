package com.coral.oxygen.middleware.in_play.service;

import static java.util.stream.Collectors.toList;

import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import java.util.Comparator;
import java.util.List;
import java.util.Objects;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

@Component
public class TopThreeOutrightOutcomesFilter implements OutrightOutcomesFilter {

  private final Comparator<Children> outcomesComparator =
      Comparator.comparing(
              // get(0) is safe as empty prices are filtered out and there can be maximum one price
              // per outcome
              (Children children) -> children.getOutcome().getPrices().get(0).getPriceDec(),
              Comparator.nullsLast(Comparator.naturalOrder()))
          .thenComparingInt(children -> children.getOutcome().getDisplayOrder())
          .thenComparing(children -> children.getOutcome().getName());
  private static final int MAX_OUTRIGHT_OUTCOMES = 3;

  public List<Event> filterOutcomes(List<Event> events) {
    events.forEach(
        event ->
            event
                .getChildren()
                .forEach(
                    eventChild -> {
                      if (eventChild.getMarket() != null
                          && "Outright".equals(eventChild.getMarket().getTemplateMarketName())) {
                        List<Children> topOutcomes =
                            filterOutcomes(eventChild.getMarket(), MAX_OUTRIGHT_OUTCOMES);
                        eventChild
                            .getMarket()
                            .getChildren()
                            .removeIf(marketChild -> marketChild.getOutcome() != null);
                        eventChild.getMarket().getChildren().addAll(topOutcomes);
                      }
                    }));
    return events;
  }

  private List<Children> filterOutcomes(Market market, int maxItemsToReturn) {
    return market.getChildren().stream()
        .filter(
            children ->
                Objects.nonNull(children)
                    && !CollectionUtils.isEmpty(children.getOutcome().getPrices())
                    && children.getOutcome().getDisplayOrder() != null
                    && children.getOutcome().getName() != null)
        .sorted(outcomesComparator)
        .limit(maxItemsToReturn)
        .collect(toList());
  }
}
