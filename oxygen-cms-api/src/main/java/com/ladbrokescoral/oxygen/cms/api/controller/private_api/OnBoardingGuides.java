package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.OnBoardingGuide;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.OnBoardingGuideService;
import java.util.List;
import java.util.Optional;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class OnBoardingGuides extends AbstractSortableController<OnBoardingGuide> {

  private final OnBoardingGuideService service;

  OnBoardingGuides(OnBoardingGuideService sortableService) {
    super(sortableService);
    service = sortableService;
  }

  @PostMapping("on-boarding-guide")
  @Override
  public ResponseEntity create(@RequestBody OnBoardingGuide entity) {
    return super.create(entity);
  }

  @GetMapping("on-boarding-guide")
  @Override
  public List<OnBoardingGuide> readAll() {
    return super.readAll();
  }

  @GetMapping("on-boarding-guide/{id}")
  @Override
  public OnBoardingGuide read(@PathVariable String id) {
    return super.read(id);
  }

  @PutMapping("on-boarding-guide/{id}")
  @Override
  public OnBoardingGuide update(@PathVariable String id, @RequestBody OnBoardingGuide entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("on-boarding-guide/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    OnBoardingGuide guide = service.findOne(id).orElseThrow(NotFoundException::new);
    service.removeSvgImage(guide);
    return delete(Optional.of(guide));
  }

  @GetMapping("on-boarding-guide/brand/{brand}")
  @Override
  public List<OnBoardingGuide> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("on-boarding-guide/{id}/image")
  public OnBoardingGuide uploadImage(
      @RequestParam("file") MultipartFile file, @PathVariable("id") String id) {
    OnBoardingGuide guide = service.findOne(id).orElseThrow(NotFoundException::new);
    service.attachSvgImage(guide, file);
    return guide;
  }

  @DeleteMapping("on-boarding-guide/{id}/image")
  public OnBoardingGuide removeImage(@PathVariable("id") String id) {
    OnBoardingGuide guide = service.findOne(id).orElseThrow(NotFoundException::new);
    service.removeSvgImage(guide);
    return guide;
  }

  @PostMapping("on-boarding-guide/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
