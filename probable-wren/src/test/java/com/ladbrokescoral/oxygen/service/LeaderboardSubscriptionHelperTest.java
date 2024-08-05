package com.ladbrokescoral.oxygen.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.util.Collections;
import java.util.HashSet;
import java.util.Set;
import org.assertj.core.util.Arrays;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class LeaderboardSubscriptionHelperTest {
  private LeaderboardSubscriptionHelper leaderboardSubscriptionHelper;
  private Gson gson;
  @Mock private LeaderboardReqPublisher showdownReqPublisher;

  String update =
      "{\"_id\":\"0\",\"contestId\":\"61eb956dd2e14e15c1139313\",\"index\":0,\"userId\":\"dev_user\",\"eventId\":\"1716332\",\"receiptId\":\"O/300078346/00\",\"outcomeIds\":[\"148123485\",\"148123512\",\"148123509\",\"148123482\",\"148123502\"],\"stake\":\"0\",\"odd\":3,\"voided\":false,\"priceNum\":\"400\",\"priceDen\":\"10\",\"overallProgressPct\":0,\"counterFlag\":true,\"_class\":\"com.entain.oxygen.showdown.model.Entry\"}";

  @BeforeEach
  public void init() {
    gson = new GsonBuilder().serializeNulls().create();
    leaderboardSubscriptionHelper = new LeaderboardSubscriptionHelper(gson, showdownReqPublisher);
  }

  @Test
  void clearShowdownSubscriptions_NoChannels() {
    leaderboardSubscriptionHelper.clearShowdownSubscriptions("10", Collections.emptySet());
    verify(showdownReqPublisher, times(1)).publish(any(), any());
  }

  @ParameterizedTest
  @ValueSource(
      strings = {
        "LDRBRD::60c38852f5860a2012497c3d::Dachanta",
        "LDRBRD::60c38852f5860a2012497c3d::Dachanta::0",
        "c::60c38852f5860a2012497c3d::Dachanta::1",
        "c::1::2",
        "c::LDRBRD",
        "LDRBRD"
      })
  void clearShowdownSubscriptions(String msg) {
    @SuppressWarnings({"rawtypes", "unchecked"})
    Set<String> channels = new HashSet(Arrays.asList(new String[] {msg}));
    leaderboardSubscriptionHelper.clearShowdownSubscriptions("10", channels);
    if (msg.equals("LDRBRD")) verify(showdownReqPublisher, times(0)).publish(any(), any());
    else verify(showdownReqPublisher, times(1)).publish(any(), any());
  }

  @Test
  void clearShowdownSubscriptionsfalse() {
    @SuppressWarnings({"rawtypes", "unchecked"})
    Set<String> channels = new HashSet(Arrays.asList(new String[] {"c::1::2"}));
    leaderboardSubscriptionHelper.clearShowdownSubscriptions("10", channels);
    verify(showdownReqPublisher, times(0))
        .publish(
            "c::1",
            "{\"contestId\":\"c\",\"userId\":\"1\",\"entryId\":null,\"type\":\"unsubscribe\",\"key\":null,\"sessionId\":\"10\"}");
  }
}
