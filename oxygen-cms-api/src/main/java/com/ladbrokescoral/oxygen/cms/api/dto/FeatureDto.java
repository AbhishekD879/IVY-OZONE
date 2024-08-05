package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;
import org.springframework.data.annotation.Id;

@Data
public class FeatureDto {
  @Id private String id;
  private String title;
  private String shortDescription;
  private String description;
  private String validityPeriodStart;
  private String validityPeriodEnd;
  private String uriMedium;
  private Integer widthMedium;
  private Integer heightMedium;
  private Boolean disabled;
  private List<String> showToCustomer;
  private String filename;
}
