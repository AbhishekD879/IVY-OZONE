package com.ladbrokescoral.oxygen.notification.services.handler.football;

import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.notification.entities.Payload;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.services.EventService;
import com.ladbrokescoral.oxygen.notification.services.ScoreChangedEvent;
import com.ladbrokescoral.oxygen.notification.services.ScoresDto;
import com.ladbrokescoral.oxygen.notification.services.notifications.NotificationsFactory;
import com.ladbrokescoral.oxygen.notification.services.repositories.Events;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationListener;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class ScoresMessageHandler extends AbstractFootballNotificationMessageHandler
    implements ApplicationListener<ScoreChangedEvent> {

  private static final String TYPE = "goals";
  private static final String GOAL_MESSAGE_TEMPLATE = "GOAL! ";
  private static final String GOAL_DISALLOWED_MESSAGE_TEMPLATE = "Goal Disallowed ";

  @Autowired
  public ScoresMessageHandler(
      Gson gson,
      Events events,
      Subscriptions subscriptions,
      EventService eventService,
      NotificationsFactory notificationsFactory) {
    super(gson, events, subscriptions, eventService, notificationsFactory);
  }

  @Override
  public Payload process(String json) {
    throw new UnsupportedOperationException();
  }

  @Override
  public void onApplicationEvent(ScoreChangedEvent scoresChangedEvent) {
    Payload payload = scoresToPayload(scoresChangedEvent.getScores());
    this.publishPayload(payload);
  }

  private Payload scoresToPayload(ScoresDto scores) {
    try {
      long eventId = scores.getEventId();
      Integer homeScore = scores.getHomeScore();
      Integer awayScore = scores.getAwayScore();
      Integer homePenalties = scores.getHomePenalties();
      Integer awayPenalties = scores.getAwayPenalties();

      final Event event = getEventById(eventId);
      String scorer =
          homeScore != event.getHomeTeamScore() ? event.getHomeTeamName() : event.getAwayTeamName();

      if (homeScore > event.getHomeTeamScore() || awayScore > event.getAwayTeamScore()) {
        event.setHomeTeamScore(homeScore).setAwayTeamScore(awayScore);
        events.save(event);
        return getPayloadFor(GOAL_MESSAGE_TEMPLATE, scorer, event, TYPE);
      }

      if (homeScore < event.getHomeTeamScore() || awayScore < event.getAwayTeamScore()) {
        event.setHomeTeamScore(homeScore).setAwayTeamScore(awayScore);
        events.save(event);
        return getPayloadFor(GOAL_DISALLOWED_MESSAGE_TEMPLATE, scorer, event, TYPE);
      }

      if (homePenalties > event.getHomeTeamPenalties()
          || awayPenalties > event.getAwayTeamPenalties()) {
        String penaltiesScorer =
            homePenalties != event.getHomeTeamPenalties()
                ? event.getHomeTeamName()
                : event.getAwayTeamName();
        event.setAwayTeamPenalties(homePenalties).setAwayTeamPenalties(awayPenalties);
        events.save(event);
        return getPayloadFor(GOAL_MESSAGE_TEMPLATE, penaltiesScorer, event, TYPE);
      }
      return Payload.builder().build();
    } catch (Exception e) {
      logger.error("Error during processing goals", e);
      return Payload.builder().build();
    }
  }
}
