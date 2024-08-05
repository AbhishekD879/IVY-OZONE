package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.ImageAbstractMenu;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "ln quicklinks")
@Data
@EqualsAndHashCode(callSuper = true)
public class DesktopQuickLink extends SortableEntity implements ImageAbstractMenu, HasBrand {
  @NotBlank private String brand;
  private String collectionType;
  private Boolean disabled;
  private Filename filename;
  private Integer heightMedium;
  private Integer heightSmall;
  private String lang;
  private String spriteClass;
  private String target;
  private String title;
  private String uriLarge;
  private String uriMedium;
  private String uriSmall;
  private Integer widthMedium;
  private Integer widthSmall;
  private Integer widthLarge;
  private Integer heightLarge;
  private Boolean isAtoZQuickLink;
}
