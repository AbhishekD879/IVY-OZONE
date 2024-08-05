package com.ladbrokescoral.oxygen.timeline.api.controller.event;

import com.ladbrokescoral.oxygen.timeline.api.model.message.TimelineConfigMessage;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.web.server.LocalServerPort;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.junit4.SpringRunner;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@DirtiesContext
public class TimelineConfigListenerTest {
  @LocalServerPort private String port;
  @Autowired ModelMapper modelMapper;
  @Autowired TimelineConfigListener listener;

  @Test
  public void onPostMessage() {
    StepVerifier.create(
            Mono.fromRunnable(
                () ->
                    listener.onPostMessage(TimelineConfigMessage.builder().enabled(true).build())))
        .verifyComplete();
  }
}
