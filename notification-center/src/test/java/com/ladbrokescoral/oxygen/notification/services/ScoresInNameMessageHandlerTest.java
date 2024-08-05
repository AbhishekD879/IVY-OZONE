package com.ladbrokescoral.oxygen.notification.services;

import static org.junit.Assert.fail;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;

import com.coral.oxygen.middleware.ms.liveserv.client.model.Message;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.notification.configs.AppConfig;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import org.springframework.context.ApplicationEventPublisher;

public class ScoresInNameMessageHandlerTest {

  private ScoresInNameMessageHandler scoresInNameHandler;
  private ApplicationEventPublisher eventPublisherMock;

  @Before
  public void setUp() throws Exception {
    scoresInNameHandler =
        new ScoresInNameMessageHandler(new AppConfig().footballBipParser(), new Gson());
    eventPublisherMock = Mockito.mock(ApplicationEventPublisher.class);
    scoresInNameHandler.setApplicationEventPublisher(eventPublisherMock);
  }

  @Test
  public void noExceptionIfCouldNotParseEventName() {
    MessageEnvelope msgEnvelop = eventUpdateEnvelopWithBody("{}");
    try {
      scoresInNameHandler.handle(msgEnvelop);
    } catch (Exception e) {
      fail();
    }
  }

  @Test
  public void scoreChangedEventIsSent() {
    String msgBody = "{\"names\": {\"en\": \"Home 5-2 Away\"}}";
    scoresInNameHandler.handle(eventUpdateEnvelopWithBody(msgBody));
    ScoresDto expectedScores = ScoresDto.builder().eventId(123).homeScore(5).awayScore(2).build();
    ScoreChangedEvent expectedEvent = new ScoreChangedEvent(scoresInNameHandler, expectedScores);

    Mockito.verify(eventPublisherMock, times(1)).publishEvent(expectedEvent);
  }

  @Test
  public void noEventIsSentWhenScoreCouldNotBeParsed() {
    String msgBody = "{\"names\": {\"en\": \"Home vs Away\"}}";
    scoresInNameHandler.handle(eventUpdateEnvelopWithBody(msgBody));
    Mockito.verify(eventPublisherMock, never()).publishEvent(any());
  }

  private MessageEnvelope eventUpdateEnvelopWithBody(String msgBody) {
    return new MessageEnvelope("sEVENT", 123, new Message("??", msgBody));
  }
}
