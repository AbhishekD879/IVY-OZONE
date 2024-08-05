package com.ladbrokescoral.oxygen.questionengine.error;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

/**
 * Standardized error response that supposed to be returned to a client in case of any exception.
 */
@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
@NoArgsConstructor
@Accessors(chain = true)
public class ApiError {
  private HttpStatus httpStatus;
  private String reason;

  /**
   * Application-specific error code. Optional.
   */
  private String errorCode;
  
  private Object context;

  public ResponseEntity<ApiError> asResponseEntity() {
    return new ResponseEntity<>(this, httpStatus);
  }

  public ResponseEntity<Object> asRawResponseEntity() {
    return new ResponseEntity<>(this, httpStatus);
  }
}
