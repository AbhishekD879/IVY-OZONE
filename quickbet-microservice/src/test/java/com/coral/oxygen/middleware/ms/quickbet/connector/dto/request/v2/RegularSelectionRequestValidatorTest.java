package com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2;

import static org.assertj.core.api.Assertions.assertThatCode;
import static org.assertj.core.api.Assertions.assertThatExceptionOfType;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/** Created by azayats on 01.12.17. */
class RegularSelectionRequestValidatorTest {

  private RegularSelectionRequestValidator validator;

  @BeforeEach
  void setUp() {
    validator = new RegularSelectionRequestValidator();
  }

  @Test
  void testSimpleRequestSuccess() {
    RegularSelectionRequest request = simpleRequest(1L);
    assertThatCode(() -> validator.validate(request)).doesNotThrowAnyException();
  }

  @Test
  void testNullRequestType() {
    RegularSelectionRequest request = simpleRequest(1L);
    request.setSelectionType(null);

    assertThatExceptionOfType(RequestValidationException.class)
        .isThrownBy(() -> validator.validate(request));
  }

  @Test
  void testInvalidRequestType() {
    RegularSelectionRequest request = simpleRequest(1L);
    request.setSelectionType("SOME INVALID VALUE");

    assertThatExceptionOfType(RequestValidationException.class)
        .isThrownBy(() -> validator.validate(request));
  }

  @Test
  void testSimpleRequestNullOutcomeIds() {
    RegularSelectionRequest request = simpleRequest(1L);
    request.setOutcomeIds(null);

    assertThatExceptionOfType(RequestValidationException.class)
        .isThrownBy(() -> validator.validate(request));
  }

  @Test
  void testSimpleRequestEmptyOutcomeIds() {
    RegularSelectionRequest request = simpleRequest(1L);
    request.setOutcomeIds(new ArrayList<>());

    assertThatExceptionOfType(RequestValidationException.class)
        .isThrownBy(() -> validator.validate(request));
  }

  @Test
  void testSimpleRequestTwoOutcomeIds() {
    RegularSelectionRequest request = simpleRequest(1L);
    List<Long> ids = new ArrayList<>();
    ids.add(1L);
    ids.add(2L);
    request.setOutcomeIds(ids);

    assertThatExceptionOfType(RequestValidationException.class)
        .isThrownBy(() -> validator.validate(request));
  }

  @Test
  void testSimpleRequestNullOutcomeId() {
    RegularSelectionRequest request = simpleRequest(1L);
    List<Long> ids = new ArrayList<>();
    ids.add(null);
    request.setOutcomeIds(ids);

    assertThatExceptionOfType(RequestValidationException.class)
        .isThrownBy(() -> validator.validate(request));
  }

  @Test
  void testSimpleRequestAddtionalExists() {
    RegularSelectionRequest request = simpleRequest(1L);
    request.setAdditional(new RegularSelectionRequest.AdditionalParameters());

    assertThatExceptionOfType(RequestValidationException.class)
        .isThrownBy(() -> validator.validate(request));
  }

  @Test
  void testScorecastRequestSuccess() {
    RegularSelectionRequest request = scorecastRequest(1L, 2L, 3L);

    assertThatCode(() -> validator.validate(request)).doesNotThrowAnyException();
  }

  @Test
  void testScorecastRequestNullOutcomeIds() {
    RegularSelectionRequest request = scorecastRequest(1L, 2L, 3L);
    request.setOutcomeIds(null);

    assertThatExceptionOfType(RequestValidationException.class)
        .isThrownBy(() -> validator.validate(request));
  }

  @Test
  void testScorecastRequestEmptyOutcomeIds() {
    RegularSelectionRequest request = scorecastRequest(1L, 2L, 3L);
    request.setOutcomeIds(new ArrayList<>());

    assertThatExceptionOfType(RequestValidationException.class)
        .isThrownBy(() -> validator.validate(request));
  }

  @Test
  void testScorecastRequestOneOutcomeIds() {
    RegularSelectionRequest request = scorecastRequest(1L, 2L, 3L);
    List<Long> ids = new ArrayList<>();
    ids.add(1L);
    request.setOutcomeIds(ids);

    assertThatExceptionOfType(RequestValidationException.class)
        .isThrownBy(() -> validator.validate(request));
  }

  @Test
  void testScorecastRequestThreeOutcomeIds() {
    RegularSelectionRequest request = scorecastRequest(1L, 2L, 3L);
    List<Long> ids = new ArrayList<>();
    ids.add(1L);
    ids.add(2L);
    ids.add(3L);
    request.setOutcomeIds(ids);

    assertThatExceptionOfType(RequestValidationException.class)
        .isThrownBy(() -> validator.validate(request));
  }

  @Test
  void testScorecastRequestNullFirstOutcomeId() {
    RegularSelectionRequest request = scorecastRequest(1L, 2L, 3L);
    List<Long> ids = new ArrayList<>();
    ids.add(null);
    ids.add(2L);
    request.setOutcomeIds(ids);

    assertThatExceptionOfType(RequestValidationException.class)
        .isThrownBy(() -> validator.validate(request));
  }

  @Test
  void testScorecastRequestNullSecondOutcomeId() {
    RegularSelectionRequest request = scorecastRequest(1L, 2L, 3L);
    List<Long> ids = new ArrayList<>();
    ids.add(2L);
    ids.add(null);
    request.setOutcomeIds(ids);

    assertThatExceptionOfType(RequestValidationException.class)
        .isThrownBy(() -> validator.validate(request));
  }

  @Test
  void testScorecastRequestNullAdditional() {
    RegularSelectionRequest request = scorecastRequest(1L, 2L, 3L);
    request.setAdditional(null);

    assertThatExceptionOfType(RequestValidationException.class)
        .isThrownBy(() -> validator.validate(request));
  }

  @Test
  void testScorecastRequestNullScorecastMarketId() {
    RegularSelectionRequest request = scorecastRequest(1L, 2L, 3L);
    request.getAdditional().setScorecastMarketId(null);

    assertThatExceptionOfType(RequestValidationException.class)
        .isThrownBy(() -> validator.validate(request));
  }

  private RegularSelectionRequest simpleRequest(long outcomeId) {
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setSelectionType(RegularSelectionRequest.SIMPLE_SELECTION_TYPE);
    request.setOutcomeIds(Collections.singletonList(outcomeId));
    return request;
  }

  private RegularSelectionRequest scorecastRequest(
      long outcomeId1, long outcomeId2, long scorecastMarketId) {
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setSelectionType(RegularSelectionRequest.SCORECAST_SELECTION_TYPE);
    request.setOutcomeIds(Arrays.asList(outcomeId1, outcomeId2));
    RegularSelectionRequest.AdditionalParameters additionalParameters =
        new RegularSelectionRequest.AdditionalParameters();
    request.setAdditional(additionalParameters);
    additionalParameters.setScorecastMarketId(scorecastMarketId);
    return request;
  }
}
