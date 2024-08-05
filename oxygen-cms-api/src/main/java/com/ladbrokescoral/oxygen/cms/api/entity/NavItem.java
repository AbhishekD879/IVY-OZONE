package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "navItem")
public class NavItem extends SortableEntity implements HasBrand {
  @NotBlank private String brand;
  @NotBlank private String name;
  @NotBlank private String navigationGroupId;
  @NotBlank private String navType;
  private String url;
  private String descriptionTxt;
  private String leaderboardId;
}
