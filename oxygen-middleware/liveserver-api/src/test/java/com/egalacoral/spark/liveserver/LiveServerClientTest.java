package com.egalacoral.spark.liveserver;

import com.egalacoral.spark.liveserver.meta.EventMetaCachedRepoImpl;
import java.io.IOException;
import java.util.concurrent.TimeUnit;
import org.junit.Assert;
import org.junit.Test;
import org.mockito.Mockito;

public class LiveServerClientTest extends BaseTest {

  private static final Long HOURS_5 = 5 * 60 * 60L;

  @Test
  public void testConnect() throws IOException, InterruptedException {
    TestListener liveServerListener = new TestListener();
    LiveServerClient client = createClient(liveServerListener);
    client.subscribeOnEvent("5196558");
    client.connect();
    Assert.assertTrue(client.isRunning());
    client.getCallExecutor().getExecutorService().shutdown();
    client.getCallExecutor().getExecutorService().awaitTermination(300, TimeUnit.MILLISECONDS);
    Assert.assertNotNull(liveServerListener.messages.get(0));
    Assert.assertFalse(client.getCallExecutor().getExecutorService().isTerminated());
  }

  @Test
  public void testDisconnect() throws IOException, InterruptedException {
    TestListener liveServerListener = new TestListener();
    LiveServerClient client = createClient(liveServerListener);
    client.subscribeOnEvent("5196558");
    client.connect();
    Assert.assertTrue(client.isRunning());
    client.disconnect();
    Assert.assertFalse(client.isRunning());
    client.getCallExecutor().getExecutorService().awaitTermination(300, TimeUnit.MILLISECONDS);
    Assert.assertTrue(client.getCallExecutor().getExecutorService().isTerminated());
  }

  @Test
  public void testRestart() throws IOException, InterruptedException {
    TestListener liveServerListener = new TestListener();
    LiveServerClient client = createClient(liveServerListener);
    client.subscribeOnEvent("5196558");
    Assert.assertFalse(client.isRunning());
    client.connect();
    Assert.assertTrue(client.isRunning());
    client.disconnect();
    Assert.assertFalse(client.isRunning());
    client.getCallExecutor().getExecutorService().awaitTermination(300, TimeUnit.MILLISECONDS);
    client.connect();
    Assert.assertTrue(client.isRunning());
    client.getCallExecutor().getExecutorService().awaitTermination(300, TimeUnit.MILLISECONDS);
    Assert.assertFalse(client.getCallExecutor().getExecutorService().isTerminated());
  }

  private LiveServerClient createClient(TestListener liveServerListener) throws IOException {
    Call call = Mockito.mock(Call.class);
    Mockito.when(call.execute(Mockito.any())).thenReturn(createResponse());
    LiveServerClient client =
        new LiveServerClient(
            "http://push.test.com",
            call,
            HOURS_5,
            liveServerListener,
            Mockito.mock(EventMetaCachedRepoImpl.class),
            "123");
    return client;
  }
}
