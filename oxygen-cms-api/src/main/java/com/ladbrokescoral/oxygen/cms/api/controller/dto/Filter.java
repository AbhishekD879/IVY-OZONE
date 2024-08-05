package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import lombok.Builder;
import lombok.Builder.Default;
import lombok.Data;

@Data
@Builder
@JsonInclude(Include.NON_EMPTY)
public class Filter<T> {

  private boolean enabled;
  @Default private List<T> values = new ArrayList<>();

  @JsonIgnore
  public List<T> getDataIfEnabled() {
    return enabled && values != null ? values : Collections.emptyList();
  }
}
