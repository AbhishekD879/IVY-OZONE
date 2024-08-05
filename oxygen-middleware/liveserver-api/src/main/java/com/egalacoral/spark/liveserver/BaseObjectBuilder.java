package com.egalacoral.spark.liveserver;

import static com.coral.oxygen.middleware.common.configuration.DistributedKey.LIVE_SERVER_MODULE_MAP;

import com.coral.oxygen.middleware.common.service.DefaultCommentaryValuesType;
import com.egalacoral.spark.liveserver.meta.EventMetaInfo;
import com.egalacoral.spark.liveserver.meta.EventMetaInfoRepository;
import com.egalacoral.spark.liveserver.utils.JsonMapper;
import com.ladbrokescoral.scoreboards.parser.api.BipParserFactory;
import com.ladbrokescoral.scoreboards.parser.model.BipComment;
import com.ladbrokescoral.scoreboards.parser.model.Comment;
import com.ladbrokescoral.scoreboards.parser.model.EventCategory;
import java.math.BigInteger;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.apache.commons.lang3.math.NumberUtils;
import org.springframework.util.CollectionUtils;

/** Created by Aliaksei Yarotski on 9/19/17. */
@Slf4j
public class BaseObjectBuilder {

  private final BaseObject baseObject;
  private BaseObject scbrdObject;
  private Message message;
  private boolean isValidMessage = true;
  private int clientId = -1;
  private JsonMapper jsonMapper;
  private static final String EVENT_ID_NOT_RESOLVED_TEMPLATE =
      "Event ID can't be resolved for message {}";

  private EventMetaInfoRepository eventMetaInfoRepository;

  public BaseObjectBuilder() {
    this.baseObject = new BaseObject();
  }

  public BaseObjectBuilder message(Message message) {
    if (StringUtils.isBlank(message.getBody())) {
      isValidMessage = false;
    }
    if (message.getBody().length() < 34) {
      isValidMessage = false;
    }
    this.message = message;
    return this;
  }

  private <T> T readData(Class<T> targetType) {
    return jsonMapper.read(message.getJsonData(), targetType);
  }

  public static BaseObjectBuilder create(Message message, JsonMapper jsonMapper) {
    return new BaseObjectBuilder().message(message).jsonMapper(jsonMapper);
  }

  private BaseObjectBuilder jsonMapper(JsonMapper jsonMapper) {
    this.jsonMapper = jsonMapper;
    return this;
  }

  public BaseObjectBuilder eventMetaInfoRepository(
      EventMetaInfoRepository eventMetaInfoRepository) {
    this.eventMetaInfoRepository = eventMetaInfoRepository;
    return this;
  }

  public BaseObjectBuilder clientId(Integer clientId) {
    this.clientId = clientId;
    return this;
  }

  private BaseObject fromMessage() {
    if (!isValidMessage) {
      return null;
    }
    this.baseObject.setPublishedDate(message.getPublishedDate());
    this.baseObject.setType(fromBody(29, 5));
    BigInteger entityId = new BigInteger(fromBody(7, 10));
    switch (this.baseObject.getType()) {
      case "PRICE", "PSTRM":
        this.baseObject.setEvent(
            new BaseObject.Event()
                .eventId(
                    eventMetaInfoRepository
                        .getBySelectionId(entityId)
                        .map(EventMetaInfo::getEventId)
                        .orElseGet(
                            () -> {
                              isValidMessage = false;
                              log.error(EVENT_ID_NOT_RESOLVED_TEMPLATE, message.toString());
                              return null;
                            }))
                .market(
                    new BaseObject.Market()
                        .outcome(
                            new BaseObject.Outcome()
                                .outcomeId(new BigInteger(fromBody(34, 10)))
                                .price(
                                    jsonMapper.read(
                                        message.getJsonData(), BaseObject.Price.class)))));
        break;
      case "EVMKT":
        this.baseObject.setEvent(
            new BaseObject.Event()
                .eventId(
                    eventMetaInfoRepository
                        .getByMarketId(entityId)
                        .map(EventMetaInfo::getEventId)
                        .orElseGet(
                            () -> {
                              isValidMessage = false;
                              log.error(EVENT_ID_NOT_RESOLVED_TEMPLATE, message.toString());
                              return null;
                            }))
                .market(
                    readData(BaseObject.Market.class)
                        .marketId(Integer.parseInt(fromBody(34, 10)))
                        .outcome(new BaseObject.Outcome())));
        break;
      case "SELCN":
        this.baseObject.setEvent(new BaseObject.Event());
        this.baseObject
            .getEvent()
            .eventId(
                eventMetaInfoRepository
                    .getBySelectionId(entityId)
                    .map(EventMetaInfo::getEventId)
                    .orElseGet(
                        () -> {
                          isValidMessage = false;
                          log.error(EVENT_ID_NOT_RESOLVED_TEMPLATE, message.toString());
                          return null;
                        }))
            .market(new BaseObject.Market());
        this.baseObject
            .getEvent()
            .getMarket()
            .setOutcome(
                jsonMapper
                    .read(message.getJsonData(), BaseObject.Outcome.class)
                    .outcomeId(new BigInteger(fromBody(34, 10))));
        this.baseObject
            .getEvent()
            .getMarket()
            .marketId(this.baseObject.getEvent().getMarket().getOutcome().getEvMktId());
        this.baseObject.getEvent().getMarket().getOutcome().setEvMktId(null);

        this.baseObject
            .getEvent()
            .getMarket()
            .getOutcome()
            .price(
                new BaseObject.Price()
                    .lpDen(this.baseObject.getEvent().getMarket().getOutcome().getLpDen())
                    .lpNum(this.baseObject.getEvent().getMarket().getOutcome().getLpNum()));
        break;
      case "EVENT":
        this.baseObject.setEvent(jsonMapper.read(message.getJsonData(), BaseObject.Event.class));
        this.baseObject.getEvent().setEventId(entityId);
        this.baseObject
            .getEvent()
            .market(new BaseObject.Market().outcome(new BaseObject.Outcome()));
        this.scbrdObject =
            eventMetaInfoRepository.getByEventId(entityId).map(this::buildScbrdObject).orElse(null);
        break;
      case "SCBRD":
        this.baseObject.setEvent(
            new BaseObject.Event()
                .eventId(entityId)
                .scoreboard(readData(BaseObject.Scoreboard.class)));
        updateScoresCheckForReverseOrder(this.baseObject.getEvent().getScoreboard());
        break;
      case "CLOCK":
        this.baseObject.setEvent(
            new BaseObject.Event().eventId(entityId).clock(readData(BaseObject.Clock.class)));

        this.baseObject.getEvent().getClock().setEvId(null);
        break;
      default:
        isValidMessage = false;
        log.debug(
            "Invalid message for type {} from client #{}, \n BODY-> {}",
            baseObject.getType(),
            clientId,
            message.getBody());
        return null;
    }
    log.debug(
        "incoming message {}:{} from Body #{}",
        baseObject.getType(),
        baseObject.getEvent().getEventId(),
        message.getBody());
    return baseObject;
  }

  public String buildMessageKey() {
    return baseObject.getEvent().getEventId().toString();
  }

  private void updateScoresCheckForReverseOrder(BaseObject.Scoreboard scoreboard) {
    if (checkIfPlayerIdHasPresentInReverseOrder(scoreboard.all())) {
      reverseList(scoreboard.all(), 0, 1);
      reverseList(scoreboard.current(), 0, 1);
      int size = scoreboard.subperiod().size();
      reverseList(scoreboard.subperiod(), size - 2, size - 1);
    }
  }

  private void reverseList(List<BaseObject.EventDetails> eventDetails, int fromIndex, int toIndex) {
    try {
      BaseObject.EventDetails tempEvent = eventDetails.get(fromIndex);
      eventDetails.set(fromIndex, eventDetails.get(toIndex));
      eventDetails.set(toIndex, tempEvent);
    } catch (Exception ex) {
      log.info(
          "exception while reversing the order for scoreboard for {} and indexes {}: {}",
          eventDetails,
          fromIndex,
          toIndex);
    }
  }

  private boolean checkIfPlayerIdHasPresentInReverseOrder(
      List<BaseObject.EventDetails> eventDetails) {
    try {
      if (!CollectionUtils.isEmpty(eventDetails)) {
        return DefaultCommentaryValuesType.PLAYER_2
                .getValue()
                .equalsIgnoreCase(eventDetails.get(0).getRoleCode())
            && DefaultCommentaryValuesType.PLAYER_1
                .getValue()
                .equalsIgnoreCase(eventDetails.get(1).getRoleCode());
      }
    } catch (Exception ex) {
      log.info("exception while reading all for player swap", ex);
    }
    return false;
  }

  private String buildCacheName() {
    return LIVE_SERVER_MODULE_MAP.toString() + ':' + baseObject.getEvent().getEventId();
  }

  public String buildCacheKey() {
    return buildCacheName() + ":" + this.baseObject.getType();
  }

  public String buildScbdCacheKey() {
    return buildCacheName() + ":" + this.scbrdObject.getType();
  }

  private BaseObject buildScbrdObject(EventMetaInfo eventMetaInfo) {
    if (this.baseObject.getEvent() == null) {
      return null;
    }
    Optional<EventCategory> eventCategory = EventCategory.from(eventMetaInfo.getCategoryId());
    if (!eventCategory.isPresent()) {
      log.warn(
          "Category {} not supported by score parser. EventId={}",
          eventMetaInfo.getCategoryId(),
          eventMetaInfo.getEventId());
      return null;
    }
    BipComment bipComment =
        BipParserFactory.getParser(eventCategory.get())
            .parse(this.baseObject.getEvent().getName().getEn());

    if (!bipComment.isValid()) {
      return null;
    }

    this.baseObject.getEvent().getName().setEn(bipComment.getEventName());

    BaseObject scbrd = new BaseObject();
    scbrd.setType("SCBRD");
    scbrd.setPublishedDate(baseObject.getPublishedDate());

    BaseObject.Scoreboard scoreboard = new BaseObject.Scoreboard();
    final Comment playerHomeComment = bipComment.getPlayerHomeComment();
    final Comment playerAwayComment = bipComment.getPlayerAwayComment();
    Integer eventId =
        NumberUtils.isDigits(this.message.getEvenId())
            ? Integer.valueOf(this.message.getEvenId())
            : null;
    scoreboard
        .all()
        .addAll(
            Arrays.asList(
                BaseObject.EventDetails.builder()
                    .evId(eventId)
                    .value(playerHomeComment.getScore())
                    .active(playerHomeComment.getServing())
                    .buildHomeEventScore(),
                BaseObject.EventDetails.builder()
                    .evId(eventId)
                    .value(playerAwayComment.getScore())
                    .active(playerAwayComment.getServing())
                    .buildAwayEventScore()));
    if (playerHomeComment.getCurrentPoints() != null
        && playerAwayComment.getCurrentPoints() != null) {
      scoreboard
          .current()
          .addAll(
              Arrays.asList(
                  BaseObject.EventDetails.builder()
                      .evId(eventId)
                      .value(playerHomeComment.getCurrentPoints())
                      .active(playerHomeComment.getServing())
                      .buildHomeEventScore(),
                  BaseObject.EventDetails.builder()
                      .evId(eventId)
                      .value(playerAwayComment.getCurrentPoints())
                      .active(playerAwayComment.getServing())
                      .buildAwayEventScore()));
    }

    if (playerHomeComment.getPeriodScore() != null && playerAwayComment.getPeriodScore() != null) {
      scoreboard
          .subperiod()
          .addAll(
              Arrays.asList(
                  BaseObject.EventDetails.builder()
                      .evId(eventId)
                      .value(playerHomeComment.getPeriodScore())
                      .active(playerHomeComment.getServing())
                      .buildHomeEventScore(),
                  BaseObject.EventDetails.builder()
                      .evId(eventId)
                      .value(playerAwayComment.getPeriodScore())
                      .active(playerAwayComment.getServing())
                      .buildAwayEventScore()));
    }

    scbrd.setEvent(
        new BaseObject.Event()
            .eventId(this.baseObject.getEvent().getEventId())
            .scoreboard(scoreboard));

    return scbrd;
  }

  private String fromBody(int start, int length) {
    return substr(message.getBody(), start, length);
  }

  protected static String substr(String s, int start, int length) {
    return s.substring(start, start + length);
  }

  /**
   * For Test only.
   *
   * <p>Returns BaseObject in case the state of the builder is valid otherwise returns null
   */
  protected BaseObject build() {
    if (!isValidMessage || message == null) {
      return null;
    }
    BaseObject thisBaseObject = fromMessage();
    if (!isValidMessage) {
      return null;
    }
    return thisBaseObject;
  }

  /** Returns JSON BaseObject in case the state of the builder is valid otherwise returns null */
  public String toJsonString() {
    if (!isValidMessage || message == null) {
      return null;
    }
    return jsonMapper.write(build());
  }

  public boolean isValidMessage() {
    return isValidMessage;
  }

  public boolean isScbrdObjectValid() {
    return scbrdObject != null;
  }

  public String scbrdToJsonString() {
    return jsonMapper.write(this.scbrdObject);
  }
}
