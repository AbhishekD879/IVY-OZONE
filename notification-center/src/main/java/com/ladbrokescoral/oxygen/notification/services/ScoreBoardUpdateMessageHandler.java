package com.ladbrokescoral.oxygen.notification.services;

import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.notification.entities.ScoreboardItem;
import com.ladbrokescoral.oxygen.notification.entities.ScoreboardMessage;
import com.ladbrokescoral.oxygen.notification.services.handler.NotificationMessageHandler;
import java.util.List;
import java.util.Objects;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.ApplicationEventPublisherAware;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

@Component
@Slf4j
@RequiredArgsConstructor
public class ScoreBoardUpdateMessageHandler
    implements NotificationMessageHandler<String>, ApplicationEventPublisherAware {

  private static final String HOME_TEAM = "HOME";
  private static final String AWAY_TEAM = "AWAY";
  private static final String PENALTIES_PERIOD_CODE = "PENALTIES";
  private final Gson gson;
  private ApplicationEventPublisher applicationEventPublisher;

  @Override
  public void handle(String msgJson) {
    final ScoreboardMessage message = gson.fromJson(msgJson, ScoreboardMessage.class);

    List<ScoreboardItem> subPeriods = message.getSubperiod();

    if (Objects.isNull(subPeriods)) {
      logger.error("Can't handle ScoreboardMessage, subPeriods are null. Message -> {}", msgJson);
      return;
    }

    int homeScore = getScore(subPeriods, HOME_TEAM);
    int awayScore = getScore(subPeriods, AWAY_TEAM);
    int homePenalties = getPenalties(subPeriods, HOME_TEAM);
    int awayPenalties = getPenalties(subPeriods, AWAY_TEAM);

    long eventId = message.getSubperiod().get(0).getEventId();

    ScoresDto scores =
        ScoresDto.builder()
            .eventId(eventId)
            .homeScore(homeScore)
            .awayScore(awayScore)
            .homePenalties(homePenalties)
            .awayPenalties(awayPenalties)
            .build();

    applicationEventPublisher.publishEvent(new ScoreChangedEvent(this, scores));
  }

  protected int getScore(List<ScoreboardItem> items, String team) {
    return items.stream()
        .filter(s -> s.getRoleCode().equalsIgnoreCase(team))
        .map(ScoreboardItem::getValue)
        .filter(s -> !StringUtils.isEmpty(s))
        .mapToInt(Integer::valueOf)
        .sum();
  }

  protected int getPenalties(List<ScoreboardItem> items, String team) {
    return items.stream()
        .filter(
            s -> s.getPeriodCode().equals(PENALTIES_PERIOD_CODE) && s.getRoleCode().equals(team))
        .map(ScoreboardItem::getValue)
        .filter(s -> !StringUtils.isEmpty(s))
        .mapToInt(Integer::valueOf)
        .sum();
  }

  @Override
  public void setApplicationEventPublisher(ApplicationEventPublisher applicationEventPublisher) {
    this.applicationEventPublisher = applicationEventPublisher;
  }
}
