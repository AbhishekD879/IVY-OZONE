package com.coral.oxygen.middleware.in_play.service.model;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/** Created by Aliaksei Yarotski on 11/14/17. */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class InPlayCache {

  private List<SportSegmentCache> sportSegmentCaches;

  @Getter
  @Setter
  @AllArgsConstructor
  public static class SportSegmentCache {

    SportSegment sportSegment;
    List<EventsModuleData> moduleDataItem;
    RawIndex structuredKey;

    public SportSegmentCache(SportSegment sportSegment) {
      this.sportSegment = sportSegment;
    }

    public SportSegmentCache(List<EventsModuleData> moduleDataItem) {
      this.moduleDataItem = moduleDataItem;
    }

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
