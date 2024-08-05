package com.ladbrokescoral.oxygen.notification.entities;

import java.util.Date;
import lombok.Builder;
import lombok.Data;
import org.springframework.http.HttpStatus;

@Data
@Builder
public class ErrorResponse {

  private Date date = new Date();

  private HttpStatus status;

  private String errorMessage;
}
