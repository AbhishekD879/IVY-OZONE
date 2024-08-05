package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "topmenus")
@Data
@EqualsAndHashCode(callSuper = true)
public class TopMenu extends SortableEntity implements HasBrand {
  private String key;
  private String targetUri;
  private String linkTitle;
  private Boolean disabled;
  private String brand;
  private String lang;
}
