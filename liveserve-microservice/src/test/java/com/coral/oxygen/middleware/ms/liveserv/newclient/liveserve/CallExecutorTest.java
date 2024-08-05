package com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve;

import com.coral.siteserver.api.SiteServerException;
import java.lang.reflect.Method;
import lombok.SneakyThrows;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class CallExecutorTest {

  @InjectMocks private CallExecutor callExecutor;

  @Mock private LiveServerListener listener;

  @SneakyThrows
  @Test
  public void testNotify() {
    Message message = new Message();
    Mockito.doThrow(new SiteServerException()).when(listener).onMessage(Mockito.any());

    Method method = CallExecutor.class.getDeclaredMethod("notify", Message.class);
    method.setAccessible(true);
    Object invoke = method.invoke(callExecutor, message);

    Mockito.verify(listener).onError(Mockito.any());
  }
}
