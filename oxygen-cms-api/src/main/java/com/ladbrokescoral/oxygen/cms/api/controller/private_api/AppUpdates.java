package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.AppUpdate;
import com.ladbrokescoral.oxygen.cms.api.service.AppUpdateService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AppUpdates extends AbstractCrudController<AppUpdate> {

  @Autowired
  public AppUpdates(final AppUpdateService service) {
    super(service);
  }

  @PostMapping(value = "app-update")
  @Override
  public ResponseEntity create(@RequestBody AppUpdate entity) {
    return super.create(entity);
  }

  @GetMapping(value = "app-update")
  @Override
  public List<AppUpdate> readAll() {
    return super.readAll();
  }

  @GetMapping(value = "app-update/{id}")
  @Override
  public AppUpdate read(@PathVariable String id) {
    return super.read(id);
  }

  @PutMapping(value = "app-update/{id}")
  @Override
  public AppUpdate update(@PathVariable String id, @RequestBody AppUpdate entity) {
    return super.update(id, entity);
  }

  @DeleteMapping(value = "app-update/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }
}
