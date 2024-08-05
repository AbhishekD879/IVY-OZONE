package com.ladbrokescoral.oxygen.service;

import com.corundumstudio.socketio.SocketIOServer;
import com.corundumstudio.socketio.listener.DataListener;
import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.listeners.ScoreboardListener;
import com.ladbrokescoral.oxygen.listeners.ThrottleLogic;
import com.ladbrokescoral.oxygen.listeners.showdown.LeaderBoardListener;
import com.ladbrokescoral.oxygen.listeners.showdown.LeaderboardEntryInfoListener;
import com.ladbrokescoral.oxygen.listeners.showdown.MyEntriesListener;
import com.ladbrokescoral.oxygen.listeners.showdown.SubscribeShowdownListener;
import com.ladbrokescoral.oxygen.listeners.showdown.UnsubscribeShowdownListener;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import lombok.val;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@ConditionalOnProperty(
    prefix = "leaderboard",
    value = "enabled",
    havingValue = "true",
    matchIfMissing = false)
public class LeaderboardSocketIOHelper {

  // showdown MS
  final DataListener<String> leaderBoardListener;
  final DataListener<String> leaderboardEntryInfoListener;
  final DataListener<String> leaderBoardMyEntriesListener;
  final Gson gson;
  final ThrottleLogic throttleLogic;
  final LeaderboardReqPublisher leaderboardReqPublisher;

  @Autowired
  public LeaderboardSocketIOHelper(
      Gson gson,
      ScoreboardListener scoreboardListener,
      ThrottleLogic throttleLogic,
      LeaderBoardListener leaderBoardListener,
      LeaderboardEntryInfoListener leaderboardEntryInfoListener,
      MyEntriesListener leaderBoardMyEntriesListener,
      LeaderboardReqPublisher leaderboardReqPublisher) {
    this.gson = gson;
    this.throttleLogic = throttleLogic;
    this.leaderBoardListener = leaderBoardListener;
    this.leaderboardEntryInfoListener = leaderboardEntryInfoListener;
    this.leaderBoardMyEntriesListener = leaderBoardMyEntriesListener;
    this.leaderboardReqPublisher = leaderboardReqPublisher;
  }

  public void regShowdownListener(SocketIOServer socketIOServer) {

    @SuppressWarnings("unchecked")
    val typeOfPayload = (Class<List<String>>) (Object) List.class;
    // ShowDown
    socketIOServer.addEventListener("leaderboard", String.class, leaderBoardListener);
    socketIOServer.addEventListener("myentries", String.class, leaderBoardMyEntriesListener);
    socketIOServer.addEventListener("entrylegsinfo", String.class, leaderboardEntryInfoListener);
    socketIOServer.addEventListener(
        "unsubscribeshowdown",
        typeOfPayload,
        new UnsubscribeShowdownListener(leaderboardReqPublisher));
    socketIOServer.addEventListener(
        "subscribeshowdown",
        typeOfPayload,
        new SubscribeShowdownListener(throttleLogic, leaderboardReqPublisher));
  }
}
