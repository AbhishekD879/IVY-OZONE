package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.abstractions.WysiwygControllerTraits;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoPage;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.SeoPageService;
import com.ladbrokescoral.oxygen.cms.api.service.WysiwygService;
import java.util.List;
import javax.validation.constraints.NotBlank;
import org.springframework.beans.factory.annotation.Autowired;
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
public class SeoPages extends AbstractCrudController<SeoPage>
    implements WysiwygControllerTraits<SeoPage> {

  private final SeoPageService seoPageService;
  private final WysiwygService wysiwygService;

  @Autowired
  SeoPages(SeoPageService crudService, WysiwygService wysiwygService) {
    super(crudService);
    this.seoPageService = crudService;
    this.wysiwygService = wysiwygService;
  }

  @GetMapping("seo-page")
  @Override
  public List<SeoPage> readAll() {
    return super.readAll();
  }

  @GetMapping("seo-page/{id}")
  @Override
  public SeoPage read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("seo-page/brand/{brand}")
  @Override
  public List<SeoPage> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("seo-page")
  @Override
  public ResponseEntity create(@RequestBody @Validated SeoPage entity) {
    return super.create(entity);
  }

  @PutMapping("seo-page/{id}")
  @Override
  public SeoPage update(@PathVariable String id, @RequestBody @Validated SeoPage entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("seo-page/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("seo-page/{id}/wysiwyg-image")
  public ResponseEntity uploadWysiwygImage(
      @RequestParam("file") MultipartFile file, @PathVariable("id") @NotBlank String id) {
    SeoPage seoPage = seoPageService.findOne(id).orElseThrow(NotFoundException::new);
    return uploadWysiwygImage(seoPage.getBrand(), file, SeoPage.COLLECTION_NAME, id);
  }

  @DeleteMapping("seo-page/{id}/wysiwyg-image/{imageName}")
  public ResponseEntity removeWysiwygImage(
      @PathVariable("id") @NotBlank String id, @PathVariable("imageName") String imageName) {
    SeoPage seoPage = seoPageService.findOne(id).orElseThrow(NotFoundException::new);
    return removeWysiwygImage(seoPage.getBrand(), id, SeoPage.COLLECTION_NAME, imageName);
  }

  @Override
  public CrudService<SeoPage> getCRUDService() {
    return this.seoPageService;
  }

  @Override
  public WysiwygService getWysiwygService() {
    return this.wysiwygService;
  }
}
