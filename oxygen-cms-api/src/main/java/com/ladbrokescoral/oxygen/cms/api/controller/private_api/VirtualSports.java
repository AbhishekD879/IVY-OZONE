package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.service.VirtualSportService;
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
public class VirtualSports extends AbstractSortableController<VirtualSport> {
  private final VirtualSportService virtualSportService;

  VirtualSports(VirtualSportService virtualSportService) {
    super(virtualSportService);
    this.virtualSportService = virtualSportService;
  }

  @Override
  @GetMapping("/virtual-sport")
  public List<VirtualSport> readAll() {
    return super.readAll();
  }

  @GetMapping("virtual-sport/brand/{brand}")
  public List<VirtualSportWithTracksRefs> findSportsWithTracksRefsByBrand(
      @PathVariable String brand) {
    return virtualSportService.findSportsWithTracksRefsByBrand(brand);
  }

  @Override
  @PostMapping("virtual-sport/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @Override
  @PostMapping("/virtual-sport")
  public ResponseEntity create(@Valid @RequestBody VirtualSport entity) {
    return super.create(entity);
  }

  @Override
  @GetMapping("/virtual-sport/{id}")
  public VirtualSport read(@PathVariable("id") String id) {
    return super.read(id);
  }

  @Override
  @PutMapping("/virtual-sport/{id}")
  public VirtualSport update(
      @PathVariable("id") String id, @Valid @RequestBody VirtualSport updateEntity) {
    return super.update(id, updateEntity);
  }

  @Override
  @DeleteMapping("/virtual-sport/{id}")
  public ResponseEntity delete(@PathVariable("id") String id) {
    return super.delete(id);
  }

  @PostMapping("virtual-sport/{id}/icon")
  public VirtualSport uploadIcon(
      @PathVariable("id") String id, @RequestParam("file") MultipartFile icon) {
    return virtualSportService.attachIcon(id, icon);
  }

  @DeleteMapping("virtual-sport/{id}/icon")
  public VirtualSport removeIcon(@PathVariable("id") String id) {
    return virtualSportService.removeIcon(id);
  }
}
