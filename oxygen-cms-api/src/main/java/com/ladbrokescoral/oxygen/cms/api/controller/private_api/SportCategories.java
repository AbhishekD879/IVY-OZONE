package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SportNameDto;
import com.ladbrokescoral.oxygen.cms.api.dto.TierCacheDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FileType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.CompetitionService;
import com.ladbrokescoral.oxygen.cms.api.service.SportCategoryService;
import com.ladbrokescoral.oxygen.cms.api.service.TierCategoriesCache;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class SportCategories extends AbstractSortableController<SportCategory> {

  private final SportCategoryService service;
  private final TierCategoriesCache tierCategoriesCache;
  private CompetitionService competitionService;

  @Autowired
  public SportCategories(
      SportCategoryService crudService,
      TierCategoriesCache tierCategoriesCache,
      CompetitionService competitionService) {
    super(crudService);
    this.service = crudService;
    this.tierCategoriesCache = tierCategoriesCache;
    this.competitionService = competitionService;
  }

  @GetMapping("sport-category")
  @Override
  public List<SportCategory> readAll() {
    return super.readAll();
  }

  @GetMapping("sport-category/{id}")
  @Override
  public SportCategory read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("sport-category/brand/{brand}")
  @Override
  public List<SportCategory> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("sport-category")
  @Override
  public ResponseEntity create(@RequestBody SportCategory entity) {
    competitionService.updateCompetitionSportId(entity);
    return super.create(entity);
  }

  @PutMapping("sport-category/{id}")
  @Override
  public SportCategory update(@PathVariable String id, @RequestBody SportCategory entity) {
    competitionService.updateCompetitionSportId(entity);
    return super.update(id, entity);
  }

  @DeleteMapping("sport-category/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    SportCategory category = service.findOne(id).orElseThrow(NotFoundException::new);
    service.removeImage(category);
    service.removeIcon(category);
    service.removeSvgImage(category);

    return delete(Optional.of(category));
  }

  @PostMapping("sport-category/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @PostMapping("sport-category/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id,
      @RequestParam("file") MultipartFile file,
      @RequestParam(value = "fileType", defaultValue = "image", required = false)
          FileType fileType) {
    Optional<SportCategory> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<SportCategory> sportCategory = Optional.empty();
    if (fileType.equals(FileType.IMAGE)) {
      sportCategory = service.attachImage(maybeEntity.get(), file);
    }
    if (fileType.equals(FileType.ICON)) {
      sportCategory = service.attachIcon(maybeEntity.get(), file);
    }
    if (fileType.equals(FileType.SVG)) {
      sportCategory = service.attachSvgImage(maybeEntity.get(), file);
    }

    return sportCategory
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to upload image", HttpStatus.BAD_REQUEST));
  }

  @DeleteMapping("sport-category/{id}/image")
  public ResponseEntity removeImage(
      @PathVariable("id") String id,
      @RequestParam(value = "fileType", defaultValue = "image", required = false)
          FileType fileType) {
    Optional<SportCategory> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<SportCategory> removeResult = Optional.empty();
    if (fileType.equals(FileType.IMAGE)) {
      removeResult = service.removeImage(maybeEntity.get());
    }
    if (fileType.equals(FileType.ICON)) {
      removeResult = service.removeIcon(maybeEntity.get());
    }
    if (fileType.equals(FileType.SVG)) {
      removeResult = service.removeSvgImage(maybeEntity.get());
    }

    return removeResult
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to remove image", HttpStatus.BAD_REQUEST));
  }

  @GetMapping("sport-category/cache")
  public List<TierCacheDto> getCacheView() {
    return tierCategoriesCache.getCacheView();
  }

  @GetMapping("sport-category/sport-name/brand/{brand}")
  public List<SportNameDto> readSportNameByBrand(@PathVariable String brand) {
    return service.readSportNameByBrand(brand);
  }

  @GetMapping("sport-category/brand/{brand}/segment/{segmentName}")
  public List<SportCategory> readByBrandAndSegmnetName(
      @PathVariable("brand") String brand, @PathVariable("segmentName") String segmentName) {
    return service.findByBrandAndSegmentName(brand, segmentName);
  }
}
