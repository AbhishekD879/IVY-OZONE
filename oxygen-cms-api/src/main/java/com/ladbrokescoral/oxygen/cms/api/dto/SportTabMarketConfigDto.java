package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class SportTabMarketConfigDto {
  private String templateMarketName;
  private String title;

  public boolean equals(Object obj) {
    if (this == obj) return true;
    if (obj == null) return false;
    if (getClass() != obj.getClass()) return false;
    SportTabMarketConfigDto other = (SportTabMarketConfigDto) obj;
    if (templateMarketName == null) {
      if (other.templateMarketName != null) return false;
    } else if (!templateMarketName.equals(other.templateMarketName)) return false;
    return true;
  }

  @Override
  public int hashCode() {
    return templateMarketName == null ? 0 : 1;
  }
}
