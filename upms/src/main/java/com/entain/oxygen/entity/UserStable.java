package com.entain.oxygen.entity;

import com.entain.oxygen.entity.projection.view.Views;
import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonView;
import java.util.LinkedHashSet;
import java.util.Set;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "user-stable")
@Data
@EqualsAndHashCode(callSuper = true)
public class UserStable extends AbstractEntity {

  @JsonView(Views.Public.class)
  @Indexed(unique = true)
  private String userName;

  private LinkedHashSet<HorseInfo> myStable;
  private Set<String> unbookmarkedHorses;
}
