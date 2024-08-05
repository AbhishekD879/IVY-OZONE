package com.entain.oxygen.entity;

import com.entain.oxygen.entity.projection.view.Views;
import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonView;
import java.util.Map;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "userPreference")
@Data
@EqualsAndHashCode(callSuper = true)
@CompoundIndex(def = "{'userName': 1, 'brand': 1}", unique = true)
public class UserPreference extends AbstractEntity {

  @JsonView(Views.Public.class)
  private String userName;

  @JsonView(Views.Public.class)
  private String transformedUserName;

  @JsonView(Views.Public.class)
  private Map<Object, Object> preferences;
}
