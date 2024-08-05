package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.time.Instant;
import java.util.List;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class NavigationGroupDto {
  private String id;
  private String title;
  private Boolean status;
  private Instant createdAt;
  private Instant updatedAt;
  private String createdByUserName;
  private String updatedByUserName;
  private List<NavItemDto> navItems;
  private List<String> promotionIds;
}
