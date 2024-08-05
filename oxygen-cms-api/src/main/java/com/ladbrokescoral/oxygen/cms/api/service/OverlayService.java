package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Overlay;
import com.ladbrokescoral.oxygen.cms.api.exception.BadRequestException;
import com.ladbrokescoral.oxygen.cms.api.repository.OverlayRepository;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/** OverlayService */
@Service
public class OverlayService extends SortableService<Overlay> {

  private final OverlayRepository overlayRepository;

  @Autowired
  public OverlayService(OverlayRepository overlayRepository) {
    super(overlayRepository);
    this.overlayRepository = overlayRepository;
  }

  @Override
  public List<Overlay> findByBrand(String brand) {
    return overlayRepository.findByBrand(brand);
  }

  public Optional<Overlay> findOneByBrand(String brand) {
    return overlayRepository.findOneByBrand(brand);
  }

  @Override
  public Overlay prepareModelBeforeSave(Overlay overlay) {
    Optional<Overlay> mayBeEntity = overlayRepository.findOneByBrand(overlay.getBrand());
    if (mayBeEntity.isPresent() && overlay.isNew()) {
      throw new BadRequestException("there is already one entity present");
    }
    return overlay;
  }
}
