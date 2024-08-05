package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class SeoPageDto {
  private String id;
  private String title;
  private String url;
  private String description;
  private String staticBlock;
  private String staticBlockTitle;
}
