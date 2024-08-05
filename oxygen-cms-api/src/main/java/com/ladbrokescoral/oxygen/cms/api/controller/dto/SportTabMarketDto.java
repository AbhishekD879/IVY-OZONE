package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import lombok.Data;

@Data
public class SportTabMarketDto {
  private String templateMarketName;
  private String title;
  private boolean isAggregated;

  @Override
  public boolean equals(Object obj) {
    if (this == obj) return true;
    if (obj == null) return false;
    if (getClass() != obj.getClass()) return false;
    SportTabMarketDto other = (SportTabMarketDto) obj;
    if (templateMarketName == null) {
      if (other.templateMarketName != null) return false;
    } else if (!templateMarketName.equals(other.templateMarketName)) return false;
    return true;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + ((templateMarketName == null) ? 0 : templateMarketName.hashCode());
    return result;
  }
}
