package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.SortableEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgFilename;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.SvgAbstractMenu;
import javax.validation.constraints.NotEmpty;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.validation.annotation.Validated;

@Data
@Validated
@EqualsAndHashCode(callSuper = true)
@Document(collection = "virtualSport")
public class VirtualSport extends SortableEntity implements SvgAbstractMenu {

  @NotEmpty private String brand;

  @NotEmpty private String title;
  private boolean active;

  private String svg;
  private SvgFilename svgFilename;
  private String svgId;

  private String ctaButtonUrl;
  private String ctaButtonText;

  private String sportsName;
  private String desktopImageId;
  private String mobileImageId;
  private String redirectionURL;
  private String signposting;
  private boolean isTopSports;
  private int topSportsIndex;
}
