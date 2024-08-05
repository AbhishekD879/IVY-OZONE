package com.ladbrokescoral.oxygen.questionengine.model.bpp;

import lombok.Data;

@Data
public class FreebetTriggerResponseModel {

  private String token;

  private FreebetFailure freebetFailure;

  private FreebetCalledTrigger freebetCalledTrigger;

 
}
