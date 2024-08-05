package com.ladbrokescoral.oxygen.seo.dto;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = false)
public class ContestResponse extends Response {
  private Contest contest;
}
