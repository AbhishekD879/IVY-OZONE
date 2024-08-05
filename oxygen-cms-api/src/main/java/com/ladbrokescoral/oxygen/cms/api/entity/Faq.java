package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "faq")
@Data
@EqualsAndHashCode(callSuper = true)
public class Faq extends SortableEntity implements HasBrand {
  private String question;
  private String answer;
  private String brand;
}
