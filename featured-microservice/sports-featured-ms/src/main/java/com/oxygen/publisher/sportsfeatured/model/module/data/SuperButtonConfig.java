package com.oxygen.publisher.sportsfeatured.model.module.data;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class SuperButtonConfig extends AbstractModuleData {
  private Integer pageId;
}
