package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSport;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSportTrack;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSportTrackRef;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSportWithTracksRefs;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.mapping.VirtualSportWithTracksRefsMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.VirtualSportRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.VirtualSportTrackRepository;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import java.util.*;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import org.springframework.web.multipart.MultipartFile;

@Service
public class VirtualSportService extends SortableService<VirtualSport> {
  private final VirtualSportRepository virtualSportRepository;
  private final VirtualSportTrackRepository virtualSportTrackRepository;
  private final SvgEntityService<VirtualSport> svgEntityService;
  private final String svgMenuPath;

  public VirtualSportService(
      VirtualSportRepository repository,
      VirtualSportTrackRepository virtualSportTrackRepository,
      SvgEntityService<VirtualSport> svgEntityService,
      @Value("${images.virtualSport.svg}") String svgMenuPath) {
    super(repository);
    this.virtualSportRepository = repository;
    this.virtualSportTrackRepository = virtualSportTrackRepository;
    this.svgEntityService = svgEntityService;
    this.svgMenuPath = svgMenuPath;
  }

  @Override
  @SuppressWarnings("unchecked")
  public VirtualSport save(VirtualSport virtualSport) {
    return super.save(virtualSport);
  }

  @Override
  public VirtualSport update(VirtualSport existingEntity, VirtualSport updateEntity) {
    prepareModelBeforeUpdate(existingEntity, updateEntity);
    return save(updateEntity);
  }

  public VirtualSport prepareModelBeforeUpdate(
      VirtualSport existingEntity, VirtualSport updateEntity) {
    dropChildrenSilksIfTitleChanged(existingEntity, updateEntity);
    return updateEntity;
  }

  private void dropChildrenSilksIfTitleChanged(
      VirtualSport existingEntity, VirtualSport updateEntity) {
    if (!existingEntity.getTitle().equals(updateEntity.getTitle())) {
      Optional<List<VirtualSportTrack>> optionalTracks =
          Optional.ofNullable(
              virtualSportTrackRepository.findBySportIdOrderBySortOrderAsc(updateEntity.getId()));
      optionalTracks.ifPresent(
          tracks ->
              tracks.forEach(
                  (VirtualSportTrack track) -> {
                    if (!CollectionUtils.isEmpty(track.getRunnerImages())
                        || !CollectionUtils.isEmpty(track.getEventRunnerImages())) {
                      track.setRunnerImages(new ArrayList<>());
                      track.setEventRunnerImages(new HashMap<>());
                      track.setEventAliases(new HashMap<>());
                      track.setShowRunnerImages(false);

                      virtualSportTrackRepository.save(track);
                    }
                  }));
    }
  }

  public VirtualSport attachIcon(String id, @ValidFileType("svg") MultipartFile file) {
    VirtualSport virtualSport = findOne(id).orElseThrow(NotFoundException::new);

    return svgEntityService
        .attachSvgImage(virtualSport, file, svgMenuPath)
        .map(virtualSportRepository::save)
        .orElseThrow(() -> new IllegalStateException("Couldn't upload an svg"));
  }

  public VirtualSport removeIcon(String id) {
    VirtualSport virtualSport = findOne(id).orElseThrow(NotFoundException::new);

    return svgEntityService
        .removeSvgImage(virtualSport)
        .map(virtualSportRepository::save)
        .orElseThrow(() -> new IllegalStateException("Couldn't remove an svg"));
  }

  @Override
  public void delete(String id) {
    VirtualSport virtualSport = findOne(id).orElseThrow(NotFoundException::new);

    virtualSportRepository.delete(virtualSport);
    svgEntityService.removeSvgImage(virtualSport);
  }

  public List<VirtualSportWithTracksRefs> findSportsWithTracksRefsByBrand(String brand) {
    return super.findByBrand(brand).stream()
        .map(VirtualSportWithTracksRefsMapper.getInstance()::withTrackRefs)
        .map(
            sport ->
                sport.setTracksRefs(
                    virtualSportTrackRepository.findBySportIdOrderBySortOrderAsc(sport.getId())
                        .stream()
                        .map(track -> new VirtualSportTrackRef(track.getId(), track.getTitle()))
                        .collect(Collectors.toList())))
        .collect(Collectors.toList());
  }
}
