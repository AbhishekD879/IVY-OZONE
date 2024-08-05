package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class LeagueDTO {
  private String name;
  private Integer typeId;
  private String categoryId;
  private String ssCategoryCode;
  private String banner;
  private String betBuilderUrl;
  private String leagueUrl;
  private String redirectionUrl;

  public static LeagueDTO newLeagueDTO(final League source) {
    return builder()
        .name(source.getName())
        .typeId(source.getTypeId())
        .categoryId(source.getCategoryId())
        .ssCategoryCode(source.getSsCategoryCode())
        .banner(source.getBanner())
        .betBuilderUrl(source.getBetBuilderUrl())
        .leagueUrl(source.getLeagueUrl())
        .redirectionUrl(source.getRedirectionUrl())
        .build();
  }
}
