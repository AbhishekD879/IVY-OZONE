package com.ladbrokescoral.cashout.bpptoken;

import java.time.Duration;
import lombok.Builder;
import lombok.Data;
import lombok.NonNull;

@Data
@Builder(toBuilder = true)
public class BppToken {
  @NonNull private String token;
  /** How much time is left until this token expires as calculated on object creation (parsing) */
  @NonNull private Duration timeLeftToExpire;
  /** {@link User} object associated (encoded) in this token */
  @NonNull private User encodedUser;
}
