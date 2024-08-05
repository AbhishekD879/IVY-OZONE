package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.AbstractMenu;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "headermenus")
@Data
@EqualsAndHashCode(callSuper = true)
public class HeaderMenu extends AbstractMenuEntity implements AbstractMenu, HasBrand {
  private Boolean disabled;
  private String lang = "en";
  private String level = "1";
  private String targetUri;
  private String parent;
  private Boolean inApp = true;
}
