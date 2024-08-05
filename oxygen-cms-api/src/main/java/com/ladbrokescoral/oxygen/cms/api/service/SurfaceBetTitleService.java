package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.SurfaceBetTitle;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.SurfaceBetTitleRepository;
import java.util.List;
import java.util.Objects;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class SurfaceBetTitleService extends AbstractService<SurfaceBetTitle> {
  private final SurfaceBetTitleRepository titleRepository;

  public SurfaceBetTitleService(SurfaceBetTitleRepository titleRepository) {
    super(titleRepository);
    this.titleRepository = titleRepository;
  }

  public List<SurfaceBetTitle> findAllSurfaceBetTitle(String brand) {
    return titleRepository.findByBrand(brand);
  }

  public SurfaceBetTitle findSurfaceBetTitleByTitle(String title) {
    return titleRepository.findByTitle(title);
  }

  public void deleteSBTitleByBrandAndId(String brand, String id) {
    SurfaceBetTitle surfaceBetTitle = titleRepository.findByBrandAndId(brand, id);
    if (Objects.isNull(surfaceBetTitle)) {
      throw new NotFoundException();
    }
    titleRepository.deleteByBrandAndId(brand, id);
  }
}
