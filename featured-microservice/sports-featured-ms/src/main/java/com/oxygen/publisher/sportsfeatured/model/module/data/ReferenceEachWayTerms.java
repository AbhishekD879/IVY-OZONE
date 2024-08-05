package com.oxygen.publisher.sportsfeatured.model.module.data;

import lombok.Data;

// OZONE-677 added a newlist to get places field for extrasignplace feature
@Data
public class ReferenceEachWayTerms {
  private String id;
  private Integer places;
}
