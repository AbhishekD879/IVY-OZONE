package com.coral.oxygen.middleware.common.service;

import com.coral.oxygen.middleware.pojos.model.InPlayTopLevelType;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SegmentReference;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.Assert;
import org.junit.Test;

public class ModuleAdapterTest {

  @Test
  public void serializeDeserializeTest() {
    String out = ModuleAdapter.FEATURED_GSON.toJson(new EventsModule());
    AbstractFeaturedModule module =
        ModuleAdapter.FEATURED_GSON.fromJson(out, AbstractFeaturedModule.class);
    Assert.assertTrue(module instanceof EventsModule);
  }

  @Test
  public void toLiveServeModulesTest() {
    List<AbstractFeaturedModule<?>> featuredModules = new ArrayList<>();
    HighlightCarouselModule hCModule = new HighlightCarouselModule();
    hCModule.setData(new ArrayList<>());
    EventsModule eModule = new EventsModule();
    eModule.setData(Collections.singletonList(new EventsModuleData()));
    InplayModule iModule = new InplayModule();
    iModule.setData(new ArrayList<>());
    QuickLinkModule qLModule = new QuickLinkModule();
    qLModule.setData(new ArrayList<>());

    BybWidgetModule bybModule = new BybWidgetModule();
    bybModule.setData(new ArrayList<>());

    PopularAccaModule popularAccaModule = new PopularAccaModule();
    PopularAccaModuleData popularAccaModuleData = new PopularAccaModuleData();
    popularAccaModuleData.setPositions(new ArrayList<>());
    List<PopularAccaModuleData> accasData = new ArrayList<>();
    accasData.add(popularAccaModuleData);
    popularAccaModule.setData(accasData);

    featuredModules.add(hCModule);
    featuredModules.add(eModule);
    featuredModules.add(iModule);
    featuredModules.add(qLModule);
    featuredModules.add(bybModule);
    featuredModules.add(popularAccaModule);
    ModuleAdapter adapter = new ModuleAdapter() {};
    List<EventsModuleData> eventsModules = adapter.toLiveserveEventsData(featuredModules);
    Assert.assertEquals(1, eventsModules.size());
  }

  @Test
  public void toLiveServeModuleWithSegmentedDataTest() {
    List<AbstractFeaturedModule<?>> featuredModules = new ArrayList<>();
    InplayModule iModule = createInplayModuleWithData();
    prepareModuleDataSegmentView(iModule);
    featuredModules.add(iModule);

    ModuleAdapter adapter = new ModuleAdapter() {};
    List<EventsModuleData> eventsModules = adapter.toLiveserveEventsData(featuredModules);
    Assert.assertEquals(1, eventsModules.size());
  }

  @Test
  public void toLiveServeModuleWithDataTest() {
    List<AbstractFeaturedModule<?>> featuredModules = new ArrayList<>();
    InplayModule iModule = createInplayModuleWithData();
    iModule.setSegmented(false);
    featuredModules.add(iModule);

    ModuleAdapter adapter = new ModuleAdapter() {};
    List<EventsModuleData> eventsModules = adapter.toLiveserveEventsData(featuredModules);
    Assert.assertEquals(1, eventsModules.size());
  }

  private void prepareModuleDataSegmentView(InplayModule inplayModule) {
    Map<String, SegmentView> segmentMap = new HashMap<>();
    Map<String, SegmentOrderdModuleData> segmentModuleData = new HashMap<>();
    SegmentView view = new SegmentView();
    SegmentOrderdModuleData moduleData = new SegmentOrderdModuleData();
    moduleData.setSegmentOrder(1.0);
    SportSegment sportSegment = inplayModule.getData().get(0);
    moduleData.setInplayData(sportSegment);
    List<SegmentedEvents> limitedEvents = new ArrayList();
    SegmentedEvents segmentedEvents = new SegmentedEvents();
    segmentedEvents.setEventByTypeName(sportSegment.getEventsByTypeName().get(0));
    segmentedEvents.setEvents(sportSegment.getEventsByTypeName().get(0).getEvents());
    limitedEvents.add(segmentedEvents);
    moduleData.setLimitedEvents(limitedEvents);
    segmentModuleData.put("s1", moduleData);
    view.setInplayModuleData(segmentModuleData);
    segmentMap.put("s1", view);
    inplayModule.setModuleSegmentView(segmentMap);
  }

  private InplayModule createInplayModuleWithData() {

    InplayModule inplayModule = new InplayModule();
    inplayModule.setTotalEvents(10);
    updateAbstractFeaturedModule(
        inplayModule, "@InplayModule", "InplayModule", FeaturedRawIndex.PageType.sport);
    SportSegment segmentdata = new SportSegment();
    List<SportSegment> sportSegList = new ArrayList<>();
    segmentdata.setCategoryId(20);
    segmentdata.setShowInPlay(true);
    segmentdata.setCategoryName("categoryName");
    segmentdata.setCategoryCode("CatCode");
    segmentdata.setCategoryPath("path");
    segmentdata.setDisplayOrder(10);
    segmentdata.setSportUri("sporturi");
    segmentdata.setSvgId("svgid");
    segmentdata.setEventCount(10);
    segmentdata.setMarketSelector("MarketSelector");
    segmentdata.setTopLevelType(InPlayTopLevelType.UPCOMING_EVENT);
    segmentdata.setMarketSelectorOptions(Arrays.asList("213,345,678".split(",")));
    Collection<Long> eventsIds = new ArrayList<>();
    eventsIds.add(100L);
    segmentdata.setEventsIds(eventsIds);
    segmentdata.setSegments(Arrays.asList("s1,Universal".split(",")));
    List<SegmentReference> segmentReferences = new ArrayList<>();
    SegmentReference reference = new SegmentReference();
    reference.setSegment("s1");
    reference.setDisplayOrder(20.0);
    segmentReferences.add(reference);
    segmentdata.setSegmentReferences(segmentReferences);

    List<EventsModuleData> eventsModules = new ArrayList<>();
    EventsModuleData eventsModuleData = new EventsModuleData();
    eventsModules.add(eventsModuleData);

    TypeSegment segment = new TypeSegment();
    List<TypeSegment> segments = new ArrayList<>();

    segment.setClassName("className");
    segment.setCategoryName("categoryname");
    segment.setCategoryCode("categoryCode");
    segment.setTypeName("typename");
    segment.setTypeId("Typeid");
    segment.setClassDisplayOrder(10);
    segment.setTypeDisplayOrder(10);
    segment.setTypeSectionTitleAllSports("sports");
    segment.setTypeSectionTitleOneSport("sports");
    segment.setTypeSectionTitleConnectApp("connectapps");
    segment.setEventCount(10);
    segment.setEventsIds(new ArrayList<>());
    segment.setEvents(eventsModules);
    segments.add(segment);
    segmentdata.setEventsByTypeName(segments);
    sportSegList.add(segmentdata);

    inplayModule.setData(sportSegList);

    return inplayModule;
  }

  private void updateAbstractFeaturedModule(
      AbstractFeaturedModule featureModule,
      String id,
      String title,
      FeaturedRawIndex.PageType pageType) {
    if (id == null) {
      featureModule.setId("1213");
    } else {
      featureModule.setId(id);
    }
    featureModule.setPageType(pageType);
    featureModule.setSportId(0);
    featureModule.setTitle(title);
    featureModule.setDisplayOrder(BigDecimal.ZERO);
    featureModule.setSecondaryDisplayOrder(BigDecimal.ZERO);
    featureModule.setSortOrder(0.0);
    featureModule.setSegmented(true);
    featureModule.setShowExpanded(true);
    featureModule.setPublishedDevices(Arrays.asList("desktop,tablet,mobile1".split(",")));
  }
}
