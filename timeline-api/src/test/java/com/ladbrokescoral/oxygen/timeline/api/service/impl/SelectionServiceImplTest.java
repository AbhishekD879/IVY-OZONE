package com.ladbrokescoral.oxygen.timeline.api.service.impl;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.model.Event;
import java.util.Optional;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@RunWith(SpringRunner.class)
public class SelectionServiceImplTest {
  @MockBean SubscriptionServiceImpl subscriptionService;
  @MockBean ModelMapper modelMapper;

  @Test
  public void testSubscribeOnUpdates() {
    SelectionServiceImpl selectionService =
        new SelectionServiceImpl(subscriptionService, modelMapper);
    when(subscriptionService.subscribe(any())).thenReturn(getEvent());
    StepVerifier.create(Mono.fromRunnable(() -> selectionService.subscribeOnUpdates("123")))
        .verifyComplete();
  }

  private Optional<Event> getEvent() {
    Event event = new Event();
    event.setId("12345");
    event.setName("testEvent");
    return Optional.of(event);
  }
}
