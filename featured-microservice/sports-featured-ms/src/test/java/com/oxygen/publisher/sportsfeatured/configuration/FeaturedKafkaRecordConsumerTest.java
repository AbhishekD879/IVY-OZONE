package com.oxygen.publisher.sportsfeatured.configuration;

import static java.util.concurrent.TimeUnit.SECONDS;
import static org.awaitility.Awaitility.await;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.collect.ImmutableSet;
import com.oxygen.publisher.model.PageType;
import com.oxygen.publisher.service.KafkaTopic.Topic;
import com.oxygen.publisher.sportsfeatured.SportsServiceRegistry;
import com.oxygen.publisher.sportsfeatured.context.SportsMiddlewareContext;
import com.oxygen.publisher.sportsfeatured.model.FeaturedModel;
import com.oxygen.publisher.sportsfeatured.model.ModuleRawIndex;
import com.oxygen.publisher.sportsfeatured.model.PageRawIndex;
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData;
import com.oxygen.publisher.sportsfeatured.model.SportsVersionResponse;
import com.oxygen.publisher.sportsfeatured.model.module.AbstractFeaturedModule;
import com.oxygen.publisher.sportsfeatured.relation.FeaturedApi;
import com.oxygen.publisher.test.util.TestCall;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;
import org.apache.commons.collections4.CollectionUtils;
import org.assertj.core.api.BDDAssertions;
import org.assertj.core.api.SoftAssertions;
import org.awaitility.core.ThrowingRunnable;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.test.context.EmbeddedKafka;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.junit4.SpringRunner;

/**
 * On BitBucket/locally these tests works fine. On Jenkins it looks that from time to time there are
 * some time-outing issues. Disabled them for now, but still keep them here as they are useful even
 * for local testing as they tests cover most of the integration flow between publisher<->consumer
 */
@RunWith(SpringRunner.class)
@SpringBootTest
@DirtiesContext
@EmbeddedKafka(partitions = 1, bootstrapServersProperty = "spring.kafka.bootstrap-servers")
public class FeaturedKafkaRecordConsumerTest extends BDDAssertions {

  private static final String TEST_URL = "test.com";
  private static final long GENERATION_VERSION = 100L;
  private static final String CUSTOMIZED_PAGE_ID = "c0";

  private static final String CUSTOMIZED_GENERATION =
      String.format(
          "%s::%s::%d", PageType.customized.getTypeName(), CUSTOMIZED_PAGE_ID, GENERATION_VERSION);

  private static final String FEATURED_MODEL_PATH = "FeaturedModel.json";
  private static final String DEFAULT_FEATURED_MODEL_PATH = "DefaultFeaturedModel.json";

  @Mock private FeaturedApi featuredApi;

  @MockBean private FeaturedApiProvider featuredApiProvider;

  @Autowired private SportsMiddlewareContext sportsMiddlewareContext;

  @Autowired private KafkaTemplate<String, String> kafkaTemplate;

  @Autowired private SportsServiceRegistry sportsServiceRegistry;

  @Autowired private ObjectMapper objectMapper;

  @Before
  public void setUp() throws IOException {
    when(featuredApiProvider.isHealthy()).thenReturn(true);
    when(featuredApiProvider.featuredApi()).thenReturn(featuredApi);
    when(featuredApi.getVersion()).thenReturn(new TestCall<>(TEST_URL, sportsVersionResponse()));
    when(featuredApi.getModelStructure(any()))
        .thenReturn(new TestCall<>(TEST_URL, getFeaturedModel(DEFAULT_FEATURED_MODEL_PATH)));

    sportsServiceRegistry.load();
  }

  @Ignore
  @Test
  public void shouldProcessSportFeaturedStructureChangeMessage() throws IOException {
    // GIVEN
    String sportGenerationId = String.format("sport::16::%d", GENERATION_VERSION);
    FeaturedModel featuredModel = getFeaturedModel(FEATURED_MODEL_PATH);
    PageRawIndex featuredModuleIndex = PageRawIndex.fromModel(featuredModel);
    List<? extends AbstractFeaturedModule<?>> modules = featuredModel.getModules();

    when(featuredApi.getModelStructure(sportGenerationId))
        .thenReturn(new TestCall<>(TEST_URL, featuredModel));
    mockGetModuleCalls(featuredModel);

    // WHEN
    kafkaTemplate.send(Topic.FEATURED_STRUCTURE_CHANGED.getKey(), sportGenerationId);

    // THEN
    SportsCachedData sportsCachedData = sportsMiddlewareContext.getFeaturedCachedData();

    awaitUntilAsserted(
        () -> assertThat(sportsCachedData.getGenerationMap()).isEqualTo(sportGenerationId));
    awaitUntilAsserted(() -> validateModulesCache(modules, sportsCachedData));
    awaitUntilAsserted(
        () ->
            assertThat(sportsCachedData.getStructure(featuredModuleIndex))
                .isEqualTo(featuredModel));
  }

  @Ignore
  @Test
  public void shouldProcessCustomFeaturedStructureChangeMessage() throws IOException {
    // GIVEN
    FeaturedModel featuredModel = getFeaturedModel(FEATURED_MODEL_PATH);
    List<? extends AbstractFeaturedModule<?>> modules = featuredModel.getModules();

    when(featuredApi.getModelStructure(CUSTOMIZED_GENERATION))
        .thenReturn(new TestCall<>(TEST_URL, featuredModel));
    mockGetModuleCalls(featuredModel);

    // WHEN
    kafkaTemplate.send(Topic.FEATURED_STRUCTURE_CHANGED.getKey(), CUSTOMIZED_GENERATION);

    // THEN
    SportsCachedData sportsCachedData = sportsMiddlewareContext.getFeaturedCachedData();

    awaitUntilAsserted(
        () -> assertThat(sportsCachedData.getGenerationMap()).isEqualTo(CUSTOMIZED_GENERATION));
    awaitUntilAsserted(() -> validateModulesCache(modules, sportsCachedData));
    awaitUntilAsserted(() -> validatePrimaryMarketCache(sportsCachedData));
    awaitUntilAsserted(
        () ->
            assertThat(sportsCachedData.getStructure(PageRawIndex.fromModel(featuredModel)))
                .isEqualTo(featuredModel));
  }

  @Ignore
  @Test
  public void shouldProcessModuleContentChangeMessage() throws IOException {
    FeaturedModel featuredModel = getFeaturedModel(FEATURED_MODEL_PATH);
    AbstractFeaturedModule<?> moduleToUpdate = featuredModel.getModules().get(1);
    insertInitialDataToStructureCache(featuredModel, moduleToUpdate);
    ModuleRawIndex moduleRawIndex = ModuleRawIndex.fromModule(moduleToUpdate);
    String newModuleTitle = "New Title";
    AbstractFeaturedModule<?> moduleWithChangedContent =
        getChangedModule(moduleToUpdate, newModuleTitle);

    when(featuredApi.getModule(PageType.customized.getTypeName(), CUSTOMIZED_PAGE_ID))
        .thenReturn(new TestCall<>(TEST_URL, moduleWithChangedContent));

    // WHEN
    kafkaTemplate.send(Topic.FEATURED_MODULE_CONTENT_CHANGED.getKey(), CUSTOMIZED_GENERATION);

    // THEN
    SportsCachedData sportsCachedData = sportsMiddlewareContext.getFeaturedCachedData();

    awaitUntilAsserted(
        () ->
            assertThat(sportsCachedData.getModuleIfPresent(moduleRawIndex))
                .isEqualTo(moduleWithChangedContent));
    awaitUntilAsserted(
        () ->
            assertThat(sportsCachedData.getModuleIfPresent(moduleRawIndex).getTitle())
                .isEqualTo(newModuleTitle));
  }

  @Ignore
  @Test
  public void shouldProcessModuleContentChangeMinorMessage() throws IOException {
    FeaturedModel featuredModel = getFeaturedModel(FEATURED_MODEL_PATH);
    AbstractFeaturedModule<?> moduleToUpdate = featuredModel.getModules().get(1);
    insertInitialDataToStructureCache(featuredModel, moduleToUpdate);
    ModuleRawIndex moduleRawIndex = ModuleRawIndex.fromModule(moduleToUpdate);
    String newModuleTitle = "New Title";
    AbstractFeaturedModule<?> moduleWithChangedContent =
        getChangedModule(moduleToUpdate, newModuleTitle);

    when(featuredApi.getModule(PageType.customized.getTypeName(), CUSTOMIZED_PAGE_ID))
        .thenReturn(new TestCall<>(TEST_URL, moduleWithChangedContent));

    // WHEN
    kafkaTemplate.send(Topic.FEATURED_MODULE_CONTENT_CHANGED_MINOR.getKey(), CUSTOMIZED_GENERATION);

    // THEN
    SportsCachedData sportsCachedData = sportsMiddlewareContext.getFeaturedCachedData();

    awaitUntilAsserted(
        () ->
            assertThat(sportsCachedData.getModuleIfPresent(moduleRawIndex))
                .isEqualTo(moduleWithChangedContent));
    awaitUntilAsserted(
        () ->
            assertThat(sportsCachedData.getModuleIfPresent(moduleRawIndex).getTitle())
                .isEqualTo(newModuleTitle));
  }

  private AbstractFeaturedModule<?> getChangedModule(
      AbstractFeaturedModule<?> moduleToUpdate, String moduleTitle) {
    AbstractFeaturedModule<?> moduleWithChangedContent = moduleToUpdate.copyWithEmptyData();
    moduleWithChangedContent.setTitle(moduleTitle);
    return moduleWithChangedContent;
  }

  private void insertInitialDataToStructureCache(
      FeaturedModel featuredModel, AbstractFeaturedModule<?> moduleToUpdate) {
    PageRawIndex index =
        PageRawIndex.from(moduleToUpdate.getSportId(), moduleToUpdate.getPageType());
    sportsMiddlewareContext.getFeaturedCachedData().getStructureMap().put(index, featuredModel);
  }

  private void awaitUntilAsserted(ThrowingRunnable assertion) {
    await().atMost(30, SECONDS).untilAsserted(assertion);
  }

  private void validateModulesCache(
      List<? extends AbstractFeaturedModule<?>> modules, SportsCachedData sportsCachedData) {
    SoftAssertions softly = new SoftAssertions();
    modules.forEach(
        module ->
            softly
                .assertThat(sportsCachedData.getModuleIfPresent(ModuleRawIndex.fromModule(module)))
                .as("Validating: " + module.getId())
                .isEqualTo(module));
    softly.assertAll();
  }

  private void mockGetModuleCalls(FeaturedModel featuredModel) {
    featuredModel
        .getModules()
        .forEach(
            module -> {
              if (CollectionUtils.isEmpty(module.getData())) {
                when(featuredApi.getModule(module.getId(), String.valueOf(GENERATION_VERSION)))
                    .thenReturn(new TestCall<>(TEST_URL, module));
              }
            });
  }

  private SportsVersionResponse sportsVersionResponse() {
    return new SportsVersionResponse(
        ImmutableSet.of(
            new PageRawIndex.GenerationKey(
                PageType.customized, CUSTOMIZED_PAGE_ID, GENERATION_VERSION)));
  }

  private void validatePrimaryMarketCache(SportsCachedData sportsCachedData) {
    assertThat(sportsCachedData.getPrimaryMarketCache().keySet())
        .containsExactlyInAnyOrder(
            "9754492", "9751701", "9753505", "9751788", "9753502", "9753508", "9755772", "9216976",
            "9754189", "9216788", "9753504", "9753506", "9216803", "9560462", "9753519", "9753136",
            "9753520", "9753529", "9753840", "9753476", "9753501", "7077801", "9753527", "9560459",
            "9216800", "9753533", "9753522", "9752309", "9216889", "9751703", "9753526");
  }

  public FeaturedModel getFeaturedModel(String filename) throws IOException {
    InputStream inputStream = getClass().getClassLoader().getResourceAsStream(filename);
    return objectMapper.readValue(inputStream, FeaturedModel.class);
  }
}
