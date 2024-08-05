package com.ladbrokescoral.oxygen.notification.utils;

import com.ladbrokescoral.oxygen.notification.entities.dto.MessageDTO;
import java.util.Locale;
import java.util.function.Function;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.MessageSource;
import org.springframework.context.i18n.LocaleContextHolder;
import org.springframework.http.HttpStatus;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;

@Slf4j
@ControllerAdvice
public class NotNullHandler {

  private final MessageSource messageSource;

  @Autowired
  public NotNullHandler(final MessageSource messageSource) {
    this.messageSource = messageSource;
  }

  @ExceptionHandler(MethodArgumentNotValidException.class)
  @ResponseStatus(HttpStatus.BAD_REQUEST)
  @ResponseBody
  public MessageDTO processValidationError(MethodArgumentNotValidException exception) {

    final Function<FieldError, MessageDTO> converter =
        (e) -> {
          MessageDTO messageDTO = null;
          if (e != null) {
            Locale currentLocale = LocaleContextHolder.getLocale();
            String message = messageSource.getMessage(e.getDefaultMessage(), null, currentLocale);
            messageDTO = MessageDTO.from(message);
          }
          return messageDTO;
        };

    MessageDTO messageDto = converter.apply(exception.getBindingResult().getFieldError());
    return messageDto;
  }
}
