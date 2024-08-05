package com.ladbrokescoral.reactions.controller;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.ladbrokescoral.reactions.dto.ErrorDTO;
import com.ladbrokescoral.reactions.exception.*;
import org.junit.jupiter.api.Test;

class ReactionControllerAdviceTest {
  @Test
  void handleBadRequestTest() {
    BadRequestException exception = new BadRequestException("Invalid request");
    ReactionControllerAdvice advice = new ReactionControllerAdvice();
    ErrorDTO response = advice.handleBadRequest(exception);
    assertEquals(ErrorCode.BAD_REQUEST, response.errorCode());
    assertEquals("Invalid request", response.errorMessage());
  }

  @Test
  void handleServerErrorTest() {
    ServiceExecutionException exception = new ServiceExecutionException("Invalid request");
    ReactionControllerAdvice advice = new ReactionControllerAdvice();
    ErrorDTO response = advice.handleServerError(exception);
    assertEquals(ErrorCode.SERVER_ERROR, response.errorCode());
    assertEquals("Invalid request", response.errorMessage());
  }

  @Test
  void handleUnexpectedTest() {
    RuntimeException exception = new RuntimeException("Invalid request");
    ReactionControllerAdvice advice = new ReactionControllerAdvice();
    ErrorDTO response = advice.handleUnexpected(exception);
    assertEquals(ErrorCode.SERVER_ERROR, response.errorCode());
    assertEquals("An unexpected error has occurred.", response.errorMessage());
  }

  @Test
  void handleNotFoundTest() {
    GenericException exception = new UserNotFoundException("Not found error occurred. ");
    ReactionControllerAdvice advice = new ReactionControllerAdvice();
    ErrorDTO response = advice.handleNotFound(exception);
    assertEquals(ErrorCode.NOT_FOUND, response.errorCode());
    assertEquals("Not found error occurred. ", response.errorMessage());
  }
}
