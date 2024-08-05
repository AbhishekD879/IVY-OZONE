package com.coral.oxygen.middleware.in_play.service.market.selector;

import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import java.util.List;

/** Created by azayats on 22.05.17. */
public interface MarketSelector {

  List<SportSegment> extract(SportSegment sportSegment);
}
