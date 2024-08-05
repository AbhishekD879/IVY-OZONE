package com.ladbrokescoral.cashout.api.client.entity.request;

import com.fasterxml.jackson.annotation.JsonIgnore;
import java.util.List;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class CashoutRequest {
  private List<CashoutOfferRequest> cashoutOfferRequests;
  private Boolean shouldActivate;

  @JsonIgnore
  public boolean isActivationRequest() {
    return Boolean.TRUE.equals(shouldActivate);
  }
}
