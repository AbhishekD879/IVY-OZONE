package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.apache.commons.lang3.ObjectUtils;

@Builder
@Data
@EqualsAndHashCode
@NoArgsConstructor
@AllArgsConstructor
public class SystemConfigProperty {

  private String multiselectValue;
  private String name;
  private String type;
  private Object value;
  private Object structureValue;

  public Object getStructureValueOrDefault() {
    return ObjectUtils.defaultIfNull(structureValue, value);
  }
}
