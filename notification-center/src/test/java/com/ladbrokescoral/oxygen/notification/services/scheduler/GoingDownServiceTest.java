package com.ladbrokescoral.oxygen.notification.services.scheduler;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import com.ladbrokescoral.oxygen.notification.entities.dto.SubscriptionDTO;
import com.ladbrokescoral.oxygen.notification.services.NotificationsMessageHandler;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import com.ladbrokescoral.oxygen.notification.utils.time.TimeProvider;
import java.util.ArrayList;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class GoingDownServiceTest {

  GoingDownService goingDownService;
  Gson gson = new GsonBuilder().create();
  @Mock TimeProvider timeProvider;
  @Mock Subscriptions subscriptions;
  @Mock NotificationsMessageHandler handler;
  MasterSlaveExecutor executor = (runnable, runnable1) -> runnable.run();

  @Before
  public void init() {
    goingDownService =
        new GoingDownService(gson, timeProvider, subscriptions, handler, executor, 100);
  }

  @Test
  public void testNullDateTime() {
    ArrayList<SubscriptionDTO> list = new ArrayList<>();
    list.add(new SubscriptionDTO());
    Mockito.when(subscriptions.findAllByType(Mockito.anyString())).thenReturn(list);
    goingDownService.checkGoingDown();
  }
}
