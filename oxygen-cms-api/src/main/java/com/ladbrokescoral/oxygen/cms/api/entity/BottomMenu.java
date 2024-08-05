package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "bottommenus")
@Data
@EqualsAndHashCode(callSuper = true)
public class BottomMenu extends AbstractMenuEntity implements HasBrand {
  private Boolean disabled;
  private Boolean inApp;
  private String lang;
  private String targetUri;
  private String section;
  private Boolean authRequired;
  private Integer systemID;
  private String startUrl;
}
