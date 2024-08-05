package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.AbstractMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.SvgAbstractMenu;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "connectmenus")
@Data
@EqualsAndHashCode(callSuper = true)
public class ConnectMenu extends AbstractMenuEntity
    implements AbstractMenu, SvgAbstractMenu, HasBrand {
  private String parent;
  private String level;
  private String lang;
  private String showItemFor;
  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated private String svg;

  private String svgId;
  private Boolean inApp;
  private Boolean disabled;
  private String targetUri;
  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated private SvgFilename svgFilename;

  private String linkSubtitle;
  private Boolean upgradePopup;
}
