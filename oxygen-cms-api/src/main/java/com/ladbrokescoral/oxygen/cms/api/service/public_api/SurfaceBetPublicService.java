package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static com.ladbrokescoral.oxygen.cms.api.entity.AbstractSportEntity.SPORT_HOME_PAGE;
import static java.util.Comparator.*;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.egalacoral.spark.siteserver.model.Price;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeCompleteEventDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeCompleteMarketDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeCompleteOutcomeDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SurfaceBetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Relation;
import com.ladbrokescoral.oxygen.cms.api.entity.RelationType;
import com.ladbrokescoral.oxygen.cms.api.entity.SurfaceBet;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.exception.SurfaceBetException;
import com.ladbrokescoral.oxygen.cms.api.mapping.SiteServeEventDtoMapper;
import com.ladbrokescoral.oxygen.cms.api.mapping.SiteServeMarketDtoMapper;
import com.ladbrokescoral.oxygen.cms.api.mapping.SiteServeOutcomeDtoMapper.SiteServeOutcomeDtoMapperInstance;
import com.ladbrokescoral.oxygen.cms.api.mapping.SurfaceBetMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SurfaceBetRepository;
import com.ladbrokescoral.oxygen.cms.api.service.SurfaceBetSortHelper;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Slf4j
@Service
@RequiredArgsConstructor
public class SurfaceBetPublicService {

  private static final Comparator<SurfaceBetDto> SURFACE_BET_COMPARATOR =
      comparing(SurfaceBetDto::getEventIsLive, nullsLast(reverseOrder()))
          .thenComparing(SurfaceBetDto::getDisplayOrder, nullsLast(naturalOrder()))
          .thenComparing(SurfaceBetDto::getEventStartTime, nullsLast(naturalOrder()))
          .thenComparing(sb -> sb.getSelectionEvent().getName(), nullsLast(naturalOrder()));

  public static final String SORT_ORDER_FIELD = "sortOrder";
  public static final Sort SORT_BY_SORT_ORDER_ASC = Sort.by(SORT_ORDER_FIELD);

  private final SurfaceBetRepository repository;
  private final SiteServeApiProvider siteServerApiProvider;
  private final SegmentRepository segmentRepository;

  /**
   * Finds active SurfaceBets by brand. SurfaceBets with references to sport and eventhub will be
   * returned
   */
  public List<SurfaceBetDto> findActiveByBrandAndRelationType(
      String brand, AtomicInteger counter, RelationType... relationTypes) {
    List<SurfaceBet> activeSurfaceBets =
        repository
            .findByBrandAndDisplayFromIsBeforeAndDisplayToIsAfterAndDisabledIsFalseOrderBySortOrderAsc(
                brand, Instant.now(), Instant.now());

    List<String> segments =
        segmentRepository.findByBrand(brand).stream()
            .map(Segment::getSegmentName)
            .collect(Collectors.toList());
    if (!segments.contains(SegmentConstants.UNIVERSAL)) segments.add(SegmentConstants.UNIVERSAL);
    Set<String> relationNames =
        Stream.of(relationTypes).map(RelationType::name).collect(Collectors.toSet());

    activeSurfaceBets =
        SurfaceBetSortHelper.sortSurfaceBetUniversalRecords(
            activeSurfaceBets, RelationType.sport, SPORT_HOME_PAGE);

    List<SurfaceBetDto> surfaceBetDtoList =
        activeSurfaceBets.stream()
            .map(this::updateHomePageReference)
            .flatMap(sb -> SurfaceBetMapper.getInstance().toDtoStream(sb, segments))
            .map(sb -> updateSurfaceBetDTO(sb, counter))
            .filter(
                sb ->
                    sb.getReference().isEnabled()
                        && relationNames.contains(sb.getReference().getRelationType()))
            .collect(Collectors.toList());

    return SurfaceBetSortHelper.getHomeAndReamingSportPagesSortedOrder(surfaceBetDtoList);
  }

  public SurfaceBetDto updateSurfaceBetDTO(SurfaceBetDto dto, AtomicInteger counter) {
    dto.setDisplayOrder(counter.getAndAdd(1));
    return dto;
  }

  private SurfaceBet updateHomePageReference(SurfaceBet sb) {
    Relation homeRelation =
        Relation.builder()
            .relatedTo(RelationType.sport)
            .refId(SPORT_HOME_PAGE)
            .enabled(sb.getHighlightsTabOn())
            .build();
    if (CollectionUtils.isEmpty(sb.getReferences())) {
      sb.setReferences(Collections.singleton(homeRelation));
    } else {
      Relation homeRelationOfSb =
          sb.getReferences().stream()
              .filter(
                  relation ->
                      RelationType.sport.equals(relation.getRelatedTo())
                          && SPORT_HOME_PAGE.equals(relation.getRefId()))
              .findFirst()
              .orElse(null);
      if (homeRelationOfSb == null) {
        sb.getReferences().add(homeRelation);
      }
    }

    return sb;
  }

  /**
   * @param brand - brand to which surfaceBets are related
   * @param eventId - related to the surfaceBets edp
   * @return list of active SurfaceBets for the brand and related to the given eventId
   */
  @Cacheable("edp-surface-bets")
  public List<SurfaceBetDto> findActiveEdpSurfaceBets(String brand, String eventId) {
    try {
      List<String> segments =
          segmentRepository.findByBrand(brand).stream()
              .map(Segment::getSegmentName)
              .collect(Collectors.toList());
      List<SurfaceBet> bets =
          repository.findUniversalRecordsByBrandAndActiveTrue(
              brand, Instant.now(), Instant.now(), SORT_BY_SORT_ORDER_ASC);
      log.info("surface bets found {} ", bets.size());
      List<SurfaceBetDto> surfaceBetDtos =
          repository
              .findUniversalRecordsByBrandAndActiveTrue(
                  brand, Instant.now(), Instant.now(), SORT_BY_SORT_ORDER_ASC)
              .stream()
              .flatMap(sb -> SurfaceBetMapper.getInstance().toDtoStream(sb, segments))
              .filter(
                  sb ->
                      sb.getReference().isEnabled()
                          && RelationType.edp.name().equals(sb.getReference().getRelationType())
                          && eventId.equals(sb.getReference().getRefId()))
              .collect(Collectors.toList());
      log.info(
          "Found {} surfaceBets for brand {} and eventId {}",
          surfaceBetDtos.size(),
          brand,
          eventId);
      if (!CollectionUtils.isEmpty(surfaceBetDtos)) {
        injectSelectionData(brand, surfaceBetDtos);
        return surfaceBetDtos.stream()
            .filter(sb -> Objects.nonNull(sb.getSelectionEvent()))
            .sorted(SURFACE_BET_COMPARATOR)
            .collect(Collectors.toList());
      }
      return surfaceBetDtos;
    } catch (Exception e) {
      log.error("Failed to get SurfaceBets for {} brand and eventId {}", brand, eventId, e);
      throw new SurfaceBetException();
    }
  }

  private void injectSelectionData(String brand, List<SurfaceBetDto> surfaceBets) {
    Map<String, SurfaceBetDto> surfaceBetsBySelectionId =
        surfaceBets.stream()
            .collect(Collectors.toMap(sb -> sb.getSelectionId().toString(), Function.identity()));

    List<Event> events = getEvents(brand, surfaceBetsBySelectionId.keySet());
    log.info(
        "Received {} events from SiteServe for {} selectionIds",
        events.size(),
        surfaceBetsBySelectionId.size());
    injectEventsIntoSurfaceBets(events, surfaceBetsBySelectionId);
  }

  private void injectEventsIntoSurfaceBets(
      List<Event> events, Map<String, SurfaceBetDto> surfaceBets) {
    for (Event event : events) {
      for (Market market : event.getMarkets()) {
        for (Outcome outcome : market.getOutcomes()) {
          if (!surfaceBets.containsKey(outcome.getId())) {
            continue;
          }
          Optional<Price> price = outcome.getPrices().stream().findFirst();
          if (price.isPresent() || market.getPriceTypeCodes().contains("SP")) {
            SurfaceBetDto surfaceBetDto = surfaceBets.get(outcome.getId());
            surfaceBetDto.setDisplayOrder(event.getDisplayOrder());
            surfaceBetDto.setSelectionEvent(toDto(event, market, outcome, price.orElse(null)));
          }
        }
      }
    }
  }

  private List<Event> getEvents(String brand, Set<String> selectionIds) {
    return siteServerApiProvider
        .api(brand)
        .getEventToOutcomeForOutcome(
            new ArrayList<>(selectionIds),
            (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build(),
            new ArrayList<>())
        .orElse(Collections.emptyList());
  }

  private SiteServeCompleteEventDto toDto(
      Event event, Market market, Outcome outcome, Price price) {
    SiteServeCompleteEventDto eventDto =
        SiteServeEventDtoMapper.INSTANCE.toDtoWithoutMarkets(event);
    SiteServeCompleteMarketDto marketDto =
        SiteServeMarketDtoMapper.INSTANCE.toDtoWithoutOutcomes(market);
    SiteServeCompleteOutcomeDto outcomeDto =
        SiteServeOutcomeDtoMapperInstance.INSTANCE.toDtoWithoutPrices(outcome);
    eventDto.setMarkets(Collections.singletonList(marketDto));
    marketDto.setOutcomes(Collections.singletonList(outcomeDto));
    outcomeDto.setPrices(Collections.singletonList(SurfaceBetMapper.getInstance().toDto(price)));
    return eventDto;
  }
}
