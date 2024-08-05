package com.oxygen.publisher.sportsfeatured.model.module.data;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class RacingModuleConfig extends AbstractModuleData {
  private String name;
  private boolean active;
}
