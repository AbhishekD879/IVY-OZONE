package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ConnectMenu;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.ConnectMenuService;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class ConnectMenus extends AbstractSortableController<ConnectMenu> {

  private final ConnectMenuService menuService;

  @Autowired
  ConnectMenus(ConnectMenuService crudService) {
    super(crudService);
    this.menuService = crudService;
  }

  @PostMapping("connect-menu")
  @Override
  public ResponseEntity create(@RequestBody ConnectMenu entity) {
    return super.create(entity);
  }

  @GetMapping("connect-menu")
  @Override
  public List<ConnectMenu> readAll() {
    return super.readAll();
  }

  @GetMapping("connect-menu/{id}")
  @Override
  public ConnectMenu read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("connect-menu/brand/{brand}")
  @Override
  public List<ConnectMenu> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("connect-menu/{id}")
  @Override
  public ConnectMenu update(@PathVariable String id, @RequestBody ConnectMenu entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("connect-menu/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    ConnectMenu menu = menuService.findOne(id).orElseThrow(NotFoundException::new);
    menuService.removeImage(menu);
    return delete(Optional.of(menu));
  }

  @PostMapping("connect-menu/{id}/image")
  public ResponseEntity uploadImage(
      @RequestParam("file") MultipartFile file, @PathVariable("id") String id) {
    Optional<ConnectMenu> maybeEntity = menuService.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<ConnectMenu> menu = menuService.attachImage(maybeEntity.get(), file);

    return menu.map(menuService::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to upload image", HttpStatus.BAD_REQUEST));
  }

  @DeleteMapping("connect-menu/{id}/image")
  public ResponseEntity removeImage(@PathVariable("id") String id) {
    Optional<ConnectMenu> maybeEntity = menuService.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<ConnectMenu> removeResult = menuService.removeImage(maybeEntity.get());

    return removeResult
        .map(menuService::save)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity("Failed to remove image", HttpStatus.BAD_REQUEST));
  }

  @PostMapping("connect-menu/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
