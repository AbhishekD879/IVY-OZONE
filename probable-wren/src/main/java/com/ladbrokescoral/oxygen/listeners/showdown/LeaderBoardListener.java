package com.ladbrokescoral.oxygen.listeners.showdown;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.listener.DataListener;
import com.google.gson.Gson;
import com.ladbrokes.oxygen.dto.leaderboard.Request;
import com.ladbrokescoral.oxygen.service.LeaderboardReqPublisher;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class LeaderBoardListener implements DataListener<String> {

  @Autowired LeaderboardReqPublisher leaderboardReqPublisher;
  Gson gson = new Gson();

  @Override
  public void onData(SocketIOClient client, String data, AckRequest ackSender) throws Exception {
    String[] output = data.split("::");
    String contestId = output[1];
    log.info("Starting to work with contestId: {} userid: {}", contestId);
    client.joinRoom(data);
    Request request = new Request();
    request.setContestId(contestId);
    request.setType("leaderboard");
    leaderboardReqPublisher.publish(data, gson.toJson(request));
    log.info("Info Requested over kafka {} ", gson.toJson(request));
  }
}
