package com.ladbrokescoral.oxygen.cms.api.service;

import com.egalacoral.spark.siteserver.api.ExistsFilter;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.HighlightCarouselArchiveRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.HighlightCarouselArchive;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionModule;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionModuleType;
import com.ladbrokescoral.oxygen.cms.api.entity.HighlightCarousel;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.HighlightCarouselRepository;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import org.springframework.util.ObjectUtils;
import org.springframework.web.multipart.MultipartFile;

@Service
public class HighlightCarouselService extends AbstractSportSegmentService<HighlightCarousel> {
  private final HighlightCarouselRepository highlightCarouselRepository;
  private final SvgEntityService<HighlightCarousel> svgEntityService;
  private final String svgMenuPath;
  private final SiteServeApiProvider siteServeApiProvider;

  private ModelMapper modelMapper;
  private final CompetitionModuleService competitionModuleService;

  public HighlightCarouselService(
      HighlightCarouselRepository repository,
      HighlightCarouselArchiveRepository highlightCarouselArchiveRepository,
      SvgEntityService<HighlightCarousel> svgEntityService,
      @Value("${images.highlightscarousel.svg}") String svgMenuPath,
      SiteServeApiProvider siteServeApiProvider,
      EventHubService eventHubService,
      ModelMapper modelMapper,
      SegmentService segmentService,
      CompetitionModuleService competitionModuleService) {
    super(repository, highlightCarouselArchiveRepository, segmentService, eventHubService);
    this.highlightCarouselRepository = repository;
    this.svgEntityService = svgEntityService;
    this.svgMenuPath = svgMenuPath;
    this.siteServeApiProvider = siteServeApiProvider;
    this.modelMapper = modelMapper;
    this.competitionModuleService = competitionModuleService;
  }

  @Override
  public HighlightCarousel save(HighlightCarousel highlightCarousel) {
    if (!CollectionUtils.isEmpty(highlightCarousel.getEvents())) {
      if ((highlightCarousel.getTypeId() != null)
          || (!CollectionUtils.isEmpty(highlightCarousel.getTypeIds()))) {
        throw new IllegalArgumentException(
            "HighlightCarousel.typedId and HighlightCarousel.typedIds  must be null when HighlightCarousel.events is specified");
      }
      isUniqueEventIdsPerSegment(highlightCarousel);

      highlightCarousel.getEvents().stream()
          .filter(
              eventId ->
                  ObjectUtils.isEmpty(eventId)
                      || !siteServeApiProvider
                          .api(highlightCarousel.getBrand())
                          .getEvent(eventId, true)
                          .isPresent())
          .findFirst()
          .ifPresent(
              eventId -> {
                throw new IllegalArgumentException(
                    String.format(
                        "Cannot save Highlights Carousel since Event ID '%s' doesn't exist",
                        eventId));
              });
    } else if ((highlightCarousel.getTypeId() == null)
        && (CollectionUtils.isEmpty(highlightCarousel.getTypeIds()))) {
      throw new IllegalArgumentException(
          "Either HighlightCarousel.typedId or HighlightCarousel.typedIds or HighlightCarousel.events must be set");
    } else if ((highlightCarousel.getTypeId() != null)
        && (!CollectionUtils.isEmpty(highlightCarousel.getTypeIds()))) {
      throw new IllegalArgumentException(
          "Both HighlightCarousel.typedId and HighlightCarousel.typedIds must not be set at same time");
    } else if (isUniqueTypeIdPerSegment(highlightCarousel)) {
      throw new IllegalArgumentException(
          String.format(
              "Type ID: %s is already used for same period. Please amend your schedule.",
              highlightCarousel.getTypeId()));
    } else if (isTypeIdNotValid(highlightCarousel)) {
      throw new IllegalArgumentException(
          "Cannot save Highlights Carousel since Type ID/Type IDs doesn't exist");
    }
    return super.save(highlightCarousel);
  }
  // story BMA-62182

  private boolean isTypeIdNotValid(HighlightCarousel highlightCarousel) {
    if (highlightCarousel.getTypeId() != null) {
      return !siteServeApiProvider
          .api(highlightCarousel.getBrand())
          .getClassToSubTypeForType(
              String.valueOf(highlightCarousel.getTypeId()),
              new ExistsFilter.ExistsFilterBuilder().build())
          .filter(result -> !result.isEmpty())
          .isPresent();
    } else {
      return !siteServeApiProvider
          .api(highlightCarousel.getBrand())
          .getClassToSubTypeForType(
              highlightCarousel.getTypeIds(), new ExistsFilter.ExistsFilterBuilder().build())
          .filter(result -> !result.isEmpty())
          .isPresent();
    }
  }

  public List<HighlightCarousel> findAllByBrandAndPageId(
      String brand, PageType pageType, String pageId) {
    return highlightCarouselRepository.findByBrandAndPageTypeAndPageIdOrderBySortOrderAsc(
        brand, pageType, pageId);
  }

  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public HighlightCarousel attachSvgImage(String id, @ValidFileType("svg") MultipartFile file) {
    HighlightCarousel highlightCarousel = findOne(id).orElseThrow(NotFoundException::new);

    return svgEntityService
        .attachSvgImage(highlightCarousel, file, svgMenuPath)
        .map(highlightCarouselRepository::save)
        .orElseThrow(() -> new IllegalStateException("Couldn't upload an image"));
  }

  /**
   * @deprecated use SvgImages api to remove images and use update the menu endpoint to set the
   *     svgId to null delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public HighlightCarousel removeSvgImage(String id) {
    HighlightCarousel highlightCarousel = findOne(id).orElseThrow(NotFoundException::new);

    return svgEntityService
        .removeSvgImage(highlightCarousel)
        .map(highlightCarouselRepository::save)
        .orElseThrow(() -> new IllegalStateException("Couldn't remove an image"));
  }

  @Override
  public HighlightCarouselArchive prepareArchivalEntity(HighlightCarousel entity) {
    return modelMapper.map(entity, HighlightCarouselArchive.class);
  }

  @Override
  public void delete(String id) {
    HighlightCarousel highlightCarousel = findOne(id).orElseThrow(NotFoundException::new);
    HighlightCarouselArchive archive = prepareArchivalEntity(highlightCarousel);
    archive.setDeleted(true);
    super.saveArchivalEntity(archive);
    highlightCarouselRepository.delete(highlightCarousel);
    svgEntityService.removeSvgImage(highlightCarousel);
    removeHighLightCarouselIdsFromCompetitionModules(id);
  }

  public List<HighlightCarousel> findByBrandAndSegmentNameAndPageRef(
      String brand, String pageType, String pageId, String segmentName) {

    List<HighlightCarousel> records =
        SegmentConstants.UNIVERSAL.equalsIgnoreCase(segmentName)
            ? getUniversal(brand, PageType.valueOf(pageType), pageId)
            : getSegmentAndUniversal(brand, segmentName, PageType.valueOf(pageType), pageId);

    return records.stream().map(this::enhanceEntity).collect(Collectors.toList());
  }

  private List<HighlightCarousel> getUniversal(String brand, PageType pageType, String pageId) {

    return highlightCarouselRepository.findUniversalRecordsByBrandAndPageRef(
        brand, pageType, pageId, SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  private List<HighlightCarousel> getSegmentAndUniversal(
      String brand, String segmentName, PageType pageType, String pageId) {

    List<HighlightCarousel> recordsWithSegmentReference =
        super.sortByOrder(
            segmentName,
            highlightCarouselRepository.findAllByBrandAndSegmentNameAndPageRef(
                brand, Arrays.asList(segmentName), pageType, pageId));
    isUniversalSegmentChanged(recordsWithSegmentReference, segmentName);
    List<String> inclusiveListIds =
        recordsWithSegmentReference.stream()
            .map(HighlightCarousel::getId)
            .collect(Collectors.toList());
    List<HighlightCarousel> universalList =
        highlightCarouselRepository
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

  public void isUniqueEventIdsPerSegment(HighlightCarousel highlightCarousel) {
    if (!isHomePage(highlightCarousel)) return;
    highlightCarousel.getEvents().stream()
        .filter(eventId -> isUniqueEventIdPerSegment(highlightCarousel, eventId))
        .findFirst()
        .ifPresent(
            (String eventId) -> {
              throw new IllegalArgumentException(
                  String.format(
                      "Event IDs: %s are already used for same period. Please amend your schedule.",
                      eventId));
            });
  }

  public boolean isUniqueEventIdPerSegment(HighlightCarousel highlightCarousel, String eventId) {

    List<HighlightCarousel> highlightCarousels =
        highlightCarouselRepository.findByEventIdAndBrandAndPageTypeAndPageId(
            eventId, highlightCarousel.getBrand(), PageType.sport, "0");
    if (CollectionUtils.isEmpty(highlightCarousels)) return false;
    return highlightCarousels.stream()
        .filter(carousels -> !carousels.getId().equals(highlightCarousel.getId()))
        .anyMatch(hightlight -> isUniqueHc(hightlight, highlightCarousel));
  }

  public boolean isUniqueTypeIdPerSegment(HighlightCarousel highlightCarousel) {
    if (!isHomePage(highlightCarousel)) return false;
    List<HighlightCarousel> highlightCarousels =
        highlightCarouselRepository.findByTypeIdAndBrandAndPageTypeAndPageId(
            highlightCarousel.getTypeId(), highlightCarousel.getBrand(), PageType.sport, "0");
    if (CollectionUtils.isEmpty(highlightCarousels)) return false;
    return highlightCarousels.stream()
        .filter(carousels -> !carousels.getId().equals(highlightCarousel.getId()))
        .anyMatch(hightlight -> isUniqueHc(hightlight, highlightCarousel));
  }

  private boolean ismatchPeriod(
      HighlightCarousel exsistinghightlightCarousel, HighlightCarousel highlightCarousel) {

    return highlightCarousel.getDisplayFrom().isBefore(exsistinghightlightCarousel.getDisplayTo())
        && highlightCarousel.getDisplayTo().isAfter(exsistinghightlightCarousel.getDisplayFrom());
  }

  private Boolean isUniqueHc(
      HighlightCarousel exsistinghightlightCarousel, HighlightCarousel highlightCarousel) {
    boolean isPeriodMatched = ismatchPeriod(exsistinghightlightCarousel, highlightCarousel);
    if (!isPeriodMatched) return isPeriodMatched;
    List<String> segments =
        segmentService.getSegmentsForSegmentedViews(highlightCarousel.getBrand());
    List<String> newSegmentsViews = getSegmentView(highlightCarousel, segments);

    if (exsistinghightlightCarousel.isUniversalSegment()) {
      if (CollectionUtils.isEmpty(exsistinghightlightCarousel.getExclusionList())) return true;
      List<String> exsistingSegmentsViews = getSegmentView(exsistinghightlightCarousel, segments);
      return exsistingSegmentsViews.stream().anyMatch(newSegmentsViews::contains);

    } else {
      return exsistinghightlightCarousel.getInclusionList().stream()
          .anyMatch(newSegmentsViews::contains);
    }
  }

  private List<String> getSegmentView(HighlightCarousel highlightCarousel, List<String> segments) {
    if (highlightCarousel.isUniversalSegment()) {

      if (CollectionUtils.isEmpty(highlightCarousel.getExclusionList())) return segments;
      return segments
          .parallelStream()
          .filter(segment -> !highlightCarousel.getExclusionList().contains(segment))
          .collect(Collectors.toList());

    } else {

      return highlightCarousel.getInclusionList();
    }
  }

  private boolean isHomePage(HighlightCarousel highlightCarousel) {
    return PageType.sport == PageType.valueOf(highlightCarousel.getPageType().toString())
        && "0".equals(highlightCarousel.getPageId());
  }

  /* removing the highlightCarousel ids in competitionModules entity as well */
  private void removeHighLightCarouselIdsFromCompetitionModules(String id) {
    List<CompetitionModule> highlightModules =
        this.competitionModuleService.findCompetitionModulesByType(
            CompetitionModuleType.HIGHLIGHT_CAROUSEL);
    highlightModules.stream()
        .filter(competitionModule -> competitionModule.getHighlightCarousels().contains(id))
        .forEach(
            (CompetitionModule competitionModule) -> {
              competitionModule.getHighlightCarousels().remove(id);
              this.competitionModuleService.save(competitionModule);
            });
  }
}
