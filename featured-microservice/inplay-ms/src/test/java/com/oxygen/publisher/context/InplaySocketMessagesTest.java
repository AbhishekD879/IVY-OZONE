package com.oxygen.publisher.context;

import static org.junit.Assert.assertEquals;

import com.oxygen.publisher.inplay.context.InplaySocketMessages;
import org.junit.Test;

public class InplaySocketMessagesTest {

  @Test
  public void testWithMultipleConstructor() {

    InplaySocketMessages messages = InplaySocketMessages.GET_RIBBON_REQUEST;
    assertEquals("GET_RIBBON", messages.getCode());
    assertEquals("GET_RIBBON", messages.messageId());
  }

  @Test
  public void testWithSingleConstructor() {

    InplaySocketMessages messages = InplaySocketMessages.GET_INPLAY_STRUCTURE_RESPONSE;

    assertEquals("INPLAY_STRUCTURE", messages.getCode());
    assertEquals("INPLAY_STRUCTURE", messages.messageId());
  }
}
