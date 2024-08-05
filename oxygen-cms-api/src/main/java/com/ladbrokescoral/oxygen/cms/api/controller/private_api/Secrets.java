package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SecretBaseDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SecretDetailedDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Secret;
import com.ladbrokescoral.oxygen.cms.api.mapping.SecretMapper;
import com.ladbrokescoral.oxygen.cms.api.service.SecretService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import java.util.List;
import java.util.stream.Collectors;
import javax.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class Secrets extends AbstractCrudController<Secret> {

  private final SecretService secretService;
  private final SecretMapper mapper;

  public Secrets(SecretService crudService, SecretMapper mapper) {
    super(crudService);
    this.secretService = crudService;
    this.mapper = mapper;
  }

  @GetMapping("secret")
  public List<SecretBaseDto> readAllSecrets() {
    return super.readAll().stream().map(mapper::toBaseDto).collect(Collectors.toList());
  }

  @GetMapping("secret/brand/{brand}")
  public List<SecretBaseDto> readSecretsByBrand(@PathVariable @Brand String brand) {
    return super.readByBrand(brand).stream().map(mapper::toBaseDto).collect(Collectors.toList());
  }

  @GetMapping("secret/{id}")
  public SecretDetailedDto readDetailed(@PathVariable String id) {
    return mapper.toDetailedDto(super.read(id));
  }

  @GetMapping("secret/{id}/decoded")
  public SecretDetailedDto readDetailedDecoded(@PathVariable String id) {
    return mapper.toDetailedDto(secretService.readDecoded(id));
  }

  @PostMapping("secret")
  public ResponseEntity<SecretDetailedDto> create(@RequestBody @Valid SecretDetailedDto dto) {
    Secret newEntity = mapper.toEntity(dto);
    return ResponseEntity.ok(mapper.toDetailedDto(super.createEntity(newEntity)));
  }

  @PutMapping("secret/{id}")
  public SecretDetailedDto update(
      @PathVariable String id, @RequestBody @Valid SecretDetailedDto dto) {
    return mapper.toDetailedDto(super.update(id, mapper.toEntity(dto)));
  }

  @DeleteMapping("secret/{id}")
  @Override
  public ResponseEntity<Secret> delete(@PathVariable String id) {
    return super.delete(secretService.beforeDelete(id));
  }
}
