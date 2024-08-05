package com.ladbrokescoral.oxygen.cms.api.service;

import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.StatisticContent;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.MarketType;
import com.ladbrokescoral.oxygen.cms.api.entity.StatisticContentTitleDto;
import com.ladbrokescoral.oxygen.cms.api.exception.MarketTypeInvalidException;
import com.ladbrokescoral.oxygen.cms.api.exception.SiteServEventAndMarketValidationException;
import com.ladbrokescoral.oxygen.cms.api.exception.StatisticalContentNotUniqueException;
import com.ladbrokescoral.oxygen.cms.api.repository.StatisticContentRepository;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.time.Duration;
import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.util.Assert;

@Service
@Slf4j
public class StatisticContentService extends SortableService<StatisticContent> {

  private static final List<MarketType> BMA_MARKET_TYPES =
      Arrays.asList(MarketType.OB, MarketType.BMOB);

  private static final List<MarketType> LADS_MARKET_TYPES =
      Arrays.asList(MarketType.PB, MarketType.SPB);

  private final StatisticContentRepository contentRepository;

  private final SiteServeApiProvider siteServeApiProvider;

  private final ScheduledTaskExecutor taskExecutor;

  private final int expiredDuration;

  public StatisticContentService(
      StatisticContentRepository contentRepository,
      SiteServeApiProvider siteServeApiProvider,
      ScheduledTaskExecutor taskExecutor,
      @Value("${staticContent.removeExpired.afterDays}") int expiredDuration) {
    super(contentRepository);
    this.contentRepository = contentRepository;
    this.siteServeApiProvider = siteServeApiProvider;
    this.taskExecutor = taskExecutor;
    this.expiredDuration = expiredDuration;
  }

  public StatisticContentTitleDto getTitleAndMarketIds(String brand, String eventId) {

    return this.siteServeApiProvider
        .api(brand)
        .getEventToMarketForEvent(
            Collections.singletonList(eventId), Optional.empty(), Optional.empty(), true)
        .filter(CollectionUtils::isNotEmpty)
        .map(events -> events.get(0))
        .map(
            (Event event) -> {
              StatisticContentTitleDto dto = new StatisticContentTitleDto();
              buildStatisticalContentTitle(dto, event);
              return dto;
            })
        .orElseThrow(
            () -> {
              log.error("Event with Id::{} does not exist in OB", eventId);
              return new SiteServEventAndMarketValidationException();
            });
  }

  private void buildStatisticalContentTitle(StatisticContentTitleDto dto, Event event) {
    List<String> marketIds =
        event.getMarkets().stream().map(Market::getId).collect(Collectors.toList());
    dto.setEventTitle(event.getName().replace("|", ""));
    dto.setMarketIds(marketIds);
  }

  @Override
  public StatisticContent prepareModelBeforeSave(StatisticContent model) {
    validate(model);
    return super.prepareModelBeforeSave(model);
  }

  private void validate(StatisticContent model) {
    if (StringUtils.isEmpty(model.getId())) {
      validateForCreate(model);
    } else {
      validateForUpdate(model);
    }
  }

  /**
   * @param model when document with same eventId, marketId and marketType of a particular brand is
   *     already there in database. then we should consider it as a duplicate and abort saving the
   *     incoming model
   */
  private void validateForCreate(StatisticContent model) {
    model.setMarketDescription(model.getMarketType().getDescription());
    validateForMarketType(model.getBrand(), model.getMarketType());
    validateEventIdAndMarketIdInOB(model.getBrand(), model.getEventId(), model.getMarketId());
    Optional<List<StatisticContent>> existingModels =
        this.contentRepository.findByBrandAndEventIdAndMarketIdAndMarketType(
            model.getBrand(), model.getEventId(), model.getMarketId(), model.getMarketType());
    existingModels.ifPresent(
        existingContents ->
            existingContents.forEach(existing -> validateForDuplication(existing, model)));
  }

  private void validateEventIdAndMarketIdInOB(String brand, String eventId, String marketId) {
    Optional<Market> market =
        this.siteServeApiProvider.api(brand).getEventToMarketForMarket(marketId);
    if ((!market.isPresent()) || (!eventId.equalsIgnoreCase(market.get().getEventId()))) {
      log.error("Event :: {} with Market ::{} does not exist in OB", eventId, marketId);
      throw new SiteServEventAndMarketValidationException();
    }
  }

  private void validateForDuplication(StatisticContent existingModel, StatisticContent model) {

    Instant existingStartTime = existingModel.getStartTime();
    Instant existingEndTime = existingModel.getEndTime();
    Instant modelStartTime = model.getStartTime();
    Instant modelEndTime = model.getEndTime();

    if ((modelStartTime.isAfter(existingStartTime) && modelStartTime.isBefore(existingEndTime))
        || (modelEndTime.isAfter(existingStartTime) && modelEndTime.isBefore(existingEndTime))) {
      throw new StatisticalContentNotUniqueException();
    }

    if (modelStartTime.equals(existingStartTime) || modelEndTime.equals(existingEndTime)) {
      throw new StatisticalContentNotUniqueException();
    }

    if (modelStartTime.isBefore(existingStartTime) && modelEndTime.isAfter(existingEndTime)) {
      throw new StatisticalContentNotUniqueException();
    }
  }

  /**
   * once the document is saved in the database. we cannot edit the eventId and marketId if
   * attempted we have to set the existing eventId and marketId to the updated model.
   *
   * @param updatedModel updated model
   */
  private void validateForUpdate(StatisticContent updatedModel) {
    updatedModel.setMarketDescription(updatedModel.getMarketType().getDescription());
    validateForMarketType(updatedModel.getBrand(), updatedModel.getMarketType());
    Optional<StatisticContent> existing =
        this.contentRepository.findByIdAndBrand(updatedModel.getId(), updatedModel.getBrand());

    existing.ifPresent(
        (StatisticContent existingEntity) -> {
          updatedModel.setEventId(existingEntity.getEventId());
          updatedModel.setMarketId(existingEntity.getMarketId());
        });

    this.contentRepository
        .findByBrandAndEventIdAndMarketIdAndMarketType(
            updatedModel.getBrand(),
            updatedModel.getEventId(),
            updatedModel.getMarketId(),
            updatedModel.getMarketType())
        .filter(CollectionUtils::isNotEmpty)
        .ifPresent(
            contents ->
                contents.stream()
                    .filter(
                        (StatisticContent e) -> {
                          Assert.notNull(e.getId(), "id should not be null");
                          return !e.getId().equalsIgnoreCase(updatedModel.getId());
                        })
                    .forEach((StatisticContent e) -> this.validateForDuplication(e, updatedModel)));
  }

  private void validateForMarketType(String brand, MarketType marketType) {
    if (brand.equalsIgnoreCase(Brand.BMA) && LADS_MARKET_TYPES.contains(marketType)) {
      throw new MarketTypeInvalidException();
    }
    if (brand.equalsIgnoreCase(Brand.LADBROKES) && BMA_MARKET_TYPES.contains(marketType)) {
      throw new MarketTypeInvalidException();
    }
  }

  public List<StatisticContent> findByEventId(String eventId) {
    return this.contentRepository.findByEventId(eventId);
  }

  /**
   * Scheduler have to run at a specified cron expression to delete the statistic content documents
   * in mongoDb automatically after the specified duration of end time of the document
   */
  @Scheduled(cron = "${staticContent.removeExpired.cron}")
  public void removeExpiredEntities() {
    this.taskExecutor.execute(
        () -> {
          List<StatisticContent> contents = this.contentRepository.findAll();
          contents.stream()
              .filter(Objects::nonNull)
              .forEach(
                  (StatisticContent content) -> {
                    Instant expireAt =
                        content.getEndTime().plus(Duration.ofDays(this.expiredDuration));
                    if (Instant.now().isAfter(expireAt)) {
                      log.info("removing the statistic Content::{}", content);
                      this.contentRepository.delete(content);
                    }
                  });
        });
  }
}
