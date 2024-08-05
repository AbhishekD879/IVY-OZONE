package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSport;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSportTrack;
import com.ladbrokescoral.oxygen.cms.api.dto.VirtualSportAliasesDto;
import com.ladbrokescoral.oxygen.cms.api.dto.VirtualSportDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.VirtualSportMapper;
import com.ladbrokescoral.oxygen.cms.api.mapping.VirtualSportTrackMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.VirtualSportRepository;
import com.ladbrokescoral.oxygen.cms.api.service.VirtualSportTrackService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Service;

@Service
public class VirtualSportPublicService {
  private final VirtualSportRepository virtualSportRepository;
  private final VirtualSportTrackService virtualSportTrackService;

  public VirtualSportPublicService(
      VirtualSportRepository virtualSportRepository,
      @Lazy VirtualSportTrackService virtualSportTrackService) {
    this.virtualSportRepository = virtualSportRepository;
    this.virtualSportTrackService = virtualSportTrackService;
  }

  public List<VirtualSportDto> findActiveSportsWithActiveTracksOnly(String brand) {
    List<VirtualSport> activeSports =
        virtualSportRepository.findByBrandAndActiveIsTrueOrderBySortOrderAsc(brand);

    return activeSports.stream()
        .map(VirtualSportMapper.getInstance()::toDto)
        .map(
            activeSport ->
                activeSport.setTracks(
                    virtualSportTrackService.findActiveTracksBySportId(activeSport.getId()).stream()
                        .filter(VirtualSportTrack::isActive)
                        .map(VirtualSportTrackMapper.getInstance()::toDto)
                        .collect(Collectors.toList())))
        .collect(Collectors.toList());
  }

  public List<VirtualSportAliasesDto> findAliases(String brand) {
    return findActiveSportsWithActiveTracksOnly(brand).stream()
        .flatMap(
            sport ->
                sport.getTracks().stream()
                    .map(
                        track ->
                            new VirtualSportAliasesDto()
                                .setClassId(track.getClassId())
                                .setParent(virtualSportTrackService.formatAsAlias(sport.getTitle()))
                                .setChild(virtualSportTrackService.formatAsAlias(track.getTitle()))
                                .setEvents(track.getEventAliases())))
        .collect(Collectors.toList());
  }
}
