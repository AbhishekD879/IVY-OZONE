package com.ladbrokescoral.oxygen.service;

import com.google.gson.Gson;
import com.ladbrokes.oxygen.dto.leaderboard.Request;
import java.util.Set;
import java.util.regex.Pattern;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Slf4j
@Service
@ConditionalOnProperty(
    prefix = "leaderboard",
    value = "enabled",
    havingValue = "true",
    matchIfMissing = false)
public class LeaderboardSubscriptionHelper {

  private static final int THREE = 3;
  private static final int TWO = 2;
  private static final int FOUR = 4;
  private static final String UNSUBSCRIBE_TOPIC = "unsubscribe";
  private static final Pattern splitPattern = Pattern.compile("::");

  final Gson gson;
  final LeaderboardReqPublisher leaderboardReqPublisher;

  @Autowired
  public LeaderboardSubscriptionHelper(Gson gson, LeaderboardReqPublisher leaderboardReqPublisher) {
    this.gson = gson;
    this.leaderboardReqPublisher = leaderboardReqPublisher;
  }

  public void clearShowdownSubscriptions(String sessionId, Set<String> channels) {
    if (!CollectionUtils.isEmpty(channels)) {
      channels.forEach(channel -> unsubscribeChannel(sessionId, channel));
    } else {
      clearSubscriptionBySession(sessionId);
    }
  }

  private void unsubscribeChannel(String sessionId, String channel) {
    if (channel.contains("::")) {
      Request request = new Request();
      request.setType(UNSUBSCRIBE_TOPIC);
      request.setSessionId(sessionId);
      if (splitPattern.split(channel).length == TWO) {
        request.setUserId(splitPattern.split(channel)[1]);
        request.setContestId(splitPattern.split(channel)[0]);
        request.setContentType("myentries");
      } else if (splitPattern.split(channel).length == THREE && channel.contains("LDRBRD")) {
        request.setUserId(splitPattern.split(channel)[TWO]);
        request.setContestId(splitPattern.split(channel)[1]);
        request.setContentType("leaderboardV2");
      } else if (splitPattern.split(channel).length == FOUR && channel.contains("LDRBRD")) {
        request.setContestId(splitPattern.split(channel)[1]);
        request.setUserId(splitPattern.split(channel)[TWO]);
        request.setToken(splitPattern.split(channel)[THREE]);
        request.setContentType("leaderboardV2");
      }
      leaderboardReqPublisher.publish(channel, gson.toJson(request));
    }
  }

  private void clearSubscriptionBySession(String sessionId) {
    Request request = new Request();
    request.setType(UNSUBSCRIBE_TOPIC);
    request.setSessionId(sessionId);
    leaderboardReqPublisher.publish(sessionId, gson.toJson(request));
  }
}
