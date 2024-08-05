package com.ladbrokescoral.aggregation;

import com.ladbrokescoral.aggregation.config.EmbededRedis;
import com.ladbrokescoral.aggregation.exception.BadRequestException;
import com.ladbrokescoral.aggregation.service.AggregationService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.ApplicationContext;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.reactive.server.WebTestClient;

@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT, classes = EmbededRedis.class)
@ActiveProfiles("UNIT")
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
public class AggregationControllerTest {

  private WebTestClient webClient;
  @MockBean AggregationService aggregationService;
  @Autowired ApplicationContext webApplicationContext;

  @BeforeEach
  public void setup() {
    this.webClient = WebTestClient.bindToApplicationContext(webApplicationContext).build();
  }

  @Test
  public void imageAggregation() {

    webClient.get().uri("/silks/racingpost/1,2,3,4").exchange().expectStatus().isOk();
  }

  @Test
  public void requestTeamTalk() {
    webClient.get().uri("/silks/teamtalk/1,2,3,4").exchange().expectStatus().isOk();
  }

  @Test
  public void requestV2() {
    webClient.get().uri("/silks/racingpost/v2/1,2,3,4").exchange().expectStatus().isOk();
  }

  @Test
  public void requestV3() {
    webClient.get().uri("/silks/racingpost/v3/1,2,3,4").exchange().expectStatus().isOk();
  }

  @Test
  public void imageAggregationTestOriginCoral() {

    webClient
        .get()
        .uri("/silks/racingpost/1,2,3,4")
        .header("TestOrigin", "coral.co.uk")
        .exchange()
        .expectStatus()
        .isOk();

    Mockito.verify(aggregationService, Mockito.times(1))
        .imageAggregationByProvider(Mockito.any(), Mockito.eq("racingpost-coral"), Mockito.any());
  }

  @Test
  public void imageAggregationTestOriginAny() {

    webClient
        .get()
        .uri("/silks/racingpost/1,2,3,4")
        .header("TestOrigin", "test")
        .exchange()
        .expectStatus()
        .isOk();

    Mockito.verify(aggregationService, Mockito.times(1))
        .imageAggregationByProvider(
            Mockito.any(), Mockito.eq("racingpost-ladbrokes"), Mockito.any());
  }

  @Test
  public void imageAggregationNoTestOrigin() {

    webClient.get().uri("/silks/racingpost/1,2,3,4").exchange().expectStatus().isOk();

    Mockito.verify(aggregationService, Mockito.times(1))
        .imageAggregationByProvider(
            Mockito.any(), Mockito.eq("racingpost-ladbrokes"), Mockito.any());
  }

  @Test
  public void imageAggregationNoTestEmpty() {

    webClient
        .get()
        .uri("/silks/racingpost/1,2,3,4")
        .header("TestOrigin", "")
        .exchange()
        .expectStatus()
        .isOk();

    Mockito.verify(aggregationService, Mockito.times(1))
        .imageAggregationByProvider(
            Mockito.any(), Mockito.eq("racingpost-ladbrokes"), Mockito.any());
  }

  @Test
  public void imageAggregationV2TestOriginCoral() {

    webClient
        .get()
        .uri("/silks/racingpost/v2/1,2,3,4")
        .header("TestOrigin", "coral.co.uk")
        .exchange()
        .expectStatus()
        .isOk();

    Mockito.verify(aggregationService, Mockito.times(1))
        .imageAggregationByProvider(
            Mockito.any(), Mockito.eq("racingpost-v2-coral"), Mockito.any());
  }

  @Test
  public void imageAggregationV3TestOriginCoral() {

    webClient
        .get()
        .uri("/silks/racingpost/v3/1,2,3,4")
        .header("TestOrigin", "coral.co.uk")
        .exchange()
        .expectStatus()
        .isOk();

    Mockito.verify(aggregationService, Mockito.times(1))
        .imageAggregationByBrand(Mockito.any(), Mockito.eq("coral"), Mockito.any());
  }

  @Test
  public void imageAggregationBadRequestException() {

    Mockito.doThrow(new BadRequestException("Error while fetching silks"))
        .when(aggregationService)
        .imageAggregationByBrand(Mockito.any(), Mockito.any(), Mockito.any());

    webClient
        .get()
        .uri("/silks/racingpost/v3/1,2,3,4")
        .header("TestOrigin", "coral.co.uk")
        .exchange()
        .expectStatus()
        .isBadRequest();
  }
}
