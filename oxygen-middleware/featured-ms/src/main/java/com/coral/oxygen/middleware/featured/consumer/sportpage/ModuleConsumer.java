package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.AbstractFeaturedModule;
import java.util.List;
import java.util.Set;

public interface ModuleConsumer<T extends AbstractFeaturedModule> {

  default T processModule(
      SportPageModule moduleConfig, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEventIds)
      throws SportsModuleProcessException {
    throw new UnsupportedOperationException("Not implemented");
  }

  default List<T> processModules(
      SportPageModule moduleConfig, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEventIds) {
    throw new UnsupportedOperationException("Not implemented");
  }
}
