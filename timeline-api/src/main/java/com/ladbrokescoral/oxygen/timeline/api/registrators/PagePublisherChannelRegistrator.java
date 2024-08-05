package com.ladbrokescoral.oxygen.timeline.api.registrators;

import com.ladbrokescoral.oxygen.timeline.api.channel.ChannelHandlersContext;
import com.ladbrokescoral.oxygen.timeline.api.controller.Room;
import java.util.Arrays;
import java.util.concurrent.atomic.AtomicBoolean;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@RequiredArgsConstructor
public class PagePublisherChannelRegistrator implements ReloadableService {
  private AtomicBoolean isOnService = new AtomicBoolean();

  @Override
  public void start() {
    this.isOnService.set(true);
    Arrays.stream(Room.values()).forEach(room -> this.checkOrRegisterPagePublisher(room.name()));
  }

  public void checkOrRegisterPagePublisher(String room) {
    getPageChannel(room);
    this.isOnService.set(true);
  }

  private void getPageChannel(String room) {
    ChannelHandlersContext.createIfAbsentAndReturnChannel(room);
  }

  @Override
  public void evict() {
    this.isOnService.set(false);
  }

  @Override
  public boolean isHealthy() {
    return isOnService.get();
  }

  @Override
  public void onFail(Exception ex) {
    this.isOnService.set(false);
    log.error("WS namespace registration failed.", ex);
  }
}
