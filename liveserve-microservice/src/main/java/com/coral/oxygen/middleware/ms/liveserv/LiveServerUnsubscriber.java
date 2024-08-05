package com.coral.oxygen.middleware.ms.liveserv;

import lombok.extern.slf4j.Slf4j;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class LiveServerUnsubscriber implements ChannelUnsubscribeEventListener {
  private final LiveServService liveServService;

  public LiveServerUnsubscriber(LiveServService liveServService) {
    this.liveServService = liveServService;
  }

  @Async
  @EventListener
  @Override
  public void onChannelUnsubscribe(ChannelUnsubcribeEvent channelUnsubcribeEvent) {
    String liveServChannel = channelUnsubcribeEvent.getLiveServChannel();
    liveServService.unsubscribe(liveServChannel);
    log.debug("Unsubcribed from liveserve channel {}", liveServChannel);
  }
}
