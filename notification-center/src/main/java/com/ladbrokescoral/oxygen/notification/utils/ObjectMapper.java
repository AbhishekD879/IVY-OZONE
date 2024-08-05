package com.ladbrokescoral.oxygen.notification.utils;

import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.FinalPosition;
import com.egalacoral.spark.siteserver.model.RacingResult;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.ladbrokescoral.oxygen.notification.entities.Item;
import com.ladbrokescoral.oxygen.notification.entities.Outcome;
import com.ladbrokescoral.oxygen.notification.entities.Position;
import com.ladbrokescoral.oxygen.notification.entities.WinAlertSubscriptionRequest;
import com.ladbrokescoral.oxygen.notification.entities.dto.ChannelDTO;
import com.ladbrokescoral.oxygen.notification.entities.dto.RacingDTO;
import com.ladbrokescoral.oxygen.notification.entities.dto.SubscriptionDTO;
import com.ladbrokescoral.oxygen.notification.entities.dto.WinAlertDTO;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.EventScores;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Meta;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.SportsBookUpdate;
import com.ladbrokescoral.oxygen.notification.mappers.ChannelMapper;
import com.ladbrokescoral.oxygen.notification.mappers.ItemMapper;
import com.ladbrokescoral.oxygen.notification.mappers.SubscriptionMapper;
import com.ladbrokescoral.oxygen.notification.services.ConsumeEventException;
import com.ladbrokescoral.oxygen.notification.services.handler.AbstractSportsbookUpdateMapper;
import com.ladbrokescoral.oxygen.notification.utils.types.CardType;
import com.ladbrokescoral.oxygen.notification.utils.types.GoalType;
import com.ladbrokescoral.oxygen.notification.utils.types.KickOffType;
import com.ladbrokescoral.oxygen.notification.utils.types.PeriodType;
import com.ladbrokescoral.oxygen.notification.utils.types.UnknownType;
import com.ladbrokescoral.scoreboards.parser.api.BipParser;
import com.ladbrokescoral.scoreboards.parser.api.BipParserFactory;
import com.ladbrokescoral.scoreboards.parser.model.BipComment;
import com.ladbrokescoral.scoreboards.parser.model.EventCategory;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import javax.validation.constraints.NotNull;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.BooleanUtils;
import org.joda.time.DateTime;
import org.joda.time.DateTimeZone;
import org.mapstruct.factory.Mappers;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.util.StringUtils;

@Slf4j
public class ObjectMapper {

  @Value("${event.category.id.greyhounds}")
  public static String categoryIdGreyhounds = "19";

  @Value("${event.category.id.horses}")
  public static String categoryIdHorses = "21";

  @Value("${event.category.id.tote}")
  public static String categoryIdTote = "151";

  @Value("${event.category.name.greyhounds}")
  public static String greyhoundsCategoryCode = "greyhound-racing";

  private static final String FIRST_HALF = "FIRST_HALF";
  private static final String EVENT_PREFIX = "event/";
  private static final String TOTE = "tote";

  private static final String TEAM_SEPERATOR_REGEX = " vs | v ";
  private static final Pattern TEAM_SEPERATOR_PATTERN =
      Pattern.compile(TEAM_SEPERATOR_REGEX, Pattern.CASE_INSENSITIVE);

  private static Map<String, Type> typesMap =
      new HashMap<String, Type>() {
        {
          put("cards", new CardType());
          put("goals", new GoalType());
          put("kick_off", new KickOffType());
          put("periods", new PeriodType());
        }
      };

  private static Gson gson = new GsonBuilder().create();

  private static ItemMapper itemMapper = Mappers.getMapper(ItemMapper.class);
  private static ChannelMapper channelMapper = Mappers.getMapper(ChannelMapper.class);
  private static SubscriptionMapper subscriptionMapper =
      Mappers.getMapper(SubscriptionMapper.class);

  private static BipParser scoresParser = BipParserFactory.getParser(EventCategory.FOOTBALL);

  public static RacingDTO toRacingDto(Item item) {
    return RacingDTO.builder()
        .eventId(item.getEventId())
        .platform(item.getPlatform())
        .token(item.getToken())
        .types(item.getTypes())
        .build();
  }

  public static List<ChannelDTO> toChannelDTO(@NotNull Item item) {
    return item.getTypes().stream()
        .map(type -> typesMap.getOrDefault(type, new UnknownType(type)).channels())
        .flatMap(Collection::stream)
        .distinct()
        .map(type -> itemMapper.toItemDTO(item).setType(type))
        .map(channelMapper::toChannelDTO)
        .collect(Collectors.toList());
  }

  public static List<SubscriptionDTO> toSubscriptionDTO(@NotNull Item item) {
    return item.getTypes().stream()
        .distinct()
        .map(type -> itemMapper.toItemDTO(item).setType(type))
        .map(subscriptionMapper::toSubscriptionDTO)
        .collect(Collectors.toList());
  }

  public static WinAlertDTO toWinAlertDto(WinAlertSubscriptionRequest request, String betId) {
    return WinAlertDTO.builder()
        .userName(request.getUserName())
        .token(request.getToken())
        .platform(request.getPlatform())
        .appVersionInt(request.getAppVersionInt())
        .betId(betId)
        .build();
  }

  public static SportsBookUpdate toUpdateEntity(Event event) {
    return new SportsBookUpdate()
        .setEvent(
            (Event)
                event.setMeta(
                    new Meta()
                        .setOperation(AbstractSportsbookUpdateMapper.UPDATE)
                        .setRecordModifiedTime(new DateTime(DateTimeZone.UTC).toString())));
  }

  public static Event toEvent(com.egalacoral.spark.siteserver.model.Event ssEvent) {
    if (ssEvent == null) {
      return null;
    }

    try {
      Event event = createEvent(ssEvent);
      addParticipants(event, ssEvent);
      return event;
    } catch (Exception e) {
      logger.error("Failed to parse initial data for event {}", ssEvent.getId(), e);
      throw new ConsumeEventException(
          String.format("Can't parse initial data for event: '%s'", gson.toJson(ssEvent)), e);
    }
  }

  private static Event createEvent(com.egalacoral.spark.siteserver.model.Event ssEvent) {
    String sportUri = createSportUri(ssEvent);
    logger.info("EventService: generated event URI: " + sportUri);

    return Event.builder()
        .eventId(Long.valueOf(ssEvent.getId()))
        .name(ssEvent.getName())
        .period(FIRST_HALF)
        .startTime(ssEvent.getStartTime())
        .isLive(normalize(ssEvent.isLiveNowEvent()))
        .isEventStarted(normalize(ssEvent.isStarted()))
        .isEventResulted(normalize(ssEvent.isResulted()))
        .sportUri(sportUri)
        .categoryId(ssEvent.getCategoryId())
        .build();
  }

  public static Event toEventWithScores(
      @NotNull com.egalacoral.spark.siteserver.model.Event ssEvent,
      @NotNull EventScores eventScores) {
    try {
      Event event = createEvent(ssEvent);
      addScoreAndParticipants(event, eventScores);
      return event;
    } catch (Exception e) {
      logger.error("Failed to parse initial data for event {}", ssEvent.getId(), e);
      throw new ConsumeEventException(
          String.format("Can't parse initial data for event: '%s'", gson.toJson(ssEvent)), e);
    }
  }

  private static void addParticipants(
      Event eventDto, com.egalacoral.spark.siteserver.model.Event ssEvent) {
    String[] participants = TEAM_SEPERATOR_PATTERN.split(ssEvent.getName().replace("|", ""));
    if (participants.length == 2) {
      eventDto.setHomeTeamName(participants[0]);
      eventDto.setAwayTeamName(participants[1]);
    } else {
      try {
        Optional<BipComment> bipComment =
            Optional.ofNullable(scoresParser.parse(ssEvent.getName()));
        bipComment
            .flatMap(comment -> Optional.ofNullable(comment.getPlayerHomeComment()))
            .ifPresent(
                c -> {
                  eventDto.setHomeTeamName(c.getName());
                  eventDto.setHomeTeamScore(parseIntOrDefault(c.getScore(), 0));
                });
        bipComment
            .flatMap(comment -> Optional.ofNullable(comment.getPlayerAwayComment()))
            .ifPresent(
                c -> {
                  eventDto.setAwayTeamName(c.getName());
                  eventDto.setAwayTeamScore(parseIntOrDefault(c.getScore(), 0));
                });
      } catch (Exception e) {
        logger.warn("Failed to parse participant name: {}", ssEvent.getName(), e);
      }
    }
  }

  private static Integer parseIntOrDefault(String score, int defaultValue) {
    try {
      return Optional.ofNullable(score)
          .filter(s -> !StringUtils.isEmpty(s))
          .map(Integer::valueOf)
          .orElse(defaultValue);
    } catch (Exception e) {
      logger.error("Failed to parse score {}", score, e);
      return defaultValue;
    }
  }

  private static void addScoreAndParticipants(Event eventDto, EventScores comments) {
    List<EventScores.Team> teams = comments.getTeams();

    if (!StringUtils.isEmpty(comments.getPeriod())) {
      eventDto.setPeriod(comments.getPeriod());
    }
    // re-order for home team by taking role code..issue reference BMA-63004
    teams = orderHomeAndAwayTeam(teams);

    EventScores.Team homeTeam = teams.get(0);
    eventDto.setHomeTeamName(homeTeam.getName());
    eventDto.setHomeTeamScore(homeTeam.getScore());
    eventDto.setHomeTeamPenalties(homeTeam.getPenalties());

    EventScores.Team awayTeam = teams.get(1);
    eventDto.setAwayTeamName(awayTeam.getName());
    eventDto.setAwayTeamScore(awayTeam.getScore());
    eventDto.setAwayTeamPenalties(awayTeam.getPenalties());
  }

  private static List<EventScores.Team> orderHomeAndAwayTeam(List<EventScores.Team> teams) {
    List<EventScores.Team> orderedTeams = new ArrayList<>();
    // check second team is home team or not. else keep same order
    if (isHomeTeam(teams.get(1))) {
      orderedTeams.add(teams.get(1));
      orderedTeams.add(teams.get(0));
    } else {
      orderedTeams = teams;
    }
    return orderedTeams;
  }

  public static boolean isHomeTeam(EventScores.Team team) {
    String roleCode = team.getRoleCode();
    List<String> codes = Arrays.asList("TEAM_1", "HOME");
    return (StringUtils.hasText(roleCode) && codes.contains(roleCode));
  }

  private static Boolean normalize(Boolean nullableValue) {
    return BooleanUtils.toBoolean(nullableValue);
  }

  private static String createSportUri(com.egalacoral.spark.siteserver.model.Event ssEvent) {
    if (categoryIdTote.equals(ssEvent.getCategoryId())) {
      return TOTE + "/" + EVENT_PREFIX;
    }

    String sportUri =
        replaceSpecialSymbols(getCategoryCode(ssEvent))
            + "/"
            + replaceSpecialSymbols(ssEvent.getClassName())
            + "/"
            + replaceSpecialSymbols(ssEvent.getTypeName())
            + "/"
            + replaceSpecialSymbols(ssEvent.getName())
            + "/";

    if (!categoryIdGreyhounds.equals(ssEvent.getCategoryId())
        && !categoryIdHorses.equals(ssEvent.getCategoryId())) {
      sportUri = EVENT_PREFIX + sportUri;
    }

    return sportUri;
  }

  private static String getCategoryCode(com.egalacoral.spark.siteserver.model.Event ssEvent) {
    if (categoryIdGreyhounds.equals(ssEvent.getCategoryId())) {
      return greyhoundsCategoryCode;
    } else {
      return ssEvent.getCategoryCode();
    }
  }

  private static String replaceSpecialSymbols(String source) {
    return source.replaceAll("\\s-\\s|[^a-zA-Z0-9]", "-").toLowerCase();
  }

  public static List<Position> toPositions(RacingResult result) {
    return result.getConcreteChildren(Children::getFinalPosition).stream()
        .filter(finalPosition -> finalPosition.getRunnerNumber() != null)
        .map(ObjectMapper::mapPosition)
        .collect(Collectors.toList());
  }

  private static Position mapPosition(FinalPosition finalPosition) {
    int position = finalPosition.getPosition() != null ? finalPosition.getPosition() : 0;
    return Position.builder()
        .id(finalPosition.getId())
        .position(position)
        .name(finalPosition.getName())
        .runnerNumber(finalPosition.getRunnerNumber())
        .build();
  }

  public static Outcome mapOutcome(com.egalacoral.spark.siteserver.model.Outcome ssOutcome) {
    Outcome outcome =
        Outcome.builder()
            .id(ssOutcome.getId())
            .name(ssOutcome.getName())
            .resultCode(ssOutcome.getResultCode())
            .build();
    if (ssOutcome.getPosition() != null) {
      outcome.setPosition(Integer.parseInt(ssOutcome.getPosition()));
    }
    return outcome;
  }
}
