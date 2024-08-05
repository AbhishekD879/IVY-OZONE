package com.ladbrokescoral.reactions.dto;

import static com.ladbrokescoral.reactions.util.ValidationHelper.notNull;

import com.ladbrokescoral.reactions.exception.ErrorCode;
import java.time.OffsetDateTime;

/**
 * @author PBalarangakumar 26-06-2023
 */
public record ErrorDTO(ErrorCode errorCode, String errorMessage, OffsetDateTime timestamp) {

  public ErrorDTO {
    notNull(errorCode, "errorCode");
    notNull(errorMessage, "errorMessage");
    notNull(timestamp, "timestamp");
  }
}
