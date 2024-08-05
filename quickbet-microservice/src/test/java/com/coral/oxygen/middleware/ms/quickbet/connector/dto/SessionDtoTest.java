package com.coral.oxygen.middleware.ms.quickbet.connector.dto;

import static org.assertj.core.api.Assertions.assertThat;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.utils.TestUtils;
import java.util.List;
import org.junit.jupiter.api.Test;

public class SessionDtoTest {

  @Test
  public void testDeserializeSessionDtoWithSimpleOutcome() {
    // WHEN
    SessionDto sessionDto =
        TestUtils.deserializeWithJackson("sessionDtoWithSimpleOutcome.json", SessionDto.class);

    // THEN
    assertThat(sessionDto).isNotNull();
    assertThat(sessionDto.getSessionId()).isEqualTo("e1995a3b-fdb6-44ec-abf3-fe715ed7eff5");

    RegularSelectionRequest regularSelectionRequest = sessionDto.getRegularSelectionRequest();
    List<Long> outcomeIds = regularSelectionRequest.getOutcomeIds();
    assertThat(outcomeIds).containsExactly(464888859L);
    assertThat(regularSelectionRequest.getSelectionType()).isEqualTo("simple");
  }

  @Test
  public void testDeserializeSessionDtoWithScorecastOutcome() {
    // WHEN
    SessionDto sessionDto =
        TestUtils.deserializeWithJackson("sessionDtoWithScorecast.json", SessionDto.class);

    // THEN
    assertThat(sessionDto).isNotNull();
    assertThat(sessionDto.getSessionId()).isEqualTo("2f34465b-12b7-4538-8a1f-2bc41d903fb2");

    RegularSelectionRequest regularSelectionRequest = sessionDto.getRegularSelectionRequest();
    List<Long> outcomeIds = regularSelectionRequest.getOutcomeIds();
    assertThat(outcomeIds).containsExactlyInAnyOrder(111L, 222L);
    assertThat(regularSelectionRequest.getAdditional().getScorecastMarketId()).isEqualTo(333L);
    assertThat(regularSelectionRequest.getSelectionType()).isEqualTo("scorecast");
  }
}
