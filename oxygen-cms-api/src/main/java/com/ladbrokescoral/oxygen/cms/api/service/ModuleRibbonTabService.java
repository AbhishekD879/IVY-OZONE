package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.ModuleRibbonTabArchiveRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.ModuleRibbonTabArchive;
import com.ladbrokescoral.oxygen.cms.api.entity.ModuleRibbonTab;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.repository.ModuleRibbonTabRepository;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Component;

@Component
public class ModuleRibbonTabService extends AbstractSegmentService<ModuleRibbonTab> {

  private ModelMapper modelMapper;
  private final ModuleRibbonTabRepository moduleRibbonTabRepository;

  @Autowired
  public ModuleRibbonTabService(
      ModuleRibbonTabRepository repository,
      ModuleRibbonTabArchiveRepository moduleRibbonTabArchivalRepository,
      ModelMapper modelMapper,
      SegmentService segmentService) {
    super(repository, moduleRibbonTabArchivalRepository, segmentService);
    this.modelMapper = modelMapper;
    this.moduleRibbonTabRepository = repository;
  }

  public List<ModuleRibbonTab> findAllByBrandAndVisible(String brand) {
    return moduleRibbonTabRepository.findAllByBrandAndVisibleOrderBySortOrderAsc(brand, true);
  }

  @Override
  public ModuleRibbonTab prepareModelBeforeSave(ModuleRibbonTab moduleRibbonTab) {
    moduleRibbonTab.setTitle_brand(generateTitleBrand(moduleRibbonTab));
    return moduleRibbonTab;
  }

  private String generateTitleBrand(ModuleRibbonTab moduleRibbonTab) {
    return new StringBuilder(moduleRibbonTab.getTitle().toLowerCase())
        .append("-")
        .append(moduleRibbonTab.getBrand())
        .toString();
  }

  @Override
  public ModuleRibbonTabArchive prepareArchivalEntity(ModuleRibbonTab entity) {
    return modelMapper.map(entity, ModuleRibbonTabArchive.class);
  }

  @Override
  public void delete(String id) {
    Optional<ModuleRibbonTab> point = findOne(id);
    if (point.isPresent()) {
      ModuleRibbonTabArchive archive = prepareArchivalEntity(point.get());
      archive.setDeleted(true);
      super.saveArchivalEntity(archive);
      super.delete(id);
    }
  }

  public List<ModuleRibbonTab> findAllUniversalModuleRibbonTabs() {
    return moduleRibbonTabRepository.findAllByUniversalSegment();
  }

  public List<ModuleRibbonTab> findAllSegmentedByBrandAndVisible(String brand, String segmentName) {

    return SegmentConstants.UNIVERSAL.equalsIgnoreCase(segmentName)
        ? moduleRibbonTabRepository.findAllUniversalByBrandAndVisibleOrderBySortOrderAsc(
            brand, true, Sort.by(Sort.Direction.ASC, "sortOrder"))
        : findAllSegmentAndUniversalByBrandAndVisible(brand, true, segmentName);
  }

  private List<ModuleRibbonTab> findAllSegmentAndUniversalByBrandAndVisible(
      String brand, boolean active, String segmentName) {
    List<ModuleRibbonTab> recordsWithSegmentReference =
        moduleRibbonTabRepository.findAllByBrandAndSegmentName(
            brand, active, Arrays.asList(segmentName));
    recordsWithSegmentReference = super.sortByOrder(segmentName, recordsWithSegmentReference);

    List<String> inclusiveListIds =
        recordsWithSegmentReference.stream()
            .map(ModuleRibbonTab::getId)
            .collect(Collectors.toList());
    List<ModuleRibbonTab> universalList =
        moduleRibbonTabRepository
            .findByBrandAndDeviceTypeAndIsVisableAndApplyUniversalSegmentsAndNotInExclusionListAndInInclusiveList(
                brand,
                Arrays.asList(segmentName),
                inclusiveListIds,
                active,
                SortableService.SORT_BY_SORT_ORDER_ASC);

    recordsWithSegmentReference.addAll(universalList);
    return recordsWithSegmentReference;
  }

  @Override
  public List<ModuleRibbonTab> findByBrand(String brand) {

    return moduleRibbonTabRepository.findUniversalRecordAndInclusiveNotNullAndBrand(
        brand, SORT_BY_SORT_ORDER_ASC);
  }

  public boolean existsByBrandAndBybVisbleTrue(String brand) {
    return moduleRibbonTabRepository.existsByBrandAndDirectiveNameAndBybVisbleTrue(
        brand, "BuildYourBet");
  }
}
