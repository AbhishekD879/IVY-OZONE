package com.oxygen.publisher.model;

import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/** Created by Aliaksei Yarotski on 11/14/17. */
@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = false)
public class InPlayCache {

  private List<SportSegmentCache> sportSegmentCaches;

  @Getter
  @Setter
  @NoArgsConstructor
  @AllArgsConstructor
  public static class SportSegmentCache {
    // either sportSegment or moduleDataItem is null, no case when both are not null
    SportSegment sportSegment;
    List<ModuleDataItem> moduleDataItem;
    RawIndex structuredKey;

    @Override
    public boolean equals(Object o) {
      if (this == o) {
        return true;
      }
      if (o == null || getClass() != o.getClass()) {
        return false;
      }
      SportSegmentCache that = (SportSegmentCache) o;
      return structuredKey.equals(that.structuredKey);
    }

    @Override
    public int hashCode() {
      return structuredKey.hashCode();
    }
  }
}
