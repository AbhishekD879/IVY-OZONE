package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.Relation;
import com.ladbrokescoral.oxygen.cms.api.entity.RelationType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.entity.SurfaceBet;
import com.ladbrokescoral.oxygen.cms.api.repository.HighlightCarouselRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.HomeModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportQuickLinkRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SurfaceBetRepository;
import com.ladbrokescoral.oxygen.cms.util.ParallelExecutor;
import java.util.Set;
import java.util.concurrent.ExecutionException;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;
import org.springframework.util.ObjectUtils;

@Component
@Slf4j
public class DeleteEntityService {

  private SportModuleRepository sportModuleRepository;
  private HomeModuleRepository homeModuleRepository;
  private SportQuickLinkRepository sportQuickLinkRepository;
  private HighlightCarouselRepository carouselRepository;
  private SurfaceBetRepository surfaceBetRepository;

  @Autowired
  public DeleteEntityService(
      SportModuleRepository moduleRepository,
      HomeModuleRepository homeModuleRepository,
      SportQuickLinkRepository sportQuickLinkRepository,
      HighlightCarouselRepository carouselRepository,
      SurfaceBetRepository surfaceBetRepository) {
    this.sportModuleRepository = moduleRepository;
    this.homeModuleRepository = homeModuleRepository;
    this.sportQuickLinkRepository = sportQuickLinkRepository;
    this.carouselRepository = carouselRepository;
    this.surfaceBetRepository = surfaceBetRepository;
  }

  public void delete(String pageId, String brand, PageType pageType, SportModuleType moduleType)
      throws InterruptedException, ExecutionException {
    if (ObjectUtils.isEmpty(moduleType)) {
      deleteAllDependencies(pageId, brand, pageType);
    } else {
      deleteSingleDependencies(pageId, brand, pageType, moduleType);
    }
  }

  private void deleteSingleDependencies(
      String pageId, String brand, PageType pageType, SportModuleType moduleType) {
    switch (moduleType) {
      case QUICK_LINK:
        sportQuickLinkRepository.deleteAllByBrandAndPageTypeAndPageId(brand, pageType, pageId);
        break;
      case FEATURED:
        homeModuleRepository.deleteAll(brand, pageType, pageId);
        break;
      case HIGHLIGHTS_CAROUSEL:
        carouselRepository.deleteAllByBrandAndPageTypeAndPageId(brand, pageType, pageId);
        break;
      case SURFACE_BET:
        deleteSurfaceBetsReferences(brand, pageType, pageId);
        break;
      default:
        log.info("Did't support delete for {} objects", moduleType);
    }
  }

  private void deleteAllDependencies(String pageId, String brand, PageType pageType)
      throws InterruptedException, ExecutionException {
    ParallelExecutor executor = new ParallelExecutor();
    executor.execute(
        () -> sportModuleRepository.deleteAllByBrandAndPageTypeAndPageId(brand, pageType, pageId),
        () -> homeModuleRepository.deleteAll(brand, pageType, pageId),
        () ->
            sportQuickLinkRepository.deleteAllByBrandAndPageTypeAndPageId(brand, pageType, pageId),
        () -> carouselRepository.deleteAllByBrandAndPageTypeAndPageId(brand, pageType, pageId),
        () -> deleteSurfaceBetsReferences(brand, pageType, pageId));
  }

  public void deleteSurfaceBetsReferences(String brand, PageType pageType, String refId) {
    String relatedTo = pageType.name();
    final RelationType refType = RelationType.valueOf(relatedTo);
    surfaceBetRepository
        .findByBrand(brand)
        .parallelStream()
        .filter(sb -> hasOnPage(RelationType.valueOf(relatedTo), refId, sb.getReferences()))
        .forEach(sb -> deleteSurfaceBetsReferences(sb, refType, refId));
  }

  private void deleteSurfaceBetsReferences(SurfaceBet sb, RelationType refType, String refId) {
    Set<Relation> relationsToDelete =
        sb.getReferences().stream()
            .filter(r -> r.getRefId().equals(refId) && r.getRelatedTo().equals(refType))
            .collect(Collectors.toSet());
    sb.getReferences().removeAll(relationsToDelete);
    surfaceBetRepository.save(sb);
  }

  private boolean hasOnPage(RelationType relatedTo, String refId, Set<Relation> refs) {
    return !CollectionUtils.isEmpty(refs)
        && refs.stream()
            .anyMatch(ref -> refId.equals(ref.getRefId()) && relatedTo.equals(ref.getRelatedTo()));
  }
}
