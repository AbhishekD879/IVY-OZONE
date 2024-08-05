package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.ActiveSurfaceBetDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Relation;
import com.ladbrokescoral.oxygen.cms.api.entity.RelationType;
import com.ladbrokescoral.oxygen.cms.api.entity.SurfaceBet;
import com.ladbrokescoral.oxygen.cms.api.entity.SurfaceBetTitle;
import com.ladbrokescoral.oxygen.cms.api.service.SurfaceBetService;
import com.ladbrokescoral.oxygen.cms.api.service.SurfaceBetTitleService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class SurfaceBets extends AbstractSortableController<SurfaceBet> {

  private final SurfaceBetService sbService;

  private final SurfaceBetTitleService titleService;

  @Autowired
  SurfaceBets(SurfaceBetService sortableService, SurfaceBetTitleService titleService) {
    super(sortableService);
    this.sbService = sortableService;
    this.titleService = titleService;
  }

  @Override
  @GetMapping("surface-bet")
  public List<SurfaceBet> readAll() {
    return super.readAll();
  }

  @Override
  @GetMapping("surface-bet/brand/{brand}")
  public List<SurfaceBet> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @GetMapping("surface-bet/brand/{brand}/segment/{segmentName}")
  public List<SurfaceBet> readByBrandAndSegment(
      @PathVariable String brand, @PathVariable String segmentName) {
    return sbService.findByBrandAndSegmentName(brand, segmentName);
  }

  @GetMapping("surface-bet/brand/{brand}/title")
  public List<SurfaceBetTitle> readAllSurfaceBetTitle(@PathVariable String brand) {
    return titleService.findAllSurfaceBetTitle(brand);
  }

  @Override
  @PostMapping("surface-bet/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @Override
  @PostMapping("surface-bet")
  public ResponseEntity create(@Valid @Validated @RequestBody SurfaceBet entity) {
    sbService.verifyAndSaveSBTitle(entity);
    return super.create(entity);
  }

  @Override
  @GetMapping("surface-bet/{id}")
  public SurfaceBet read(@PathVariable("id") String id) {
    return super.read(id);
  }

  @Override
  @PutMapping("surface-bet/{id}")
  public SurfaceBet update(
      @PathVariable("id") String id, @Valid @Validated @RequestBody SurfaceBet updateEntity) {
    sbService.verifyAndSaveSBTitle(updateEntity);
    return super.update(id, updateEntity);
  }

  @GetMapping("surface-bet/brand/{brand}/{relatedTo}/{refId}")
  public List<SurfaceBet> readByBrandForPageId(
      @PathVariable String brand, @PathVariable String relatedTo, @PathVariable String refId) {
    return sbService.findAllForBrandByPage(brand, relatedTo, refId);
  }

  @GetMapping("surface-bet/brand/{brand}/segment/{segmentName}/{relatedTo}/{refId}")
  public List<SurfaceBet> readByBrandAndSegmentName(
      @PathVariable String brand,
      @PathVariable String segmentName,
      @PathVariable String relatedTo,
      @PathVariable String refId) {
    return RelationType.sport == RelationType.valueOf(relatedTo) && "0".equals(refId)
        ? sbService.findByBrandAndSegmentNameAndRelationRef(brand, relatedTo, refId, segmentName)
        : sbService.findAllForBrandByPage(brand, relatedTo, refId);
  }

  @GetMapping("surface-bet/has-active-bets/{brand}/{relatedTo}/{refId}")
  public Boolean hasActiveBetsOnPage(
      @PathVariable String brand, @PathVariable String relatedTo, @PathVariable String refId) {
    return sbService.findAllForBrandByPage(brand, relatedTo, refId).stream()
        .flatMap(sb -> sb.getReferences().stream())
        .filter(sb -> sb.getRelatedTo().equals(RelationType.valueOf(relatedTo)))
        .filter(sb -> sb.getRefId().equals(refId))
        .filter(Relation::isEnabled)
        .findAny()
        .orElse(Relation.builder().enabled(false).build())
        .isEnabled();
  }

  @DeleteMapping("surface-bet/{idList}")
  public void deleteWithImage(@PathVariable("idList") List<String> idList) {
    idList.forEach(sbService::delete);
  }

  @DeleteMapping("surface-bet/brand/{brand}/id/{id}")
  public void deleteSurfaceBetTitleByBrand(
      @PathVariable("brand") String brand, @PathVariable("id") String id) {
    titleService.deleteSBTitleByBrandAndId(brand, id);
  }

  @PostMapping("surface-bet/{id}/image")
  public SurfaceBet uploadImage(
      @PathVariable("id") String id, @RequestParam("file") MultipartFile image) {
    return sbService.attachSvgImage(id, image);
  }

  @DeleteMapping("surface-bet/{id}/image")
  public SurfaceBet removeImage(@PathVariable("id") String id) {
    return sbService.removeSvgImage(id);
  }

  @PostMapping("surface-bet/enable/{brand}/{relatedTo}/{refId}")
  public void enableSurfaceBetsForPage(
      @PathVariable("brand") String brand,
      @PathVariable("relatedTo") String relatedTo,
      @PathVariable("refId") String refId) {
    sbService.enableSurfaceBetsForPage(brand, relatedTo, refId, true);
  }

  @PostMapping("surface-bet/disable/{brand}/{relatedTo}/{refId}")
  public void disabledSurfaceBetsForPage(
      @PathVariable("brand") String brand,
      @PathVariable("relatedTo") String relatedTo,
      @PathVariable("refId") String refId) {
    sbService.enableSurfaceBetsForPage(brand, relatedTo, refId, false);
  }

  @PutMapping("surface-bets")
  public void updateActiveSurfaceBets(
      @Valid @Validated @RequestBody List<ActiveSurfaceBetDto> activeSurfaceBetDtos) {

    sbService.updateActiveSurfaceBets(activeSurfaceBetDtos);
  }
}
