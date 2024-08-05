package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import org.hibernate.validator.constraints.Range;

@Data
public class VirtualDto {

  @NotBlank(message = "should not be empty")
  private String title;

  @Range(min = 1, max = 12)
  private int limit;

  @NotBlank(message = "should not be blank")
  private String typeIds;

  @NotBlank(message = "should not be blank")
  private String classIds;

  private String mobileImageId;

  private String desktopImageId;
  @Brand protected String brand;

  private String pageId;

  private PageType pageType = PageType.sport;
  private boolean disabled = true;

  private String buttonText;
  private String redirectionUrl;
  private Double sortOrder;
}
