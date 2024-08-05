package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Homepage;
import com.ladbrokescoral.oxygen.cms.api.entity.HomepageMenu;
import com.ladbrokescoral.oxygen.cms.api.service.HomepageService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class Homepages extends AbstractSortableController<Homepage> {

  private final HomepageService homepageService;

  @Autowired
  public Homepages(HomepageService homepageService) {
    super(homepageService);
    this.homepageService = homepageService;
  }

  @PostMapping("homepages")
  public ResponseEntity create(@RequestBody HomepageMenu entities) {
    entities.getHomepages().forEach(super::create);
    return new ResponseEntity<List<Homepage>>(readAll(), HttpStatus.CREATED);
  }

  @PostMapping("homepage")
  public ResponseEntity create(@RequestBody Homepage entity) {
    return super.create(entity);
  }

  @GetMapping("homepage")
  @Override
  public List<Homepage> readAll() {
    return homepageService.readAll();
  }

  @PostMapping("homepage/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @PutMapping("homepage/{id}")
  @Override
  public Homepage update(@PathVariable String id, @RequestBody Homepage entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("homepage/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }
}
