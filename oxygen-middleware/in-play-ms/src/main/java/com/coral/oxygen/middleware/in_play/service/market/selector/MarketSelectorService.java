package com.coral.oxygen.middleware.in_play.service.market.selector;

import static com.coral.oxygen.middleware.in_play.service.market.selector.MarketSelectorConstants.*;

import com.coral.oxygen.middleware.pojos.model.InPlayTopLevelType;
import com.coral.oxygen.middleware.pojos.model.output.MarketSwitcherSelection;
import com.coral.oxygen.middleware.pojos.model.output.Sport;
import com.coral.oxygen.middleware.pojos.model.output.SportMarketSwitcher;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.google.common.reflect.TypeToken;
import com.google.gson.Gson;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.function.BiConsumer;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

@Component
public class MarketSelectorService {

  private final Gson gson;
  private final Map<String, List<MarketSelector>> liveNowSportsMarketSelector;

  @Autowired
  public MarketSelectorService(Gson gson) throws IOException {
    this.gson = gson;
    liveNowSportsMarketSelector = new HashMap<>();

    // Reading market selections from json file instead constants to support cms driven approach in
    // future
    Resource marketSwitcherSelections = new ClassPathResource(MARKET_SWITCHER_SELECTIONS_JSON);

    getMarketSwitcherSelectinsForSports(gson, marketSwitcherSelections).stream()
        .collect(
            Collectors.toMap(
                SportMarketSwitcher::getSport, SportMarketSwitcher::getMarketSwitcherSelections))
        .forEach(prepareMarketSelectorTemplates(gson));
  }

  // Creates template for each selection from the json data based on selection templateType
  private BiConsumer<Sport, List<MarketSwitcherSelection>> prepareMarketSelectorTemplates(
      Gson gson) {
    return (Sport sport, List<MarketSwitcherSelection> switcherSelections) ->
        switcherSelections.forEach(
            (MarketSwitcherSelection switcherSelection) -> {
              if (!switcherSelection.isDisabled())
                switch (switcherSelection.getTemplateType()) {
                  case PRIMARY_MARKETS:
                    addMarketSelector(
                        sport,
                        switcherSelection.getMarketName(),
                        templateNames ->
                            new PrimaryMarketSelector(templateNames.split(DELIMETER), gson));
                    break;
                  case SIMPLE_MARKET:
                    addMarketSelector(
                        sport,
                        switcherSelection.getMarketName(),
                        templateNames ->
                            new TemplateNameMarketSelector(templateNames.split(DELIMETER), gson));
                    break;
                  case RAW_HANDICAP_VALUE_MARKET:
                    addMarketSelector(
                        sport,
                        switcherSelection.getMarketName(),
                        templateNames ->
                            new TemplateNameRawHandicapValueMarketSelector(
                                templateNames, switcherSelection.getHandicapValue(), gson));
                    break;
                  case FAVOURITE_MARKET_SELECTOR:
                    addMarketSelector(
                        sport,
                        switcherSelection.getMarketName(),
                        templateNames ->
                            new FavouriteMarketSelector(templateNames.split(DELIMETER), gson));
                    break;
                  case MARKET_WITH_MULTIPLE_NAMES:
                    addMarketSelector(
                        sport,
                        switcherSelection.getMarketName(),
                        templateNames ->
                            new MultipleNameMarketSelector(templateNames.split(DELIMETER), gson));
                    break;
                  case DEFAULT_MARKETS:
                    addMarketSelector(
                        sport,
                        switcherSelection.getMarketName(),
                        templateNames ->
                            new DefaultMarketSelector(templateNames.split(DELIMETER), gson));
                    break;
                  default:
                    break;
                }
            });
  }
  // Reads data from json file.
  private List<SportMarketSwitcher> getMarketSwitcherSelectinsForSports(
      Gson gson, Resource marketSwitcherSelections) throws IOException {
    List<SportMarketSwitcher> sportsMarketSwitcher = new ArrayList<>();
    if (marketSwitcherSelections != null) {
      try (InputStreamReader switcherSelectionStream =
          new InputStreamReader(marketSwitcherSelections.getInputStream())) {
        Type type =
            new TypeToken<List<SportMarketSwitcher>>() {
              private static final long serialVersionUID = 1L;
            }.getType();
        sportsMarketSwitcher = gson.fromJson(switcherSelectionStream, type);
      }
    }
    return sportsMarketSwitcher;
  }

  private void addMarketSelector(
      Sport sport,
      String templateNames,
      Function<String, MarketSelector> createMarketSelectorFunction) {
    if (Objects.isNull(sport)) {
      return;
    }
    addMarketSelector(sport.getCategoryName(), createMarketSelectorFunction, templateNames);
  }

  private void addMarketSelector(
      String categoryName,
      Function<String, MarketSelector> createMarketSelectorFunction,
      String templateName) {
    if (templateName == null) {
      return;
    }
    if (!CollectionUtils.isEmpty(liveNowSportsMarketSelector.get(categoryName))) {
      liveNowSportsMarketSelector
          .get(categoryName)
          .add(createMarketSelectorFunction.apply(templateName));
    } else {
      List<MarketSelector> marketSelectors = new ArrayList<>();
      marketSelectors.add(createMarketSelectorFunction.apply(templateName));
      liveNowSportsMarketSelector.put(categoryName, marketSelectors);
    }
  }

  public Collection<SportSegment> splitByMarketSelectors(SportSegment sportSegment) {
    Collection<SportSegment> result = splits(sportSegment);
    List<String> marketSelectorOptions =
        result.stream()
            .map(SportSegment::getMarketSelector)
            .filter(Objects::nonNull)
            .collect(Collectors.toList());
    if (!marketSelectorOptions.isEmpty()) {
      result.forEach(segment -> segment.setMarketSelectorOptions(marketSelectorOptions));
      sportSegment.setMarketSelectorOptions(marketSelectorOptions);
    }
    return result;
  }

  private Collection<SportSegment> splits(SportSegment sportSegment) {
    String categoryCode = sportSegment.getCategoryCode();
    if (SWITCHER_ENABLED_SPORTS.contains(categoryCode) || TIER_TWO_SPORTS.contains(categoryCode)) {
      if (InPlayTopLevelType.LIVE_EVENT.equals(sportSegment.getTopLevelType())
          || InPlayTopLevelType.STREAM_EVENT.equals(sportSegment.getTopLevelType())) {
        List<SportSegment> result = new ArrayList<>();
        for (MarketSelector marketSelector : liveNowSportsMarketSelector.get(categoryCode)) {
          result.addAll(marketSelector.extract(sportSegment));
        }
        return result;
      } else {
        return cloneAsIs(sportSegment);
      }
    }
    return cloneAsIs(sportSegment);
  }

  private Collection<SportSegment> cloneAsIs(SportSegment sportSegment) {
    List<SportSegment> result = new ArrayList<>(1);
    SportSegment clone = gson.fromJson(gson.toJson(sportSegment), SportSegment.class);
    result.add(clone);
    return result;
  }
}
