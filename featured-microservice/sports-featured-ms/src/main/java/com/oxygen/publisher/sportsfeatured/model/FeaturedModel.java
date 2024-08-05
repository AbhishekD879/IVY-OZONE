package com.oxygen.publisher.sportsfeatured.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.oxygen.publisher.sportsfeatured.model.module.*;
import com.oxygen.publisher.sportsfeatured.model.module.AbstractFeaturedModule;
import com.oxygen.publisher.sportsfeatured.model.module.InplayModule;
import com.oxygen.publisher.sportsfeatured.model.module.QuickLinkModule;
import com.oxygen.publisher.sportsfeatured.model.module.SegmentView;
import com.oxygen.publisher.sportsfeatured.model.module.SurfaceBetModule;
import com.oxygen.publisher.sportsfeatured.model.module.data.EventsModuleData;
import com.oxygen.publisher.sportsfeatured.relation.FeaturedApi;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.function.Function;
import java.util.stream.Collectors;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

/**
 * Represents the Featured model. Used for data retrieval in {@link FeaturedApi}. Copied from
 * Middleware Service.
 *
 * @author tvuyiv
 */
@Data
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
@JsonIgnoreProperties(ignoreUnknown = true)
public class FeaturedModel {

  private String directiveName;

  @JsonDeserialize(as = HashMap.class)
  private Map<Long, EventsModuleData> eventsModuleData = new HashMap<>();

  @Setter(AccessLevel.NONE)
  @Getter(AccessLevel.NONE)
  @JsonDeserialize(as = CopyOnWriteArrayList.class)
  private final List<AbstractFeaturedModule<?>> modules = new CopyOnWriteArrayList<>();

  @JsonDeserialize(as = HashMap.class)
  private Map<String, SegmentView> segmentWiseModules = new HashMap<>();

  @JsonDeserialize(as = HashMap.class)
  private Map<String, FanzoneSegmentView> fanzoneSegmentWiseModules = new HashMap<>();

  private SurfaceBetModule surfaceBetModule;
  private QuickLinkModule quickLinkModule;
  private InplayModule inplayModule;
  private TeamBetsModule teamBetsModule;
  private FanBetsModule fanBetsModule;

  private String showTabOn;
  private String title;
  private boolean visible;
  private boolean segmented;
  @EqualsAndHashCode.Include private String pageId;
  private boolean useFSCCached;

  public FeaturedModel(String pageId) {
    this.pageId = pageId;
  }

  public <T extends AbstractFeaturedModule<?>> void replaceModules(
      Identifier moduleTypeId, List<? extends AbstractFeaturedModule<?>> modulesToSet) {
    Map<String, AbstractFeaturedModule<?>> newModulesById =
        modulesToSet.stream()
            .collect(Collectors.toMap(AbstractFeaturedModule::getId, Function.identity()));
    this.modules.replaceAll(
        m -> moduleTypeId.test(m) ? newModulesById.getOrDefault(m.getId(), m) : m);
  }

  /**
   * @return immutable projection of {@link #modules} of the specified {@code moduleTypeId}
   */
  public <T extends AbstractFeaturedModule<?>> List<T> getModules(Identifier moduleTypeId) {
    return modules.stream()
        .filter(moduleTypeId)
        .map(module -> (T) module)
        .collect(Collectors.collectingAndThen(Collectors.toList(), Collections::unmodifiableList));
  }

  public List<? extends AbstractFeaturedModule<?>> getModules() {
    return Collections.unmodifiableList(modules);
  }

  public void addModule(AbstractFeaturedModule module) {
    modules.add(module);
  }
}
