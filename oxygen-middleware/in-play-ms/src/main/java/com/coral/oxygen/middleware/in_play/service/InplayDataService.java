package com.coral.oxygen.middleware.in_play.service;

import com.coral.oxygen.middleware.in_play.service.model.InPlayCache;
import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportEvents;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportsRibbon;
import java.util.List;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Service;

@Service
@ConditionalOnProperty(name = "inplay.scheduled.task.enabled")
public interface InplayDataService {

  InPlayData getInPlayModel(String version);

  SportsRibbon getSportsRibbon(String version);

  InPlayCache getInPlayCache(String version);

  String getGeneration();

  SportSegment getSportSegment(String storageKey);

  List<VirtualSportEvents> getVirtualSportData(String storageKey);
}
