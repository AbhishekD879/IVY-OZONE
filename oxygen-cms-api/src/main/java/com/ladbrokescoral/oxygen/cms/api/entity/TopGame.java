package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.IconAbstractMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.ImageAbstractMenu;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "topgames")
@Data
@EqualsAndHashCode(callSuper = true)
public class TopGame extends SortableEntity
    implements IconAbstractMenu, ImageAbstractMenu, HasBrand {
  private Integer widthMediumIcon;
  private Integer heightMediumIcon;
  private Integer widthSmallIcon;
  private Integer heightSmallIcon;
  private Integer widthMedium;
  private Integer heightMedium;
  private Integer widthSmall;
  private Integer heightSmall;
  private String spriteClass;
  private String imageTitle;
  private String lang;
  @NotBlank private String brand;
  private String collectionType;
  private Boolean disabled;
  private String path;
  private String alt;
  private Filename icon;
  private String targetUri;
  private Filename filename;
  private String uriMedium;
  private String uriMediumIcon;
  private String uriSmall;
  private String uriSmallIcon;
  private Integer heightLarge;
  private Integer heightLargeIcon;
  private Integer widthLarge;
  private Integer widthLargeIcon;
  private String uriLargeIcon;
  private String uriLarge;
  private String showItemOn;
}
