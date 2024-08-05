package com.ladbrokescoral.oxygen.cms.api.controller.error_handler;

import static org.junit.jupiter.api.Assertions.*;

import com.ladbrokescoral.oxygen.cms.api.exception.LuckyDipConfigNotFoundException;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class ApiErrorHandlerTest extends BDDMockito {

  @InjectMocks private ApiErrorHandler apiErrorHandler;

  @Test
  void handleInternalServerExceptionTest() throws Exception {
    ApiErrorHandler.ResponseDto responseDto =
        apiErrorHandler.handleInternalServerException(
            new LuckyDipConfigNotFoundException("Lucky Dip not found"));
    assertNotNull(responseDto);
  }
}
