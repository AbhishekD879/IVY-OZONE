package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document("virtual_next_event")
@Data
@EqualsAndHashCode(callSuper = true)
public class VirtualNextEvent extends AbstractSportEntity {

  private String title;

  private int limit;

  private String typeIds;

  private String classIds;

  private String mobileImageId;

  private String desktopImageId;

  private String buttonText;
  private String redirectionUrl;
}
