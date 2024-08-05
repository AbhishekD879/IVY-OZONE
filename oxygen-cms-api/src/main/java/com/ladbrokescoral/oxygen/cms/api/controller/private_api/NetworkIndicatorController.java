package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.NetworkIndicatorRequest;
import com.ladbrokescoral.oxygen.cms.api.entity.NetworkIndicatorConfig;
import com.ladbrokescoral.oxygen.cms.api.service.NetworkIndicatorService;
import javax.validation.Valid;
import org.springframework.beans.BeanUtils;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class NetworkIndicatorController extends AbstractSortableController<NetworkIndicatorConfig> {

  private NetworkIndicatorService networkIndicatorService;

  NetworkIndicatorController(NetworkIndicatorService networkIndicatorService) {
    super(networkIndicatorService);
    this.networkIndicatorService = networkIndicatorService;
  }

  @PostMapping("networkIndicator")
  public ResponseEntity<NetworkIndicatorConfig> create(
      @RequestBody @Valid NetworkIndicatorRequest connectionRequest) {
    NetworkIndicatorConfig networkConnectionIndicator = new NetworkIndicatorConfig();
    BeanUtils.copyProperties(connectionRequest, networkConnectionIndicator);
    return super.create(networkConnectionIndicator);
  }

  @GetMapping("networkIndicator/{id}")
  @Override
  public NetworkIndicatorConfig read(@PathVariable String id) {
    return super.read(id);
  }

  @PutMapping("networkIndicator/{id}")
  public NetworkIndicatorConfig update(
      @PathVariable String id, @RequestBody NetworkIndicatorRequest entity) {
    NetworkIndicatorConfig networkConnectionIndicator = new NetworkIndicatorConfig();
    BeanUtils.copyProperties(entity, networkConnectionIndicator);
    return super.update(id, networkConnectionIndicator);
  }

  @GetMapping("networkIndicator/brand/{brand}")
  public ResponseEntity<NetworkIndicatorConfig> readOneByBrand(@PathVariable String brand) {
    return networkIndicatorService.readOneByBrand(brand);
  }
}
