package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import lombok.Data;

@Data
public class InplayStatsSortingDto {

  @Brand private String brand;

  private Integer categoryId;

  private String label;

  private String referenceKey;

  private boolean enabled;

  private Double sortOrder;
}
