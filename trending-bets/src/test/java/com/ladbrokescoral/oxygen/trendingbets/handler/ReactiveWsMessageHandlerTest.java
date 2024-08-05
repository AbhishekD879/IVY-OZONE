package com.ladbrokescoral.oxygen.trendingbets.handler;

import static org.junit.Assert.*;
import static org.mockito.ArgumentMatchers.any;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.trendingbets.context.ChannelHandlersContext;
import com.ladbrokescoral.oxygen.trendingbets.model.MessageContent;
import com.ladbrokescoral.oxygen.trendingbets.model.MessageContentException;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.springframework.messaging.Message;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.reactive.socket.WebSocketMessage;
import org.springframework.web.reactive.socket.WebSocketSession;
import reactor.core.publisher.FluxSink;
import reactor.core.publisher.Sinks;

class ReactiveWsMessageHandlerTest {

  @Mock private WebSocketSession session;

  @Mock private FluxSink<WebSocketMessage> sink;
  private String channelId = "channelId";

  @InjectMocks
  private ReactiveWsMessageHandler handler =
      ReactiveWsMessageHandler.builder().session(session).sink(sink).build();

  @Test
  void testErrorHandling() {
    handler.subscribe(channelId);
    Sinks.Many<Message<String>> sink = ChannelHandlersContext.getChannels().get(channelId);
    sink.tryEmitError(new RuntimeException());

    assertNotNull(handler.getSubscriber());
  }

  @Test
  void testMessageContentWithPayloadException() throws JsonProcessingException {
    ObjectMapper mapper = Mockito.mock(ObjectMapper.class);
    ObjectMapper originalMapper =
        (ObjectMapper) ReflectionTestUtils.getField(MessageContent.class, "mapper");
    ReflectionTestUtils.setField(MessageContent.class, "mapper", mapper);
    Mockito.when(mapper.writeValueAsString(any())).thenThrow(new JsonProcessingException("") {});
    Assertions.assertThrows(
        MessageContentException.class, () -> MessageContent.withPayload("event", "data"));
    Assertions.assertThrows(
        MessageContentException.class, () -> MessageContent.withInitialPayload("sid"));
    Assertions.assertNotNull(new MessageContent("").getHeaders());
    ReflectionTestUtils.setField(MessageContent.class, "mapper", originalMapper);
  }
}
