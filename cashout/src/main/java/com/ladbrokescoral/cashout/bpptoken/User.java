package com.ladbrokescoral.cashout.bpptoken;

import java.io.Serializable;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

// FIXME copy-past from bpp - to be moved to separate library for token management
// Library will be created in scope of BMA-54770
@Data
@Builder(toBuilder = true)
@AllArgsConstructor
@NoArgsConstructor
@Deprecated
public class User implements Serializable {

  private static final long serialVersionUID = 4200630021708808281L;

  private String customerRef;
  private String oxiApiToken;
  private String sportBookUserName;
  private String currency;

  public User(String name) {
    this.sportBookUserName = name;
  }
}
