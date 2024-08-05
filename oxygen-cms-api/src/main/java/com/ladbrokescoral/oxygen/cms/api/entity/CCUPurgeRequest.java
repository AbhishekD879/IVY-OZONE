package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.util.HashSet;
import java.util.Set;
import lombok.Builder;
import lombok.ToString;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@ToString
@Builder
public class CCUPurgeRequest {
  @Builder.Default private Set<String> objects = new HashSet<>();
}
