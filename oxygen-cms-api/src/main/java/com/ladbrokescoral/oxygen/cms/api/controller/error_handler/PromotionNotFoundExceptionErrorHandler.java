package com.ladbrokescoral.oxygen.cms.api.controller.error_handler;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.AbstractCrudController;
import com.ladbrokescoral.oxygen.cms.api.exception.PromoLeaderboardException;
import com.ladbrokescoral.oxygen.cms.api.exception.PromotionNotFound;
import java.text.MessageFormat;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.servlet.error.ErrorAttributes;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;

@ControllerAdvice(basePackageClasses = AbstractCrudController.class)
@Slf4j
public class PromotionNotFoundExceptionErrorHandler extends AbstractErrorHandler {

  private static final String MESSAGE_TEMPLATE = "Promotions with ids {0} are not found";

  @Autowired
  public PromotionNotFoundExceptionErrorHandler(ErrorAttributes errorAttributes) {
    super(errorAttributes);
  }

  @ExceptionHandler(PromotionNotFound.class)
  @ResponseStatus(HttpStatus.BAD_REQUEST)
  @ResponseBody
  public Map<String, Object> validationError(PromotionNotFound e, HttpServletRequest request) {
    String message = MessageFormat.format(MESSAGE_TEMPLATE, e.getPromotionId());
    return buildResponseEntity(
        request,
        HttpStatus.BAD_REQUEST.value(),
        "PromotionIdsIsNotFound",
        e.getPromotionId(),
        message);
  }

  @ExceptionHandler(PromoLeaderboardException.class)
  @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
  @ResponseBody
  public ResponseDto handleInternalServerException(Exception e) {
    log.error("Internal Server Error", e);
    return new ResponseDto(e.getMessage());
  }

  @Data
  @AllArgsConstructor
  public static class ResponseDto {
    private String message;
  }
}
