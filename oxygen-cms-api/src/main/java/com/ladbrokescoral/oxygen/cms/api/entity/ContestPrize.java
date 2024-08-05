package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "contestprizes")
public class ContestPrize extends AbstractEntity implements HasBrand, Comparable<ContestPrize> {

  private String contestId;
  private String type;
  private String value;
  private String text;
  private Filename icon;
  private Filename signPosting;
  private String percentageOfField;
  private String numberOfEntries;
  private String brand;
  private String freebetOfferId;

  @Override
  public int compareTo(ContestPrize o) {
    return this.getType().compareToIgnoreCase(o.getType());
  }
}
