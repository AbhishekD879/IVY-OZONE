package com.oxygen.publisher.sportsfeatured.model;

import com.oxygen.publisher.model.OutputMarket;
import com.oxygen.publisher.sportsfeatured.model.module.data.EventsModuleData;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import lombok.Builder;
import lombok.Data;

/** Created by Aliaksei Yarotski on 4/23/18. */
@Data
@Builder
public class FeaturedByEventMarket {

  private EventsModuleData moduleData;

  @Builder.Default private Set<String> moduleIds = Collections.synchronizedSet(new HashSet<>());
  private List<OutputMarket> primaryMarkets;
}
