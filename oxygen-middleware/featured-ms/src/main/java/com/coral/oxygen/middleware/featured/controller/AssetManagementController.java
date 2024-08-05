package com.coral.oxygen.middleware.featured.controller;

import com.coral.oxygen.middleware.common.service.AssetManagementService;
import com.coral.oxygen.middleware.pojos.model.output.AssetManagement;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/featured/asset-management")
@RequiredArgsConstructor
@ConditionalOnProperty(name = "featured.scheduled.task.enabled")
public class AssetManagementController {

  private final AssetManagementService assetManagementService;

  @GetMapping
  public Iterable<AssetManagement> getAll() {
    return assetManagementService.findAll();
  }
}
