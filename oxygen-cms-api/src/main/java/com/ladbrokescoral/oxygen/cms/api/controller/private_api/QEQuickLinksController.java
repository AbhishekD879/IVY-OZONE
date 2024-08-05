package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.QEQuickLinks;
import com.ladbrokescoral.oxygen.cms.api.service.QEQuickLinksService;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class QEQuickLinksController extends AbstractCrudController<QEQuickLinks> {

  private final QEQuickLinksService service;

  QEQuickLinksController(QEQuickLinksService service) {
    super(service);
    this.service = service;
  }

  @GetMapping("question-engine/quick-links")
  @Override
  public List<QEQuickLinks> readAll() {
    return super.readAll();
  }

  @GetMapping("question-engine/quick-links/{id}")
  @Override
  public QEQuickLinks read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("question-engine/quick-links/brand/{brand}")
  @Override
  public List<QEQuickLinks> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("question-engine/quick-links")
  @Override
  public ResponseEntity create(@RequestBody QEQuickLinks entity) {
    return super.create(entity);
  }

  @PutMapping("question-engine/quick-links/{id}")
  @Override
  public QEQuickLinks update(@PathVariable String id, @RequestBody QEQuickLinks entity) {
    QEQuickLinks updatedQuickLinks = super.update(id, entity);
    service.updateQuizzesQuickLinks(updatedQuickLinks);
    return updatedQuickLinks;
  }

  @DeleteMapping("question-engine/quick-links/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    service.deleteQuizzesQuickLinks(id);
    return super.delete(id);
  }
}
