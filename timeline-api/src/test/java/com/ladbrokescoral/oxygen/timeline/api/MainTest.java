package com.ladbrokescoral.oxygen.timeline.api;

import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.timeline.api.registrators.TimelineServiceRegistry;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.test.annotation.DirtiesContext;

@RunWith(MockitoJUnitRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@DirtiesContext
public class MainTest {

  @Mock private ConfigurableApplicationContext applicationContext;
  @Mock private TimelineServiceRegistry timelineServiceRegistry;

  @Test
  public void testMainThrowsException() {
    boolean thrown = false;
    when(applicationContext.getBean(TimelineServiceRegistry.class))
        .thenReturn(timelineServiceRegistry);
    doThrow(new RuntimeException()).when(timelineServiceRegistry).load();
    try {
      TimelineApiApplication.startTimeLineApplication(applicationContext);
    } catch (Exception e) {
      thrown = true;
    }
    assertTrue(thrown);
  }

  @Test
  public void testMain() {
    TimelineApiApplication.main(new String[] {});
    assertTrue(true);
  }
}
