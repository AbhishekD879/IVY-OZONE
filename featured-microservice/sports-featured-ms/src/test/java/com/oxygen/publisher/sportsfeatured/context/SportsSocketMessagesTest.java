package com.oxygen.publisher.sportsfeatured.context;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

public class SportsSocketMessagesTest {

  @Test
  public void testWithMultipleConstructor() {

    SportsSocketMessages messages = SportsSocketMessages.ERROR_500;
    assertEquals("FD", messages.getSportId());
    assertEquals("ERROR:500", messages.getCode());
    assertEquals("FD:ERROR:500", messages.messageId());
  }

  @Test
  public void testWithSingleConstructor() {

    SportsSocketMessages messages = SportsSocketMessages.PAGE_SWITCH;

    assertEquals("page-switch", messages.getCode());
    assertEquals("page-switch", messages.messageId());
  }
}
