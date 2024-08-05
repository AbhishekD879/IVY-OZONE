package com.coral.oxygen.middleware.in_play.service.market.selector;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment;
import com.google.gson.Gson;
import java.util.Collection;
import java.util.Comparator;
import java.util.Objects;
import java.util.Optional;

public class FavouriteMarketSelector extends AbstractMultipleMarketSelector {

  private static final int SIZE = 2;
  private final String[] markteNamesToFilter;

  public FavouriteMarketSelector(String[] marketNamesToKeep, Gson gson) {
    super(marketNamesToKeep, gson);
    this.markteNamesToFilter = marketNamesToKeep;
  }

  @Override
  protected String selectorName() {
    return markteNamesToFilter[0];
  }

  @Override
  protected SportSegment getCloneWithFilteredMarkets(SportSegment sportSegment) {
    SportSegment clone = deepClone(sportSegment);
    // remove not acceptable markets

    clone.getEventsByTypeName().stream()
        .map(TypeSegment::getEvents)
        .flatMap(Collection::stream)
        .forEach(
            (EventsModuleData event) -> {
              String[] priorityMarket = getPriorityMarket(event);
              event.getMarkets().removeIf(market -> !priorityMarket(market, priorityMarket));
            });
    clone.setMarketSelector(selectorName());

    // remove market without outcomes
    clone.getEventsByTypeName().forEach(AbstractMarketSelector::removeMarketsWithoutOutcomes);
    return clone;
  }

  private boolean priorityMarket(OutputMarket market, String[] priorityMarket) {
    String marketTemplateName = market.getTemplateMarketName();
    if (Objects.nonNull(marketTemplateName)) {
      return marketTemplateName
              .replace("|", "")
              .toLowerCase()
              .equalsIgnoreCase(selectorName().toLowerCase())
          && market.getTemplateMarketName().equalsIgnoreCase(priorityMarket[0])
          && market.getRawHandicapValue() != null
          && market.getRawHandicapValue().toString().equals(priorityMarket[1]);
    }
    return false;
  }

  private String[] getPriorityMarket(EventsModuleData event) {
    String[] prioritymarket = new String[SIZE];
    Optional<OutputMarket> selectedMarket =
        event.getMarkets().stream()
            .filter(market -> market.getName() != null && market.getName().contains(selectorName()))
            .min(Comparator.comparing(OutputMarket::getDisplayOrder));
    if (selectedMarket.isPresent()) {
      String rawHandicapValue = null;
      if (selectedMarket.get().getRawHandicapValue() != null)
        rawHandicapValue = selectedMarket.get().getRawHandicapValue().toString();
      prioritymarket[0] = selectedMarket.get().getTemplateMarketName();
      prioritymarket[1] = rawHandicapValue;
    }
    return prioritymarket;
  }
}
