package com.coral.oxygen.middleware.ms.liveserv;

/**
 * Listener for {@link ChannelUnsubcribeEvent} which is published when system should unsubscribe
 * from OpenBet Event's channel. {@link UnsubscribeService} publishes such unsubscribe events.
 */
public interface ChannelUnsubscribeEventListener {
  void onChannelUnsubscribe(ChannelUnsubcribeEvent channelUnsubcribeEvent);
}
