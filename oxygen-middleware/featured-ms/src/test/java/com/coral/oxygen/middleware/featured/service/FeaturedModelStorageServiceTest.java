package com.coral.oxygen.middleware.featured.service;

import static com.coral.oxygen.middleware.common.configuration.DistributedKey.ATOMIC_FEATURED_DATA;
import static com.coral.oxygen.middleware.common.configuration.DistributedKey.FEATURED_PAGE_MODEL_MAP;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.common.configuration.DistributedKey;
import com.coral.oxygen.middleware.common.imdg.DistributedAtomicLong;
import com.coral.oxygen.middleware.common.imdg.adapters.redisson.RedisDistributedInstance;
import com.coral.oxygen.middleware.common.service.GenerationStorageService;
import com.coral.oxygen.middleware.featured.consumer.FeaturedConsumerUtil;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.AbstractFeaturedModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModel;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex;
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.util.CollectionUtils;

@RunWith(MockitoJUnitRunner.class)
public class FeaturedModelStorageServiceTest {

  private FeaturedModelStorageService service;
  private FeaturedModel model;
  @Mock private GenerationStorageService storageService;
  @Mock private DistributedAtomicLong generation;
  @Mock private RedisDistributedInstance instance;
  private ObjectMapper objectMapper = new ObjectMapper();
  FaeturemodelUtil util = new FaeturemodelUtil();

  @Before
  public void init() {
    service = new FeaturedModelStorageService(instance, storageService, new ObjectMapper());
  }

  @Test
  public void saveGenerationIndexTest() {
    Set<FeaturedRawIndex.VersionedPageKey> thisIndex = new HashSet<>();
    thisIndex.add(new FeaturedRawIndex.VersionedPageKey(FeaturedRawIndex.PageType.sport, "16", 1l));
    service.saveGenerationIndex(thisIndex);
    verify(storageService, times(1)).putLatest(any(), any());
  }

  @Test
  public void getPreviousVersionTest() {
    Long previousver = service.getPreviousVersion(11l);
    Assert.assertEquals(10l, previousver.longValue());
  }

  @Test
  public void getNextVersionTest() {
    DistributedAtomicLong datalong =
        new DistributedAtomicLong() {
          @Override
          public long addAndGet(long number) {
            return 20;
          }

          @Override
          public long get() {
            return 10;
          }
        };
    when(instance.getAtomicLong(ATOMIC_FEATURED_DATA)).thenReturn(datalong);
    Long nextver = service.getNextVersion();
    Assert.assertEquals(20l, nextver.longValue());
  }

  @Test
  public void saveToStorage() throws JsonProcessingException {
    model = util.creatFeatureModel(false);
    FeaturedModel resultmodel = service.save(model, 1L);
    Assert.assertNotNull(resultmodel);
  }

  @Test
  public void saveTonewObjectModules() throws JsonProcessingException {
    model = util.creatFeatureModel(false);
    ObjectMapper om = Mockito.spy(new ObjectMapper());
    Mockito.when(om.writeValueAsString(any(AbstractFeaturedModule.class)))
        .thenThrow(new JsonProcessingException("") {});
    Mockito.when(om.writeValueAsString(any(FeaturedModel.class)))
        .thenThrow(new JsonProcessingException("") {});
    service = new FeaturedModelStorageService(instance, storageService, om);
    FeaturedModel resultmodel = service.save(model, 1L);
    Assert.assertNotNull(resultmodel);
  }

  @Test
  public void saveToStorageShownExpandFalse() throws JsonProcessingException {
    model = util.creatFeatureModel(false);
    model.getModules().get(0).setShowExpanded(false);
    model.getModules().get(2).setShowExpanded(false);
    FeaturedModel resultmodel = service.save(model, 1L);
    Assert.assertNotNull(resultmodel);
  }

  @Test
  public void saveToStoragepageIdZero() throws JsonProcessingException {
    model = util.creatFeatureModel(false);
    model.getModules().get(0).setShowExpanded(false);
    model.getModules().get(2).setShowExpanded(false);
    model.setPageId("3");
    FeaturedModel resultmodel = service.save(model, 1L);
    Assert.assertNotNull(resultmodel);
  }

  @Test
  public void getAndSaveFeaturedSportsTest() {
    List<String> strings = Arrays.asList(new String[] {"football", "baseball"});
    when(instance.updateExpirableValue(any(), any())).thenReturn("s1");
    List<String> resultstrings = service.getAndSaveFeaturedSports(strings);
    Assert.assertNotNull(resultstrings);
  }

  @Test
  public void LatestFeatureModelIsNotPresentIfFeatureModuleMapIsEmpty() {
    when(instance.getValue(FEATURED_PAGE_MODEL_MAP, String.valueOf(1L))).thenReturn("test");
    when(instance.getAtomicLong(DistributedKey.ATOMIC_FEATURED_DATA)).thenReturn(generation);

    when(generation.get()).thenReturn(1L);
    Optional<String> optional = service.getLatestFeatureModelJson();
    Assert.assertTrue(optional.isPresent() && "test".equals(optional.get()));
  }

  @Test
  public void getFeaturedModelByIdTest() throws JsonProcessingException {

    String[] arrayString = new String[] {"1232", "3434534", "424242"};
    List<String> listString = Arrays.asList(arrayString);
    model = util.creatFeatureModel(false);
    String s = objectMapper.writeValueAsString(model.getModules());
    List<String> strings =
        model.getModules().stream()
            .map(
                x -> {
                  try {
                    return objectMapper.writeValueAsString(x);
                  } catch (JsonProcessingException e) {
                    return null;
                  }
                })
            .collect(Collectors.toList());
    when(instance.getValues(any(), any())).thenReturn(strings);
    List<AbstractFeaturedModule> lists = service.getModulesById(1L, listString);
    Assert.assertEquals(11, lists.size());
  }

  @Test
  public void getFeaturedModelByIdTestException() throws JsonProcessingException {
    String[] arrayString = new String[] {"1232", "3434534", "424242"};
    List<String> listString = Arrays.asList(arrayString);
    model = util.creatFeatureModel(false);
    String s = objectMapper.writeValueAsString(model);
    List<String> strings = new ArrayList<>();
    strings.add(s);
    when(instance.getValues(any(), any())).thenReturn(strings);
    List<AbstractFeaturedModule> lists = service.getModulesById(1L, listString);
    Assert.assertFalse(CollectionUtils.isEmpty(lists));
  }

  @Test
  public void ModuleJsonNotEmptyByLastModulesByIds() throws JsonProcessingException {
    String[] arrayString = new String[] {"1232", "3434534", "424242"};
    List<String> listString = Arrays.asList(arrayString);
    model = util.creatFeatureModel(false);
    when(instance.getValue(any(), any())).thenReturn(objectMapper.writeValueAsString(model));
    model = service.getFeaturedModel("0", 1L);
    String s = objectMapper.writeValueAsString(model);
    List<String> strings = new ArrayList<>();
    strings.add(s);
    when(instance.getValues(any(), any())).thenReturn(strings);
    when(instance.getAtomicLong(DistributedKey.ATOMIC_FEATURED_DATA)).thenReturn(generation);
    when(generation.get()).thenReturn(1L);
    String optional = service.getLastModulesById(Arrays.asList("3434534"));
    Assert.assertFalse(optional.isEmpty());
  }

  @Test
  public void testgetFeaturedModel() throws JsonProcessingException {
    FeaturedModel featureModel = util.creatFeatureModel(false);
    Map<Long, EventsModuleData> eventsModuleData = new HashMap<>();
    List<String> markets = new ArrayList<>();
    markets.add("TwoUp");
    featureModel
        .getModules()
        .forEach(
            module -> {
              if (module.getModuleType().equals(ModuleType.HIGHLIGHTS_CAROUSEL)
                  || module.getModuleType().equals(ModuleType.INPLAY)
                  || module.getModuleType().equals(ModuleType.FEATURED))
                FeaturedConsumerUtil.setEventsModuleData(eventsModuleData, module, markets);
            });
    featureModel.setEventsModuleData(eventsModuleData);
    when(instance.getValue(any(), any())).thenReturn(objectMapper.writeValueAsString(featureModel));
    FeaturedModel resultedModel = service.getFeaturedModel("0", 1L);
    Assert.assertNotNull(resultedModel);
    Assert.assertTrue(compare(featureModel, resultedModel));
  }

  @Test
  public void testgetFeaturedModelException() {

    FeaturedModel featureModel = util.creatFeatureModel(false);
    when(instance.getValue(any(), any())).thenReturn("{");
    FeaturedModel resultedModel = service.getFeaturedModel("0", 1L);
    Assert.assertNull(resultedModel);
  }

  @Test
  public void testgetFeaturedModelNullString() throws JsonProcessingException {
    FeaturedModel featureModel = util.creatFeatureModel(false);
    when(instance.getValue(any(), any())).thenReturn(null);
    FeaturedModel resultedModel = service.getFeaturedModel("0", 1L);
    Assert.assertNull(resultedModel);
  }

  @Test
  public void saveLastRunTime() throws JsonProcessingException {
    service.saveLastRunTime(Long.valueOf("1640176190014"));
    verify(instance, times(1)).updateExpirableValue(any(), any());
  }

  @Test
  public void testgetLastRunTimeAsNull() throws JsonProcessingException {
    when(instance.getValue(any())).thenReturn(null);
    Long lastRunTime = service.getLastRunTime();
    Assert.assertNull(lastRunTime);
  }

  @Test
  public void testgetLastRunTimeAsNotNull() throws JsonProcessingException {
    when(instance.getValue(any())).thenReturn("1640176190014");
    Long lastRunTime = service.getLastRunTime();
    Assert.assertNotNull(lastRunTime);
  }

  private boolean compare(FeaturedModel featureModel, FeaturedModel resultedModel) {
    if (featureModel != null && resultedModel != null) {
      if (compareFeatureModel(featureModel, resultedModel)) {

        return compareModules(featureModel.getModules(), resultedModel.getModules());
      }
    }

    return false;
  }

  private boolean compareModules(
      List<AbstractFeaturedModule<?>> modules, List<AbstractFeaturedModule<?>> resultmodules1) {
    if (modules.size() == resultmodules1.size()) {
      Map<String, AbstractFeaturedModule<?>> moduleMap = new HashMap<>();
      Map<String, AbstractFeaturedModule<?>> resultmoduleMap = new HashMap<>();

      for (AbstractFeaturedModule module : modules) {
        moduleMap.put(module.getTitle(), module);
      }
      for (AbstractFeaturedModule module : resultmodules1) {
        resultmoduleMap.put(module.getTitle(), module);
      }

      return compareModuleMap(moduleMap, resultmoduleMap);
    }
    return false;
  }

  private boolean compareModuleMap(
      Map<String, AbstractFeaturedModule<?>> moduleMap,
      Map<String, AbstractFeaturedModule<?>> resultmoduleMap) {

    for (String key : moduleMap.keySet()) {

      if (!compareModule(moduleMap.get(key), resultmoduleMap.get(key))) {

        return false;
      }
    }
    return true;
  }

  private boolean compareModule(
      AbstractFeaturedModule<?> abstractFeaturedModule,
      AbstractFeaturedModule<?> resultabstractFeaturedModule1) {

    return abstractFeaturedModule
            .getModuleType()
            .equals(resultabstractFeaturedModule1.getModuleType())
        && abstractFeaturedModule.getShowExpanded()
        && resultabstractFeaturedModule1.getShowExpanded()
        && abstractFeaturedModule
            .getDisplayOrder()
            .equals(resultabstractFeaturedModule1.getDisplayOrder())
        && abstractFeaturedModule
            .getSecondaryDisplayOrder()
            .equals(resultabstractFeaturedModule1.getSecondaryDisplayOrder())
        && abstractFeaturedModule.getPublishedDevices().size()
            == resultabstractFeaturedModule1.getPublishedDevices().size()
        && abstractFeaturedModule.getTitle().equals(resultabstractFeaturedModule1.getTitle())
        && abstractFeaturedModule.isSegmented()
        && resultabstractFeaturedModule1.isSegmented()
        && abstractFeaturedModule.isValid()
        && resultabstractFeaturedModule1.isValid()
        && abstractFeaturedModule
            .getErrorMessage()
            .equals(resultabstractFeaturedModule1.getErrorMessage())
        && abstractFeaturedModule.getData().size() == resultabstractFeaturedModule1.getData().size()
        && abstractFeaturedModule.hasStaticContent()
            == resultabstractFeaturedModule1.hasStaticContent()
        && abstractFeaturedModule.getId().equals(resultabstractFeaturedModule1.getId());
  }

  private boolean compareFeatureModel(FeaturedModel featureModel, FeaturedModel resultedModel) {

    return featureModel.getDirectiveName().equals(resultedModel.getDirectiveName())
        && featureModel.getPageId().equals(resultedModel.getPageId())
        && featureModel.isVisible()
        && resultedModel.isVisible()
        && featureModel.isFeatureStructureChanged()
        && resultedModel.isFeatureStructureChanged()
        && featureModel.isSegmented()
        && resultedModel.isSegmented();
  }
}
