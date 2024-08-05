package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FileType;
import com.ladbrokescoral.oxygen.cms.api.entity.UserMenu;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.UserMenuService;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
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
public class UserMenus extends AbstractSortableController<UserMenu> {

  private final UserMenuService service;

  @Autowired
  UserMenus(UserMenuService crudService) {
    super(crudService);
    this.service = crudService;
  }

  @GetMapping("user-menu")
  @Override
  public List<UserMenu> readAll() {
    return super.readAll();
  }

  @GetMapping("user-menu/{id}")
  @Override
  public UserMenu read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("user-menu/brand/{brand}")
  @Override
  public List<UserMenu> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("user-menu")
  @Override
  public ResponseEntity create(@RequestBody UserMenu entity) {
    return super.create(entity);
  }

  @PutMapping("user-menu/{id}")
  @Override
  public UserMenu update(@PathVariable String id, @RequestBody UserMenu entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("user-menu/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    UserMenu menu = service.findOne(id).orElseThrow(NotFoundException::new);
    service.removeImage(menu);
    service.removeSvgImage(menu);

    return delete(Optional.of(menu));
  }

  @PostMapping("user-menu/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @PostMapping("user-menu/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id,
      @RequestParam("file") MultipartFile file,
      @RequestParam(value = "fileType", defaultValue = "image", required = false)
          FileType fileType) {
    Optional<UserMenu> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<UserMenu> userMenu = Optional.empty();
    if (fileType.equals(FileType.IMAGE)) {
      userMenu = service.attachImage(maybeEntity.get(), file);
    }
    if (fileType.equals(FileType.SVG)) {
      userMenu = service.attachSvgImage(maybeEntity.get(), file);
    }

    return userMenu
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to upload image", HttpStatus.BAD_REQUEST));
  }

  @DeleteMapping("user-menu/{id}/image")
  public ResponseEntity removeImage(
      @PathVariable("id") String id,
      @RequestParam(value = "fileType", defaultValue = "image", required = false)
          FileType fileType) {
    Optional<UserMenu> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<UserMenu> removeResult = Optional.empty();
    if (fileType.equals(FileType.IMAGE)) {
      removeResult = service.removeImage(maybeEntity.get());
    }
    if (fileType.equals(FileType.SVG)) {
      removeResult = service.removeSvgImage(maybeEntity.get());
    }

    return removeResult
        .map(service::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to remove image", HttpStatus.BAD_REQUEST));
  }
}
