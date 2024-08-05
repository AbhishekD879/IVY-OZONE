package com.ladbrokescoral.oxygen.cms.api;

import com.ladbrokescoral.oxygen.cms.InitListener;
import com.ladbrokescoral.oxygen.cms.util.CustomEvent;
import com.ladbrokescoral.oxygen.cms.util.EventEnum;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mockito;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.web.context.WebApplicationContext;

@RunWith(SpringRunner.class)
public class InitListenerTest {

  @MockBean private WebApplicationContext applicationEventPublisher;

  @InjectMocks private InitListener initListener;

  @Before
  public void init() {
    initListener = new InitListener(applicationEventPublisher);
    Mockito.doNothing()
        .when(applicationEventPublisher)
        .publishEvent(Mockito.any(CustomEvent.class));
  }

  @Test
  public void onApplicationEventTest() {
    initListener.onApplicationEvent(null);
    Mockito.verify(applicationEventPublisher, Mockito.times(2 * getCount()))
        .publishEvent(Mockito.any(CustomEvent.class));
  }

  private int getCount() {
    int count = 0;
    for (EventEnum e : EventEnum.values()) {
      if (e.isPublishEvent()) {
        count++;
      }
    }
    return count;
  }
}
