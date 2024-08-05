package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.AbstractMenu;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "leftmenus")
@Data
@EqualsAndHashCode(callSuper = true)
public class LeftMenu extends SortableEntity implements AbstractMenu {
  @Field(value = "linkTitle_brand")
  private String linkTitleBrand;

  private String parent;
  private String level;
  private String uriMedium;
  private String uriSmall;
  private String linkTitle;
  private String lang;
  private String brand;
  private String svg;
  private String svgId;
  private String iconAligment;
  private String menuItemView;
  private String showItemFor;
  private Boolean inApp;
  private Boolean disabled;
  private String targetUri;
}
