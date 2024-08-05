package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.AbstractMenu;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "header-submenus")
@Data
@EqualsAndHashCode(callSuper = true)
public class HeaderSubMenu extends AbstractMenuEntity implements AbstractMenu, HasBrand {
  private Boolean disabled;
  private String lang = "en";
  private String targetUri;
  @JsonIgnore private String parent;
  private Boolean inApp = true;
}
