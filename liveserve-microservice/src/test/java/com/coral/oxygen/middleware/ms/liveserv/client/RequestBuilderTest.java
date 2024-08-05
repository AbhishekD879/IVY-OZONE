package com.coral.oxygen.middleware.ms.liveserv.client;

import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStatsOld;
import com.coral.oxygen.middleware.ms.liveserv.newclient.LiveUpdatesChannelFactory;
import com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve.Payload;
import com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve.RequestBuilder;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import okhttp3.Request;
import okio.Buffer;
import org.junit.*;

/** Created by azayats on 16.05.17. */
public class RequestBuilderTest {

  private RequestBuilder requestBuilder;
  private List<SubscriptionStats> subscriptions;

  @Before
  public void setUp() {
    subscriptions = new ArrayList<>();
    requestBuilder = new RequestBuilder();
  }

  @After
  public void tearDown() {
    requestBuilder = null;
    subscriptions = null;
  }

  private SubscriptionStats newSubscription(String channel) {
    SubscriptionStats stats = new SubscriptionStatsOld(channel, 1L);
    return stats;
  }

  private SubscriptionStats updatedSubscription(String channel, String watermark) {
    SubscriptionStats stats = new SubscriptionStatsOld(channel, 1L);
    if (watermark.length() > 10) {
      Assert.fail("Too long watermark. Incorrect test configuration");
    }
    while (watermark.length() < 10) {
      watermark = "!" + watermark;
    }
    stats.setWaterMark(watermark);
    return stats;
  }

  private static final long HOURS_24 = 24 * 60 * 1000L;

  @Test
  public void test() throws IOException {
    RequestBuilder builder = new RequestBuilder();
    Payload payload = new Payload(HOURS_24);
    payload.addItem(LiveUpdatesChannelFactory.onEventSubscription("5196558"));
    Request request = builder.build("http://test.push.com", payload);
    Buffer body = new Buffer();
    request.body().writeTo(body);
    Assert.assertEquals("[text=CL0000S0001sEVENT0005196558!!!!!!!!!0]", body.toString());
  }
}
