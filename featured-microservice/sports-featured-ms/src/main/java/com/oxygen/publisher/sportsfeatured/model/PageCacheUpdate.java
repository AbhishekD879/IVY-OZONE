package com.oxygen.publisher.sportsfeatured.model;

import com.oxygen.publisher.api.EntityLock;
import com.oxygen.publisher.sportsfeatured.model.module.AbstractFeaturedModule;
import java.util.Collections;
import java.util.Map;
import java.util.Objects;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Builder.Default;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@Builder
@AllArgsConstructor
@EqualsAndHashCode(onlyExplicitlyIncluded = true, callSuper = false)
public class PageCacheUpdate implements EntityLock {

  @EqualsAndHashCode.Include private final PageRawIndex.GenerationKey pageVersion;
  private FeaturedModel pageModel;

  @Default
  private Map<ModuleRawIndex, AbstractFeaturedModule<?>> moduleMap = Collections.emptyMap();

  @Default private Map<String, FeaturedByEventMarket> primaryMarketCache = Collections.emptyMap();

  public PageCacheUpdate(PageRawIndex.GenerationKey pageVersion) {
    this.pageVersion = Objects.requireNonNull(pageVersion, "Page Version can not be null.");
  }

  @Override
  public String getEntityGUID() {
    return String.valueOf(pageVersion.getVersion());
  }

  public void addModule(AbstractFeaturedModule<?> module) {
    moduleMap.put(ModuleRawIndex.fromModule(module), module);
  }

  public boolean isFullFill() {
    return pageVersion != null && pageModel != null;
  }
}
