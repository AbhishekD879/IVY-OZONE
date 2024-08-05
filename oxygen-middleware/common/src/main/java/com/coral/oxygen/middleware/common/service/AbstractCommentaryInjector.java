package com.coral.oxygen.middleware.common.service;

import static java.util.stream.Collectors.toList;
import static java.util.stream.Collectors.toSet;
import static org.springframework.util.CollectionUtils.isEmpty;

import com.coral.oxygen.cms.api.SystemConfigProvider;
import com.coral.oxygen.middleware.common.service.commentary.CommentaryService;
import com.coral.oxygen.middleware.common.service.commentary.FactScore;
import com.coral.oxygen.middleware.common.service.commentary.Period;
import com.coral.oxygen.middleware.common.service.commentary.TeamScore;
import com.coral.oxygen.middleware.pojos.model.output.Clock;
import com.coral.oxygen.middleware.pojos.model.output.Comment;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.scoreboards.parser.api.BipParserFactory;
import com.ladbrokescoral.scoreboards.parser.model.BipComment;
import com.ladbrokescoral.scoreboards.parser.model.EventCategory;
import com.newrelic.api.agent.NewRelic;
import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.joda.time.DateTime;
import org.springframework.beans.factory.annotation.Autowired;

@Slf4j
public class AbstractCommentaryInjector {

  private CommentaryService commentaryService;

  private static final Map<String, String> footballRoleCode;
  private static final Set<String> BIP_CATEGORY_CODES =
      Stream.of(EventCategory.values()).map(Enum::name).collect(toSet());

  private static final String FOOTBALL = "16";
  private static final String BASKETBALL = "6";
  private static final String TENNIS = "34";

  private static final String BADMINTON = "51";
  protected static final String HOME_ROLE_CODE = "home";
  protected static final String AWAY_ROLE_CODE = "away";

  static {
    footballRoleCode = new HashMap<>();
    footballRoleCode.put("team_1", HOME_ROLE_CODE);
    footballRoleCode.put("team_2", AWAY_ROLE_CODE);
  }

  private final AbstractSiteServeService siteServerService;
  private final SystemConfigProvider systemConfigProvider;

  public AbstractCommentaryInjector(
      AbstractSiteServeService siteServerService, SystemConfigProvider systemConfigProvider) {
    this.siteServerService = siteServerService;
    this.systemConfigProvider = systemConfigProvider;
  }

  protected void injectData(List<Long> eventsIds, Collection<EventsModuleData> events) {
    injectWithSiteServerApi(eventsIds, events);
    injectWithBipScoreParser(events);
  }

  private void injectWithSiteServerApi(List<Long> eventsIds, Collection<EventsModuleData> events) {
    List<String> footballBasketballTennisBadbintonIds =
        events.stream()
            .filter(
                e ->
                    eventsIds.contains(e.getId())
                        && Arrays.asList(FOOTBALL, BASKETBALL, TENNIS, BADMINTON)
                            .contains(e.getCategoryId()))
            .map(e -> e.getId().toString())
            .collect(toList());
    Map<String, Event> commentsMap =
        siteServerService.getCommentaryForEvent(footballBasketballTennisBadbintonIds);
    events.stream()
        .filter(event -> event.getId() != null)
        .filter(event -> commentsMap.containsKey(String.valueOf(event.getId())))
        .forEach(event -> populateEvent(event, commentsMap.get(String.valueOf(event.getId()))));
  }

  protected void injectWithBipScoreParser(Collection<EventsModuleData> events) {
    Set<String> cmsBipScoreCategories = getBipScoreCategoriesFromCms();
    events.stream()
        .filter(event -> cmsBipScoreCategories.contains(event.getCategoryId()))
        .filter(this::isSupportedByBipScoreParser)
        .forEach(this::populateEventWithNameAndCommentary);
  }

  private boolean isSupportedByBipScoreParser(EventsModuleData event) {
    if (BIP_CATEGORY_CODES.contains(event.getCategoryCode())) {
      return true;
    } else {
      log.warn(
          "Ignored event id '{}' while processing Bip scores as category '{}' doesn't support Bip scores. Check CMS system configuration.",
          event.getId(),
          event.getCategoryCode());
      return false;
    }
  }

  private Set<String> getBipScoreCategoriesFromCms() {
    return systemConfigProvider.systemConfig().getBipScoreEvents().entrySet().stream()
        .filter(Map.Entry::getValue)
        .map(Map.Entry::getKey)
        .collect(Collectors.toSet());
  }

  /**
   * event.getSsName() - 'name' field returned by cms event.getName() - 'overrideName' field
   * returned by cms
   *
   * @param event
   */
  protected void populateEventWithNameAndCommentary(EventsModuleData event) {
    if (Objects.nonNull(event.getComments())) {
      return;
    }
    BipComment bipComment =
        parseNameWithBipScoreParser(
            event.getSsName() == null ? event.getName() : event.getSsName(),
            event.getCategoryCode());

    if (event.getSsName() != null) {
      BipComment bipCommentFromNameOverride =
          parseNameWithBipScoreParser(event.getName(), event.getCategoryCode());
      event.setName(bipCommentFromNameOverride.getEventName());
    } else {
      event.setName(bipComment.getEventName());
    }

    if (bipComment.getPlayerAComment() != null && bipComment.getPlayerBComment() != null) {
      Comment comment =
          commentaryService.populateCommentaryFromEventName(event.getId(), bipComment);
      if (!Objects.isNull(comment) && Objects.isNull(comment.getTeams())) {
        Map<String, Object> teams = new HashMap<>();
        teams.put(HOME_ROLE_CODE, bipComment.getPlayerAComment());
        teams.put(AWAY_ROLE_CODE, bipComment.getPlayerBComment());
        comment.setTeams(teams);
      }
      event.setComments(comment);
    }
  }

  private BipComment parseNameWithBipScoreParser(String eventName, String eventCategoryCode) {
    return BipParserFactory.getParser(EventCategory.valueOf(eventCategoryCode)).parse(eventName);
  }

  protected void populateComments(EventsModuleData event, Event comments) {
    List<Map<String, Object>> eventParticipants = comments.getEventParticipants();
    List<Map<String, Object>> eventPeriods = comments.getEventPeriods();
    Comment comment = new Comment();
    if (!isEmpty(eventParticipants)) {
      Map<String, Object> teams = new HashMap<>();
      eventParticipants.forEach(
          ep -> teams.put(getCorrectRoleCodeForFootball(String.valueOf(ep.get("roleCode"))), ep));
      comment.setTeams(teams);
      if (!isEmpty(eventPeriods)) {
        List<Map<String, Object>> facts =
            (List) eventPeriods.get(eventPeriods.size() - 1).get(CommentaryField.CHILDREN);
        facts.stream()
            .map(f -> f.get(CommentaryField.EVENT_FACT))
            .filter(Objects::nonNull)
            .map(ef -> (Map<String, Object>) ef)
            .forEach(ef -> addFact(teams, ef));
      }
    }

    if (!isEmpty(eventPeriods)) {
      comment.setFacts(
          (List) eventPeriods.get(eventPeriods.size() - 1).get(CommentaryField.CHILDREN));
    }

    if (comment.getFacts() != null || comment.getTeams() != null) {
      event.setComments(comment);
    }
  }

  protected void populateFootballComments(EventsModuleData event, Event comments) {
    if (isEmpty(comments.getChildren())) {
      return;
    }
    Period rootPeriod = null;
    TeamScore home = null;
    TeamScore away = null;
    Comment comment = new Comment();
    Map<String, Object> teams = new HashMap<>();
    for (Children children : comments.getChildren()) {
      TeamScore team = new TeamScore(children.getEventParticipant());
      if (children.getEventPeriod() != null) { // ALL periods.
        rootPeriod = new Period(children.getEventPeriod());
        comment.setFacts((List<Object>) rootPeriod.getField(Period.FieldNames.children));
      } else if (!team.isEmpty()
          && ("HOME".equals(team.getRoleCode()) || "TEAM_1".equals(team.getRoleCode()))) {
        home = team;
        teams.put(HOME_ROLE_CODE, home.toMap());
      } else if (!team.isEmpty()
          && ("AWAY".equals(team.getRoleCode()) || "TEAM_2".equals(team.getRoleCode()))) {
        away = team;
        teams.put(AWAY_ROLE_CODE, away.toMap());
      } else {
        log.warn("Unknown type of the children -> {}", children);
      }
    }
    if (home != null && away != null) {
      comment.setTeams(teams);
    }
    if (home != null && away != null && rootPeriod != null) {
      calculateScoreFromEventPeriodChildren(home, away, rootPeriod);
    }
    event.setComments(comment);
  }

  protected void calculateScoreFromEventPeriodChildren(
      TeamScore home, TeamScore away, Period rootPeriod) {
    List<Period> subPeriods = rootPeriod.extractSubPeriods();
    if (subPeriods.isEmpty()) {
      parseScoresFromPeriodTypeAll(home, away, rootPeriod);
    } else {
      calculateScores(home, away, subPeriods);
    }
  }

  private void parseScoresFromPeriodTypeAll(TeamScore home, TeamScore away, Period rootPeriod) {
    FactScore[] allPeriodScores = rootPeriod.extractScores(home.getId());
    if (allPeriodScores.length >= 2) {
      home.setScore(String.valueOf(allPeriodScores[0].getScore()));
      away.setScore(String.valueOf(allPeriodScores[1].getScore()));
    }
  }

  private void calculateScores(TeamScore home, TeamScore away, List<Period> subPeriods) {
    int homeScore = 0;
    int awayScore = 0;
    int homeExtraTimeScore = 0;
    int awayExtraTimeScore = 0;
    int homePenaltyScore = 0;
    int awayPenaltyScore = 0;

    for (Period period : subPeriods) {
      FactScore[] scores = period.extractScores(home.getId());
      if (scores.length < 2) {
        continue;
      }
      if (period.isMainPeriod()) {
        homeScore += scores[0].getScore();
        awayScore += scores[1].getScore();
      } else if (period.isExtraPeriod()) {
        homeScore += scores[0].getScore();
        awayScore += scores[1].getScore();
        homeExtraTimeScore += scores[0].getScore();
        awayExtraTimeScore += scores[1].getScore();
      } else if (period.isPenaltiesPeriod()) {
        homePenaltyScore = scores[0].getScore();
        awayPenaltyScore = scores[1].getScore();
      }
    }
    home.setScore(String.valueOf(homeScore));
    away.setScore(String.valueOf(awayScore));
    home.setExtraTimeScore(String.valueOf(homeExtraTimeScore));
    away.setExtraTimeScore(String.valueOf(awayExtraTimeScore));
    home.setPenaltyScore(String.valueOf(homePenaltyScore));
    away.setPenaltyScore(String.valueOf(awayPenaltyScore));
  }

  protected Map<String, Object> extractLatestPeriod(Event comments) {
    List<Map<String, Object>> eventPeriods = comments.getEventPeriods();
    if (eventPeriods != null) {
      for (Map<String, Object> eventPeriodRaw : eventPeriods) {
        if (eventPeriodRaw.get(CommentaryField.CHILDREN) != null) {
          List<Map<String, Object>> children = (List) eventPeriodRaw.get(CommentaryField.CHILDREN);
          List<Map> childPeriods =
              children.stream()
                  .map(child -> child.get(CommentaryField.EVENT_PERIOD))
                  .filter(o -> o instanceof Map)
                  .map(Map.class::cast)
                  .collect(Collectors.toList());
          if (!childPeriods.isEmpty()) {
            childPeriods.sort(
                Comparator.comparing(
                    period -> String.valueOf(period.get("startTime")),
                    Comparator.nullsLast(Comparator.reverseOrder())));
            return childPeriods.get(0);
          }
        }
      }
    }
    return null;
  }

  protected void populateEvent(EventsModuleData event, Event comments) {
    if ("tennis".equalsIgnoreCase(event.getCategoryCode())) {
      populateComments(event, comments);
      populateTennisData(event);

    } else if ("football".equalsIgnoreCase(event.getCategoryCode())) {
      populateFootballComments(event, comments);

    } else if ("basketball".equalsIgnoreCase(event.getCategoryCode())) {
      populateComments(event, comments);

    } else if ("badminton".equalsIgnoreCase(event.getCategoryCode())) {
      populateComments(event, comments);
      populateBadmintonData(event);
    }
  }

  private void populateTennisData(EventsModuleData event) {
    populateScoresIfCommentsExist(
        event,
        comments -> {
          List<Period> periods = Period.listFromFacts(comments.getFacts());
          comments.setSetsScores(getSetScores(periods));
          int runningSetIndex = getRunningSetIndex(periods);
          comments.setRunningSetIndex(runningSetIndex);
          comments.setRunningGameScores(getRunningGameScores(periods, runningSetIndex));
        });
  }

  private void populateBadmintonData(EventsModuleData event) {
    populateScoresIfCommentsExist(
        event,
        comments -> {
          List<Period> periods = Period.listFromFacts(comments.getFacts());
          comments.setSetsScores(getSetScores(periods));
          comments.setRunningSetIndex(getRunningSetIndex(periods));
        });
  }

  private void populateScoresIfCommentsExist(
      EventsModuleData event, Consumer<Comment> commentsConsumer) {
    Comment comments = event.getComments();
    if (comments != null && comments.getFacts() != null) {
      commentsConsumer.accept(comments);
    } else {
      String errorMsg =
          String.format(
              "Couldn't parse scores from SiteServer commentaries for event=%s. Comments are empty or without eventPeriods",
              event.getId());
      log.warn(errorMsg);
      NewRelic.noticeError(errorMsg);
    }
  }

  private String getCorrectRoleCodeForFootball(String code) {
    String codeLoverCase = code.toLowerCase();
    String result = footballRoleCode.get(codeLoverCase);
    if (result == null) {
      result = codeLoverCase;
    }
    return result;
  }

  private void addFact(Map<String, Object> teams, Map<String, Object> fact) {
    teams.values().stream()
        .filter(
            t -> {
              Map<String, Object> team = (Map<String, Object>) t;
              return team.get("id").equals(fact.get(CommentaryField.EVENT_PARTICIPANT_ID));
            })
        .forEach(
            t -> {
              Map<String, Object> team = (Map<String, Object>) t;
              team.put(
                  String.valueOf(fact.get(CommentaryField.FACT_CODE)).toLowerCase(),
                  fact.get("fact"));
            });
  }

  private int getRunningSetIndex(List<Period> periods) {
    return periods.stream()
        .filter(Period::isSet)
        .max(Comparator.comparingInt(Period::getPeriodIndex))
        .map(Period::getPeriodIndex)
        .orElse(0);
  }

  private Map<String, Object> getSetScores(List<Period> periods) {
    Map<String, Object> setScores = new HashMap<>();
    periods.stream()
        .filter(Period::isSet)
        .forEach(
            period -> {
              Integer setIndex = period.getPeriodIndex();
              Map<String, Object> scores = new HashMap<>();
              period
                  .getScoreFacts()
                  .forEach(
                      scoreFact ->
                          scores.put(
                              scoreFact.getEventParticipantId(), scoreFact.getField("fact")));
              setScores.put(String.valueOf(setIndex), scores);
            });
    return setScores;
  }

  private Map<String, Object> getRunningGameScores(List<Period> periods, int runningSetIndex) {
    Map<String, Object> runningGameScores = new HashMap<>();
    periods.stream()
        .filter(Period::isSet)
        .filter(period -> Objects.equals(period.getPeriodIndex(), runningSetIndex))
        .map(Period::getGamePeriods)
        .forEach(
            gamePeriods ->
                gamePeriods.stream()
                    .max(Comparator.comparingInt(Period::getPeriodIndex)) // get last game
                    .map(Period::getScoreFacts)
                    .orElse(Collections.emptyList())
                    .forEach(
                        scoreFact ->
                            runningGameScores.put(
                                scoreFact.getEventParticipantId(), scoreFact.getField("fact"))));
    return runningGameScores;
  }

  protected void populateClockData(EventsModuleData event, Event comments) {
    try {
      Map<String, Object> latestPeriod = extractLatestPeriod(comments);
      if (latestPeriod == null) {
        return;
      }
      Map<String, Object> periodClockState = getPeriodClockStateMap(latestPeriod);
      if (isEmpty(periodClockState)) {
        return;
      }

      Clock clock = new Clock();
      clock.setSport(event.getCategoryCode().toLowerCase());
      clock.setEv_id(convertOrNull(latestPeriod.get("eventId"), Long::parseLong));
      clock.setLast_update(stringOrNull(periodClockState.get(CommentaryField.LAST_UPDATE)));
      clock.setPeriod_code(stringOrNull(latestPeriod.get(CommentaryField.PERIOD_CODE)));
      clock.setState(stringOrNull(periodClockState.get("state")));
      clock.setClock_seconds(stringOrNull(periodClockState.get("offset")));
      clock.setLast_update_secs(
          convertOrNull(
              periodClockState.get(CommentaryField.LAST_UPDATE),
              v -> String.valueOf(DateTime.parse(v).getMillis() / 1000)));
      clock.setStart_time_secs(
          convertOrNull(
              event.getStartTime(), v -> String.valueOf(DateTime.parse(v).getMillis() / 1000)));

      DateTime creationTime =
          DateTime.parse(event.getResponseCreationTime()); // event.responseCreationTime
      DateTime periodClockStateLastUpdate =
          convertOrNull(
              periodClockState.get(CommentaryField.LAST_UPDATE),
              DateTime::parse); // latestPeriod.periodClockState.lastUpdate
      if (Objects.nonNull(periodClockStateLastUpdate)) {
        long deltaSeconds =
            TimeUnit.MILLISECONDS.toSeconds(
                Math.abs(creationTime.getMillis() - periodClockStateLastUpdate.getMillis()));
        clock.setOffset_secs(
            convertOrNull(
                periodClockState.get("offset"),
                v -> String.valueOf(Integer.parseInt(v) + deltaSeconds)));
      }
      event.setInitClock(clock);
    } catch (Exception e) {
      NewRelic.noticeError(e);
      log.error("Suppressed error creation clock data", e);
    }
  }

  private Map<String, Object> getPeriodClockStateMap(Map<String, Object> latestPeriod) {
    Map<String, Object> periodClockState = null;
    if (latestPeriod.get(CommentaryField.CHILDREN) instanceof Collection) {
      periodClockState =
          (Map)
              ((Collection) latestPeriod.get(CommentaryField.CHILDREN))
                  .stream()
                      .filter(e -> e instanceof Map)
                      .map(Map.class::cast)
                      .map(map -> ((Map) map).get("eventPeriodClockState"))
                      .filter(Objects::nonNull)
                      .findFirst()
                      .orElse(periodClockState);
    }
    return periodClockState;
  }

  private <R> R convertOrNull(Object o, Function<String, R> convertFunction) {
    return Optional.ofNullable(o).map(Object::toString).map(convertFunction).orElse(null);
  }

  private String stringOrNull(Object o) {
    return convertOrNull(o, Function.identity());
  }

  @Autowired
  public void setCommentaryService(CommentaryService commentaryService) {
    this.commentaryService = commentaryService;
  }

  /**
   * @deprecated cover by units tests: populateEvent; change code to use AbstractModel hierarchy,
   *     then remove CommentaryField
   */
  @Deprecated
  @NoArgsConstructor(access = AccessLevel.PRIVATE)
  protected static class CommentaryField {
    static final String EVENT_PERIOD = "eventPeriod";
    public static final String CHILDREN = "children";
    static final String PERIOD_CODE = "periodCode";
    static final String EVENT_FACT = "eventFact";
    static final String FACT_CODE = "factCode";
    static final String EVENT_PARTICIPANT_ID = "eventParticipantId";
    static final String LAST_UPDATE = "lastUpdate";
  }
}
