package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Data;

@Data
public class CSVHeaderColumns {
  private String originalName;
  private String displayName;
  private String subtitle;
  private String style;
  private Boolean applyMasking;
}
