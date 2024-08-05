package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static com.ladbrokescoral.oxygen.cms.api.controller.private_api.AbstractCrudController.notFound;

import com.ladbrokescoral.oxygen.cms.api.dto.SecretDetailedDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SecretPublicService;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.enums.ParameterIn;
import io.swagger.v3.oas.annotations.media.Schema;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SecretApi implements Public {

  private final SecretPublicService service;

  public static final String REQUEST_HEADER_X_API_KEY_NAME = "x-api-key";

  @Autowired
  public SecretApi(SecretPublicService service) {
    this.service = service;
  }

  @Parameter(
      name = REQUEST_HEADER_X_API_KEY_NAME,
      in = ParameterIn.HEADER,
      required = true,
      schema = @Schema(type = "string"))
  @GetMapping(value = "secured/{brand}/secret/{uri}")
  public ResponseEntity<SecretDetailedDto> findSecretByBrandAndUri(
      @PathVariable("brand") String brand, @PathVariable("uri") String uri) {
    return service.findSecret(brand, uri).map(ResponseEntity::ok).orElseGet(notFound());
  }
}
