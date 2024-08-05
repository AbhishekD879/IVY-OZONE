package com.ladbrokescoral.reactions.config;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import reactor.netty.http.client.HttpClient;

@MockitoSettings(strictness = Strictness.LENIENT)
@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = {WebClientConfig.class})
class WebClientConfigTest {

  @Autowired WebClientConfig webClientConfig;
  @MockBean HttpClient httpClient;

  @Test
  void testHttpClient() {
    Assertions.assertNotNull(webClientConfig.webClient());
  }
}
