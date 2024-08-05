package com.oxygen.publisher.sportsfeatured.model.module.data;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class BybWidgetModuleData extends EventsModuleData {
  private String id;
  private String title;
}
