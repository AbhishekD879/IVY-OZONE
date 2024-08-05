package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.ladbrokescoral.oxygen.questionengine.configuration.properties.ApplicationProperties;
import com.ladbrokescoral.oxygen.questionengine.dto.AbstractQuizDto;
import com.ladbrokescoral.oxygen.questionengine.dto.UpsellDto;
import com.ladbrokescoral.oxygen.questionengine.dto.UpsellPriceDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.UpsellConfigurationDto;
import com.ladbrokescoral.oxygen.questionengine.service.UpsellService;
import com.ladbrokescoral.oxygen.questionengine.util.Utils;
import io.vavr.collection.Stream;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections4.MapUtils;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Collectors;

@Service
@Slf4j
@RequiredArgsConstructor
public class UpsellServiceImpl implements UpsellService {

  private final ApplicationProperties applicationProperties;
  private final SiteServerApi siteServerApi;

  @Override
  @Cacheable(value = "upsellCache", key = "#quiz.sourceId")
  public Optional<UpsellDto> findUpsellFor(AbstractQuizDto quiz) {
    if (quiz.getUpsellConfiguration() == null) {
      return Optional.empty();
    }
    UpsellConfigurationDto upsellConfiguration = quiz.getUpsellConfiguration();
    UpsellDto upsell = new UpsellDto()
        .setFallbackImagePath(upsellConfiguration.getFallbackImagePath())
        .setImageUrl(upsellConfiguration.getImageUrl());

    List<Long> selectionIds = new ArrayList<>();
    if (upsellConfiguration.getDefaultUpsellOption() != null) {
      selectionIds.add(upsellConfiguration.getDefaultUpsellOption());
    }
    if (isDynamicUpsellConfigured(quiz)) {
      selectionIds.addAll(upsellConfiguration.getOptions().values());
    }
    Map<Long, UpsellPriceDto> selectionToPrice = Utils.splitIntoBatches(selectionIds, applicationProperties.getSiteServerSelectionIdsLimit())
        .stream()
        .map(this::computePrices)
        .map(Map::entrySet)
        .flatMap(Set::stream)
        .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));

    Map<String, UpsellPriceDto> dynamicUpsellOptions = upsellConfiguration.getOptions().entrySet()
        .stream()
        .filter(questionIdsToSelection -> selectionToPrice.containsKey(questionIdsToSelection.getValue()))
        .collect(Collectors.toMap(Map.Entry::getKey, questionIdsToSelection -> selectionToPrice.get(questionIdsToSelection.getValue())));

    log.info("Collected the following upsell: {}", dynamicUpsellOptions);

    upsell
        .setDefaultUpsellOption(selectionToPrice.get(upsellConfiguration.getDefaultUpsellOption()))
        .setDynamicUpsellOptions(dynamicUpsellOptions);

    return Optional.of(upsell);
  }

  private boolean isDynamicUpsellConfigured(AbstractQuizDto quiz) {
    return MapUtils.isNotEmpty(quiz.getUpsellConfiguration().getOptions());
  }

  private Map<Long, UpsellPriceDto> computePrices(Collection<Long> selectionIds) {
    Optional<List<Event>> maybeEvents = siteServerApi.getEventToOutcomeForOutcome(
        selectionIds.stream()
            .map(Object::toString)
            .collect(Collectors.toList()),
        (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build(),
        Collections.emptyList()
    );

    return maybeEvents.map(Stream::ofAll)
        .orElse(Stream.empty())
        .flatMap(Event::getMarkets)
        .flatMap(this::computePrices)
        .collect(Collectors.toMap(UpsellPriceDto::getSelectionId, Function.identity()));
  }

  private Stream<UpsellPriceDto> computePrices(Market market) {
    return Stream.ofAll(market.getOutcomes()).flatMap(outcome -> computePrices(market, outcome));
  }

  private Stream<UpsellPriceDto> computePrices(Market market, Outcome outcome) {
    return Stream.ofAll(outcome.getPrices())
        .map(price -> new UpsellPriceDto()
            .setMarketName(market.getName())
            .setSelectionName(outcome.getName())
            .setSelectionId(Long.valueOf(outcome.getId()))
            .setPrice(BigDecimal.valueOf(price.getPriceDec()))
            .setPriceDen(price.getPriceDen())
            .setPriceNum(price.getPriceNum())
        )
        .peek(price -> log.info("Found Price for selection id '{}': {}", price.getSelectionId(), price));
  }
}
