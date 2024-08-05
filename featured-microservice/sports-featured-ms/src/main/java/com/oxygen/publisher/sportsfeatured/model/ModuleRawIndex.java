package com.oxygen.publisher.sportsfeatured.model;

import com.oxygen.publisher.sportsfeatured.model.module.AbstractFeaturedModule;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.EqualsAndHashCode;
import lombok.Getter;

@Getter
@AllArgsConstructor
@Builder
@EqualsAndHashCode
public class ModuleRawIndex {

  public static final String KEY_FORMAT = "%s::%s";

  private PageRawIndex page;
  private String moduleId;

  public static final ModuleRawIndex fromModule(AbstractFeaturedModule<?> module) {
    return new ModuleRawIndex(
        PageRawIndex.from(module.getSportId(), module.getPageType()), module.getId());
  }

  public boolean isSamePage(ModuleRawIndex other) {
    return isSamePage(other.page);
  }

  public boolean isSamePage(PageRawIndex pageRawIndex) {
    return this.page.equals(pageRawIndex);
  }
}
