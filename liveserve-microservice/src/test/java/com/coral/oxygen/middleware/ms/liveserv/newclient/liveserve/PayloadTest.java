package com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve;

import static org.junit.Assert.*;

import com.coral.oxygen.middleware.ms.liveserv.model.ChannelType;
import com.coral.oxygen.middleware.ms.liveserv.newclient.LiveUpdatesChannel;
import com.coral.oxygen.middleware.ms.liveserv.newclient.LiveUpdatesChannelFactory;
import java.util.ArrayList;
import java.util.List;
import org.junit.Assert;
import org.junit.Ignore;
import org.junit.Test;

public class PayloadTest {

  private static final long HOURS_24 = 24 * 60 * 1000L;

  @Test
  public void testUpdate() {
    Payload payload = new Payload(HOURS_24);
    LiveUpdatesChannel LiveUpdatesChannel =
        payload.addItem(LiveUpdatesChannelFactory.onEventSubscription("7082039"));
    List<Message> messages = new ArrayList<>();
    messages.add(
        new Message(
            "M" + ChannelType.sEVENT.toString(),
            "lmid",
            "json",
            LiveUpdatesChannel.messageHashKey(),
            "body"));
    org.junit.Assert.assertEquals("", LiveUpdatesChannel.getLastMessageID());
    payload.update(messages);
    org.junit.Assert.assertEquals("lmid", LiveUpdatesChannel.getLastMessageID());
  }

  @Test
  public void testUpdateAndAdd() {
    Payload payload = new Payload(HOURS_24);
    LiveUpdatesChannel LiveUpdatesChannel =
        payload.addItem(LiveUpdatesChannelFactory.onEventSubscription("2"));
    LiveUpdatesChannel.addLastMessageID("testlastmessageid");
    LiveUpdatesChannel = payload.addItem(LiveUpdatesChannelFactory.onEventSubscription("2"));
    Assert.assertEquals(1, payload.getPayloadItems().size());
    Assert.assertEquals("testlastmessageid", LiveUpdatesChannel.getLastMessageID());
  }

  @Test
  @Ignore
  public void testEvict() throws InterruptedException {
    Payload payload = new Payload(1L);
    LiveUpdatesChannel LiveUpdatesChannel =
        payload.addItem(LiveUpdatesChannelFactory.onEventSubscription("1"));
    Thread.sleep(1200);
    Assert.assertTrue(payload.getPayloadItems().get(LiveUpdatesChannel.messageHashKey()) == null);
  }

  @Test
  @Ignore
  public void testGet() throws InterruptedException {
    Payload payload = new Payload(10L);
    LiveUpdatesChannel LiveUpdatesChannel =
        payload.addItem(LiveUpdatesChannelFactory.onEventSubscription("1"));
    Thread.sleep(1200);
    Assert.assertTrue(payload.getPayloadItems().get(LiveUpdatesChannel.messageHashKey()) != null);
  }
}
