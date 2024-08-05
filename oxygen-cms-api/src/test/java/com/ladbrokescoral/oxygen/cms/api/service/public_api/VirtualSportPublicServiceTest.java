package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.AdditionalAnswers.returnsFirstArg;

import com.google.common.collect.ImmutableMap;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSport;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSportTrack;
import com.ladbrokescoral.oxygen.cms.api.dto.VirtualSportAliasesDto;
import com.ladbrokescoral.oxygen.cms.api.dto.VirtualSportDto;
import com.ladbrokescoral.oxygen.cms.api.dto.VirtualSportTrackDto;
import com.ladbrokescoral.oxygen.cms.api.repository.VirtualSportRepository;
import com.ladbrokescoral.oxygen.cms.api.service.VirtualSportTrackService;
import java.util.Arrays;
import java.util.Collections;
import java.util.UUID;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class VirtualSportPublicServiceTest extends BDDMockito {

  private final String brand = "test-brand";

  @Mock private VirtualSportRepository virtualSportRepository;

  @Mock private VirtualSportTrackService virtualSportTrackService;

  @InjectMocks private VirtualSportPublicService virtualSportPublicService;

  @Before
  public void setUp() {
    when(virtualSportTrackService.formatAsAlias(any())).thenAnswer(returnsFirstArg());
  }

  @Test
  public void testNoActiveSports() {
    VirtualSport virtualSport = new VirtualSport();
    virtualSport.setActive(false);
    virtualSport.setId(UUID.randomUUID().toString());

    when(virtualSportRepository.findByBrandAndActiveIsTrueOrderBySortOrderAsc(any()))
        .thenReturn(Collections.emptyList());

    assertThat(virtualSportPublicService.findActiveSportsWithActiveTracksOnly(brand)).isEmpty();
  }

  @Test
  public void testNoActiveTracks() {
    VirtualSport virtualSport = new VirtualSport();
    virtualSport.setActive(true);
    virtualSport.setId(UUID.randomUUID().toString());

    when(virtualSportRepository.findByBrandAndActiveIsTrueOrderBySortOrderAsc(any()))
        .thenReturn(Collections.singletonList(virtualSport));
    when(virtualSportTrackService.findActiveTracksBySportId(any()))
        .thenReturn(
            Arrays.asList(
                new VirtualSportTrack().setActive(false).setSportId(virtualSport.getId()),
                new VirtualSportTrack().setActive(false).setSportId(virtualSport.getId())));

    assertThat(virtualSportPublicService.findActiveSportsWithActiveTracksOnly(brand)).isNotEmpty();
  }

  @Test
  public void testInactiveTrackFiltering() {
    VirtualSport virtualSport = new VirtualSport();
    virtualSport.setActive(true);
    virtualSport.setId(UUID.randomUUID().toString());

    VirtualSportTrack activeTrack =
        new VirtualSportTrack().setActive(true).setSportId(virtualSport.getId());
    activeTrack.setId(UUID.randomUUID().toString());
    VirtualSportTrack inactiveTrack =
        new VirtualSportTrack().setActive(false).setSportId(virtualSport.getId());
    inactiveTrack.setId(UUID.randomUUID().toString());

    when(virtualSportTrackService.findActiveTracksBySportId(any()))
        .thenReturn(Arrays.asList(inactiveTrack, activeTrack));
    when(virtualSportRepository.findByBrandAndActiveIsTrueOrderBySortOrderAsc(any()))
        .thenReturn(Collections.singletonList(virtualSport));

    assertThat(virtualSportPublicService.findActiveSportsWithActiveTracksOnly(brand))
        .isNotEmpty()
        .flatExtracting(VirtualSportDto::getTracks)
        .extracting(VirtualSportTrackDto::getId)
        .containsExactly(activeTrack.getId());
  }

  @Test
  public void testAllActive() {
    VirtualSport virtualSport = new VirtualSport();
    virtualSport.setActive(true);
    virtualSport.setId(UUID.randomUUID().toString());

    VirtualSportTrack firstActiveTrack =
        new VirtualSportTrack().setActive(true).setSportId(virtualSport.getId());
    firstActiveTrack.setId(UUID.randomUUID().toString());
    VirtualSportTrack secondActiveTrack =
        new VirtualSportTrack().setActive(true).setSportId(virtualSport.getId());
    secondActiveTrack.setId(UUID.randomUUID().toString());

    when(virtualSportTrackService.findActiveTracksBySportId(any()))
        .thenReturn(Arrays.asList(secondActiveTrack, firstActiveTrack));
    when(virtualSportRepository.findByBrandAndActiveIsTrueOrderBySortOrderAsc(any()))
        .thenReturn(Collections.singletonList(virtualSport));

    assertThat(virtualSportPublicService.findActiveSportsWithActiveTracksOnly(brand))
        .isNotEmpty()
        .flatExtracting(VirtualSportDto::getTracks)
        .extracting(VirtualSportTrackDto::getId)
        .containsOnly(firstActiveTrack.getId(), secondActiveTrack.getId());
  }

  @Test
  public void findAliasesNoneEmptyEvents() {
    VirtualSport virtualSport = new VirtualSport();
    virtualSport.setActive(true);
    virtualSport.setTitle("test-sport");
    virtualSport.setId(UUID.randomUUID().toString());

    VirtualSportTrack firstActiveTrack =
        new VirtualSportTrack()
            .setActive(true)
            .setSportId(virtualSport.getId())
            .setTitle("first")
            .setClassId("firstClass")
            .setEventAliases(ImmutableMap.of("firstAlias", "first-path"));
    firstActiveTrack.setId(UUID.randomUUID().toString());

    VirtualSportTrack secondActiveTrack =
        new VirtualSportTrack()
            .setActive(true)
            .setSportId(virtualSport.getId())
            .setTitle("second")
            .setClassId("secondClass")
            .setEventAliases(ImmutableMap.of("secondAlias", "second-path"));
    secondActiveTrack.setId(UUID.randomUUID().toString());

    when(virtualSportTrackService.findActiveTracksBySportId(any()))
        .thenReturn(Arrays.asList(secondActiveTrack, firstActiveTrack));
    when(virtualSportRepository.findByBrandAndActiveIsTrueOrderBySortOrderAsc(any()))
        .thenReturn(Collections.singletonList(virtualSport));

    assertThat(virtualSportPublicService.findAliases(brand))
        .isNotEmpty()
        .containsOnly(
            new VirtualSportAliasesDto()
                .setClassId("firstClass")
                .setEvents(ImmutableMap.of("firstAlias", "first-path"))
                .setParent("test-sport")
                .setChild("first"),
            new VirtualSportAliasesDto()
                .setClassId("secondClass")
                .setEvents(ImmutableMap.of("secondAlias", "second-path"))
                .setParent("test-sport")
                .setChild("second"));
  }

  @Test
  public void findAliasesShouldFilterOutEmptyEventAliases() {
    VirtualSport virtualSport = new VirtualSport();
    virtualSport.setActive(true);
    virtualSport.setTitle("test-sport");
    virtualSport.setId(UUID.randomUUID().toString());

    VirtualSportTrack firstActiveTrack =
        new VirtualSportTrack()
            .setActive(true)
            .setSportId(virtualSport.getId())
            .setTitle("first")
            .setClassId("firstClass");
    firstActiveTrack.setId(UUID.randomUUID().toString());

    VirtualSportTrack secondActiveTrack =
        new VirtualSportTrack()
            .setActive(true)
            .setSportId(virtualSport.getId())
            .setTitle("second")
            .setClassId("secondClass")
            .setEventAliases(ImmutableMap.of("secondAlias", "second-path"));
    secondActiveTrack.setId(UUID.randomUUID().toString());

    when(virtualSportTrackService.findActiveTracksBySportId(any()))
        .thenReturn(Arrays.asList(secondActiveTrack, firstActiveTrack));
    when(virtualSportRepository.findByBrandAndActiveIsTrueOrderBySortOrderAsc(any()))
        .thenReturn(Collections.singletonList(virtualSport));

    assertThat(virtualSportPublicService.findAliases(brand))
        .isNotEmpty()
        .containsOnly(
            new VirtualSportAliasesDto()
                .setClassId("firstClass")
                .setEvents(null)
                .setParent("test-sport")
                .setChild("first"),
            new VirtualSportAliasesDto()
                .setClassId("secondClass")
                .setEvents(ImmutableMap.of("secondAlias", "second-path"))
                .setParent("test-sport")
                .setChild("second"));
  }
}
