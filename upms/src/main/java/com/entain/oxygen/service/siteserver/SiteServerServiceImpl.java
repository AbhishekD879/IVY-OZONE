package com.entain.oxygen.service.siteserver;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.model.Event;
import com.entain.oxygen.util.FilterUtil;
import java.util.*;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class SiteServerServiceImpl implements SiteServerService {

  private final SiteServerApiProvider siteServerApiProvider;
  private static final List<String> PRUNE_EVENT_N_MARKET = Arrays.asList("event", "market");

  @Value("${user-stable.horseRacing.classId.uk_ie}")
  private String classIdUKIE;

  @Override
  public List<Event> getHorseEvents() {

    List<String> classIds = new ArrayList<>();
    classIds.add(classIdUKIE);
    return siteServerApiProvider
        .getSiteServerApi()
        .getEventToOutcomeForClass(
            classIds,
            (SimpleFilter) FilterUtil.buildSimpleFilterForUKIEHorses().build(),
            FilterUtil.limitToFilter(),
            FilterUtil.limitRecordsFilter(),
            FilterUtil.existsFilter(),
            PRUNE_EVENT_N_MARKET)
        .orElseThrow(() -> new RuntimeException("No data found from SS"));
  }
}
