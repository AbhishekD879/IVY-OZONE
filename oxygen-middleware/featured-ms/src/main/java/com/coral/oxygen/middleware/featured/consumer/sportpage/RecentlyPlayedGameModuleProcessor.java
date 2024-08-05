package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.RecentlyPlayedGame;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.RecentlyPlayedGameModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.RpgConfig;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class RecentlyPlayedGameModuleProcessor implements ModuleConsumer<RecentlyPlayedGameModule> {

  @Override
  public RecentlyPlayedGameModule processModule(
      SportPageModule cmsModule, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEventIds)
      throws SportsModuleProcessException {
    RecentlyPlayedGameModule rpgModule = new RecentlyPlayedGameModule(cmsModule.getSportModule());
    List<RpgConfig> data =
        cmsModule.getPageData().stream()
            .map(cmsData -> (RecentlyPlayedGame) cmsData)
            .map(RpgConfig::new)
            .collect(Collectors.toList());
    rpgModule.setData(data);
    return rpgModule;
  }

  @Override
  public List<RecentlyPlayedGameModule> processModules(
      SportPageModule moduleConfig, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEventIds) {
    try {
      return Arrays.asList(processModule(moduleConfig, cmsSystemConfig, excludedEventIds));
    } catch (Exception e) {
      log.error("Recently played game module processor exception {} ", moduleConfig, e);
      return Collections.emptyList();
    }
  }
}
