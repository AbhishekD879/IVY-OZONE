package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import lombok.Data;

@Data
public class InplayStatsDisplayDto {

  @Brand private String brand;

  private Integer categoryId;

  private String label;

  private String statsKey;

  private Double sortOrder;
}
