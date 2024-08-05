package com.egalacoral.spark.liveserver;

import java.io.IOException;
import okhttp3.Request;
import okio.Buffer;
import org.junit.Assert;
import org.junit.Test;

public class RequestBuilderTest {

  private static final long HOURS_24 = 24 * 60 * 1000L;

  @Test
  public void test() throws IOException {
    RequestBuilder builder = new RequestBuilder();
    Payload payload = new Payload(HOURS_24);
    payload.addItem(SubscriptionSubjectFactory.onEventSubscription("5196558"));
    Request request = builder.build("http://test.push.com", payload);
    Buffer body = new Buffer();
    request.body().writeTo(body);
    Assert.assertEquals("[text=CL0000S0001sEVENT0005196558!!!!!!!!!0]", body.toString());
  }
}
