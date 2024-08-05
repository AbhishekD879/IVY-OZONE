package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.Post;
import com.ladbrokescoral.oxygen.cms.api.service.PostService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class Posts extends AbstractCrudController<Post> {
  @Autowired
  Posts(PostService crudService) {
    super(crudService);
  }

  @PostMapping("post")
  @Override
  public ResponseEntity create(@RequestBody Post entity) {
    return super.create(entity);
  }

  @GetMapping("post")
  @Override
  public List<Post> readAll() {
    return super.readAll();
  }

  @GetMapping("post/{id}")
  @Override
  public Post read(@PathVariable String id) {
    return super.read(id);
  }

  @PutMapping("post/{id}")
  @Override
  public Post update(@PathVariable String id, @RequestBody Post entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("post/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }
}
