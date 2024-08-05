package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.output.AbstractModuleData;
import com.fasterxml.jackson.annotation.JsonFilter;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * Represents the Featured model. Used for data retrieval in {@link }. Copied from Middleware
 * Service.
 *
 * @author tvuyiv
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
@JsonFilter("segmentedFeaturedModel")
public class SegmentedFeaturedModel implements AbstractFeaturedModel {

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
      String directiveName, String showTabOn, String title, boolean visible, String pageId) {
    this.directiveName = directiveName;
    this.showTabOn = showTabOn;
    this.title = title;
    this.visible = visible;
    this.pageId = pageId;
  }

  public void addModules(
      List<? extends AbstractFeaturedModule<? extends AbstractModuleData>> modules) {
    if (!modules.isEmpty()) {
      this.modules.addAll(modules);
    }
  }

  public <T extends AbstractFeaturedModule<?>> List<T> getModules() {
    return (List<T>) Collections.unmodifiableList(modules);
  }
}
