package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportQuickLinkArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.SportQuickLinkArchive;
import com.ladbrokescoral.oxygen.cms.api.dto.AutomaticUpdateDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportQuickLink;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfiguration;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.mapping.SystemConfigurationMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.SportQuickLinkRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SystemConfigurationRepository;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import java.time.Instant;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import org.springframework.web.multipart.MultipartFile;

@Service
public class SportQuickLinkService extends AbstractSportSegmentService<SportQuickLink> {
  private static final String PREFIX = "QL:";
  public static final int DEFAULT_MAX_SIZE = 5;
  private SvgEntityService<SportQuickLink> svgEntityService;
  private SportQuickLinkRepository sportQuickLinkRepository;
  private String svgMenuPath;
  private ModelMapper modelMapper;
  private SystemConfigurationRepository systemConfigurationRepository;

  private AutomaticUpdateService automaticUpdateService;

  @Autowired
  public SportQuickLinkService(
      SportQuickLinkRepository sportQuickLinkRepository,
      SvgEntityService<SportQuickLink> imageEntityService,
      @Value("${images.sportquicklinks.svg}") String svgMenuPath,
      EventHubService hubService,
      SportQuickLinkArchivalRepository sportQuickLinkArchivalRepository,
      ModelMapper modelMapper,
      SegmentService segmentService,
      SystemConfigurationRepository systemConfigurationRepository,
      AutomaticUpdateService automaticUpdateService) {
    super(sportQuickLinkRepository, sportQuickLinkArchivalRepository, segmentService, hubService);
    this.sportQuickLinkRepository = sportQuickLinkRepository;
    this.svgEntityService = imageEntityService;
    this.svgMenuPath = svgMenuPath;
    this.modelMapper = modelMapper;
    this.systemConfigurationRepository = systemConfigurationRepository;
    this.automaticUpdateService = automaticUpdateService;
  }

  public List<SportQuickLink> findAllByBrandAndPageTypeAndPageId(
      String brand, PageType pageType, String pageId) {
    return sportQuickLinkRepository.findAllByBrandAndPageTypeAndPageIdOrderBySortOrderAsc(
        brand, pageType, pageId);
  }

  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public Optional<SportQuickLink> attachSvgImage(
      SportQuickLink menu, @ValidFileType("svg") MultipartFile file) {
    return svgEntityService.attachSvgImage(menu, file, svgMenuPath);
  }

  /**
   * @deprecated use SvgImages api to remove images and use update the menu endpoint to set the
   *     svgId to null delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public Optional<SportQuickLink> removeSvgImage(SportQuickLink menu) {
    return svgEntityService.removeSvgImage(menu);
  }

  @Override
  public SportQuickLink save(SportQuickLink sportQuickLink) {

    if ("0".equals(sportQuickLink.getPageId()) && !sportQuickLink.isDisabled())
      isEligibleTocreate(sportQuickLink);

    return super.save(sportQuickLink);
  }

  /*
   * step 1. Get the segments in the system : List<String> allSegments
   * step 2. Prepare the segments which are having >= system config - empty retun true
   *  case 1: Universal (with no excl) : step 2 is not empty then fail. return step 2 list.
   * Case 2: Universal (with excl) : from step 1 list  remove these excl
   * segments. subsetOfAllSegments and from step 2 list  intersection - send the
   * error with intersection
   *  Case 3: Inclusive : List<String> inclusiceList. step
   * 2 list and inclusiceList intersection - send the error with intersection
   */
  private void isEligibleTocreate(SportQuickLink sportQuickLink) {

    Long macConfig = getMaxConfigurationValue(sportQuickLink);

    Map<String, Long> segmentCounts = getGroupBySegments(sportQuickLink);

    Set<String> notEligibleSegments =
        segmentCounts.entrySet().stream()
            .parallel()
            .filter(entry -> entry.getValue() >= macConfig)
            .map(Map.Entry::getKey)
            .collect(Collectors.toSet());
    Set<String> resultednotEligiblesegments = new HashSet<>();

    if (!sportQuickLink.isUniversalSegment()) {
      resultednotEligiblesegments =
          sportQuickLink.getInclusionList().stream()
              .parallel()
              .filter(notEligibleSegments::contains)
              .collect(Collectors.toSet());

    } else if (!CollectionUtils.isEmpty(sportQuickLink.getExclusionList())) {
      resultednotEligiblesegments =
          segmentCounts.keySet().stream()
              .parallel()
              .filter(
                  seg ->
                      !sportQuickLink.getExclusionList().contains(seg)
                          && notEligibleSegments.contains(seg))
              .collect(Collectors.toSet());

    } else {
      resultednotEligiblesegments.addAll(notEligibleSegments);
    }

    if (!CollectionUtils.isEmpty(resultednotEligiblesegments))
      throw new ValidationException(
          macConfig
              + " Quick Links are already scheduled for this period for segment(s) with "
              + String.join(", ", resultednotEligiblesegments)
              + ". Please amend your schedule for segment(s)");
  }

  // find all quickQuicks with active ,validate Ddate and brand Criteria.then
  // group
  // by segmentname then get count based on the segmentname

  private Map<String, Long> getGroupBySegments(SportQuickLink sportQuickLink) {
    List<SportQuickLink> sportQuickLinks =
        sportQuickLinkRepository
            .findAllActiveAndvalidityPeriodStartIsAfterAndvalidityPeriodEndIsBefore(
                sportQuickLink.getId(), Instant.now(), sportQuickLink.getBrand());

    List<List<String>> sportQuickLinkDtos =
        enhanceToDtoWithSegments(sportQuickLink.getBrand(), sportQuickLinks);

    Map<String, Long> segmetConfigMap =
        sportQuickLinkDtos.stream()
            .parallel()
            .flatMap(Collection::stream)
            .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));

    if (!sportQuickLink.isUniversalSegment()) {
      List<String> newSegments =
          sportQuickLink.getInclusionList().stream()
              .parallel()
              .filter((String segment) -> !segmetConfigMap.containsKey(segment))
              .collect(Collectors.toList());
      newSegments.stream()
          .forEach(
              (String segment) ->
                  segmetConfigMap.put(
                      segment,
                      segmetConfigMap.get(SegmentConstants.UNIVERSAL) != null
                          ? segmetConfigMap.get(SegmentConstants.UNIVERSAL)
                          : 0));
    }

    return segmetConfigMap;
  }

  private List<List<String>> enhanceToDtoWithSegments(String brand, List<SportQuickLink> links) {
    List<String> segments = segmentService.getSegmentsForSegmentedViews(brand);
    // segment service filtered universal segments. Universal segment won't come...
    segments.add(SegmentConstants.UNIVERSAL);

    return links.stream().map(ql -> getSegments(ql, segments)).collect(Collectors.toList());
  }

  private List<String> getSegments(SportQuickLink sportQuickLink, List<String> segments) {
    if (sportQuickLink.isUniversalSegment()) {
      if (!CollectionUtils.isEmpty(sportQuickLink.getExclusionList())) {
        return segments.stream()
            .filter(seg -> !sportQuickLink.getExclusionList().contains(seg))
            .collect(Collectors.toList());
      }
      return segments;
    } else {
      return sportQuickLink.getInclusionList();
    }
  }

  private Long getMaxConfigurationValue(SportQuickLink sportQuickLink) {

    Optional<SystemConfiguration> segconfig =
        systemConfigurationRepository.findOneByBrandAndName(
            sportQuickLink.getBrand(), "Sport Quick Links");

    Optional<Object> maxObject =
        segconfig
            .map(c -> SystemConfigurationMapper.INSTANCE.getStructureProperties(c.getProperties()))
            .map(config -> config.get("maxAmount"));

    return maxObject.isPresent() ? Long.valueOf(maxObject.get().toString()) : DEFAULT_MAX_SIZE;
  }

  @Override
  public SportQuickLinkArchive prepareArchivalEntity(SportQuickLink entity) {
    return modelMapper.map(entity, SportQuickLinkArchive.class);
  }

  @Override
  public void delete(String id) {
    Optional<SportQuickLink> point = findOne(id);
    if (point.isPresent()) {
      SportQuickLinkArchive archive = prepareArchivalEntity(point.get());
      archive.setDeleted(true);
      super.saveArchivalEntity(archive);
      super.delete(id);
    }
  }

  public List<SportQuickLink> findByBrandAndSegmentNameAndPageRef(
      String brand, String pageType, String pageId, String segmentName) {

    List<SportQuickLink> records =
        SegmentConstants.UNIVERSAL.equalsIgnoreCase(segmentName)
            ? getUniversal(brand, PageType.valueOf(pageType), pageId)
            : getSegmentAndUniversal(brand, segmentName, PageType.valueOf(pageType), pageId);

    return records.stream().map(this::enhanceEntity).collect(Collectors.toList());
  }

  private List<SportQuickLink> getUniversal(String brand, PageType pageType, String pageId) {

    return sportQuickLinkRepository.findUniversalRecordsByBrandAndPageRef(
        brand, pageType, pageId, SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  private List<SportQuickLink> getSegmentAndUniversal(
      String brand, String segmentName, PageType pageType, String pageId) {

    List<SportQuickLink> recordsWithSegmentReference =
        super.sortByOrder(
            segmentName,
            sportQuickLinkRepository.findAllByBrandAndSegmentNameAndPageRef(
                brand, Arrays.asList(segmentName), pageType, pageId));
    List<String> inclusiveListIds =
        recordsWithSegmentReference.stream()
            .map(SportQuickLink::getId)
            .collect(Collectors.toList());
    isUniversalSegmentChanged(recordsWithSegmentReference, segmentName);
    List<SportQuickLink> universalList =
        sportQuickLinkRepository
            .findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
                brand,
                Arrays.asList(segmentName),
                inclusiveListIds,
                pageType,
                pageId,
                SortableService.SORT_BY_SORT_ORDER_ASC);
    recordsWithSegmentReference.addAll(universalList);
    return recordsWithSegmentReference;
  }

  @Override
  public SportQuickLink update(SportQuickLink existingEntity, SportQuickLink updateEntity) {
    if (!updateEntity.getTitle().equalsIgnoreCase(existingEntity.getTitle())) {
      AutomaticUpdateDto automaticUpdateDto = new AutomaticUpdateDto();
      automaticUpdateDto.setId(updateEntity.getId());
      automaticUpdateDto.setBrand(updateEntity.getBrand());
      automaticUpdateDto.setUpdatedTitle(PREFIX + updateEntity.getTitle());
      this.automaticUpdateService.doUpdate(automaticUpdateDto);
    }
    return super.update(existingEntity, updateEntity);
  }
}
