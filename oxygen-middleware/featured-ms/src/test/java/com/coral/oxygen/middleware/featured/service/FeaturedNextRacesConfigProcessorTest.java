package com.coral.oxygen.middleware.featured.service;

import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.middleware.common.configuration.cfcache.DeliveryNetworkService;
import com.coral.oxygen.middleware.common.utils.QueryFilterBuilder;
import com.coral.oxygen.middleware.featured.repository.NextRacesFilterRepository;
import com.coral.oxygen.middleware.pojos.model.NextRace;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportDto;
import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportTrackDto;
import com.coral.oxygen.middleware.pojos.model.output.NextRaceFilterDto;
import com.coral.oxygen.middleware.pojos.model.output.NextRacesClfDto;
import com.egalacoral.spark.siteserver.api.ExistsFilter;
import com.egalacoral.spark.siteserver.api.LimitRecordsFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Event;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;
import org.junit.runner.RunWith;
import org.mockito.AdditionalAnswers;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class FeaturedNextRacesConfigProcessorTest {

  private FeaturedNextRacesConfigProcessor thisService;

  @Mock private NextRacesFilterRepository repository;
  @Mock private DeliveryNetworkService context;
  @Mock private SiteServerApi siteServerApi;
  @Mock private CmsService cmsService;

  @Mock private QueryFilterBuilder queryFilterBuilder;

  @Before
  public void init() {
    thisService =
        new FeaturedNextRacesConfigProcessor(
            context, siteServerApi, repository, cmsService, queryFilterBuilder, "bma", 3, 12, 5);
    Mockito.when(queryFilterBuilder.getActiveClassesForTheCategory(Mockito.any()))
        .thenReturn((SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build());
    Mockito.when(queryFilterBuilder.buildSimpleFilterForNextRaces(Mockito.any()))
        .thenReturn((SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build());
    Mockito.when(queryFilterBuilder.buildExistsFilterForNextRaces())
        .thenReturn(new ExistsFilter.ExistsFilterBuilder().build());
    Mockito.when(queryFilterBuilder.buildLimitRecordsFilterForNextRaces())
        .thenReturn(new LimitRecordsFilter.LimitRecordsFilterBuilder().build());
  }

  private CmsSystemConfig createSystemConfig(
      Object virtuals, String exclude, Object virtualsEnabled) {

    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig();

    Map<String, Object> nextRaces = new HashMap<>();
    nextRaces.put(FeaturedNextRacesConfigProcessor.CmsConfigConstants.VIRTUALS_INCLUDED, virtuals);
    nextRaces.put(FeaturedNextRacesConfigProcessor.CmsConfigConstants.VIRTUALS_EXCLUDED, exclude);
    nextRaces.put(
        FeaturedNextRacesConfigProcessor.CmsConfigConstants.VIRTUALS_ENABLED, virtualsEnabled);
    Map<String, Object> greyHoundNextRaces = new HashMap<>();
    greyHoundNextRaces.put(
        FeaturedNextRacesConfigProcessor.CmsConfigConstants.VIRTUALS_INCLUDED, virtuals);
    greyHoundNextRaces.put(
        FeaturedNextRacesConfigProcessor.CmsConfigConstants.VIRTUALS_EXCLUDED, exclude);
    greyHoundNextRaces.put(
        FeaturedNextRacesConfigProcessor.CmsConfigConstants.VIRTUALS_ENABLED, virtualsEnabled);
    cmsSystemConfig.setNextRaces(nextRaces);
    cmsSystemConfig.setGreyhoundNextRaces(greyHoundNextRaces);
    return cmsSystemConfig;
  }

  @Test
  public void testNextRaces1() {
    CmsSystemConfig cmsSystemConfig =
        createSystemConfig(List.of("Chase Park", "Epsom Down"), "", "Yes");
    List<Event> events = getSiteServEvents(Arrays.asList("UK", "IE", "INT"));
    Event event = new Event();
    event.setCategoryId("39");
    event.setStartTime(Instant.now().plus(5, ChronoUnit.HOURS).toString());
    event.setTypeFlagCodes("VR");
    events.add(event);
    Mockito.when(this.repository.findByCategoryId(Mockito.any())).thenReturn(Optional.empty());
    Mockito.when(this.siteServerApi.getClasses(Mockito.any(), Mockito.any()))
        .thenReturn(getCategories());
    Mockito.when(this.cmsService.getVirtualSportsByBrand())
        .thenReturn(
            Arrays.asList(
                getVirtualSports(NextRace.HR.getSportName(), "Chase Park"),
                getVirtualSports(NextRace.GH.getSportName(), "Epsom Down")));
    Mockito.when(
            this.siteServerApi.getNextNEventToOutcomeForClass(
                Mockito.eq(12),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.eq(true),
                Mockito.eq(false)))
        .thenReturn(Optional.of(events));
    Mockito.when(this.repository.save(Mockito.any()))
        .thenAnswer(AdditionalAnswers.returnsFirstArg());
    Assertions.assertDoesNotThrow(() -> this.thisService.processNextRaces(cmsSystemConfig));
  }

  @Test
  public void testNextRaces2() {
    CmsSystemConfig cmsSystemConfig =
        createSystemConfig(
            List.of("Epsom", "Chae"),
            "{from={hh=0.0, mm=00, ss=00}, to={hh=0.0, mm=00, ss=00}}",
            "No");
    List<Event> events = getSiteServEvents(Arrays.asList("UK", "IE", "INT"));
    Mockito.when(this.repository.findByCategoryId(Mockito.eq("21")))
        .thenReturn(Optional.of(buildDto("21")));
    Mockito.when(this.repository.findByCategoryId(Mockito.eq("19")))
        .thenReturn(Optional.of(buildDto("19")));
    Mockito.when(this.siteServerApi.getClasses(Mockito.any(), Mockito.any()))
        .thenReturn(getCategories());
    Mockito.when(this.cmsService.getVirtualSportsByBrand())
        .thenReturn(
            Arrays.asList(
                getVirtualSports(NextRace.HR.getSportName(), "Chase Park"),
                getVirtualSports(NextRace.GH.getSportName(), "Epsom Down")));
    Mockito.when(
            this.siteServerApi.getNextNEventToOutcomeForClass(
                Mockito.eq(12),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.eq(true),
                Mockito.eq(false)))
        .thenReturn(Optional.of(events));
    Mockito.when(this.repository.save(Mockito.any()))
        .thenAnswer(AdditionalAnswers.returnsFirstArg());
    Assertions.assertDoesNotThrow(() -> this.thisService.processNextRaces(cmsSystemConfig));
  }

  @Test
  public void testNextRaces3() {
    CmsSystemConfig cmsSystemConfig =
        createSystemConfig(
            List.of("Epsom", "Chase"),
            "{from={hh=0.0, mm=00, ss=00}, to={hh=0.0, mm=00, ss=00}}",
            "No");
    List<Event> events = getSiteServEvents(Arrays.asList("IE", "INT", "GKC"));
    Event event = new Event();
    event.setCategoryId("39");
    event.setStartTime(Instant.now().plus(5, ChronoUnit.HOURS).toString());
    event.setTypeFlagCodes("VR");
    events.add(event);
    NextRaceFilterDto dto = buildDto("21");
    NextRacesClfDto clfDto = dto.getNextRaces().get("UK");
    clfDto.setLastEventTime(Instant.now().plus(1, ChronoUnit.HOURS));
    dto.setExcludeFrom(Instant.now().plus(4, ChronoUnit.HOURS));
    dto.setExcludeTo(Instant.now().plus(6, ChronoUnit.HOURS));

    NextRaceFilterDto dto1 = buildDto("19");
    NextRacesClfDto clfDto1 = dto.getNextRaces().get("VR");
    clfDto1.setLastEventTime(Instant.now().plus(1, ChronoUnit.HOURS));
    dto1.setExcludeFrom(Instant.now().plus(6, ChronoUnit.HOURS));
    dto1.setExcludeTo(Instant.now().minus(6, ChronoUnit.HOURS));
    Mockito.when(this.repository.findByCategoryId(Mockito.eq("21"))).thenReturn(Optional.of(dto));
    Mockito.when(this.repository.findByCategoryId(Mockito.eq("19"))).thenReturn(Optional.of(dto1));
    Mockito.when(this.siteServerApi.getClasses(Mockito.any(), Mockito.any()))
        .thenReturn(getCategories());
    Mockito.when(this.cmsService.getVirtualSportsByBrand())
        .thenReturn(
            Arrays.asList(
                getVirtualSports(NextRace.HR.getSportName(), "Chase Park"),
                getVirtualSports(NextRace.GH.getSportName(), "Epsom Down")));
    Mockito.when(
            this.siteServerApi.getNextNEventToOutcomeForClass(
                Mockito.eq(12),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.eq(true),
                Mockito.eq(false)))
        .thenReturn(Optional.of(events));
    Mockito.when(this.repository.save(Mockito.any()))
        .thenAnswer(AdditionalAnswers.returnsFirstArg());
    Assertions.assertDoesNotThrow(() -> this.thisService.processNextRaces(cmsSystemConfig));
  }

  @Test
  public void testNextRaces4() {
    CmsSystemConfig cmsSystemConfig =
        createSystemConfig(new Thread(), "{from={}, to={hh=0.0, mm=00, ss=00}}", new Thread());
    List<Event> events = getSiteServEvents(Arrays.asList("IE", "INT", "GKC"));
    Event event = new Event();
    event.setCategoryId("39");
    event.setStartTime(Instant.now().plus(5, ChronoUnit.HOURS).toString());
    event.setTypeFlagCodes("VTR");
    events.add(event);
    Mockito.when(this.repository.findByCategoryId(Mockito.any())).thenReturn(Optional.empty());
    Mockito.when(this.siteServerApi.getClasses(Mockito.any(), Mockito.any()))
        .thenReturn(getCategories());
    Mockito.when(this.cmsService.getVirtualSportsByBrand())
        .thenReturn(
            Arrays.asList(
                getVirtualSports(NextRace.HR.getSportName(), "Chase Park"),
                getVirtualSports(NextRace.GH.getSportName(), "Epsom Down")));
    Mockito.when(
            this.siteServerApi.getNextNEventToOutcomeForClass(
                Mockito.eq(12),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.eq(true),
                Mockito.eq(false)))
        .thenReturn(Optional.of(events));
    Mockito.when(this.repository.save(Mockito.any()))
        .thenAnswer(AdditionalAnswers.returnsFirstArg());
    Assertions.assertDoesNotThrow(() -> this.thisService.processNextRaces(cmsSystemConfig));
  }

  private List<Event> getSiteServEvents(List<String> typesCodes) {
    List<Event> events = new ArrayList<>();

    typesCodes.forEach(
        typesCode -> {
          Event event = new Event();
          event.setStartTime(Instant.now().plus(5, ChronoUnit.HOURS).toString());
          event.setTypeFlagCodes(typesCode);
          event.setId("123");
          events.add(event);
        });

    return events;
  }

  private Optional<List<Category>> getCategories() {
    Category c1 = new Category();
    c1.setId(21);
    Category c2 = new Category();
    c2.setId(34);
    return Optional.of(List.of(c1, c2));
  }

  private VirtualSportDto getVirtualSports(String sportName, String title) {
    VirtualSportDto virtualSportDto = new VirtualSportDto();
    virtualSportDto.setTitle(sportName);
    VirtualSportTrackDto trackDto = new VirtualSportTrackDto();
    trackDto.setTitle(title);
    trackDto.setClassId("1234");
    virtualSportDto.setTracks(List.of(trackDto));
    return virtualSportDto;
  }

  private NextRaceFilterDto buildDto(String categoryId) {
    NextRaceFilterDto dto = new NextRaceFilterDto();
    dto.setExcludeTimeRange("{from={hh=0.0, mm=00, ss=00}, to={hh=0.0, mm=00, ss=00}}");
    Map<String, NextRacesClfDto> nextRaces = new HashMap<>();
    FeaturedNextRacesConfigProcessor.NextRacesConstants.TYPE_CODES.forEach(
        code -> updateMap(code, nextRaces));
    dto.setNextRaces(nextRaces);
    dto.setVirtualClassNames(Arrays.asList("Epsom", "Chase"));
    dto.setCategoryId(categoryId);
    return dto;
  }

  private void updateMap(String type, Map<String, NextRacesClfDto> nextRacesMap) {
    NextRacesClfDto clfDto = new NextRacesClfDto();
    clfDto.setLastEventTime(Instant.now());
    nextRacesMap.put(type, clfDto);
  }
}
