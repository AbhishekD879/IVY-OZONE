package com.coral.oxygen.edp.tracking.sports;

import com.coral.oxygen.edp.configuration.SportsDataConsumerConfiguration;
import com.coral.oxygen.edp.model.mapping.EventMapper;
import com.coral.oxygen.edp.model.output.OutputEvent;
import com.coral.oxygen.edp.service.CmsApiService;
import com.coral.oxygen.edp.tracking.QueuedMultiThreadDataConsumer;
import com.coral.oxygen.edp.tracking.UpdateScheduler;
import com.coral.oxygen.edp.tracking.model.CategoryToUpcomingEvent;
import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.api.SiteServerImpl;
import com.egalacoral.spark.siteserver.api.UnaryOperation;
import com.egalacoral.spark.siteserver.model.Category;
import com.ladbrokescoral.oxygen.cms.client.model.StreamAndBetDto;
import java.time.Clock;
import java.time.Instant;
import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class SportsDataConsumer
    extends QueuedMultiThreadDataConsumer<String, List<CategoryToUpcomingEvent>> {

  private final int minimumSecondsUntilStart;

  private final int virtualCategoryId;
  private static final List<Integer> SPORT_PRIORITIES =
      Arrays.asList(285, 287, 286, 290, 289, 288, 900, 901);
  private final CategoryToUpcomingEventComposer categoryToUpcomingEventComposer;

  private SiteServerApi siteServerApi;
  private EventMapper eventMapper;
  private UpdateScheduler updateScheduler;
  private CmsApiService cmsApiService;
  private static final int EVENT_START_TIME = 10;

  public SportsDataConsumer(
      SportsDataConsumerConfiguration configuration,
      SiteServerApi siteServerApi,
      EventMapper eventMapper,
      UpdateScheduler updateScheduler,
      CmsApiService cmsApiService,
      CategoryToUpcomingEventComposer categoryToUpcomingEventComposer) {
    super(configuration.getMaxQueueSize(), configuration.getThreadsCount());
    this.minimumSecondsUntilStart = configuration.getMinimumSecondsUntilStart();
    this.virtualCategoryId = configuration.getVirtualCategoryId();
    this.siteServerApi = siteServerApi;
    this.eventMapper = eventMapper;
    this.updateScheduler = updateScheduler;
    this.cmsApiService = cmsApiService;
    this.categoryToUpcomingEventComposer = categoryToUpcomingEventComposer;
  }

  @Override
  protected Map<String, List<CategoryToUpcomingEvent>> doConsume(Set<String> tickets) {
    Map<String, List<CategoryToUpcomingEvent>> result = new HashMap<>();
    List<CategoryToUpcomingEvent> categoriesToEvents = getCategoriesToEvents();

    result.put(tickets.stream().findFirst().orElse(""), categoriesToEvents);
    return result;
  }

  private List<CategoryToUpcomingEvent> getCategoriesToEvents() {
    StreamAndBetDto virtualDto = getVirtualDto();
    if (virtualDto != null && !isDtoDisabledWithChildren(virtualDto)) {
      List<Category> categories =
          getCategories(getExcludedClasses(virtualDto), getIncludedClasses(virtualDto));
      List<String> ids = extractIdsFromCategories(categories);
      List<OutputEvent> events = getOneUpcomingEventForEachClassId(ids);

      scheduleDataRefresh(events);
      List<CategoryToUpcomingEvent> categoriesToEvents =
          categoryToUpcomingEventComposer.composeCategoriesToEvents(categories, events);
      categoriesToEvents.sort(Comparator.comparingInt(this::getSportPriority));
      return categoriesToEvents;
    } else return Collections.emptyList();
  }

  private boolean isDtoDisabledWithChildren(StreamAndBetDto virtualDto) {
    return isDtoDisabledForBothPlatforms(virtualDto) && allDtoDisabled(virtualDto.getChildren());
  }

  private boolean allDtoDisabled(List<StreamAndBetDto> dtos) {
    for (StreamAndBetDto dto : dtos) {
      if (isDtoEnabledForBothPlatforms(dto)) return false;
    }
    return true;
  }

  private StreamAndBetDto getVirtualDto() {
    return getDto().orElse(Collections.emptyList()).stream()
        .filter(dto -> dto.getId() == virtualCategoryId)
        .findFirst()
        .orElse(null);
  }

  private List<Integer> getExcludedClasses(StreamAndBetDto virtualDto) {
    if (virtualDto == null) return Collections.emptyList();

    return virtualDto.getChildren().stream()
        .filter(this::isDtoDisabledForBothPlatforms)
        .map(StreamAndBetDto::getId)
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private List<Integer> getIncludedClasses(StreamAndBetDto virtualDto) {
    if (virtualDto == null || !isDtoDisabledForBothPlatforms(virtualDto))
      return Collections.emptyList();

    return virtualDto.getChildren().stream()
        .filter(this::isDtoEnabledForBothPlatforms)
        .map(StreamAndBetDto::getId)
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private boolean isDtoEnabledForBothPlatforms(StreamAndBetDto dto) {
    return dto.getAndroidActive() && dto.getIosActive();
  }

  private boolean isDtoDisabledForBothPlatforms(StreamAndBetDto dto) {
    return !dto.getAndroidActive() && !dto.getIosActive();
  }

  private Optional<List<StreamAndBetDto>> getDto() {
    return cmsApiService.getStreamAndBetDto();
  }

  protected void scheduleDataRefresh(List<OutputEvent> events) {

    Map<Long, Long> eventMillisToStart =
        events.stream()
            .collect(Collectors.toMap(OutputEvent::getId, OutputEvent::getMillisUntilStart));

    log.info("About to schedule refresh for events: {}", eventMillisToStart);

    updateScheduler.schedule(
        events.stream()
            .map(OutputEvent::getMillisUntilStart)
            .min(Comparator.comparing(Long::longValue))
            .orElseThrow(
                () ->
                    new IllegalStateException(
                        "Error finding the nearest event. Apparently there was no events passed")));
  }

  /** requested by business */
  private int getSportPriority(CategoryToUpcomingEvent category) {
    int priority = SPORT_PRIORITIES.indexOf(category.getId());
    return priority >= 0 ? priority : Integer.MAX_VALUE;
  }

  private List<OutputEvent> getOneUpcomingEventForEachClassId(List<String> classIds) {
    return siteServerApi
        .getNextNEventsForClass(
            1,
            classIds,
            getEventsStartInConfiguredSecondsAfterNowFilter(),
            SiteServerImpl.EMPTY_EXISTS_FILTER,
            false)
        .orElse(Collections.emptyList())
        .stream()
        .map(event -> eventMapper.map(new OutputEvent(), event))
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private SimpleFilter getEventsStartInConfiguredSecondsAfterNowFilter() {
    LocalDateTime nowPlus10Seconds =
        LocalDateTime.now(Clock.systemUTC()).plusSeconds(minimumSecondsUntilStart);
    return (SimpleFilter)
        new SimpleFilter.SimpleFilterBuilder()
            .addBinaryOperation(
                "event.startTime",
                BinaryOperation.greaterThanOrEqual,
                Instant.now().plusSeconds(EVENT_START_TIME))
            .build();
  }

  private List<Category> getCategories(List<Integer> idsToExclude, List<Integer> idsToInclude) {
    return siteServerApi
        .getClasses(
            getCategoriesSimpleFilter(idsToExclude, idsToInclude),
            SiteServerImpl.EMPTY_EXISTS_FILTER)
        .orElse(Collections.emptyList());
  }

  protected List<String> extractIdsFromCategories(List<Category> categories) {
    return categories.stream()
        .map(Category::getId)
        .map(String::valueOf)
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private SimpleFilter getCategoriesSimpleFilter(
      List<Integer> idsToExclude, List<Integer> idsToInclude) {
    SimpleFilter.SimpleFilterBuilder builder =
        new SimpleFilter.SimpleFilterBuilder()
            .addBinaryOperation("class.categoryId", BinaryOperation.equals, virtualCategoryId)
            .addUnaryOperation("class.isActive", UnaryOperation.isTrue)
            .addUnaryOperation("class.hasNext24HourEvent", UnaryOperation.isTrue)
            .addUnaryOperation("class.hasOpenEvent", UnaryOperation.isTrue);
    idsToExclude.forEach(i -> builder.addBinaryOperation("class.id", BinaryOperation.notEquals, i));
    idsToInclude.forEach(i -> builder.addBinaryOperation("class.id", BinaryOperation.equals, i));
    return (SimpleFilter) builder.build();
  }
}
