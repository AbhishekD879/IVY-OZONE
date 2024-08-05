package com.ladbrokescoral.oxygen.cms.api.service;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SurfaceBetArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.SurfaceBetArchive;
import com.ladbrokescoral.oxygen.cms.api.dto.ActiveSurfaceBetDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.SurfaceBetRepository;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import java.time.Instant;
import java.util.*;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import org.bson.types.ObjectId;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

@Service
public class SurfaceBetService extends AbstractSportSegmentService<SurfaceBet> {

  public static final String UNI_SEG_REF = "UNI_SEG_REF";
  public static final String UNI_NO_SEG_REF = "UNI_NO_SEG_REF";
  private final SurfaceBetRepository surfaceBetRepository;
  private final SvgEntityService<SurfaceBet> svgEntityService;
  private final String svgMenuPath;
  private final SiteServeApiProvider siteServeApiProvider;
  private ModelMapper modelMapper;
  public static final Sort SORT_BY_CREATED_AT_ASC = Sort.by("createdAt");
  private final CompetitionModuleService competitionModuleService;

  private final SportPagesOrderingService sportPagesOrderingService;

  private final SurfaceBetTitleService titleService;

  public SurfaceBetService(
      SurfaceBetRepository surfaceBetRepository,
      SvgEntityService<SurfaceBet> svgEntityService,
      @Value("${images.surfacebet.svg}") String svgMenuPath,
      SiteServeApiProvider siteServeApiProvider,
      SurfaceBetArchivalRepository surfaceBetArchivalRepository,
      SegmentService segmentService,
      ModelMapper modelMapper,
      CompetitionModuleService competitionModuleService,
      SportPagesOrderingService sportPagesOrderingService,
      SurfaceBetTitleService titleService) {
    super(surfaceBetRepository, surfaceBetArchivalRepository, segmentService, null);
    this.surfaceBetRepository = surfaceBetRepository;
    this.svgEntityService = svgEntityService;
    this.svgMenuPath = svgMenuPath;
    this.siteServeApiProvider = siteServeApiProvider;
    this.modelMapper = modelMapper;
    this.competitionModuleService = competitionModuleService;
    this.sportPagesOrderingService = sportPagesOrderingService;
    this.titleService = titleService;
  }

  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public SurfaceBet attachSvgImage(String id, @ValidFileType("svg") MultipartFile file) {
    SurfaceBet surfaceBet = findOne(id).orElseThrow(NotFoundException::new);
    return svgEntityService
        .attachSvgImage(surfaceBet, file, svgMenuPath)
        .map(surfaceBetRepository::save)
        .orElseThrow(() -> new IllegalStateException("Couldn't upload an image"));
  }

  /**
   * @deprecated use SvgImages api to remove images delete after release-103.0.0 goes live (check
   *     with ui)
   */
  @Deprecated
  public SurfaceBet removeSvgImage(String id) {
    SurfaceBet surfaceBet = findOne(id).orElseThrow(NotFoundException::new);
    return svgEntityService
        .removeSvgImage(surfaceBet)
        .map(surfaceBetRepository::save)
        .orElseThrow(() -> new IllegalStateException("Couldn't remove an image"));
  }

  // delete  By setting archivalId and references if null
  @Override
  public void delete(String id) {
    SurfaceBet surfaceBet = findOne(id).orElseThrow(NotFoundException::new);

    surfaceBetRepository.delete(surfaceBet);
    svgEntityService.removeSvgImage(surfaceBet);
    SurfaceBetArchive surfaceBetArchive = prepareArchivalEntity(surfaceBet);
    surfaceBetArchive.getReferences().forEach(this::setIdIfNotFind);
    surfaceBetArchive.setDeleted(true);
    super.saveArchivalEntity(surfaceBetArchive);
    removeIdsFromCompetitionModules(id);
  }

  @Override
  public SurfaceBet save(SurfaceBet surfaceBet) {
    final List<String> prune = new ArrayList<>();
    prune.add("event");
    prune.add("market");
    Optional<List<Event>> events =
        siteServeApiProvider
            .api(surfaceBet.getBrand())
            .getEventToOutcomeForOutcome(
                Arrays.asList(String.valueOf(surfaceBet.getSelectionId())),
                (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build(),
                prune);
    if (!events.isPresent()) {
      throw new IllegalArgumentException(
          String.format(
              "Cannot save SurfaceBet since Selection ID '%s' doesn't exist'",
              surfaceBet.getSelectionId()));
    }

    isUniqueSelectionIdPerSegment(surfaceBet)
        .ifPresent(
            (SurfaceBet resurfaceBet) -> {
              throw new IllegalArgumentException(
                  String.format(
                      "This selection ID is already used in: %s", resurfaceBet.getTitle()));
            });
    updateReferences(surfaceBet);
    sportPagesOrderingService.incrementSortOrderForSportPages(surfaceBet);
    surfaceBet = saveEntity(surfaceBet);
    prepareAndSaveArchivalEntity(surfaceBet);

    return surfaceBet;
  }

  private void updateReferences(SurfaceBet surfaceBet) {
    // remove Relation data from references when it is Segmented Record.as segmention is applicable
    // for home page.removing references other than RefId 0
    // remove segment references which doesn't have reference id.and -1
    removeDeletedRelationData(surfaceBet);
    if (!StringUtils.hasText(surfaceBet.getArchivalId())) {
      surfaceBet.setArchivalId(ObjectId.get().toHexString());
    }
    surfaceBet.getReferences().forEach(this::setIdIfNotFind);
    Optional<Relation> relationOptional =
        surfaceBet.getReferences().stream()
            .filter(x -> RelationType.sport == x.getRelatedTo() && "0".equals(x.getRefId()))
            .findFirst();

    updateSegmentReferencesAndPageReference(surfaceBet, relationOptional);
    updateSegments(surfaceBet);
  }

  private void setIdIfNotFind(Relation relation) {
    if (!StringUtils.hasText(relation.getId())) {
      relation.setId(ObjectId.get().toHexString());
    }
  }

  public List<SurfaceBet> findAllForBrandByPage(String brand, String relatedTo, String refId) {
    return surfaceBetRepository.findByBrand(brand).stream()
        .filter(sb -> hasOnPage(RelationType.valueOf(relatedTo), refId, sb.getReferences()))
        .collect(Collectors.toList());
  }

  private void removeDeletedRelationData(SurfaceBet surfaceBet) {
    List<String> relationIds =
        surfaceBet.getReferences().stream()
            .filter(relation -> StringUtils.hasText(relation.getId()))
            .map(Relation::getId)
            .collect(Collectors.toList());
    removeStaleSegmentReference(surfaceBet.getSegmentReferences(), relationIds);
  }

  private void removeStaleSegmentReference(
      List<SegmentReference> segmentReferences, List<String> relationIds) {
    relationIds.add("-1");
    Iterator<SegmentReference> iterator = segmentReferences.listIterator();
    while (iterator.hasNext()) {
      if (!relationIds.contains(iterator.next().getPageRefId())) {
        iterator.remove();
      }
    }
  }

  protected boolean hasOnPage(RelationType relatedTo, String refId, Set<Relation> refs) {
    return !CollectionUtils.isEmpty(refs)
        && refs.stream()
            .anyMatch(ref -> refId.equals(ref.getRefId()) && relatedTo.equals(ref.getRelatedTo()));
  }

  public void enableSurfaceBetsForPage(
      String brand, String relatedTo, String refId, boolean isEnabled) {
    final Collection<SurfaceBet> surfaceForSport =
        this.findAllForBrandByPage(brand, relatedTo, refId);
    final RelationType refType = RelationType.valueOf(relatedTo);
    if (surfaceForSport == null) {
      return;
    }
    surfaceForSport.forEach(
        sb -> {
          Relation thisRef = buildRelation(refId, isEnabled, refType);
          sb.getReferences().remove(thisRef);
          sb.getReferences().add(thisRef);
          super.update(sb, sb);
        });
  }

  public Relation buildRelation(String refId, boolean isEnabled, final RelationType refType) {
    return Relation.builder().relatedTo(refType).refId(refId).enabled(isEnabled).build();
  }

  @Override
  public <S extends SurfaceBet> S prepareArchivalEntity(SurfaceBet entity) {
    return (S) modelMapper.map(entity, SurfaceBetArchive.class);
  }

  public List<SurfaceBet> findByBrandAndSegmentNameAndRelationRef(
      String brand, String pageType, String pageId, String segmentName) {

    List<SurfaceBet> records = new ArrayList<>();

    if (SegmentConstants.UNIVERSAL.equalsIgnoreCase(segmentName)) {

      records.addAll(getUniversalRecords(brand, RelationType.valueOf(pageType), pageId));
    } else {
      records.addAll(
          getSegmentAndUniversal(brand, segmentName, RelationType.valueOf(pageType), pageId));
    }

    return records.stream().map(this::enhanceEntity).collect(Collectors.toList());
  }

  @Override
  public List<SurfaceBet> findByBrand(String brand) {
    List<SurfaceBet> surfaceBets = super.findByBrand(brand);
    // add Universal for default segments...
    surfaceBets.stream().forEach(this::enhanceEntity);
    return surfaceBets;
  }

  private List<SurfaceBet> getUniversalRecords(String brand, RelationType valueOf, String pageId) {
    List<SurfaceBet> universalList =
        surfaceBetRepository.findUniversalRecordsByBrandAndPageRef(brand, valueOf, pageId);

    return SurfaceBetSortHelper.sortSurfaceBetUniversalRecords(universalList, valueOf, pageId);
  }

  private List<SurfaceBet> getSegmentAndUniversal(
      String brand, String segmentName, RelationType pageType, String pageId) {

    List<SurfaceBet> recordsWithSegmentReference =
        SurfaceBetSortHelper.sortByOrder(
            segmentName,
            surfaceBetRepository.findAllByBrandAndSegmentNameAndPageRef(
                brand, Arrays.asList(segmentName), pageType, pageId),
            Relation.builder().relatedTo(pageType).refId(pageId).build());

    isUniversalSegmentChanged(recordsWithSegmentReference, segmentName);
    // recordsWithSegmentReference
    // find universal.. ones...
    //
    List<String> idsFromSegmentReferences =
        recordsWithSegmentReference.stream().map(SurfaceBet::getId).collect(Collectors.toList());

    List<SurfaceBet> universalList =
        surfaceBetRepository
            .findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
                brand, Arrays.asList(segmentName), idsFromSegmentReferences, pageType, pageId);

    universalList =
        SurfaceBetSortHelper.sortSurfaceBetUniversalRecords(universalList, pageType, pageId);

    recordsWithSegmentReference.addAll(universalList);
    return recordsWithSegmentReference;
  }

  @Override
  public void dragAndDropOrder(OrderDto newOrder) {

    if (!StringUtils.hasText(newOrder.getSegmentName())) {
      newOrder.setSegmentName(SegmentConstants.UNIVERSAL);
    }
    if (newOrder.getPageId().equals("0")) {
      segmentedDragAndDropOrder(newOrder);
    } else {
      sportPagesOrderingService.dragAndDropOrder(newOrder);
    }
  }

  @Override
  public Optional<SegmentReference> getSegmentReferenceBySegmentName(
      SurfaceBet prevElement, OrderDto orderDto) {
    String pageRef = getPageRef(prevElement, orderDto);

    return prevElement.getSegmentReferences().stream()
        .filter(isSegmentExists(orderDto.getSegmentName(), pageRef))
        .filter(x -> x.getSortOrder() >= 0)
        .findFirst();
  }

  public Predicate<SegmentReference> isSegmentExists(String segmentName, String pageRef) {

    return segmentReference ->
        segmentName.equals(segmentReference.getSegmentName())
            && pageRef.equals(segmentReference.getPageRefId());
  }

  @Override
  public Optional<Double> getSortNumber(Optional<SurfaceBet> element, OrderDto orderDto) {

    if (element.isPresent() && !CollectionUtils.isEmpty(element.get().getSegmentReferences())) {
      String pageRef = getPageRef(element.get(), orderDto);

      return element.get().getSegmentReferences().stream()
          .filter(isSegmentExists(orderDto.getSegmentName(), pageRef))
          .filter(x -> x.getSortOrder() >= 0)
          .map(SegmentReference::getSortOrder)
          .findFirst();

    } else {
      return Optional.empty();
    }
  }

  @Override
  public String getPageRef(SurfaceBet element, OrderDto orderDto) {
    Optional<Relation> first =
        element.getReferences().stream()
            .filter(
                ref ->
                    orderDto.getPageId().equals(ref.getRefId())
                        && RelationType.valueOf(orderDto.getPageType()).equals(ref.getRelatedTo()))
            .findFirst();
    if (first.isPresent()) {
      Relation relation = first.get();
      if (!StringUtils.hasText(relation.getId())) {
        relation.setId(ObjectId.get().toHexString());
      }
      return relation.getId();
    }
    return null;
  }

  @Override
  public SurfaceBet enhanceDocument(
      OrderDto newOrder, Map<String, Double> idAndOrder, SurfaceBet document) {
    String id = document.getId();
    String pageRef = getPageRef(document, newOrder);
    if (!StringUtils.hasText(pageRef)) {
      document.setSegmentReferences(new ArrayList<>());
      return document;
    }
    document.getSegmentReferences().stream()
        .forEach(
            (SegmentReference segmentReference) -> {
              if ((newOrder.getSegmentName().equals(segmentReference.getSegmentName()))
                  && pageRef.equals(segmentReference.getPageRefId())) {
                Optional.ofNullable(idAndOrder.get(id))
                    .ifPresent(segmentReference::updateSortOrder);
              }
            });
    if (document.getSegmentReferences().stream()
        .noneMatch(isSegmentExists(newOrder.getSegmentName(), pageRef))) {
      document
          .getSegmentReferences()
          .add(
              buildSegmentReference(
                  newOrder.getSegmentName(),
                  Optional.ofNullable(idAndOrder.get(id)).orElse(null),
                  pageRef));
    }
    return document;
  }

  public Optional<SurfaceBet> isUniqueSelectionIdPerSegment(SurfaceBet surfaceBet) {

    List<SurfaceBet> surfaceBets =
        surfaceBetRepository.findBySelectionIdAndBrand(
            surfaceBet.getBrand(), surfaceBet.getSelectionId(), Instant.now());
    if (CollectionUtils.isEmpty(surfaceBets)) return Optional.empty();
    return surfaceBets.stream()
        .filter(
            existingsurfaceBet ->
                !existingsurfaceBet.getId().equals(surfaceBet.getId())
                    && isUniqueSB(existingsurfaceBet, surfaceBet)
                    && ismatchPeriod(surfaceBet))
        .findFirst();
  }

  public Set<String> findActiveSurfaceBetsByBrand(final String brand) {

    return surfaceBetRepository.findActiveSurfaceBetsByBrand(brand, Instant.now()).stream()
        .map(sb -> sb.getSelectionId() + "#" + sb.getId())
        .collect(Collectors.toSet());
  }

  private Boolean isUniqueSB(SurfaceBet exsistingSurfaceBet, SurfaceBet surfaceBet) {

    List<String> segments = segmentService.getSegmentsForSegmentedViews(surfaceBet.getBrand());
    List<String> newSegmentsViews = getSegmentView(surfaceBet, segments);

    if (exsistingSurfaceBet.isUniversalSegment()) {
      if (CollectionUtils.isEmpty(exsistingSurfaceBet.getExclusionList())) return true;
      List<String> exsistingSegmentsViews = getSegmentView(exsistingSurfaceBet, segments);
      return exsistingSegmentsViews.stream().anyMatch(newSegmentsViews::contains);

    } else {
      return CollectionUtils.isEmpty(exsistingSurfaceBet.getInclusionList())
          || exsistingSurfaceBet.getInclusionList().stream().anyMatch(newSegmentsViews::contains);
    }
  }

  private boolean ismatchPeriod(SurfaceBet surfaceBet) {

    return surfaceBet.getDisplayTo().compareTo(Instant.now()) >= 0;
  }

  private List<String> getSegmentView(SurfaceBet surfaceBet, List<String> segments) {
    if (surfaceBet.isUniversalSegment()) {

      if (CollectionUtils.isEmpty(surfaceBet.getExclusionList())) return segments;
      return segments
          .parallelStream()
          .filter(segment -> !surfaceBet.getExclusionList().contains(segment))
          .collect(Collectors.toList());

    } else {

      return surfaceBet.getInclusionList();
    }
  }
  /* removing the surfaceBet ids in competitionModules entity as well */
  private void removeIdsFromCompetitionModules(String id) {

    List<CompetitionModule> competitionModules =
        this.competitionModuleService.findCompetitionModulesByType(
            CompetitionModuleType.SURFACEBET);
    competitionModules.stream()
        .filter(competitionModule -> competitionModule.getSurfaceBets().contains(id))
        .forEach(
            (CompetitionModule competitionModule) -> {
              competitionModule.getSurfaceBets().remove(id);
              this.competitionModuleService.save(competitionModule);
            });
  }

  // OZONE-7673 - CMS_Enable/Disable Surface Bets from Active Surface Bets Table
  public void updateActiveSurfaceBets(List<ActiveSurfaceBetDto> activeSurfaceBetDtos) {

    Map<String, ActiveSurfaceBetDto> activeSurfaceBetMap =
        activeSurfaceBetDtos.stream()
            .parallel()
            .collect(Collectors.toMap(ActiveSurfaceBetDto::getId, Function.identity()));
    Iterable<SurfaceBet> iterables = surfaceBetRepository.findAllById(activeSurfaceBetMap.keySet());
    iterables.forEach(
        (SurfaceBet surfaceBet) -> {
          ActiveSurfaceBetDto activeSurfaceBetDto = activeSurfaceBetMap.get(surfaceBet.getId());

          surfaceBet.setDisabled(activeSurfaceBetDto.isDisabled());
          surfaceBet.setDisplayOnDesktop(activeSurfaceBetDto.isDisplayOnDesktop());
          surfaceBet.setEdpOn(activeSurfaceBetDto.isEdpOn());
          surfaceBet.setHighlightsTabOn(activeSurfaceBetDto.isHighlightsTabOn());
          if (isHighlightsTabOnChanged(surfaceBet, activeSurfaceBetDto.isHighlightsTabOn()))
            updateReferences(surfaceBet);
        });
    saveAndUpdateArchivals(iterables);
  }

  private boolean isHighlightsTabOnChanged(SurfaceBet surfaceBet, boolean highlightsTabOn) {

    Optional<Relation> relationOptional =
        surfaceBet.getReferences().stream()
            .filter(x -> RelationType.sport == x.getRelatedTo() && "0".equals(x.getRefId()))
            .findFirst();

    if (highlightsTabOn && !relationOptional.isPresent()) {
      surfaceBet.getReferences().add(buildRelation("0", true, RelationType.sport));
      return true;
    } else if (!highlightsTabOn && relationOptional.isPresent()) {
      surfaceBet.getReferences().remove(relationOptional.get());
      return true;
    }
    return false;
  }

  public void verifyAndSaveSBTitle(SurfaceBet surfaceBetEntity) {
    if (Objects.isNull(titleService.findSurfaceBetTitleByTitle(surfaceBetEntity.getTitle()))) {
      SurfaceBetTitle sbTitle = new SurfaceBetTitle();
      sbTitle.setTitle(surfaceBetEntity.getTitle());
      sbTitle.setBrand(surfaceBetEntity.getBrand());
      titleService.save(sbTitle);
    }
  }
}
