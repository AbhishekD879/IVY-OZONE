package com.ladbrokescoral.oxygen.listeners.showdown;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.listener.DataListener;
import com.google.gson.Gson;
import com.ladbrokes.oxygen.dto.leaderboard.Request;
import com.ladbrokescoral.oxygen.listeners.ThrottleLogic;
import com.ladbrokescoral.oxygen.service.LeaderboardReqPublisher;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Pattern;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class SubscribeShowdownListener implements DataListener<List<String>> {

  private static final int THREE = 3;
  private static final int TWO = 2;
  private static final int FOUR = 4;
  private static final Pattern splitPattern = Pattern.compile("::");
  ThrottleLogic throttleLogic;
  LeaderboardReqPublisher leaderboardReqPublisher;
  Gson gson = new Gson();

  public SubscribeShowdownListener(
      ThrottleLogic throttleLogic, LeaderboardReqPublisher leaderboardReqPublisher) {
    this.throttleLogic = throttleLogic;
    this.leaderboardReqPublisher = leaderboardReqPublisher;
  }

  @Override
  public void onData(SocketIOClient client, List<String> data, AckRequest ackSender)
      throws Exception {
    if (throttleLogic.hackerDetected(client, data)) {
      return;
    }
    List<String> keys = Arrays.asList("EVENT", "CLOCK", "SCORE");

    String sessionId = client.getSessionId().toString();
    data.stream()
        .forEach(
            channel -> {
              if (!client.getAllRooms().contains(channel)) {
                client.joinRoom(channel);
              }
              String[] channelInfo = channel.split("::");
              Request request = new Request();
              request.setType("subscribe");
              request.setSessionId(sessionId);
              if ((splitPattern.split(channel).length == FOUR) && channel.contains("LDRBRD")) {
                request.setContestId(channelInfo[1]);
                request.setUserId(channelInfo[TWO]);
                request.setToken(channelInfo[THREE]);
                request.setContentType("leaderboardV2");
              } else if (splitPattern.split(channel).length == TWO) {
                getContentType(channelInfo, request);
              } else if ((splitPattern.split(channel).length == THREE)
                  && channel.contains("LDRBRD")) {
                request.setContestId(channelInfo[1]);
                request.setUserId(channelInfo[TWO]);
                request.setContentType("leaderboardV2");
              }
              if (!keys.contains(channelInfo[0])) {
                leaderboardReqPublisher.publish(channel, gson.toJson(request));
              }
            });
    log.info("Were processed {} subscriptions for client {}", data, sessionId);
  }

  private void getContentType(String[] channelInfo, Request request) {
    request.setContestId(channelInfo[0]);
    request.setUserId(channelInfo[1]);
    request.setContentType("myentries");
  }
}
