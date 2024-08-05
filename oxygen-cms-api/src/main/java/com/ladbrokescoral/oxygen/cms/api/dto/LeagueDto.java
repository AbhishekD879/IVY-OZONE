package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class LeagueDto {
  private String name;
  private Integer typeId;
  private Integer categoryId;
  private String ssCategoryCode;
  private String banner;
  private String betBuilderUrl;
  private String leagueUrl;
  private String redirectionUrl;
  private String tabletBanner;
}
