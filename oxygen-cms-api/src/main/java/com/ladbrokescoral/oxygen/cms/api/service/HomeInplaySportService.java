package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportModuleArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.SportModuleArchive;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeInplaySport;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.repository.HomeInplaySportRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportModuleRepository;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Service
public class HomeInplaySportService extends AbstractSegmentService<HomeInplaySport> {

  private ModelMapper modelMapper;
  private SportModuleRepository sportModuleRepository;
  private SportModuleArchivalRepository sportModuleArchivalRepository;

  @Autowired
  public HomeInplaySportService(
      HomeInplaySportRepository homeInplaySportRepository,
      SportModuleRepository sportModuleRepository,
      SportModuleArchivalRepository sportModuleArchivalRepository,
      ModelMapper modelMapper,
      SegmentService segmentService) {
    super(homeInplaySportRepository, null, segmentService);
    this.modelMapper = modelMapper;
    this.sportModuleRepository = sportModuleRepository;
    this.sportModuleArchivalRepository = sportModuleArchivalRepository;
  }

  @Override
  public void delete(String id) {
    Optional<HomeInplaySport> point = findOne(id);
    if (!point.isPresent()) return;
    super.delete(id);
    updateArchival(point.get().getBrand());
  }

  @Override
  public HomeInplaySport save(HomeInplaySport entity) {
    updateArchivalId(entity);
    updateSegmentReferences(entity);
    entity = saveEntity(entity);
    updateSegments(entity);
    updateArchival(entity.getBrand());
    return entity;
  }

  private void updateArchival(String brand) {
    Optional<SportModule> module =
        sportModuleRepository.findAllByBrandAndPageTypeAndPageIdAndModuleType(
            brand, PageType.sport, "0", SportModuleType.INPLAY);
    if (module.isPresent()) {
      SportModuleArchive sportModuleArchive =
          modelMapper.map(module.get(), SportModuleArchive.class);
      if (module.get().getInplayConfig() != null) {

        sportModuleArchive.setId(null);
        List<HomeInplaySport> homeInplaySports =
            findByBrand(brand).stream()
                .parallel()
                .filter(
                    inplay ->
                        inplay.isUniversalSegment()
                            || !CollectionUtils.isEmpty(inplay.getInclusionList()))
                .collect(Collectors.toList());
        sportModuleArchive.getInplayConfig().setHomeInplaySports(homeInplaySports);
      }
      sportModuleArchivalRepository.save(sportModuleArchive);
    }
  }

  @Override
  public void saveAndUpdateArchivals(Iterable<HomeInplaySport> list) {
    list.forEach(this::updateArchivalId);
    List<HomeInplaySport> entities = super.save(list);
    updateArchival(entities.get(0).getBrand());
  }

  @Override
  public <S extends HomeInplaySport> S prepareArchivalEntity(HomeInplaySport entity) {

    return null;
  }
}
