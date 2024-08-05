package com.coral.oxygen.middleware.featured.service;

import static java.util.Collections.emptyList;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.then;
import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.common.configuration.cfcache.DeliveryNetworkService;
import com.coral.oxygen.middleware.common.service.featured.FeaturedModelChangeDetector;
import com.coral.oxygen.middleware.common.service.featured.FeaturedModuleChangeDetector;
import com.coral.oxygen.middleware.common.service.notification.MessagePublisher;
import com.coral.oxygen.middleware.common.service.notification.topic.TopicType;
import com.coral.oxygen.middleware.pojos.model.cms.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModel;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModelsData;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.VersionedPageKey;
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType;
import com.google.common.collect.Sets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Set;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentMatchers;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class FeaturedDataProcessorTest {

  private static final long LAST_VERSION = 1L;
  private static final long NEXT_VERSION = 11L;

  private FeaturedDataProcessor thisService;

  @Mock private FeaturedModelStorageService storageService;
  @Mock private FeaturedModuleChangeDetector featuredModuleChangeDetector;
  @Mock private FeaturedModelChangeDetector featuredModelChangeDetector;
  @Mock private MessagePublisher messagePublisher;
  @Mock private FeaturedLiveServerSubscriber featuredLiveServerSubscriber;
  FaeturemodelUtil util = new FaeturemodelUtil();

  private VersionedPageKey homeIndex;

  private VersionedPageKey footballIndex;
  @Mock private DeliveryNetworkService context;

  @Before
  public void init() {
    thisService =
        new FeaturedDataProcessor(
            storageService,
            featuredModuleChangeDetector,
            featuredModelChangeDetector,
            messagePublisher,
            featuredLiveServerSubscriber,
            context);
  }

  private Set<VersionedPageKey> createPageKeys(long version) {
    return Sets.newHashSet(
        new VersionedPageKey(FeaturedRawIndex.PageType.sport, "0", version),
        new VersionedPageKey(FeaturedRawIndex.PageType.sport, "16", version));
  }

  @Test
  public void comparePageIndexes_FirstCall_OK() {
    Set<VersionedPageKey> thisIndex = createPageKeys(LAST_VERSION);
    thisService.comparePageIndexes(LAST_VERSION, thisIndex, true);
    then(messagePublisher).shouldHaveNoInteractions();
  }

  @Test
  public void comparePageIndexes_SecondCall_NoChanges_OK() {
    comparePageIndexes_FirstCall_OK();
    Set<VersionedPageKey> thisIndex = createPageKeys(NEXT_VERSION);
    thisService.comparePageIndexes(NEXT_VERSION, thisIndex, false);
    then(messagePublisher).shouldHaveNoInteractions();
  }

  @Test
  public void comparePageIndexes_SecondCall_FoundChanges_OK() {
    comparePageIndexes_FirstCall_OK();
    Set<VersionedPageKey> thisIndex = createPageKeys(NEXT_VERSION);

    VersionedPageKey anyIndex = thisIndex.toArray(new VersionedPageKey[thisIndex.size()])[0];
    thisIndex.remove(anyIndex);

    thisService.comparePageIndexes(NEXT_VERSION, thisIndex, false);
    then(messagePublisher)
        .should(times(1))
        .publish(TopicType.SPORTS_FEATURED_PAGE_DELETED, anyIndex.toString());
  }

  @Test
  public void sportPagesNew() {
    List<String> sportPages = Arrays.asList("1", "2", "8", "16", "h1", "h3");
    FeaturedModelsData data = mock(FeaturedModelsData.class);
    doReturn(emptyList()).when(data).getFeaturedModels();
    doReturn(sportPages).when(data).getSportPages();

    thisService.process(data);

    List<String> expectedSportPages = new ArrayList<>(sportPages);
    expectedSportPages.sort(String::compareTo);
    verify(storageService, never()).getNextVersion();
    verify(messagePublisher, times(expectedSportPages.size()))
        .publish(ArgumentMatchers.eq(TopicType.SPORTS_FEATURED_PAGE_ADDED), anyString());
  }

  @Test
  public void sportPagesNotChanged() {
    List<String> sportPages = Arrays.asList("1", "2", "8", "16", "h1", "h3");
    sportPages.sort(String::compareTo);

    FeaturedModelsData data = mock(FeaturedModelsData.class);
    doReturn(emptyList()).when(data).getFeaturedModels();
    doReturn(sportPages).when(data).getSportPages();
    doReturn(sportPages).when(storageService).getAndSaveFeaturedSports(anyList());

    thisService.process(data);

    verify(storageService, never()).getNextVersion();
    verifyNoInteractions(messagePublisher);
  }

  @Test
  public void processpage() {
    FeaturedModel model = util.creatFeatureModel(false);

    when(storageService.getPreviousVersion(10l)).thenReturn(9l);
    when(storageService.getFeaturedModel("0", 9l)).thenReturn(model);

    FeaturedModel rsult = util.creatFeatureModel(false);
    rsult.setFeatureStructureChanged(true);
    when(storageService.save(any(FeaturedModel.class), anyLong())).thenReturn(rsult);
    thisService.processPage(model, 10l);
    verify(messagePublisher, times(1)).publish(any(), any());
  }

  @Test
  public void processpageStructureChngedfalse() {
    FeaturedModel model = util.creatFeatureModel(false);

    when(storageService.getPreviousVersion(10l)).thenReturn(9l);
    when(storageService.getFeaturedModel("0", 9l)).thenReturn(model);

    FeaturedModel rsult = util.creatFeatureModel(false);
    rsult.setFeatureStructureChanged(false);
    when(featuredModelChangeDetector.isSegmentedModulesChanged(
                any(FeaturedModel.class), any(FeaturedModel.class))
            || featuredModelChangeDetector.isFanzoneSegmentedModulesChanged(
                any(FeaturedModel.class), any(FeaturedModel.class)))
        .thenReturn(true);
    when(storageService.save(any(FeaturedModel.class), anyLong())).thenReturn(rsult);
    thisService.processPage(model, 10l);
    verify(messagePublisher, times(1)).publish(any(), any());
  }

  @Test
  public void processpageUseFscCachedTrueForFootBallPage() {
    FeaturedModel model = util.creatFeatureModel(false);
    model.setPageId("16");
    when(storageService.getPreviousVersion(10l)).thenReturn(9l);
    when(storageService.getFeaturedModel("16", 9l)).thenReturn(model);

    FeaturedModel rsult = util.creatFeatureModel(false);
    rsult.setPageId("16");
    rsult.setUseFSCCached(true);
    rsult.setFeatureStructureChanged(false);
    when(featuredModelChangeDetector.isSegmentedModulesChanged(
                any(FeaturedModel.class), any(FeaturedModel.class))
            || featuredModelChangeDetector.isFanzoneSegmentedModulesChanged(
                any(FeaturedModel.class), any(FeaturedModel.class)))
        .thenReturn(true);
    when(storageService.save(any(FeaturedModel.class), anyLong())).thenReturn(rsult);
    thisService.processPage(model, 10l);
    verify(messagePublisher, times(1)).publish(any(), any());
  }

  @Test
  public void processpageUseFscCachedTrueWithSegmentedModules() {
    FeaturedModel model = util.createStructureWithSegmentWiseModules("0");
    when(storageService.getPreviousVersion(10l)).thenReturn(9l);
    when(storageService.getFeaturedModel("0", 9l)).thenReturn(model);

    FeaturedModel rsult = util.createStructureWithSegmentWiseModules("0");
    rsult.setUseFSCCached(true);
    rsult.setFeatureStructureChanged(false);
    when(featuredModelChangeDetector.isSegmentedModulesChanged(
            any(FeaturedModel.class), any(FeaturedModel.class)))
        .thenReturn(true);
    when(storageService.save(any(FeaturedModel.class), anyLong())).thenReturn(rsult);
    thisService.processPage(model, 10l);
    verify(messagePublisher, times(1)).publish(any(), any());
  }

  @Test
  public void processpageUseFscCachedTrueWithNoSegmentedModules() {
    FeaturedModel model = util.createStructureWithSegmentWiseModules("0");
    when(storageService.getPreviousVersion(10l)).thenReturn(9l);
    when(storageService.getFeaturedModel("0", 9l)).thenReturn(model);

    FeaturedModel rsult = util.createStructureWithSegmentWiseModules("0");
    rsult.setSegmentWiseModules(null);
    rsult.setUseFSCCached(true);
    rsult.setFeatureStructureChanged(false);
    when(storageService.save(any(FeaturedModel.class), anyLong())).thenReturn(rsult);
    thisService.processPage(model, 10l);
    verify(messagePublisher, times(1)).publish(any(), any());
  }

  @Test
  public void processpageStructureChngedAndisSegmentedModulesChangedfalse() {
    FeaturedModel model = util.creatFeatureModel(false);

    when(storageService.getPreviousVersion(10l)).thenReturn(9l);
    when(storageService.getFeaturedModel("0", 9l)).thenReturn(model);

    FeaturedModel rsult = util.creatFeatureModel(false);
    rsult.setFeatureStructureChanged(false);
    when(featuredModelChangeDetector.isChanged(any(FeaturedModel.class), any(FeaturedModel.class)))
        .thenReturn(true);
    when(storageService.save(any(FeaturedModel.class), anyLong())).thenReturn(rsult);
    thisService.processPage(model, 10l);
    verify(messagePublisher, times(1)).publish(any(), any());
  }

  @Test
  public void processpageStructureChngedAllfalse() {
    FeaturedModel model = util.creatFeatureModel(false);
    model.setUseFSCCached(true);
    when(storageService.getPreviousVersion(10l)).thenReturn(9l);
    when(storageService.getFeaturedModel("0", 9l)).thenReturn(model);

    FeaturedModel rsult = util.creatFeatureModel(false);
    rsult.setFeatureStructureChanged(false);
    when(storageService.save(any(FeaturedModel.class), anyLong())).thenReturn(rsult);
    thisService.processPage(model, 10l);
    verify(messagePublisher, times(0)).publish(any(), any());
  }

  @Test
  public void processModuledataTest() {
    FeaturedModel previousModel = util.creatFeatureModel(false);

    when(storageService.getPreviousVersion(10l)).thenReturn(9l);
    when(storageService.getFeaturedModel("0", 9l)).thenReturn(previousModel);

    FeaturedModel model = util.creatFeatureModel(false);
    List<FeaturedModel> featuredModels = new ArrayList<>();
    featuredModels.add(model);
    List<SportPage> sportPages = new ArrayList<>();
    SportPage sportPage = sportsQuickLink();
    sportPages.add(sportPage);
    FeaturedModelsData dats = new FeaturedModelsData(featuredModels, sportPages);
    when(storageService.getNextVersion()).thenReturn(10l);
    FeaturedModel rsult = util.creatFeatureModel(false);
    rsult.setFeatureStructureChanged(false);
    when(storageService.save(any(FeaturedModel.class), anyLong())).thenReturn(rsult);
    thisService.process(dats);
    verify(messagePublisher, times(1)).publish(any(), any());
  }

  @Test
  public void processModuledataWithEmptyTest() {

    FeaturedModelsData dats = new FeaturedModelsData();
    thisService.process(dats);
    verify(messagePublisher, times(0)).publish(any(), any());
  }

  @Test
  public void testSaveLastRunTime() {

    thisService.saveLastRunTime(Long.valueOf("1640176190014"));
    verify(storageService, times(1)).saveLastRunTime(Long.valueOf("1640176190014"));
  }

  private SportPage sportsQuickLink() {
    List<SportPageModule> sportPageModules = new ArrayList<>();
    ArrayList<SportPageModuleDataItem> dataItems = new ArrayList<>();

    SportsQuickLink data = new SportsQuickLink();

    data.setTitle("test");
    dataItems.add(data);
    sportPageModules.add(
        new SportPageModule(
            SportModule.builder()
                .moduleType(ModuleType.QUICK_LINK)
                .sportId(3)
                .pageType(FeaturedRawIndex.PageType.eventhub)
                .id("test")
                .brand("bma")
                .title("test")
                .build(),
            Arrays.asList(
                SportsQuickLink.builder()
                    .id("test1")
                    .sportId(3)
                    .pageType(FeaturedRawIndex.PageType.eventhub)
                    .svgId("svgId")
                    .destination("dest")
                    .build())));
    SportPage sportPage = new SportPage("h3", sportPageModules);
    sportPage.setPageId("3");
    sportPage.setPageType(FeaturedRawIndex.PageType.eventhub);
    return sportPage;
  }
}
