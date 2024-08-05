package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.abstractions.WysiwygControllerTraits;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionSectionDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PromotionSection;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.SectionUpdatingOrDeletingForbidden;
import com.ladbrokescoral.oxygen.cms.api.mapping.PromotionSectionMapper;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.PromotionSectionService;
import com.ladbrokescoral.oxygen.cms.api.service.WysiwygService;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PromotionsSections extends AbstractSortableController<PromotionSection>
    implements WysiwygControllerTraits<PromotionSection> {

  private final PromotionSectionService sectionService;
  private final WysiwygService wysiwygService;

  @Autowired
  PromotionsSections(PromotionSectionService sectionService, WysiwygService wysiwygService) {
    super(sectionService);
    this.sectionService = sectionService;
    this.wysiwygService = wysiwygService;
  }

  @GetMapping("promotion/brand/{brand}/section")
  public List<PromotionSection> findByBrandWithDefaultSection(@PathVariable String brand) {
    return sectionService.findByBrandWithDefaultSection(brand);
  }

  @GetMapping("promotion/brand/{brand}/section/{id}")
  public PromotionSection read(@PathVariable String brand, @PathVariable String id) {
    Optional<PromotionSection> maybeEntity = sectionService.findOne(id);
    return maybeEntity
        .map(this::populateCreatorAndUpdater)
        .orElseGet(
            () -> {
              if (brand.equals(id)) {
                return sectionService.unassignedSection(brand);
              } else {
                throw new NotFoundException();
              }
            });
  }

  @PostMapping("promotion/brand/{brand}/section")
  public ResponseEntity create(@RequestBody @Validated PromotionSectionDto entity) {
    return super.create(PromotionSectionMapper.INSTANCE.toInstance(entity));
  }

  @PutMapping("promotion/brand/{brand}/section/{id}")
  public PromotionSection update(
      @PathVariable String brand,
      @PathVariable String id,
      @Validated @RequestBody PromotionSectionDto entity) {
    if (brand.equals(id)) {
      throw new SectionUpdatingOrDeletingForbidden();
    }
    return super.update(id, PromotionSectionMapper.INSTANCE.toInstance(entity));
  }

  @DeleteMapping("promotion/brand/{brand}/section/{id}")
  public ResponseEntity delete(@PathVariable String brand, @PathVariable String id) {
    if (brand.equals(id)) {
      throw new SectionUpdatingOrDeletingForbidden();
    }
    return super.delete(id);
  }

  @PostMapping("promotion/brand/{brand}/section/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @Override
  public CrudService<PromotionSection> getCRUDService() {
    return this.sectionService;
  }

  @Override
  public WysiwygService getWysiwygService() {
    return this.wysiwygService;
  }
}
