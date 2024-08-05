package com.ladbrokescoral.oxygen.timeline.api.model;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertThrows;
import static org.mockito.ArgumentMatchers.any;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.timeline.api.exceptions.MessageContentException;
import com.ladbrokescoral.oxygen.timeline.api.reactive.model.MessageContent;
import com.ladbrokescoral.oxygen.timeline.api.repository.CustomPageImpl;
import java.lang.reflect.Field;
import java.util.Collections;
import java.util.List;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.util.ReflectionUtils;
import org.springframework.web.reactive.socket.WebSocketSession;

@RunWith(MockitoJUnitRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@DirtiesContext
public class MessageContentTest {

  @Mock private ObjectMapper mapper;

  @Test
  public void testGetHeaders() {
    MessageContent messageContent = new MessageContent("");
    assertNotNull(messageContent.getHeaders());
  }

  @Test
  public void testWithPayload()
      throws JsonProcessingException, IllegalArgumentException, IllegalAccessException {
    Mockito.when(mapper.writeValueAsString(any()))
        .thenThrow(new JsonProcessingException("Error") {});
    Field field = ReflectionUtils.findField(MessageContent.class, "mapper");
    field.setAccessible(true);
    field.set(MessageContent.class, mapper);
    CustomPageImpl<List<?>> page = new CustomPageImpl<>(Collections.emptyList());
    assertThrows(MessageContentException.class, () -> MessageContent.withPayload(null, page));
  }

  @Test
  public void testWithInitialPayload()
      throws JsonProcessingException, IllegalArgumentException, IllegalAccessException {
    WebSocketSession webSocketSession = Mockito.mock(WebSocketSession.class);
    Mockito.when(webSocketSession.getId()).thenReturn("1");
    Mockito.when(mapper.writeValueAsString(any()))
        .thenThrow(new JsonProcessingException("Error") {});
    Field field = ReflectionUtils.findField(MessageContent.class, "mapper");
    field.setAccessible(true);
    field.set(MessageContent.class, mapper);
    assertThrows(
        MessageContentException.class, () -> MessageContent.withInitialPayload(webSocketSession));
  }
}
