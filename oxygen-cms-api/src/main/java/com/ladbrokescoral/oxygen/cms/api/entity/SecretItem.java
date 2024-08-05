package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SecretItem {

  private String key;
  private String value;
}
