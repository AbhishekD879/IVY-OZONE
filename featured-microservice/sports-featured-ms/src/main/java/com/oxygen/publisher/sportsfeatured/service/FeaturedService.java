package com.oxygen.publisher.sportsfeatured.service;

import com.oxygen.health.api.ReloadableService;
import com.oxygen.publisher.sportsfeatured.model.FeaturedModel;
import com.oxygen.publisher.sportsfeatured.model.PageRawIndex;
import com.oxygen.publisher.sportsfeatured.model.module.AbstractFeaturedModule;
import java.util.List;
import java.util.Set;
import java.util.function.Consumer;

/** Created by Aliaksei Yarotski on 12/22/17. */
public interface FeaturedService extends ReloadableService {

  void getLastGeneration(Consumer<Set<PageRawIndex.GenerationKey>> onSuccess);

  void getFeaturedPagesStructure(String generation, Consumer<FeaturedModel> onSuccess);

  void getModule(String id, String generation, Consumer<AbstractFeaturedModule> onSuccess);

  void getTopics(String id, String version, Consumer<List<String>> onSuccess);

  void getSportPages(Consumer<List<String>> onSuccess);
}
