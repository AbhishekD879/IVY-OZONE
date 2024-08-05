package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.ArrayList;
import java.util.List;
import javax.validation.constraints.NotBlank;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class BrandMenuItemDto {
  @NotBlank private String id;
  @NotBlank private String label;
  private String path;
  private String icon;
  @Builder.Default private Boolean active = true;
  private Integer displayOrder;

  @JsonProperty("sub-menus")
  @Builder.Default
  private List<BrandMenuItemDto> subMenu = new ArrayList<>();
}
