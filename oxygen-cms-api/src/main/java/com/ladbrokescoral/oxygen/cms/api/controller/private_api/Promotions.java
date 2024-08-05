package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.fasterxml.jackson.databind.MappingIterator;
import com.fasterxml.jackson.dataformat.csv.CsvMapper;
import com.fasterxml.jackson.dataformat.csv.CsvSchema;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.abstractions.WysiwygControllerTraits;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.*;
import javax.validation.constraints.NotBlank;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.StringUtils;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
@Slf4j
public class Promotions extends AbstractSortableController<Promotion>
    implements WysiwygControllerTraits<Promotion> {

  private final PromotionService promotionService;
  private final WysiwygService wysiwygService;
  private final PromotionSectionService sectionService;
  private final PromoLeaderboardValidationService promoLbrValidationService;

  @ResponseStatus(
      value = HttpStatus.CONFLICT,
      reason = "Promotion with the same promotionId is already created")
  static class PromotionIdNotUniqueException extends RuntimeException {}

  @ResponseStatus(
      value = HttpStatus.CONFLICT,
      reason = "Promotion with the same promoKey is already created")
  static class PromotionKeyNotUniqueException extends RuntimeException {}

  @Autowired
  Promotions(
      PromotionService promotionService,
      WysiwygService wysiwygService,
      PromotionSectionService sectionService,
      PromoLeaderboardValidationService promoLbrValidationService) {
    super(promotionService);
    this.promotionService = promotionService;
    this.wysiwygService = wysiwygService;
    this.sectionService = sectionService;
    this.promoLbrValidationService = promoLbrValidationService;
  }

  @GetMapping("promotion")
  @Override
  public List<Promotion> readAll() {
    return promotionService.findAllSorted();
  }

  @GetMapping("promotion/{id}")
  @Override
  public Promotion read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("promotion/brand/{brand}")
  @Override
  public List<Promotion> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("promotion")
  @Override
  public ResponseEntity create(@RequestBody @Validated Promotion entity) {
    validate(entity);
    validateMaxLeaderboard(entity);
    return super.create(entity);
  }

  private void validate(Promotion entity) {
    if (entity.getPromotionId() != null
        && promotionService
            .findByBrandAndPromotionId(entity.getBrand(), entity.getId())
            .isPresent()) {
      throw new PromotionIdNotUniqueException();
    }

    if (entity.getPromoKey() != null
        && promotionService
            .findByBrandAndPromoKey(entity.getBrand(), entity.getPromoKey())
            .isPresent()) {
      throw new PromotionKeyNotUniqueException();
    }
  }

  private void validateMaxLeaderboard(Promotion entity) {
    if (Objects.nonNull(entity.getNavigationGroupId())
        && !entity.getNavigationGroupId().trim().isEmpty()) {
      promoLbrValidationService.validateMaxLeaderboard(
          entity.getBrand(),
          promoLbrValidationService.getNavGrpLbrCount(entity.getNavigationGroupId()),
          new ArrayList<>());
    }
  }

  private void validateUpdate(Promotion entity) {
    final Optional<Promotion> promotion =
        promotionService.findByBrandAndPromotionId(entity.getBrand(), entity.getId());
    if (entity.getPromotionId() != null
        && promotion.isPresent()
        && !entity.getId().equals(promotion.get().getId())) {
      throw new PromotionIdNotUniqueException();
    }

    if (entity.getPromoKey() != null) {
      Optional<Promotion> promo =
          promotionService.findByBrandAndPromoKey(entity.getBrand(), entity.getPromoKey());
      if (promo.isPresent() && !Objects.equals(promo.get().getId(), entity.getId())) {
        throw new PromotionKeyNotUniqueException();
      }
    }
  }

  @PutMapping("promotion/{id}")
  @Override
  public Promotion update(@PathVariable String id, @Validated @RequestBody Promotion entity) {
    validateUpdate(entity);

    if (!StringUtils.isEmpty(entity.getId())) {
      log.warn(
          "Client passed custom id in PUT body: {}. Using id from resource path instead: {}",
          entity.getId(),
          id);
    }
    entity.setId(id);
    Optional<Promotion> maybeEntity = crudService.findOne(id);

    validateUpdateMaxLeaderboard(maybeEntity, entity);

    final Promotion update = update(maybeEntity, entity);
    maybeEntity.ifPresent(
        existingEntity -> {
          if (existingEntity.getPromotionId() != null
              && !existingEntity.getPromotionId().equals(entity.getPromotionId())) {
            if (entity.getPromotionId() == null) {
              sectionService.deletePromotionIdInSections(
                  existingEntity.getBrand(), existingEntity.getPromotionId());
            } else {
              sectionService.updatePromotionIdInSections(
                  existingEntity.getBrand(),
                  existingEntity.getPromotionId(),
                  entity.getPromotionId());
            }
          }
        });

    return update;
  }

  private void validateUpdateMaxLeaderboard(
      Optional<Promotion> maybeEntity, Promotion updatedEntity) {
    if (Objects.nonNull(updatedEntity.getNavigationGroupId())
        && !updatedEntity.getNavigationGroupId().trim().isEmpty()) {
      maybeEntity.ifPresent(
          (Promotion existingEntity) -> {
            if (Objects.isNull(existingEntity.getNavigationGroupId())) {
              promoLbrValidationService.validateMaxLeaderboard(
                  updatedEntity.getBrand(),
                  promoLbrValidationService.getNavGrpLbrCount(updatedEntity.getNavigationGroupId()),
                  new ArrayList<>());
            }
            if (Objects.nonNull(existingEntity.getNavigationGroupId())
                && !existingEntity
                    .getNavigationGroupId()
                    .equals(updatedEntity.getNavigationGroupId())) {
              List<String> promoList = new ArrayList<>();
              promoList.add(existingEntity.getId());
              promoLbrValidationService.validateMaxLeaderboard(
                  updatedEntity.getBrand(),
                  promoLbrValidationService.getNavGrpLbrCount(updatedEntity.getNavigationGroupId()),
                  promoList);
            }
          });
    }
  }

  @DeleteMapping("promotion/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    promotionService.getPromoDeleteMap().put(id, "Deleted");
    removeImage(id);
    Optional<Promotion> maybeEntity = crudService.findOne(id);
    maybeEntity.ifPresent(
        e -> sectionService.deletePromotionIdInSections(e.getBrand(), e.getPromotionId()));
    promotionService.getPromoDeleteMap().remove(id);
    return delete(maybeEntity);
  }

  @PostMapping("promotion/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @PostMapping("promotion/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id, @RequestParam("file") MultipartFile file) {
    Optional<Promotion> maybeEntity = promotionService.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }
    Optional<Promotion> promotion = promotionService.attachImage(maybeEntity.get(), file);

    return promotion
        .map(
            prom -> {
              Promotion saved = promotionService.save(prom);
              return new ResponseEntity(saved, HttpStatus.OK);
            })
        .orElseGet(() -> new ResponseEntity("Failed to upload image", HttpStatus.BAD_REQUEST));
  }

  @DeleteMapping("promotion/{id}/image")
  public ResponseEntity removeImage(@PathVariable("id") String id) {
    Promotion promotion = promotionService.findOne(id).orElseThrow(NotFoundException::new);

    return promotionService
        .removeImage(promotion)
        .map(promotionService::save)
        .map(ResponseEntity::ok)
        .orElseGet(failedToRemoveImage());
  }

  @PostMapping("promotion/{id}/wysiwyg-image")
  public ResponseEntity uploadWysiwygImage(
      @RequestParam("file") MultipartFile file, @PathVariable("id") @NotBlank String id) {
    Promotion promotion = promotionService.findOne(id).orElseThrow(NotFoundException::new);

    return uploadWysiwygImage(promotion.getBrand(), file, Promotion.COLLECTION_NAME, id);
  }

  @DeleteMapping("promotion/{id}/wysiwyg-image/{imageName}")
  public ResponseEntity removeWysiwygImage(
      @PathVariable("id") @NotBlank String id, @PathVariable("imageName") String imageName) {
    Promotion promotion = promotionService.findOne(id).orElseThrow(NotFoundException::new);

    return removeWysiwygImage(promotion.getBrand(), id, Promotion.COLLECTION_NAME, imageName);
  }

  @Override
  public CrudService<Promotion> getCRUDService() {
    return this.promotionService;
  }

  @Override
  public WysiwygService getWysiwygService() {
    return this.wysiwygService;
  }

  @PostMapping("promotion/upload-csv-file")
  public ResponseEntity<List<Map<String, String>>> uploadTableCSVFile(
      @RequestParam("file") MultipartFile file) throws IOException {
    try (Reader reader = new BufferedReader(new InputStreamReader(file.getInputStream()))) {
      // CsvToBean<TableEntity> csv
      CsvSchema schema = CsvSchema.emptySchema().withHeader();
      CsvMapper csvMapper = new CsvMapper();
      // Read data from CSV file
      MappingIterator<Map<String, String>> mappingIterator =
          csvMapper.reader().forType(Map.class).with(schema).readValues(reader);
      List<Map<String, String>> list = mappingIterator.readAll();
      return new ResponseEntity<>(list, HttpStatus.OK);
    }
  }
}
