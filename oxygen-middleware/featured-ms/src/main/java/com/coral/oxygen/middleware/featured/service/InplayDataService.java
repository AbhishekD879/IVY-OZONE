package com.coral.oxygen.middleware.featured.service;

import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportEvents;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import java.util.List;

public interface InplayDataService {
  String getInplayDataVersion();

  InPlayData getInplayData(String version);

  SportSegment getSportSegment(String version, Integer sportId);

  List<VirtualSportEvents> getVirtualSportData(String storageKey);
}
