package com.ladbrokescoral.oxygen.listeners;

import com.corundumstudio.socketio.SocketIOClient;
import com.newrelic.api.agent.NewRelic;
import java.net.SocketAddress;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class ThrottleLogic {

  private final int subscriptionLimit;

  public ThrottleLogic(@Value("${liveserve.subscription.limit}") int subscriptionLimit) {

    this.subscriptionLimit = subscriptionLimit;
  }

  public boolean hackerDetected(SocketIOClient client, List<String> data) {
    int curreentSubsciptionCount = client.getAllRooms().size();
    int newSubsriptionCount = data.size();
    int expectedRoomSize = curreentSubsciptionCount + newSubsriptionCount;
    if (expectedRoomSize > subscriptionLimit) {
      SocketAddress remoteAddress = client.getRemoteAddress();
      log.warn(
          "Too much subscriptions for client - {}. Limit - {}. Ignoring and remove all other subscription",
          remoteAddress,
          subscriptionLimit);
      NewRelic.noticeError(
          String.format("Too much subscriptions for client - %s", remoteAddress.toString()));
      return true;
    }
    return false;
  }
}
