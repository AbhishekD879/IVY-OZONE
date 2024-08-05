package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.apache.commons.io.FileUtils.ONE_KB;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.SvgImageDto;
import com.ladbrokescoral.oxygen.cms.api.controller.mapping.SvgImageMapper;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgImage;
import com.ladbrokescoral.oxygen.cms.api.service.SvgImageService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileSize;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import java.util.List;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@Validated
@RestController
public class SvgImages extends AbstractCrudController<SvgImage> {

  private static final long MAX_SVG_SIZE = 20 * ONE_KB;

  private final SvgImageService service;

  @Autowired
  SvgImages(SvgImageService crudService) {
    super(crudService);
    this.service = crudService;
  }

  @Override
  @GetMapping("svg-images/{id}")
  public SvgImage read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("svg-images/brand/{brand}")
  public List<SvgImage> readByBrand(
      @Brand(message = "is not supported") @PathVariable String brand,
      @RequestParam(required = false) String search,
      @RequestParam(required = false) Boolean active) {
    return service.searchByBrand(brand, search, active);
  }

  @GetMapping("svg-images/brand/{brand}/sprite/{sprite}")
  public List<SvgImage> readByBrandAndSprite(
      @Brand(message = "is not supported") @PathVariable String brand,
      @PathVariable String sprite) {
    return service.findAllByBrandAndSprite(brand, sprite);
  }

  @GetMapping("svg-images/brand/{brand}/sprites")
  public List<String> listSprites(@Brand(message = "is not supported") @PathVariable String brand) {
    return service.getSprites(brand);
  }

  @PostMapping(
      value = "svg-images",
      consumes = MediaType.MULTIPART_FORM_DATA_VALUE,
      produces = MediaType.APPLICATION_JSON_VALUE)
  public ResponseEntity<SvgImage> create(
      @Valid SvgImageDto dto,
      @RequestParam("file") @ValidFileType("svg") @ValidFileSize(MAX_SVG_SIZE) MultipartFile file) {
    SvgImage image = service.createSvgImage(SvgImageMapper.INSTANCE.toEntity(dto), file, "");
    return super.create(image);
  }

  @PostMapping(
      value = "svg-images/{id}",
      consumes = MediaType.MULTIPART_FORM_DATA_VALUE,
      produces = MediaType.APPLICATION_JSON_VALUE)
  public ResponseEntity<SvgImage> update(
      @PathVariable String id,
      @Valid SvgImageDto dto,
      @RequestParam(value = "file", required = false)
          @ValidFileType("svg")
          @ValidFileSize(MAX_SVG_SIZE)
          MultipartFile file) {
    SvgImage image = service.replaceSvgImage(id, file, SvgImageMapper.INSTANCE.toEntity(dto));
    return ResponseEntity.ok(super.update(id, image));
  }

  @Override
  @DeleteMapping("svg-images/{id}")
  public ResponseEntity<SvgImage> delete(@PathVariable String id) {
    service.removeSvgImage(id);
    return super.delete(id);
  }
}
