package com.oxygen.publisher.sportsfeatured.service;

import com.newrelic.api.agent.Trace;
import com.oxygen.publisher.service.ConsumerDataService;
import com.oxygen.publisher.sportsfeatured.SportsServiceRegistry;
import com.oxygen.publisher.sportsfeatured.model.FeaturedModel;
import com.oxygen.publisher.sportsfeatured.model.PageRawIndex;
import com.oxygen.publisher.sportsfeatured.model.module.AbstractFeaturedModule;
import com.oxygen.publisher.sportsfeatured.relation.FeaturedApi;
import java.util.List;
import java.util.Set;
import java.util.function.Consumer;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;

/** Created by Aliaksei Yarotski on 12/22/17. */
@Slf4j
public class FeaturedServiceImpl extends ConsumerDataService implements FeaturedService {

  @Setter private SportsServiceRegistry serviceRegistry;

  protected FeaturedApi featuredApi() {
    return serviceRegistry.getFeaturedApi();
  }

  @Trace(metricName = "GET-Version-of-the-structure", dispatcher = true)
  @Override
  public void getLastGeneration(Consumer<Set<PageRawIndex.GenerationKey>> onSuccess) {
    log.info("[FeaturedServiceImpl::getLastGeneration]");
    featuredApi().getVersion().enqueue(doCall(v -> onSuccess.accept(v.getValue())));
  }

  @Trace(metricName = "GET-Structure", dispatcher = true)
  @Override
  public void getFeaturedPagesStructure(
      final String generation, final Consumer<FeaturedModel> onSuccess) {
    log.info("[FeaturedServiceImpl::getFeaturedPagesStructure] version->{}", generation);
    featuredApi().getModelStructure(generation).enqueue(doCall(onSuccess));
  }

  @Trace(metricName = "GET-Module", dispatcher = true)
  @Override
  public void getModule(
      final String id, final String generation, final Consumer<AbstractFeaturedModule> onSuccess) {
    log.info("[FeaturedServiceImpl::getModule] id->{} version->{}", id, generation);
    featuredApi().getModule(id, generation).enqueue(doCall(onSuccess));
  }

  @Trace(metricName = "GET-Topics", dispatcher = true)
  @Override
  public void getTopics(
      final String id, final String version, final Consumer<List<String>> onSuccess) {
    log.info("[FeaturedServiceImpl::getTopics] id->{} version->{} ", id, version);
    featuredApi().getTopics(id, version).enqueue(doCall(onSuccess));
  }

  @Trace(metricName = "GET-Sport-Pages", dispatcher = true)
  @Override
  public void getSportPages(final Consumer<List<String>> onSuccess) {
    log.info("[FeaturedServiceImpl::getSportPages]");
    featuredApi().getSportPages().enqueue(doCall(onSuccess));
  }
}
