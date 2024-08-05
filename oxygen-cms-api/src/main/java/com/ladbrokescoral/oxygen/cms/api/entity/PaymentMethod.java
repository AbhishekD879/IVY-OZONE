package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "payment-methods")
@Data
@EqualsAndHashCode(callSuper = true)
public class PaymentMethod extends SortableEntity implements HasBrand {
  private String brand;
  private boolean active;
  private String name;
  private String identifier;
}
