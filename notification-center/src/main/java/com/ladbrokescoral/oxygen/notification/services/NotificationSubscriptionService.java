package com.ladbrokescoral.oxygen.notification.services;

import static com.ladbrokescoral.oxygen.notification.entities.MessageType.STREAM_STARTING;

import com.ladbrokescoral.oxygen.notification.entities.Item;
import com.ladbrokescoral.oxygen.notification.entities.ItemEmpty;
import com.ladbrokescoral.oxygen.notification.entities.ItemEmptys;
import com.ladbrokescoral.oxygen.notification.entities.Items;
import com.ladbrokescoral.oxygen.notification.entities.dto.ChannelDTO;
import com.ladbrokescoral.oxygen.notification.entities.dto.SubscriptionDTO;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.services.repositories.ChannelRepository;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import com.ladbrokescoral.oxygen.notification.utils.ObjectMapper;
import com.newrelic.api.agent.Trace;
import java.text.ParseException;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.time.DateUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Component;

/** Handles a logic of saving subscriptions */
@Slf4j
@Component
public class NotificationSubscriptionService {

  private final ChannelRepository channelRepository;
  private final Subscriptions subscriptions;
  private final StringRedisTemplate redisTemplate;
  private final EventService eventService;
  private final SiteServerApiService siteServerApiService;

  private long eventExpirationTime;

  private static final Long EXPIRY_HOURS = 24L;

  @Value("${matchAlert.expiration.time:86400}")
  private long matchAlertExpirationTime;

  @Autowired
  public NotificationSubscriptionService(
      @Qualifier("StringRedisTemplate") StringRedisTemplate redisTemplate,
      @Value("${application.event.expiration.time}") Long eventExpirationTime,
      EventService eventService,
      ChannelRepository channelRepository,
      SiteServerApiService siteServerApiService,
      Subscriptions subscriptions) {
    this.eventExpirationTime = eventExpirationTime;
    this.eventService = eventService;
    this.redisTemplate = redisTemplate;
    this.siteServerApiService = siteServerApiService;
    this.channelRepository = channelRepository;
    this.subscriptions = subscriptions;
  }

  /**
   * Obtains and saves channels if there are any (for liveserv based notifications only) Obtains
   * existing and creates new subscriptions for given request. Overrides subscriptions if necessary
   * Creates subscriptions for internal (in-Microservice) services, that handle manual updates
   * (absent on liveserv or kafka) Unsubscribes if it the request has empty list of types
   */
  public Item save(Item item) {
    List<ChannelDTO> channels = saveChannels(item);
    List<SubscriptionDTO> existingSubscriptions = getExistingSubscriptions(item);
    List<SubscriptionDTO> newSubscriptions = ObjectMapper.toSubscriptionDTO(item);
    Event event = eventService.process(item.getEventId());

    logger.info(
        "[SUBSCRIPTION FLOW][{}] Obtained: channels - {}, existed subscriptions - {}, new subscriptions - {}, event - {}",
        item.getEventId(),
        channels.toString(),
        existingSubscriptions.toString(),
        newSubscriptions.toString(),
        event.toString());

    overrideExistingSubscriptions(existingSubscriptions, item);
    saveNewSubscriptions(newSubscriptions, existingSubscriptions, event);

    return item.setListOfChannelId(
            channels.stream().map(ChannelDTO::getId).collect(Collectors.toList()))
        .setSportUri(event.getSportUri());
  }

  private List<ChannelDTO> saveChannels(Item item) {
    return ObjectMapper.toChannelDTO(item).stream()
        .parallel()
        .map(
            channel -> {
              Optional<ChannelDTO> channelDTO =
                  channelRepository.findByName(channel.getName()).stream().findFirst();
              return channelDTO.orElseGet(
                  () -> channelRepository.save(channel.setExpiration(eventExpirationTime)));
            })
        .filter(Objects::nonNull)
        .map(
            s -> {
              redisTemplate.convertAndSend("channel", s.getName());
              return s;
            })
        .collect(Collectors.toList());
  }

  /**
   * Gets subscriptions from the database (redis), that match valid token and platform, given in
   * request
   *
   * @param item a request for new subscription
   * @return subscriptions that match, as a list
   */
  private List<SubscriptionDTO> getExistingSubscriptions(Item item) {
    return subscriptionsForEvent(item.getEventId())
        .parallelStream()
        .filter(s -> Objects.nonNull(s.getToken()))
        .filter(s -> s.getToken().equalsIgnoreCase(item.getToken()))
        .filter(
            s ->
                s.getPlatform() != null
                    && s.getPlatform().getName().equalsIgnoreCase(item.getPlatform()))
        .collect(Collectors.toList());
  }

  /**
   * Saves new subscriptions in Redis storage Subscribes for going_down if necessary Maps OpenBet
   * Event id to IGameMedia Event id
   */
  private void saveNewSubscriptions(
      List<SubscriptionDTO> newSubscriptions,
      List<SubscriptionDTO> existedSubscriptions,
      Event event) {
    newSubscriptions.stream()
        .filter(s -> !existedSubscriptions.contains(s))
        .map(
            (SubscriptionDTO sub) -> {
              Long maToExpire = matchAlertExpiryTime(event.getStartTime());
              logger.info("MatchAlert To Expire: {} ", maToExpire);
              sub.setStartTime(event.getStartTime());
              sub.setExpiration(maToExpire);
              return sub;
            })
        .map(this.subscriptions::save)
        .filter(dto -> dto.getType().equals(STREAM_STARTING.getType()))
        .forEach(this::mapIGameMediaId);
  }

  /**
   * Maps OpenBet Event id to IGameMedia Event id. If there is a match - adds iGameMediaId field to
   * the event in a database
   *
   * @param subscription which event's id is going to be mapped
   */
  private void mapIGameMediaId(SubscriptionDTO subscription) {
    siteServerApiService
        .getIGameMediaIdForEvent(String.valueOf(subscription.getEventId()))
        .map(subscription::setIGameMediaId)
        .map(subscriptions::save)
        .orElseGet(
            () -> {
              subscriptions.delete(subscription);
              return subscription;
            });
  }

  /** Overrides new subscriptions in Redis storage */
  private void overrideExistingSubscriptions(
      List<SubscriptionDTO> existedSubscriptions, Item item) {
    existedSubscriptions.stream()
        .filter(s -> !item.getTypes().contains(s.getType()))
        .map(
            dto -> {
              subscriptions.delete(dto);
              return dto;
            })
        .forEach(
            dto ->
                logger.info(
                    "[SUBSCRIPTION FLOW][{}] Deleted subscription: {}",
                    dto.getEventId(),
                    dto.toString()));
  }

  @Trace(dispatcher = true)
  public Item get(ItemEmpty item) {
    List<String> types =
        subscriptionsForEvent(item.getEventId())
            .parallelStream()
            .filter(s -> item.getToken().equalsIgnoreCase(s.getToken()))
            .map(SubscriptionDTO::getType)
            .distinct()
            .collect(Collectors.toList());
    return Item.builder()
        .eventId(item.getEventId())
        .token(item.getToken())
        .types(types)
        .platform(item.getPlatform())
        .listOfChannelId(Collections.emptyList())
        .sportUri(
            eventService.getProcessedEvent(item.getEventId()).map(Event::getSportUri).orElse(null))
        .appVersionInt(item.getAppVersionInt())
        .build();
  }

  @Trace(dispatcher = true)
  public List<Items> get(ItemEmptys item) {
    return item.getEventId().stream()
        .map(
            (Long eventId) -> {
              List<String> types =
                  subscriptionsForEvent(eventId)
                      .parallelStream()
                      .filter(s -> item.getToken().equalsIgnoreCase(s.getToken()))
                      .map(SubscriptionDTO::getType)
                      .distinct()
                      .collect(Collectors.toList());
              return getItems(eventId, item, types);
            })
        .collect(Collectors.toList());
  }

  public Items getItems(Long eventId, ItemEmptys item, List<String> types) {
    return Items.builder()
        .eventId(eventId)
        .token(item.getToken())
        .types(types)
        .platform(item.getPlatform())
        .listOfChannelId(Collections.emptyList())
        .sportUri(eventService.getProcessedEvent(eventId).map(Event::getSportUri).orElse(null))
        .appVersionInt(item.getAppVersionInt())
        .isEnable(!types.isEmpty())
        .build();
  }

  private List<SubscriptionDTO> subscriptionsForEvent(long eventId) {
    return subscriptions.findByEventId(eventId);
  }

  public Long getNoTTLRecords(int page, int size) {
    Pageable pageable = PageRequest.of(page, size);
    return subscriptions.findAll(pageable).toList().stream()
        .filter(Objects::nonNull)
        .filter(this::deleteSubscription)
        .count();
  }

  private boolean deleteSubscription(SubscriptionDTO subscriptionDTO) {
    boolean flag = false;
    logger.info("deleteSubscription SubscriptionDTO value {}", subscriptionDTO);
    if (eventStartTimeCompare(subscriptionDTO.getStartTime())) {
      logger.info("deleteSubscription if condition {}", subscriptionDTO);
      subscriptions.delete(subscriptionDTO);
      flag = true;
    } else {
      flag = false;
    }
    return flag;
  }

  public static boolean eventStartTimeCompare(String startTime) {
    Date startTimePattern = null;
    try {
      startTimePattern =
          DateUtils.parseDate(
              startTime,
              "yyyy-MM-dd'T'HH:mm:ssZ",
              "yyyy-MM-dd'T'HH:mm:ss.sssZ",
              "yyyy-MM-dd'T'HH:mm:ssX",
              "yyyy-MM-dd'T'HH:mm:ss.sssX");
    } catch (ParseException e) {
      logger.error("eventStartTimeCompare exception  {} ", e.getMessage());
      return false;
    }
    LocalDateTime eventStartTime =
        startTimePattern
            .toInstant()
            .atZone(ZoneId.systemDefault())
            .toLocalDateTime()
            .plusHours(EXPIRY_HOURS);
    return eventStartTime.isBefore(LocalDateTime.now());
  }

  private Long matchAlertExpiryTime(String startTime) {
    Date startTimePattern = null;
    try {
      startTimePattern =
          DateUtils.parseDate(
              startTime,
              "yyyy-MM-dd'T'HH:mm:ssZ",
              "yyyy-MM-dd'T'HH:mm:ss.sssZ",
              "yyyy-MM-dd'T'HH:mm:ssX",
              "yyyy-MM-dd'T'HH:mm:ss.sssX");
    } catch (ParseException e) {
      logger.error("matchAlertExpiryTime exception  {} ", e.getMessage());
      return -1L;
    }
    LocalDateTime eventStartTime =
        startTimePattern
            .toInstant()
            .atZone(ZoneId.systemDefault())
            .toLocalDateTime()
            .plusSeconds(matchAlertExpirationTime);
    return LocalDateTime.now().until(eventStartTime, ChronoUnit.SECONDS);
  }
}
