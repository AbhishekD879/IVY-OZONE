package com.ladbrokescoral.oxygen.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import com.corundumstudio.socketio.BroadcastOperations;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.ladbrokescoral.oxygen.listeners.ScoreboardListener;
import com.ladbrokescoral.oxygen.listeners.ThrottleLogic;
import com.ladbrokescoral.oxygen.listeners.showdown.LeaderBoardListener;
import com.ladbrokescoral.oxygen.listeners.showdown.LeaderboardEntryInfoListener;
import com.ladbrokescoral.oxygen.listeners.showdown.MyEntriesListener;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class LeaderboardSocketIOHelperTest {

  private LeaderboardSocketIOHelper leaderboardSocketIOListener;
  private Gson gson;
  @Mock private SocketIOServer socketIOServer;
  @Mock private ScoreboardListener scoreboardListener;
  @Mock private ThrottleLogic throttleLogic;
  @Mock private LeaderBoardListener leaderBoardListener;
  @Mock private LeaderboardEntryInfoListener leaderboardEntryInfoListener;
  @Mock private MyEntriesListener leaderBoardMyEntriesListener;
  @Mock private LeaderboardReqPublisher showdownReqPublisher;
  @Mock private BroadcastOperations broadcastOperations;
  @Mock private SocketIOClient socketIOClient;
  @Mock private LeaderboardSubscriptionHelperTest leaderboardSubscriptionHelper;

  String update =
      "{\"_id\":\"0\",\"contestId\":\"61eb956dd2e14e15c1139313\",\"index\":0,\"userId\":\"dev_user\",\"eventId\":\"1716332\",\"receiptId\":\"O/300078346/00\",\"outcomeIds\":[\"148123485\",\"148123512\",\"148123509\",\"148123482\",\"148123502\"],\"stake\":\"0\",\"odd\":3,\"voided\":false,\"priceNum\":\"400\",\"priceDen\":\"10\",\"overallProgressPct\":0,\"counterFlag\":true,\"_class\":\"com.entain.oxygen.showdown.model.Entry\"}";

  @BeforeEach
  public void init() {
    gson = new GsonBuilder().serializeNulls().create();
    leaderboardSocketIOListener =
        new LeaderboardSocketIOHelper(
            gson,
            scoreboardListener,
            throttleLogic,
            leaderBoardListener,
            leaderboardEntryInfoListener,
            leaderBoardMyEntriesListener,
            showdownReqPublisher);
  }

  @Test
  void regShowdownListener() {
    leaderboardSocketIOListener.regShowdownListener(socketIOServer);
    verify(socketIOServer, times(5)).addEventListener(any(), any(), any());
  }
}
