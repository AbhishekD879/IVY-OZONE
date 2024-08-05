package com.coral.oxygen.middleware.featured.consumer;

import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.AbstractFeaturedModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class ModulePrioritizer {

  /** highlight carousel has top priority in event displaying */
  private static final List<ModuleType> MODULE_PRIORITY =
      Arrays.asList(ModuleType.HIGHLIGHTS_CAROUSEL, ModuleType.INPLAY, ModuleType.FEATURED);

  public static final Comparator<SportPageModule> SPORT_PAGE_MODULE_COMPARATOR =
      (o1, o2) -> {
        ModuleType type1 = o1.getSportModule().getModuleType();
        ModuleType type2 = o2.getSportModule().getModuleType();
        if (MODULE_PRIORITY.indexOf(type1) < 0) {
          return 1;
        }
        if (MODULE_PRIORITY.indexOf(type1) < MODULE_PRIORITY.indexOf(type2)
            || MODULE_PRIORITY.indexOf(type2) < 0) {
          return -1;
        } else {
          return 1;
        }
      };

  public static final Comparator<AbstractFeaturedModule<?>> FEATURE_MODULE_COMPARATOR =
      (AbstractFeaturedModule<?> o1, AbstractFeaturedModule<?> o2) -> {
        ModuleType type1 = o1.getModuleType();
        ModuleType type2 = o2.getModuleType();
        if (MODULE_PRIORITY.indexOf(type1) < 0) {
          return 1;
        }
        if (MODULE_PRIORITY.indexOf(type1) < MODULE_PRIORITY.indexOf(type2)
            || MODULE_PRIORITY.indexOf(type2) < 0) {
          return -1;
        } else {
          return 1;
        }
      };
}
