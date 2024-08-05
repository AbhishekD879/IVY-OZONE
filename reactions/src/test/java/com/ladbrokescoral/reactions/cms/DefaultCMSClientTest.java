package com.ladbrokescoral.reactions.cms;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.reactions.client.cms.DefaultCMSClient;
import com.ladbrokescoral.reactions.config.ReactionPropertiesConfig;
import com.ladbrokescoral.reactions.config.WebClientConfig;
import java.util.List;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.reactive.server.WebTestClient;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import reactor.netty.http.client.HttpClient;
import reactor.test.StepVerifier;

@MockitoSettings(strictness = Strictness.LENIENT)
@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = {WebClientConfig.class})
class DefaultCMSClientTest {
  @Mock private WebClient webClient;

  @Mock private ReactionPropertiesConfig reactionPropertiesConfig;
  @MockBean HttpClient httpClient;
  private DefaultCMSClient cmsClient;
  @Autowired WebClientConfig webClientConfig;

  @Mock private WebClient.Builder webClientBuilder;

  WebClient webClient1;

  private WebTestClient webTestClient;

  @BeforeEach
  public void setup() {
    MockitoAnnotations.openMocks(this);
    webClient1 = webClientConfig.webClient();
    webTestClient =
        WebTestClient.bindToController(new DefaultCMSClient(reactionPropertiesConfig, webClient1))
            .build();
    cmsClient = new DefaultCMSClient(reactionPropertiesConfig, webClient1);
  }

  @Test
  void testGetActiveSelectionIdAndSurfaceBetIdKeys() {
    String cmsBaseUrl = "http://localhost:8080/";
    String cmsSurfaceBetApiPath = "/api/surfacebet";
    WebClient webClient = mock(WebClient.class);
    when(reactionPropertiesConfig.getCmsBaseUrl()).thenReturn(cmsBaseUrl);
    when(reactionPropertiesConfig.getCmsSurfaceBetApiPath()).thenReturn(cmsSurfaceBetApiPath);
    Mono<List<String>> activeSelectionIdAndSurfaceBetIdKeys =
        cmsClient.getActiveSelectionIdAndSurfaceBetIdKeys();
    Assertions.assertNotNull(activeSelectionIdAndSurfaceBetIdKeys);
  }

  @Test
  void testGetCmsHealthSuccess() {
    Mockito.when(reactionPropertiesConfig.getCmsBaseUrl()).thenReturn("http://localhost:8080/");
    Mockito.when(reactionPropertiesConfig.getCmsHealthApiPath()).thenReturn("actuator/health");
    JsonNode sampleResponse = createUpResponse();

    Mockito.when(webClientBuilder.baseUrl(Mockito.anyString())).thenReturn(webClientBuilder);
    Mockito.when(webClientBuilder.build()).thenReturn(WebClient.builder().build());
    webTestClient
        .get()
        .uri("actuator/health")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isNotFound()
        .expectBody(JsonNode.class);

    StepVerifier.create(new DefaultCMSClient(reactionPropertiesConfig, webClient1).getCmsHealth())
        .expectNext(sampleResponse);
  }

  private JsonNode createUpResponse() {
    String upResponseJson =
        "{\"status\":\"UP\",\"components\":{\"CMS\":{\"status\":\"UP\",\"details\":{\"additionalStatus\":\"HEALTHY\",\"message\":\"Successfully connected to CMS.\",\"ping\":38}}}}";

    try {
      ObjectMapper objectMapper = new ObjectMapper();
      return objectMapper.readTree(upResponseJson);
    } catch (Exception e) {
      throw new RuntimeException("Error parsing JSON response", e);
    }
  }
}
