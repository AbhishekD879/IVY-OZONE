package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class Users extends AbstractCrudController<User> {

  @Autowired
  public Users(final CrudService<User> service) {
    super(service);
  }

  @PostMapping("user")
  @Override
  public ResponseEntity<User> create(@Validated @RequestBody User entity) {
    return super.create(entity);
  }

  @GetMapping("user")
  @Override
  public List<User> readAll() {
    return super.readAll();
  }

  @GetMapping("user/{id}")
  @Override
  public User read(@PathVariable String id) {
    return super.read(id);
  }

  @PutMapping("user/{id}")
  @Override
  public User update(@PathVariable String id, @RequestBody User entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("user/{id}")
  @Override
  public ResponseEntity<User> delete(@PathVariable String id) {
    return super.delete(id);
  }
}
