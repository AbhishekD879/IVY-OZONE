package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import javax.validation.constraints.NotNull;
import lombok.AccessLevel;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Data
@Document(collection = "betpack-filter")
@EqualsAndHashCode(callSuper = false)
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = false)
public class BetPackFilter extends SortableEntity implements HasBrand {
  @Indexed(unique = true)
  @NotNull
  private String filterName;

  @NotNull private String brand;
  @NotNull private boolean filterActive;

  @Getter(AccessLevel.NONE)
  @NotNull
  private boolean isLinkedFilter;

  @JsonProperty("isLinkedFilter")
  public boolean isLinkedFilter() {
    return isLinkedFilter;
  }

  private String linkedFilterWarningText;
}
