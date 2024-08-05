package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "homepage")
@Data
@EqualsAndHashCode(callSuper = true)
public class Homepage extends SortableEntity {

  private String identifier;
  private String label;
  private Boolean enabled;
  private String href;
  private HomeInplayConfig homeInplayConfig;
}
