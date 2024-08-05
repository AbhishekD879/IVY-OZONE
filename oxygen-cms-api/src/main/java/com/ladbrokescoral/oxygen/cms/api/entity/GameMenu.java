package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.SvgAbstractMenu;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.constraints.NotNull;
import lombok.*;
import org.hibernate.validator.constraints.URL;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "gamemenus")
@Data
@EqualsAndHashCode(callSuper = true)
@CompoundIndex(name = "brand_url", def = "{'brand' : 1, 'url': 1}", unique = true)
public class GameMenu extends SortableEntity implements SvgAbstractMenu {

  @Brand private String brand;
  private String title;
  @URL private String url;
  @NotNull private TargetWindow target = TargetWindow.CURRENT;
  private String externalImageId;
  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated private String svg;
  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated private SvgFilename svgFilename;

  private String svgId;
  private Boolean isNative;
  private Filename pngFilename;
}
