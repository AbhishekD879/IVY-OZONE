package com.ladbrokescoral.oxygen.timeline.api.repository;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;

public class CustomPageImpl<T> extends PageImpl<T> {

  public CustomPageImpl(List content) {
    super(content);
  }

  public CustomPageImpl(List<T> postMessages, PageRequest of, long count) {
    super(postMessages, of, count);
  }

  @JsonProperty("page")
  @Override
  public List getContent() {
    return super.getContent();
  }

  @JsonProperty("count")
  @Override
  public long getTotalElements() {
    return super.getTotalElements();
  }
}
