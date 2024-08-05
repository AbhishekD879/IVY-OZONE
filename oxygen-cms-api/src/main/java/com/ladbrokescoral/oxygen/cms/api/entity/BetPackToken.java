package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.Size;
import lombok.Data;
import lombok.NonNull;

@Data
public class BetPackToken {
  @NonNull private String id;

  @NonNull
  @Size(max = 25, message = "TokenId should be max of 25 chars")
  private String tokenId;

  @NonNull
  @Size(max = 50, message = "TokenTitle should be max of 50 chars")
  private String tokenTitle;

  @NonNull private Double tokenValue;
  @NonNull private String deepLinkUrl;
  @NonNull private boolean isActive;
}
