package com.egalacoral.spark.liveserver.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.common.service.notification.MessagePublisher;
import com.coral.oxygen.middleware.common.service.notification.MessagePublisherTopicSelector;
import com.coral.oxygen.middleware.common.service.notification.topic.TopicType;
import com.egalacoral.spark.liveserver.Message;
import com.egalacoral.spark.liveserver.configuration.LiveServeUtilsConfig;
import com.egalacoral.spark.liveserver.meta.EventMetaInfo;
import com.egalacoral.spark.liveserver.meta.EventMetaInfoRepository;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.io.InputStream;
import java.math.BigInteger;
import java.nio.charset.Charset;
import java.util.Optional;
import org.apache.commons.io.IOUtils;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class LiveServerMessageHandlerTest {

  private LiveServerMessageHandler handler;

  @Mock private LiveServerSubscriptionsQAStorage lsQAStorage;
  @Mock private MessagePublisher messagePublisher;
  @Mock private MessagePublisherTopicSelector topicSelector;
  @Mock private EventMetaInfoRepository eventMetaInfoRepository;

  @Before
  public void setUp() {
    LiveServeUtilsConfig utilsConfig = new LiveServeUtilsConfig();
    when(topicSelector.getLiveServeMessageTopic())
        .thenReturn(TopicType.FEATURED_LIVE_SERVER_MODULES);
    BigInteger id = new BigInteger("4618116");
    when(eventMetaInfoRepository.getByEventId(id))
        .thenAnswer(
            invocation -> {
              BigInteger eventId = new BigInteger(invocation.getArgument(0) + "");
              return Optional.of(EventMetaInfo.builder().eventId(eventId).categoryId(36).build());
            });
    handler = new LiveServerMessageHandler(messagePublisher, topicSelector, lsQAStorage, 100, 10);
    handler.setEventMetaInfoRepository(eventMetaInfoRepository);
    handler.setJsonMapper(utilsConfig.jsonMapper());
  }

  @Test
  public void testPublishWhenMessageIsValid() throws IOException {
    InputStream stream =
        getClass()
            .getClassLoader()
            .getResourceAsStream("liveServerMessageHandler/event_message.json");
    Message message = new ObjectMapper().readValue(stream, new TypeReference<Message>() {});

    handler.onMessage(message);
    verify(messagePublisher, times(1)).publish(any(TopicType.class), anyString(), anyString());
  }

  @Test
  public void testPublishWhenScrBrdEventIsCreated() throws IOException {
    InputStream stream =
        getResourceAsStream("liveServerMessageHandler/event_with_scores_message.json");
    Message message = new ObjectMapper().readValue(stream, new TypeReference<Message>() {});

    String scbrdJsonEvent = getResourceAsString("liveServerMessageHandler/SCBRD_EVENT.json").trim();
    handler.onMessage(message);
    verify(messagePublisher, times(2)).publish(any(TopicType.class), anyString(), anyString());
    verify(messagePublisher, times(1))
        .publish(any(TopicType.class), anyString(), eq(scbrdJsonEvent));
  }

  @Test
  public void testPublishWhenHandballScrBrdEventIsCreated() throws IOException {
    InputStream stream =
        getResourceAsStream("liveServerMessageHandler/volleyball_event_with_scores_message.json");
    Message message = new ObjectMapper().readValue(stream, new TypeReference<Message>() {});

    String scbrdJsonEvent =
        getResourceAsString("liveServerMessageHandler/VOLLEYBALL_SCBRD_EVENT.json").trim();
    handler.onMessage(message);
    verify(messagePublisher, times(2)).publish(any(TopicType.class), anyString(), anyString());
    verify(messagePublisher, times(1))
        .publish(any(TopicType.class), anyString(), eq(scbrdJsonEvent));
  }

  private InputStream getResourceAsStream(String resource) {
    return getClass().getClassLoader().getResourceAsStream(resource);
  }

  private String getResourceAsString(String resource) {
    try {
      return IOUtils.toString(getResourceAsStream(resource), Charset.defaultCharset());
    } catch (IOException e) {
      return "";
    }
  }
}
