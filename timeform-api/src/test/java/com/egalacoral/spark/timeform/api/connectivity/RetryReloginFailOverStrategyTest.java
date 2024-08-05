package com.egalacoral.spark.timeform.api.connectivity;

import com.egalacoral.spark.timeform.api.TimeFormException;
import okhttp3.MediaType;
import okhttp3.ResponseBody;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import retrofit2.Response;

public class RetryReloginFailOverStrategyTest {

  private static final int RETRY_COUNT = 3;
  private static final int RELOGIN_COUNT = 2;

  int reloginCount = 2;

  private RetryReloginFailOverStrategy strategy;

  @Before
  public void setUp() {
    strategy = new RetryReloginFailOverStrategy(RETRY_COUNT, RELOGIN_COUNT);
  }

  @Test
  public void testRetry() {
    for (int i = 0; i <= RETRY_COUNT; i++) {
      FailOverStrategy.FailOverAction action = strategy.onError(new TimeFormException(), i);
      Assert.assertEquals(FailOverStrategy.FailOverAction.RETRY, action);
    }
    FailOverStrategy.FailOverAction action = strategy.onError(new TimeFormException(), RETRY_COUNT + 1);
    Assert.assertNull(action);
  }

  @Test
  public void testReloginRetry() {
    for (int i = 0; i <= RELOGIN_COUNT; i++) {
      FailOverStrategy.FailOverAction action = strategy.onReloginError(new TimeFormException(), i);
      Assert.assertEquals(FailOverStrategy.FailOverAction.RETRY, action);
    }
    FailOverStrategy.FailOverAction action = strategy.onReloginError(new TimeFormException(), RELOGIN_COUNT + 1);
    Assert.assertNull(action);
  }

  @Test
  public void testRelogin() {
    // in fact we receive 302 redirect but for test 400 is used
    Response response = Response.error(400, ResponseBody.create(MediaType.parse("application/json"), "{'odata.error':{'code':'','message':{'lang':'en-US','value':'Authorization has been denied for this request.'}}}"));
    FailOverStrategy.FailOverAction action = strategy.onError(new TimeFormException(response), 0);
    Assert.assertEquals(FailOverStrategy.FailOverAction.RELOGIN_AND_RETRY, action);
  }

  @Test
  public void testUnparsableResponse() {
    // in fact we receive 302 redirect but for test 400 is used
    Response response = Response.error(400, ResponseBody.create(MediaType.parse("application/json"), "EEE"));
    FailOverStrategy.FailOverAction action = strategy.onError(new TimeFormException(response), 0);
    Assert.assertEquals(FailOverStrategy.FailOverAction.RETRY, action);
  }

}
