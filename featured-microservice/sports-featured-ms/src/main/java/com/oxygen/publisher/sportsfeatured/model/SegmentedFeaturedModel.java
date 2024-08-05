package com.oxygen.publisher.sportsfeatured.model;

import com.oxygen.publisher.sportsfeatured.model.module.AbstractFeaturedModule;
import com.oxygen.publisher.sportsfeatured.relation.FeaturedApi;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import lombok.*;

/**
 * Represents the Featured model. Used for data retrieval in {@link FeaturedApi}. Copied from
 * Middleware Service.
 *
 * @author tvuyiv
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class SegmentedFeaturedModel {

  private String directiveName;

  @Setter(AccessLevel.NONE)
  @Getter(AccessLevel.NONE)
  private final List<AbstractFeaturedModule<?>> modules = new CopyOnWriteArrayList<>();

  private String showTabOn;
  private String title;
  private boolean visible;
  private boolean segmented = true;
  @EqualsAndHashCode.Include private String pageId;
  private boolean useFSCCached;

  public SegmentedFeaturedModel(
      String directiveName,
      String showTabOn,
      String title,
      boolean visible,
      String pageId,
      boolean useFSCCached) {
    this.directiveName = directiveName;
    this.showTabOn = showTabOn;
    this.title = title;
    this.visible = visible;
    this.pageId = pageId;
    this.useFSCCached = useFSCCached;
  }

  public void addModules(List<AbstractFeaturedModule<?>> modules) {
    if (!modules.isEmpty()) {
      this.modules.addAll(modules);
    }
  }

  public <T extends AbstractFeaturedModule<?>> List<T> getModules() {
    return (List<T>) Collections.unmodifiableList(modules);
  }
}
