package com.egalacoral.spark.liveserver;

import java.util.ArrayList;
import java.util.List;
import org.junit.Assert;
import org.junit.Test;

public class PayloadTest {

  private static final long HOURS_24 = 24 * 60 * 1000L;

  @Test
  public void testUpdate() {
    Payload payload = new Payload(HOURS_24);
    SubscriptionSubject subscriptionSubject =
        payload.addItem(SubscriptionSubjectFactory.onEventSubscription("7082039"));
    List<Message> messages = new ArrayList<>();
    messages.add(
        new Message(
            "M" + ChannelType.sEVENT.toString(),
            "lmid",
            "json",
            subscriptionSubject.messageHashKey(),
            "body"));
    org.junit.Assert.assertEquals("", subscriptionSubject.getLastMessageID());
    payload.update(messages);
    org.junit.Assert.assertEquals("lmid", subscriptionSubject.getLastMessageID());
  }

  @Test
  public void testUpdateAndAdd() {
    Payload payload = new Payload(HOURS_24);
    SubscriptionSubject subscriptionSubject =
        payload.addItem(SubscriptionSubjectFactory.onEventSubscription("2"));
    subscriptionSubject.addLastMessageID("testlastmessageid");
    subscriptionSubject = payload.addItem(SubscriptionSubjectFactory.onEventSubscription("2"));
    Assert.assertEquals(1, payload.getPayloadItems().size());
    Assert.assertEquals("testlastmessageid", subscriptionSubject.getLastMessageID());
  }

  @Test
  public void testEvict() throws InterruptedException {
    Payload payload = new Payload(1L);
    SubscriptionSubject subscriptionSubject =
        payload.addItem(SubscriptionSubjectFactory.onEventSubscription("1"));
    Thread.sleep(1200);
    Assert.assertTrue(payload.getPayloadItems().get(subscriptionSubject.messageHashKey()) == null);
  }

  @Test
  public void testGet() throws InterruptedException {
    Payload payload = new Payload(10L);
    SubscriptionSubject subscriptionSubject =
        payload.addItem(SubscriptionSubjectFactory.onEventSubscription("1"));
    Thread.sleep(1200);
    Assert.assertTrue(payload.getPayloadItems().get(subscriptionSubject.messageHashKey()) != null);
  }
}
