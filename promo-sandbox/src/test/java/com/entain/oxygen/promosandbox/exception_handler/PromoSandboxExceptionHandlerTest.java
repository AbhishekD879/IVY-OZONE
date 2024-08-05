package com.entain.oxygen.promosandbox.exception_handler;

import static org.junit.jupiter.api.Assertions.assertNotNull;

import com.entain.oxygen.promosandbox.exception.BppTokenRequiredException;
import com.entain.oxygen.promosandbox.exception.InvalidBppTokenException;
import com.entain.oxygen.promosandbox.exception.PromoSandboxException;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
class PromoSandboxExceptionHandlerTest {

  @InjectMocks private GlobalExceptionHandler globalExceptionHandler;

  @Test
  void handleInvalidBppTokenExceptionTest() {
    assertNotNull(
        globalExceptionHandler.handleInvalidBppTokenException(
            new InvalidBppTokenException("error")));
  }

  @Test
  void handleBppTokenRequiredExceptionTest() {
    assertNotNull(
        globalExceptionHandler.handleBppTokenRequiredException(
            new BppTokenRequiredException("Bpp token is missing..")));
  }

  @Test
  void promoCmsExceptionTest() {
    assertNotNull(
        globalExceptionHandler.handlePromoCmsException(new PromoSandboxException("error")));
  }

  @Test
  void handleAllOtherExceptionTest() {
    assertNotNull(globalExceptionHandler.handleAllOtherException(new RuntimeException("error")));
  }
}
