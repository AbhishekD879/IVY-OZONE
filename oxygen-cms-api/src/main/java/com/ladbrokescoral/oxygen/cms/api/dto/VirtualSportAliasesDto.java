package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.Map;
import lombok.Data;
import lombok.experimental.Accessors;
import org.springframework.util.CollectionUtils;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
@Accessors(chain = true)
public class VirtualSportAliasesDto {
  private String classId;
  private String parent;
  private String child;
  private Map<String, String> events;

  public VirtualSportAliasesDto setEvents(Map<String, String> events) {
    if (!CollectionUtils.isEmpty(events)) {
      this.events = events;
    }
    return this;
  }
}
