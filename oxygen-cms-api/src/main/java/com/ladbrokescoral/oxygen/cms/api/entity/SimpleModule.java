package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "simplemodule")
@Data
@NoArgsConstructor
@SuperBuilder
@EqualsAndHashCode(callSuper = true)
public class SimpleModule extends AbstractEntity implements Comparable<SimpleModule> {

  @NotBlank private String originalName;
  @NotBlank private String displayName;
  private String description;
  private Integer displayOrder;
  private boolean disabled;

  /**
   * Compares {@link SimpleModule} instances by {@code displayOrder}. Items with null ${code
   * displayOrder} will always be last in a list sorted with this comparator
   */
  @Override
  public int compareTo(SimpleModule that) {
    Integer thisDisplayOrder = this.getDisplayOrder();
    Integer thatDisplayOrder = that.getDisplayOrder();
    if (thisDisplayOrder == null && thatDisplayOrder == null) {
      return 0;
    } else if (thisDisplayOrder == null) {
      return 1;
    } else if (thatDisplayOrder == null) {
      return -1;
    } else {
      return thisDisplayOrder.compareTo(thatDisplayOrder);
    }
  }
}
