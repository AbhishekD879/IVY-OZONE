package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.TimelineFileType;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Template;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineTemplateService;
import java.util.List;
import java.util.Optional;
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
public class TimelineTemplateController extends AbstractCrudController<Template> {
  TimelineTemplateService timelineTemplateService;

  TimelineTemplateController(TimelineTemplateService crudService) {
    super(crudService);
    this.timelineTemplateService = crudService;
  }

  @GetMapping("/timeline/template/brand/{brand}")
  public List<Template> getTemplatesByBrand(@PathVariable("brand") String brand) {
    List<Template> templates = crudService.findByBrand(brand);

    templates.forEach(this::populateCreatorAndUpdater);

    return templates;
  }

  @Override
  @PostMapping("/timeline/template")
  public ResponseEntity<Template> create(@RequestBody Template entity) {
    return super.create(populateCreatorAndUpdater(entity.prepareModelBeforeSave()));
  }

  @GetMapping("/timeline/template/{id}")
  public Template getTemplateById(@PathVariable("id") String id) {
    return super.read(id);
  }

  @Override
  @PutMapping("/timeline/template/{id}")
  public Template update(@PathVariable("id") String id, @RequestBody Template updateEntity) {
    return super.update(id, populateCreatorAndUpdater(updateEntity.prepareModelBeforeUpdate()));
  }

  @Override
  @DeleteMapping("/timeline/template/{id}")
  public ResponseEntity<Template> delete(@PathVariable("id") String id) {
    return super.delete(id);
  }

  @PostMapping("/timeline/template/{id}/image")
  public ResponseEntity<Template> uploadImage(
      @PathVariable("id") String id,
      @RequestParam String imageType,
      @RequestParam("file") MultipartFile file) {
    Optional<Template> maybeEntity = crudService.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Template template;
    if (file.getOriginalFilename().toLowerCase().contains(".svg")) {
      template = timelineTemplateService.uploadAndSetSvgImage(maybeEntity.get(), file);
    } else {
      template = timelineTemplateService.uploadAndSetRightCornerImage(maybeEntity.get(), file);
    }

    return new ResponseEntity<>(template, HttpStatus.OK);
  }

  @DeleteMapping(value = "/timeline/template/{id}/image")
  public ResponseEntity<Template> deleteTimelineImageForTemplate(
      @PathVariable String id, @RequestParam String imageType) {
    Optional<Template> maybeEntity = crudService.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    TimelineFileType fileType = TimelineFileType.fromValue(imageType);
    return new ResponseEntity<>(
        timelineTemplateService.deleteImage(maybeEntity.get(), fileType), HttpStatus.OK);
  }
}
