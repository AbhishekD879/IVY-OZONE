package com.ladbrokescoral.oxygen.timeline.api.controller.event;

import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import java.time.Instant;
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
public class PostMessageListenerTest {
  @LocalServerPort private String port;
  @Autowired ModelMapper modelMapper;
  @Autowired PostMessageListener listener;

  @Test
  public void onPostMessage() {
    PostMessage postMessage = PostMessage.builder().build();
    postMessage.setCampaignId("12345");
    postMessage.setCampaignName("abcd");
    postMessage.setPinned(true);
    postMessage.setHeaderText("abcd");
    postMessage.setSpotlight(true);
    postMessage.setId("12345");
    postMessage.setText("hello");
    postMessage.setVerdict(true);
    Instant instant = Instant.now();
    postMessage.setCreatedDate(instant);
    postMessage.setBrand("coral");
    StepVerifier.create(Mono.fromRunnable(() -> listener.onPostMessage(postMessage)))
        .verifyComplete();
  }
}
