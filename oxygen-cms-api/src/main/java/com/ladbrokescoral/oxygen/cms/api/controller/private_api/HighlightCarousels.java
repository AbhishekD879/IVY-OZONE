package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HighlightCarousel;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.service.HighlightCarouselService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
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
public class HighlightCarousels extends AbstractSortableController<HighlightCarousel> {

  private final HighlightCarouselService highlightCarouselService;

  HighlightCarousels(HighlightCarouselService highlightCarouselService) {
    super(highlightCarouselService);
    this.highlightCarouselService = highlightCarouselService;
  }

  @Override
  @GetMapping("/highlight-carousel")
  public List<HighlightCarousel> readAll() {
    return super.readAll();
  }

  @Override
  @GetMapping("highlight-carousel/brand/{brand}")
  public List<HighlightCarousel> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @GetMapping("highlight-carousel/brand/{brand}/{pageType}/{pageId}")
  public List<HighlightCarousel> readByBrandAndSportId(
      @PathVariable String brand, @PathVariable PageType pageType, @PathVariable String pageId) {
    return highlightCarouselService.findAllByBrandAndPageId(brand, pageType, pageId);
  }

  @Override
  @PostMapping("highlight-carousel/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @Override
  @PostMapping("/highlight-carousel")
  public ResponseEntity<HighlightCarousel> create(
      @Valid @Validated @RequestBody HighlightCarousel entity) {
    return super.create(entity);
  }

  @Override
  @GetMapping("/highlight-carousel/{id}")
  public HighlightCarousel read(@PathVariable("id") String id) {
    return super.read(id);
  }

  @Override
  @PutMapping("/highlight-carousel/{id}")
  public HighlightCarousel update(
      @PathVariable("id") String id,
      @Valid @Validated @RequestBody HighlightCarousel updateEntity) {
    return super.update(id, updateEntity);
  }

  @DeleteMapping("/highlight-carousel/{id}")
  public ResponseEntity<HighlightCarousel> deleteWithImage(@PathVariable("id") String id) {
    return super.delete(id);
  }

  @PostMapping("highlight-carousel/{id}/image")
  public HighlightCarousel uploadImage(
      @PathVariable("id") String id, @RequestParam("file") MultipartFile image) {
    return highlightCarouselService.attachSvgImage(id, image);
  }

  @DeleteMapping("highlight-carousel/{id}/image")
  public HighlightCarousel removeImage(@PathVariable("id") String id) {
    return highlightCarouselService.removeSvgImage(id);
  }

  @GetMapping("highlight-carousel/brand/{brand}/segment/{segmentName}")
  public List<HighlightCarousel> readByBrandAndSegmentName(
      @PathVariable String brand, @PathVariable String segmentName) {
    return highlightCarouselService.findByBrandAndSegmentName(brand, segmentName);
  }

  @GetMapping("highlight-carousel/brand/{brand}/segment/{segmentName}/{pageType}/{pageId}")
  public List<HighlightCarousel> readByBrandAndSegmentName(
      @PathVariable String brand,
      @PathVariable String segmentName,
      @PathVariable @Valid String pageType,
      @PathVariable String pageId) {
    return highlightCarouselService.findByBrandAndSegmentNameAndPageRef(
        brand, pageType, pageId, segmentName);
  }
}
