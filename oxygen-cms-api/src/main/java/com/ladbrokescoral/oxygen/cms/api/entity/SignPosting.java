package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "signposting")
@Data
@EqualsAndHashCode(callSuper = true)
public class SignPosting extends SortableEntity implements HasBrand {

  @NotBlank private String brand;
  private String freeBetType;
  private String fromOffer;
  private String betConditions;
  private String sport;
  private String event;
  private String market;
  private Price price;
  private String signPost;
  private Boolean disabled;
  private Boolean isActive;
  private String title;
}
