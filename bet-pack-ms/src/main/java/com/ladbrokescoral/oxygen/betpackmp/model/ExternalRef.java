package com.ladbrokescoral.oxygen.betpackmp.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Accessors(chain = true)
public class ExternalRef {
  private String provider;
  private String id;
  private String refType;
}
