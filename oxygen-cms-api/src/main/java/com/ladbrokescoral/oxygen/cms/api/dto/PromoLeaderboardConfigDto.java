package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class PromoLeaderboardConfigDto {
  private String id;
  private String name;
  private String brand;
  private String navGIds;
  private Boolean status;
  private String updatedAt;

  public PromoLeaderboardConfigDto(String id, String name) {
    this.id = id;
    this.name = name;
  }
}
