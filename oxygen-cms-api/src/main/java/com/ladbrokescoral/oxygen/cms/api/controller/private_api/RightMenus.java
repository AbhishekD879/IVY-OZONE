package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FileType;
import com.ladbrokescoral.oxygen.cms.api.entity.RightMenu;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.RightMenuService;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class RightMenus extends AbstractSortableController<RightMenu> {

  private final RightMenuService service;

  @Autowired
  RightMenus(RightMenuService crudService) {
    super(crudService);
    this.service = crudService;
  }

  @GetMapping("right-menu")
  @Override
  public List<RightMenu> readAll() {
    return super.readAll();
  }

  @GetMapping("right-menu/{id}")
  @Override
  public RightMenu read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("right-menu/brand/{brand}")
  @Override
  public List<RightMenu> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("right-menu")
  @Override
  public ResponseEntity<RightMenu> create(@RequestBody RightMenu entity) {
    return super.create(entity);
  }

  @PutMapping("right-menu/{id}")
  @Override
  public RightMenu update(@PathVariable String id, @RequestBody RightMenu entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("right-menu/{id}")
  @Override
  public ResponseEntity<RightMenu> delete(@PathVariable String id) {
    RightMenu menu = service.findOne(id).orElseThrow(NotFoundException::new);

    service.removeImage(menu);
    service.removeSvgImage(menu);

    return delete(Optional.of(menu));
  }

  @PostMapping("right-menu/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @PostMapping("right-menu/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id,
      @RequestParam("file") MultipartFile file,
      @RequestParam(value = "fileType", defaultValue = "image", required = false)
          FileType fileType) {
    Optional<RightMenu> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<RightMenu> rightMenu = Optional.empty();
    if (fileType.equals(FileType.IMAGE)
        && !file.getOriginalFilename().toLowerCase().contains(".svg")) {
      rightMenu = service.attachImage(maybeEntity.get(), file);
    }
    if (fileType.equals(FileType.SVG)
        || file.getOriginalFilename().toLowerCase().contains(".svg")) {
      rightMenu = service.attachSvgImage(maybeEntity.get(), file);
    }

    return rightMenu.map(service::save).map(ResponseEntity::ok).orElseGet(failedToUpdateImage());
  }

  @DeleteMapping("right-menu/{id}/image")
  public ResponseEntity removeImage(
      @PathVariable("id") String id,
      @RequestParam(value = "fileType", defaultValue = "image", required = false)
          FileType fileType) {
    Optional<RightMenu> maybeEntity = service.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    Optional<RightMenu> removeResult = Optional.empty();
    if (fileType.equals(FileType.IMAGE)) {
      removeResult = service.removeImage(maybeEntity.get());
    }
    if (fileType.equals(FileType.SVG)) {
      removeResult = service.removeSvgImage(maybeEntity.get());
    }

    return removeResult.map(service::save).map(ResponseEntity::ok).orElseGet(failedToRemoveImage());
  }
}
