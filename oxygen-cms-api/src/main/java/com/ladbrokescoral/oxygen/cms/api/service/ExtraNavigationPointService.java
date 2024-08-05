package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.AutomaticUpdateDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ExtraNavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.repository.ExtraNavigationPointRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ExtraNavigationPointService extends SortableService<ExtraNavigationPoint> {

  private static final String PREFIX = "SB:";
  private AutomaticUpdateService automaticUpdateService;

  @Autowired
  public ExtraNavigationPointService(
      ExtraNavigationPointRepository extraNavigationPointRepository,
      AutomaticUpdateService automaticUpdateService) {
    super(extraNavigationPointRepository);
    this.automaticUpdateService = automaticUpdateService;
  }

  @Override
  public boolean isNewElementCreatedFirstInTheList() {
    return false;
  }

  public List<ExtraNavigationPoint> getAllExtraNavPtsByBrandSorted(String brand) {
    return super.findByBrand(brand);
  }

  @Override
  public ExtraNavigationPoint update(
      ExtraNavigationPoint existingEntity, ExtraNavigationPoint updateEntity) {
    if (!updateEntity.getTitle().equalsIgnoreCase(existingEntity.getTitle())) {
      AutomaticUpdateDto automaticUpdateDto = new AutomaticUpdateDto();
      automaticUpdateDto.setId(updateEntity.getId());
      automaticUpdateDto.setBrand(updateEntity.getBrand());
      automaticUpdateDto.setUpdatedTitle(PREFIX + updateEntity.getTitle());
      this.automaticUpdateService.doUpdate(automaticUpdateDto);
    }
    return super.update(existingEntity, updateEntity);
  }
}
