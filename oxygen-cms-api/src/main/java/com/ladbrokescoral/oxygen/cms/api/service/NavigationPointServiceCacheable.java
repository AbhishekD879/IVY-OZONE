package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.NavigationPointDto;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;

@Service
@Primary
public class NavigationPointServiceCacheable extends AbstractService<NavigationPoint> {

  private final NavigationPointService navigationPointService;

  @Autowired
  public NavigationPointServiceCacheable(NavigationPointService navigationPointService) {
    super(navigationPointService.navigationPointRepository);
    this.navigationPointService = navigationPointService;
  }

  @Cacheable("navigation-points")
  public List<NavigationPointDto> getNavigationPointByBrandEnabled(
      @PathVariable("brand") String brand) {
    return navigationPointService.getNavigationPointByBrandEnabled(
        brand, SegmentConstants.UNIVERSAL, null);
  }

  @CacheEvict(
      cacheNames = {"navigation-points"},
      key = "#entity.id")
  public NavigationPoint save(NavigationPoint entity) {
    return navigationPointService.save(entity);
  }

  @CacheEvict(
      cacheNames = {"navigation-points"},
      key = "#id")
  @Override
  public void delete(String id) {
    navigationPointService.delete(id);
  }
}
