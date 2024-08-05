package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.SplashPage;
import com.ladbrokescoral.oxygen.cms.api.service.QuizSplashPageService;
import java.util.List;
import javax.validation.Valid;
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
public class QuizSplashPageController extends AbstractCrudController<SplashPage> {

  private final QuizSplashPageService service;

  QuizSplashPageController(QuizSplashPageService service) {
    super(service);
    this.service = service;
  }

  @PostMapping("splash-page")
  @Override
  public ResponseEntity create(@RequestBody @Valid SplashPage entity) {
    return super.create(entity);
  }

  @GetMapping("splash-page")
  public List<SplashPage> getAll() {
    return super.readAll();
  }

  @GetMapping("splash-page/{id}")
  public SplashPage readById(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("splash-page/brand/{brand}")
  public List<SplashPage> readQuizByBrand(@PathVariable String brand) {
    return service.findByBrand(brand);
  }

  @PutMapping("splash-page/{id}")
  @Override
  public SplashPage update(@PathVariable String id, @RequestBody @Valid SplashPage entity) {
    SplashPage updatedSplashPage = super.update(id, entity);
    service.updateQuizzesSplashPages(updatedSplashPage);
    return updatedSplashPage;
  }

  @DeleteMapping("splash-page/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    service.deleteAllFiles(id);
    service.deleteQuizzesSplashPages(id);
    return super.delete(id);
  }

  @PostMapping("splash-page/{id}/file")
  public SplashPage uploadImage(
      @PathVariable String id,
      @RequestParam(value = "svg", required = false) boolean isSvg,
      @RequestParam(value = "logo", required = false) MultipartFile logoFile,
      @RequestParam(value = "background", required = false) MultipartFile backgroundFile,
      @RequestParam(value = "footer", required = false) MultipartFile footer) {
    return service.handleFileUploading(id, isSvg, logoFile, backgroundFile, footer);
  }

  @DeleteMapping("splash-page/{id}/file")
  public SplashPage deleteImage(
      @PathVariable String id, @RequestParam(value = "imageType") String imageType) {
    return service.handleFileDelete(id, imageType);
  }
}
