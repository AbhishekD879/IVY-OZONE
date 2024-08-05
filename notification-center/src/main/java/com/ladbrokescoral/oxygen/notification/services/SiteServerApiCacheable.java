package com.ladbrokescoral.oxygen.notification.services;

import static java.util.stream.Collectors.toList;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.api.SiteServerImpl;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Media;
import com.egalacoral.spark.siteserver.model.RacingResult;
import com.ladbrokescoral.oxygen.notification.entities.Outcome;
import com.ladbrokescoral.oxygen.notification.utils.ObjectMapper;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

@Service
public class SiteServerApiCacheable implements SiteServerApiService {

  private static final String MEDIA_PROPERTIES_SPLIT_REGEX = ":";

  private SiteServerApi siteServerApi;
  private String iGameMediaProviderId;

  @Autowired
  public SiteServerApiCacheable(
      SiteServerApi siteServerApi,
      @Value("${media.provider.igamemedia.id}") String iGameMediaProviderId) {
    this.siteServerApi = siteServerApi;
    this.iGameMediaProviderId = iGameMediaProviderId;
  }

  @Override
  public Optional<Event> getEvent(String eventId) {
    return siteServerApi.getEvent(eventId, true);
  }

  @Override
  public Optional<Event> getCommentaryForEvent(String eventId) {
    return siteServerApi
        .getCommentaryForEvent(Collections.singletonList(eventId))
        .flatMap(list -> list.stream().findAny());
  }

  @Cacheable(CACHE_EVENT)
  @Override
  public Optional<Event> getCachedEvent(String eventId) {
    return siteServerApi.getEvent(eventId, true);
  }

  @Cacheable(CACHE_EVENT_FOR_OUTCOME)
  @Override
  public Optional<Event> getCachedEventForOutcome(String selectionId) {
    return siteServerApi
        .getEventToOutcomeForOutcome(
            Collections.singletonList(selectionId), SiteServerImpl.EMPTY_SIMPLE_FILTER, null, true)
        .flatMap(events -> events.stream().findFirst());
  }

  @Override
  public Optional<RacingResult> getCachedRacingResults(String eventId) {
    return siteServerApi.getRacingResultsForEvent(eventId);
  }

  @Override
  public Optional<String> getIGameMediaIdForEvent(String eventId) {
    return siteServerApi
        .getMedia(eventId)
        .flatMap(
            providers ->
                providers.stream()
                    .filter(
                        provider ->
                            provider
                                .getId()
                                .equalsIgnoreCase(iGameMediaProviderId)) // only iGameMedia provider
                    .findFirst())
        .flatMap(
            provider ->
                provider.getChildren().stream()
                    .filter(children -> Objects.nonNull(children.getMedia()))
                    .findFirst()
                    .map(Children::getMedia)) // get the media for provider
        .map(Media::getAccessProperties) // find access properties for media - should contain
        // iGameMedia event id
        .map(this::mapAccessProperties);
  }

  private String mapAccessProperties(String properties) {
    String[] propertiesArray = properties.split(MEDIA_PROPERTIES_SPLIT_REGEX);
    String id = null;
    // get the id (the accessProperties should look like e.g.
    // "eeyaaEventId:UKGH000000ZA20190508-11")
    if (propertiesArray.length >= 2) {
      id = propertiesArray[1];
    }
    return id;
  }

  @Cacheable(CACHE_OUTCOME_NAME)
  @Override
  public String getOutcomeName(String outcomeId) {
    return findMatchingOutcome(getOutcomes(getEventForOutcome(outcomeId), outcomeId), outcomeId)
        .getName();
  }

  private List<Event> getEventForOutcome(String outcomeId) {
    return siteServerApi
        .getEventToOutcomeForOutcome(
            Collections.singletonList(outcomeId),
            (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build(),
            null,
            true)
        .orElse(Collections.emptyList());
  }

  private List<Outcome> getOutcomes(List<Event> events, String outcomeId) {
    return events.stream()
        .map(this::mapEvent)
        .findFirst()
        .orElseThrow(() -> noEventsForOutcome(outcomeId))
        .getOutcomes();
  }

  private Outcome findMatchingOutcome(List<Outcome> outcomes, String outcomeId) {
    return outcomes.stream()
        .filter(outcome -> outcome.getId().equals(outcomeId))
        .findFirst()
        .orElseThrow(() -> noOutcomes(outcomeId));
  }

  private com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event mapEvent(Event event) {
    return com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event.builder()
        .outcomes(
            event.getChildren().stream()
                .map(Children::getMarket)
                .filter(Objects::nonNull)
                .filter(market -> !market.getOutcomes().isEmpty())
                .flatMap(market -> market.getOutcomes().stream())
                .collect(toList())
                .stream()
                .map(ObjectMapper::mapOutcome)
                .collect(toList()))
        .build();
  }

  private IllegalStateException noOutcomes(String id) {
    return new IllegalStateException("No outcomes found in event for ID: " + id);
  }

  private IllegalStateException noEventsForOutcome(String outcomeId) {
    return new IllegalStateException("No events for outcome ID: " + outcomeId);
  }
}
