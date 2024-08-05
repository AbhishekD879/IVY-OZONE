package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.SvgAbstractMenu;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "footerlogos")
@Data
@EqualsAndHashCode(callSuper = true)
public class FooterLogo extends SortableEntity implements SvgAbstractMenu, HasBrand {
  private String title;
  private String target;
  private Boolean disabled;
  private String lang;
  @NotBlank private String brand;
  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated private String svg;

  private String svgId;
  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated private SvgFilename svgFilename;

  private Filename filename;
  private String uriMedium;
  private String uriOriginal;
}
