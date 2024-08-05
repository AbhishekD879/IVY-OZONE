package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.SvgMigration;
import com.ladbrokescoral.oxygen.cms.api.service.SvgMigrationService;
import java.time.Instant;
import java.util.List;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import lombok.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class SvgMigrate implements Abstract {

  private final SvgMigrationService service;

  @GetMapping("migrate-svgs/{brand}/start")
  public ResponseEntity<SvgMigrationStatus> start(@PathVariable String brand) {
    return ResponseEntity.ok(new SvgMigrationStatus(service.start(brand)));
  }

  @GetMapping("migrate-svgs/{brand}/active")
  public ResponseEntity<SvgMigrationStatus> active(@PathVariable String brand) {
    return ResponseEntity.ok(new SvgMigrationStatus(service.active(brand)));
  }

  @GetMapping("migrate-svgs/{brand}/last")
  public ResponseEntity<SvgMigrationStatus> last(@PathVariable String brand) {
    return ResponseEntity.ok(new SvgMigrationStatus(service.last(brand)));
  }

  @GetMapping("migrate-svgs/{brand}/{id}")
  public ResponseEntity<SvgMigrationStatus> migrationById(
      @PathVariable String brand, @PathVariable String id) {
    return ResponseEntity.ok(new SvgMigrationStatus(service.showById(id)));
  }

  @GetMapping("migrate-svgs/{brand}")
  public ResponseEntity<List<SvgMigrationStatusMin>> showAll(@PathVariable String brand) {
    List<SvgMigrationStatusMin> response =
        service.findAllByBrand(brand).stream()
            .map(SvgMigrationStatusMin::new)
            .collect(Collectors.toList());
    return ResponseEntity.ok(response);
  }
}

@Value
class SvgMigrationStatus {

  String id;
  String status;
  String messages;
  Instant updatedAt;
  Instant createdAt;

  SvgMigrationStatus(SvgMigration entity) {
    id = entity.getId();
    status = entity.getStatus();
    messages = entity.getMessages();
    updatedAt = entity.getUpdatedAt();
    createdAt = entity.getCreatedAt();
  }
}

@Value
class SvgMigrationStatusMin {

  String id;
  String status;
  Instant updatedAt;
  Instant createdAt;

  SvgMigrationStatusMin(SvgMigration entity) {
    id = entity.getId();
    status = entity.getStatus();
    updatedAt = entity.getUpdatedAt();
    createdAt = entity.getCreatedAt();
  }
}
