package com.ladbrokescoral.oxygen.listeners.showdown;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.listener.DataListener;
import com.google.gson.Gson;
import com.ladbrokes.oxygen.dto.leaderboard.Request;
import com.ladbrokescoral.oxygen.service.LeaderboardReqPublisher;
import java.util.List;
import java.util.regex.Pattern;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;

@Slf4j
public class UnsubscribeShowdownListener implements DataListener<List<String>> {

  private static final int THREE = 3;

  private static final int TWO = 2;

  private static final int FOUR = 4;

  private static final Pattern splitPattern = Pattern.compile("::");

  @Autowired LeaderboardReqPublisher leaderboardReqPublisher;
  Gson gson = new Gson();

  public UnsubscribeShowdownListener(LeaderboardReqPublisher leaderboardReqPublisher) {
    this.leaderboardReqPublisher = leaderboardReqPublisher;
  }

  @Override
  public void onData(SocketIOClient client, List<String> data, AckRequest ackSender)
      throws Exception {
    String sessionId = client.getSessionId().toString();
    data.forEach(
        channel -> {
          if (client.getAllRooms().contains(channel)) {
            client.leaveRoom(channel);
          }
          String[] channelInfo = splitPattern.split(channel);
          Request request = new Request();
          request.setSessionId(sessionId);
          request.setType("unsubscribe");
          if (splitPattern.split(channel).length == FOUR && channel.contains("LDRBRD")) {
            setUserInfo(channelInfo, request);
            request.setToken(channelInfo[THREE]);
            request.setContentType("leaderboardV2");
          } else if (splitPattern.split(channel).length == TWO) {
            getContentType(channelInfo, request);
          } else if ((splitPattern.split(channel).length == THREE) && channel.contains("LDRBRD")) {
            setUserInfo(channelInfo, request);
            request.setContentType("leaderboardV2");
          }
          leaderboardReqPublisher.publish(channel, gson.toJson(request));
        });
    log.debug("Were processed {} un-subscriptions for client {}", data, sessionId);
  }

  private void setUserInfo(String[] channelInfo, Request request) {
    request.setContestId(channelInfo[1]);
    request.setUserId(channelInfo[TWO]);
  }

  private void getContentType(String[] channelInfo, Request request) {
    request.setContestId(channelInfo[0]);
    request.setUserId(channelInfo[1]);
    request.setContentType("myentries");
  }
}
