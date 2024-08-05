package com.ladbrokescoral.oxygen.notification.services;

import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.notification.entities.EventLiveUpdate;
import com.ladbrokescoral.oxygen.notification.services.handler.NotificationMessageHandler;
import com.ladbrokescoral.scoreboards.parser.api.BipParser;
import com.ladbrokescoral.scoreboards.parser.model.BipComment;
import com.ladbrokescoral.scoreboards.parser.model.Comment;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.ApplicationEventPublisherAware;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

@Component
@RequiredArgsConstructor
@Slf4j
public class ScoresInNameMessageHandler
    implements NotificationMessageHandler<MessageEnvelope>, ApplicationEventPublisherAware {

  private final BipParser scoresParser;
  private final Gson gson;
  private ApplicationEventPublisher applicationEventPublisher;

  @Override
  public void handle(MessageEnvelope message) {
    String messageBody = message.getMessage().getJsonData();
    EventLiveUpdate eventLiveUpdate = gson.fromJson(messageBody, EventLiveUpdate.class);
    if (StringUtils.isEmpty(eventLiveUpdate)
        || StringUtils.isEmpty(eventLiveUpdate.getNames())
        || StringUtils.isEmpty(eventLiveUpdate.getNames().getEn())) {
      logger.warn("Couldn't parse event name from message: {}", message);
    } else {
      String eventName = eventLiveUpdate.getNames().getEn();
      Optional<BipComment> bipComment = maybeParseEventName(eventName);

      bipComment.ifPresent(
          comment -> {
            long eventId = message.getEventId();

            Integer homeScore = extractScore(comment.getPlayerHomeComment());
            Integer awayScore = extractScore(comment.getPlayerAwayComment());

            if (homeScore != null && awayScore != null) {
              ScoresDto scores =
                  ScoresDto.builder()
                      .eventId(eventId)
                      .homeScore(homeScore)
                      .awayScore(awayScore)
                      .build();

              applicationEventPublisher.publishEvent(new ScoreChangedEvent(this, scores));
            }
          });
    }
  }

  private Integer extractScore(Comment comment) {
    if (comment == null || comment.getScore() == null) {
      return null;
    }
    return Integer.parseInt(comment.getScore());
  }

  private Optional<BipComment> maybeParseEventName(String eventName) {
    try {
      return Optional.ofNullable(scoresParser.parse(eventName));
    } catch (Exception e) {
      logger.warn("Failed to parse scores from eventName: {}", eventName, e);
      return Optional.empty();
    }
  }

  @Override
  public void setApplicationEventPublisher(ApplicationEventPublisher applicationEventPublisher) {
    this.applicationEventPublisher = applicationEventPublisher;
  }
}
