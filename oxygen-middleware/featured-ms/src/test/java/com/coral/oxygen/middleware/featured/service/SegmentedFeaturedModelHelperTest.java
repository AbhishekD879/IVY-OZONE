package com.coral.oxygen.middleware.featured.service;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment;
import java.math.BigDecimal;
import java.util.*;
import java.util.stream.Collectors;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SegmentedFeaturedModelHelperTest {

  @Test
  public void shouldPrepareSFMwithEmptyModules() {

    FeaturedModel featuredModel = createStructureWithEmptySegmentWiseModules("0");

    SegmentView segmentView = featuredModel.getSegmentWiseModules().get("Universal");
    List<AbstractFeaturedModule<?>> nonSegmentedModules = new ArrayList<>();
    SegmentedFeaturedModelHelper.fillNonSegmentedModules(featuredModel, nonSegmentedModules);
    SegmentedFeaturedModel segmentedFeaturedModel =
        SegmentedFeaturedModelHelper.createSegmentedFeaturedModel(featuredModel);
    SegmentedFeaturedModelHelper.populateSegmentedFeaturedModel(
        featuredModel, segmentedFeaturedModel, segmentView);
    segmentedFeaturedModel.addModules(nonSegmentedModules);

    Assert.assertEquals("0", segmentedFeaturedModel.getPageId());
    Assert.assertTrue(segmentedFeaturedModel.getModules().isEmpty());
  }

  @Test
  public void shouldPrepareSFMwithUniqueIds() {

    FeaturedModel featuredModel = createStructureWithSegmentWiseModules("0");
    Set<String> deserializedUniqueIds = new HashSet<>();
    featuredModel.getModules().stream()
        .filter(module -> module instanceof HighlightCarouselModule)
        .forEach(
            hc -> {
              deserializedUniqueIds.addAll(
                  hc.getData().stream()
                      .map(emd -> ((EventsModuleData) emd).getUniqueId())
                      .collect(Collectors.toSet()));
            });

    SegmentView segmentView = featuredModel.getSegmentWiseModules().get("Universal");
    List<AbstractFeaturedModule<?>> nonSegmentedModules = new ArrayList<>();
    SegmentedFeaturedModelHelper.fillNonSegmentedModules(featuredModel, nonSegmentedModules);
    SegmentedFeaturedModel segmentedFeaturedModel =
        SegmentedFeaturedModelHelper.createSegmentedFeaturedModel(featuredModel);
    SegmentedFeaturedModelHelper.populateSegmentedFeaturedModel(
        featuredModel, segmentedFeaturedModel, segmentView);
    segmentedFeaturedModel.addModules(nonSegmentedModules);

    Set<String> serializedUniqueIds = new HashSet<>();
    segmentedFeaturedModel.getModules().stream()
        .filter(module -> module instanceof HighlightCarouselModule)
        .forEach(
            hc -> {
              serializedUniqueIds.addAll(
                  hc.getData().stream()
                      .map(emd -> ((EventsModuleData) emd).getUniqueId())
                      .collect(Collectors.toSet()));
            });

    Assert.assertEquals("0", segmentedFeaturedModel.getPageId());
    Assert.assertFalse(serializedUniqueIds.containsAll(deserializedUniqueIds));
  }

  private FeaturedModel createStructureWithEmptySegmentWiseModules(String pageId) {
    FeaturedModel model = new FeaturedModel();
    model.setPageId(pageId);
    SegmentView segmentView = new SegmentView();
    Map<String, SegmentView> segmentWiseModules = new HashMap<>();
    segmentWiseModules.put("Universal", segmentView);
    model.setSegmentWiseModules(segmentWiseModules);
    return model;
  }

  private FeaturedModel createStructureWithSegmentWiseModules(String pageId) {
    FeaturedModel model = new FeaturedModel();

    List<AbstractFeaturedModule<?>> modules = new ArrayList<>();
    model.setPageId(pageId);
    modules.add(createInternationalToteModule("Tote Module"));
    Map<String, SegmentView> segmentWiseModules = new HashMap<>();
    SegmentView segmentView = new SegmentView();
    HighlightCarouselModule highlightCarouselModule =
        createHighlightCarouselModule("Highlight Carousel");
    modules.add(highlightCarouselModule);
    SegmentOrderdModule segmentOrderdModuleForHc =
        new SegmentOrderdModule(1, highlightCarouselModule);
    segmentView
        .getHighlightCarouselModules()
        .put(highlightCarouselModule.getId(), segmentOrderdModuleForHc);

    EventsModule featureModule = createFeaturedModule("Feature Module");
    modules.add(featureModule);
    SegmentOrderdModule segmentOrderdModuleForEventModule =
        new SegmentOrderdModule(1, featureModule);
    segmentView.getEventModules().put(featureModule.getId(), segmentOrderdModuleForEventModule);

    EventsModule featureModule2 = createFeaturedModule("Feature Module 2");
    featureModule2.setShowExpanded(true);
    modules.add(featureModule2);
    SegmentOrderdModule segmentOrderdModuleForEventModule2 =
        new SegmentOrderdModule(1, featureModule2);
    List<EventsModuleData> eventsModuleDataList2 = new ArrayList<>();
    EventsModuleData eventsModuleData2 = new EventsModuleData();
    eventsModuleDataList2.add(eventsModuleData2);
    segmentOrderdModuleForEventModule2.setEventsModuleData(eventsModuleDataList2);
    segmentView.getEventModules().put(featureModule2.getId(), segmentOrderdModuleForEventModule2);

    QuickLinkModule quickLinkModule = createQuickLinkModule("Quick Link");
    modules.add(quickLinkModule);
    model.setQuickLinkModule(quickLinkModule);
    SegmentOrderdModuleData segmentOrderdModuleForQl =
        new SegmentOrderdModuleData(1, quickLinkModule.getData().get(0));
    segmentView.getQuickLinkData().put(quickLinkModule.getId(), segmentOrderdModuleForQl);

    SurfaceBetModule surfaceBetModule = createSurfaceBetModule("surfaceBet Link");
    modules.add(surfaceBetModule);
    model.setSurfaceBetModule(surfaceBetModule);
    SegmentOrderdModuleData segmentOrderdModuleForSb =
        new SegmentOrderdModuleData(1, surfaceBetModule.getData().get(0));
    segmentView.getSurfaceBetModuleData().put(surfaceBetModule.getId(), segmentOrderdModuleForSb);

    InplayModule inplayModule = createInplayModule("Inplay Module");
    modules.add(inplayModule);
    model.setInplayModule(inplayModule);
    SegmentOrderdModuleData segmentOrderdModuleForInplay =
        new SegmentOrderdModuleData(1, inplayModule.getData().get(0));
    List<SegmentedEvents> limitedEvents = new ArrayList<>();
    SegmentedEvents segmentedEvents = new SegmentedEvents();
    TypeSegment eventByTypeName = new TypeSegment();
    EventsModuleData eventsModuleData = new EventsModuleData();
    List<EventsModuleData> events = new ArrayList<>();
    events.add(eventsModuleData);
    segmentedEvents.setEventByTypeName(eventByTypeName);
    segmentedEvents.setEvents(events);
    limitedEvents.add(segmentedEvents);
    segmentOrderdModuleForInplay.setLimitedEvents(limitedEvents);
    segmentView.getInplayModuleData().put(inplayModule.getId(), segmentOrderdModuleForInplay);

    segmentWiseModules.put("Universal", segmentView);
    segmentWiseModules.put("segment-one", segmentView);
    model.setSegmentWiseModules(segmentWiseModules);

    model.setModules(modules);
    return model;
  }

  InternationalToteRaceModule createInternationalToteModule(String id) {
    InternationalToteRaceModule module = new InternationalToteRaceModule();
    module.setId(id);
    module.setDisplayOrder(new BigDecimal(1));
    return module;
  }

  private SurfaceBetModule createSurfaceBetModule(String id) {
    SurfaceBetModule module = new SurfaceBetModule();
    module.setId(id);
    module.setDisplayOrder(new BigDecimal(1));
    SurfaceBetModuleData surfaceBetModuleData = new SurfaceBetModuleData();
    List<SurfaceBetModuleData> data = new ArrayList();
    data.add(surfaceBetModuleData);
    module.setData(data);
    return module;
  }

  private HighlightCarouselModule createHighlightCarouselModule(String id) {
    HighlightCarouselModule module = new HighlightCarouselModule();
    module.setId(id);
    EventsModuleData data = new EventsModuleData();
    data.setId(123L);
    ArrayList list = new ArrayList();
    list.add(data);
    module.setData(list);
    return module;
  }

  private QuickLinkModule createQuickLinkModule(String id) {
    QuickLinkModule qlModule = new QuickLinkModule();
    qlModule.setTitle("quinklink");
    qlModule.setDisplayOrder(new BigDecimal(2));
    qlModule.setId(id);
    List<QuickLinkData> data = new ArrayList();
    QuickLinkData quickLinkData = new QuickLinkData();
    data.add(quickLinkData);
    qlModule.setData(data);
    return qlModule;
  }

  EventsModule createFeaturedModule(String id) {
    EventsModuleData eventData = new EventsModuleData();
    eventData.setId(12L);
    eventData.setDisplayOrder(4);
    List<EventsModuleData> data = new ArrayList<>();
    data.add(eventData);

    EventsModule thisModule = new EventsModule();
    thisModule.setId(id);
    thisModule.setSportId(0);
    thisModule.setTitle("eventmodule");
    thisModule.setData(data);
    return thisModule;
  }

  private InplayModule createInplayModule(String id) {
    InplayModule module = new InplayModule();
    module.setId(id);
    module.setDisplayOrder(new BigDecimal(1));
    SportSegment sportSegment = new SportSegment();
    List<SportSegment> data = new ArrayList();
    data.add(sportSegment);
    module.setData(data);

    return module;
  }
}
