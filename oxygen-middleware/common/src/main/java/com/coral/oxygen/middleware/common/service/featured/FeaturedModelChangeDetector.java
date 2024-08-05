package com.coral.oxygen.middleware.common.service.featured;

import com.coral.oxygen.middleware.pojos.model.output.featured.AbstractFeaturedModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.FanzoneSegmentView;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModel;
import com.coral.oxygen.middleware.pojos.model.output.featured.SegmentView;
import java.util.Map;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class FeaturedModelChangeDetector {

  public boolean isChanged(FeaturedModel actual, FeaturedModel previous) {
    if (previous == null) {
      log.info("sport={} change: previous = null", actual.getPageId());
      return true;
    }
    if (actual.getModules().size() != previous.getModules().size()) {
      log.info("sport={} change: modules size change", actual.getPageId());
      return true;
    }
    boolean moduleIdsChanged = !moduleIds(actual).equals(moduleIds(previous));
    boolean orderChanged = isOrderChanged(actual, previous);
    boolean moduleStructureChanged = isStructureChanged(actual, previous);

    boolean isAnythingChanged = moduleIdsChanged || orderChanged || moduleStructureChanged;
    if (isAnythingChanged) {
      log.info(
          "sport={} change: moduleIdsChanged={}, orderChanged={}, moduleStructureChanged={}",
          actual.getPageId(),
          moduleIdsChanged,
          orderChanged,
          moduleStructureChanged);
    }
    log.info("isAnythingChanged {}", isAnythingChanged);
    return isAnythingChanged;
  }

  public boolean isSegmentedModulesChanged(FeaturedModel actual, FeaturedModel previous) {
    if (previous == null) {
      log.info("isSegmentedModulesChanged :: sport={} change: previous = null", actual.getPageId());
      return true;
    }
    Map<String, SegmentView> actualSegmentWiseModules = actual.getSegmentWiseModules();
    Map<String, SegmentView> previousSegmentWiseModules = previous.getSegmentWiseModules();
    if (actualSegmentWiseModules != null
        && !actualSegmentWiseModules.keySet().equals(previousSegmentWiseModules.keySet())) {
      log.info("isSegmentedModulesChanged :: sport={} change: segments change", actual.getPageId());
      return true;
    }
    if (actualSegmentWiseModules != null) {
      return actualSegmentWiseModules.keySet().stream()
          .anyMatch(
              (String seg) ->
                  isSegmentViewChanged(
                      actualSegmentWiseModules.get(seg), previousSegmentWiseModules.get(seg)));
    }
    log.info("isSegmentedModulesChanged :: returning false", actual.getPageId());
    return false;
  }

  /**
   * Fanzone BMA-62182: Checking for FanzoneSegmentedModulesChanged
   *
   * @param actual
   * @param previous
   * @return true/false
   */
  public boolean isFanzoneSegmentedModulesChanged(FeaturedModel actual, FeaturedModel previous) {
    if (previous == null) {
      log.info(
          "isFanzoneSegmentedModulesChanged :: sport={} change: previous = null",
          actual.getPageId());
      return true;
    }
    Map<String, FanzoneSegmentView> actualFanzoneSegmentWiseModules =
        actual.getFanzoneSegmentWiseModules();
    Map<String, FanzoneSegmentView> previousFanzoneSegmentWiseModules =
        previous.getFanzoneSegmentWiseModules();
    if (actualFanzoneSegmentWiseModules != null
        && !actualFanzoneSegmentWiseModules
            .keySet()
            .equals(previousFanzoneSegmentWiseModules.keySet())) {
      log.info(
          "isFanzoneSegmentedModulesChanged :: sport={} change: segments change",
          actual.getPageId());
      return true;
    }
    if (actualFanzoneSegmentWiseModules != null) {
      return actualFanzoneSegmentWiseModules.keySet().stream()
          .anyMatch(
              (String seg) ->
                  isFanzoneSegmentViewChanged(
                      actualFanzoneSegmentWiseModules.get(seg),
                      previousFanzoneSegmentWiseModules.get(seg)));
    }
    log.info("isFanzoneSegmentedModulesChanged :: returning false", actual.getPageId());
    return false;
  }

  /**
   * Fanzone BMA-62182: checking for FanzoneSegmentViewChanged
   *
   * @param actual
   * @param previous
   * @return true/False
   */
  private boolean isFanzoneSegmentViewChanged(
      FanzoneSegmentView actual, FanzoneSegmentView previous) {
    if (!actual
        .getHighlightCarouselModules()
        .keySet()
        .equals(previous.getHighlightCarouselModules().keySet())) {
      log.info("isFanzoneSegmentViewChanged :: HC :: returning true");
      return true;
    }

    if (isOnlyOneSetIsEmpty(
        actual.getSurfaceBetModuleData().keySet().isEmpty(),
        previous.getSurfaceBetModuleData().keySet().isEmpty())) {
      log.info("isFanzoneSegmentViewChanged :: SBD :: returning true");
      return true;
    }
    if (isOnlyOneSetIsEmpty(
        actual.getQuickLinkModuleData().keySet().isEmpty(),
        previous.getQuickLinkModuleData().keySet().isEmpty())) {
      log.info("isFanZoneSegmentViewChanged :: QLD :: returning true");
      return true;
    }
    if (isOnlyOneSetIsEmpty(
        actual.getTeamBetsModuleData().keySet().isEmpty(),
        previous.getTeamBetsModuleData().keySet().isEmpty())) {
      log.info("isFanzoneSegmentViewChanged :: TBD :: returning true");
      return true;
    }
    if (isOnlyOneSetIsEmpty(
        actual.getFanBetsModuleData().keySet().isEmpty(),
        previous.getFanBetsModuleData().keySet().isEmpty())) {
      log.info("isFanzoneSegmentViewChanged :: FBD :: returning true");
      return true;
    }
    return false;
  }

  private boolean isSegmentViewChanged(SegmentView actual, SegmentView previous) {
    if (!actual.getEventModules().keySet().equals(previous.getEventModules().keySet())) {
      log.info("isSegmentViewChanged :: EventModules :: returning true");
      return true;
    }
    if (!actual
        .getHighlightCarouselModules()
        .keySet()
        .equals(previous.getHighlightCarouselModules().keySet())) {
      log.info("isSegmentViewChanged :: HC :: returning true");
      return true;
    }

    if (isOnlyOneSetIsEmpty(
        actual.getQuickLinkData().keySet().isEmpty(),
        previous.getQuickLinkData().keySet().isEmpty())) {
      log.info("isSegmentViewChanged :: QLD :: returning true");
      return true;
    }
    if (isOnlyOneSetIsEmpty(
        actual.getSurfaceBetModuleData().keySet().isEmpty(),
        previous.getSurfaceBetModuleData().keySet().isEmpty())) {
      log.info("isSegmentViewChanged :: SBD :: returning true");
      return true;
    }
    if (isOnlyOneSetIsEmpty(
        actual.getInplayModuleData().keySet().isEmpty(),
        previous.getInplayModuleData().keySet().isEmpty())) {
      log.info("isSegmentViewChanged :: INPLAY :: returning true");
      return true;
    }
    return false;
  }

  private boolean isOnlyOneSetIsEmpty(boolean isActualSetEmpty, boolean isPreviousSetEmpty) {
    if (isActualSetEmpty) {
      return !isPreviousSetEmpty;
    } else {
      return isPreviousSetEmpty;
    }
  }

  private Set<String> moduleIds(FeaturedModel model) {
    return model.getModules().stream()
        .map(AbstractFeaturedModule::getId)
        .collect(Collectors.toSet());
  }

  private boolean isOrderChanged(FeaturedModel actual, FeaturedModel previous) {
    return !actual.getModules().stream()
        .map(AbstractFeaturedModule::getId)
        .collect(Collectors.toList())
        .equals(
            previous.getModules().stream()
                .map(AbstractFeaturedModule::getId)
                .collect(Collectors.toList()));
  }

  private boolean isStructureChanged(FeaturedModel actual, FeaturedModel previous) {
    Map<String, AbstractFeaturedModule> previousModulesMap =
        previous.getModules().stream()
            .collect(Collectors.toMap(AbstractFeaturedModule::getId, Function.identity()));
    return actual.getModules().stream()
        .anyMatch(
            actualModule ->
                actualModule.hasStructureChanges(previousModulesMap.get(actualModule.getId())));
  }
}
