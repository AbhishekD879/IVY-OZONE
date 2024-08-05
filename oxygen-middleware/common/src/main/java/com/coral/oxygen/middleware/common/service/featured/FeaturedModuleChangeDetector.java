package com.coral.oxygen.middleware.common.service.featured;

import com.coral.oxygen.middleware.common.service.ChangeDetector;
import com.coral.oxygen.middleware.pojos.model.output.featured.AbstractFeaturedModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.InplayModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType;
import java.util.Objects;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class FeaturedModuleChangeDetector {

  public boolean isChanged(AbstractFeaturedModule actual, AbstractFeaturedModule previous) {
    if (actual.getModuleType() == ModuleType.INPLAY) {
      return isChanged((InplayModule) actual, (InplayModule) previous);
    } else {
      log.debug(" ChangeDetector > Featured module > actual > {} previous > {} ", actual, previous);
      return ChangeDetector.changeDetected(actual, previous);
    }
  }

  private boolean isChanged(InplayModule actual, InplayModule previous) {
    if (previous == null) {
      return true;
    }
    return !Objects.equals(actual.getTotalEvents(), previous.getTotalEvents());
  }

  public boolean isChangedIncludingMinor(
      AbstractFeaturedModule actual, AbstractFeaturedModule previous) {
    log.debug(
        "Minor ChangeDetector > Featured module > actual > {} previous > {} ", actual, previous);
    return ChangeDetector.changeDetected(actual, previous, true);
  }
}
