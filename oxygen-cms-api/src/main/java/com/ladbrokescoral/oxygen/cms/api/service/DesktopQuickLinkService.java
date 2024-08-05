package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.DesktopQuickLink;
import com.ladbrokescoral.oxygen.cms.api.repository.DesktopQuickLinkRepository;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig.ImagePath;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.multipart.MultipartFile;

@Component
@Validated
public class DesktopQuickLinkService extends SortableService<DesktopQuickLink> {

  private final DesktopQuickLinkRepository desktopQuickLinkRepository;
  private final ImageEntityService<DesktopQuickLink> imageEntityService;

  private final ImagePath desktopQuickLinkImagePath;

  @Autowired
  public DesktopQuickLinkService(
      DesktopQuickLinkRepository desktopQuickLinkRepository,
      ImageEntityService<DesktopQuickLink> imageEntityService,
      ImagePath desktopQuickLinkImagePath) {
    super(desktopQuickLinkRepository);
    this.desktopQuickLinkRepository = desktopQuickLinkRepository;
    this.imageEntityService = imageEntityService;

    this.desktopQuickLinkImagePath = desktopQuickLinkImagePath;
  }

  public List<DesktopQuickLink> findAllByBrandAndDisabled(String brand) {
    return desktopQuickLinkRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, false);
  }

  public Optional<DesktopQuickLink> attachImage(
      DesktopQuickLink menu, @ValidFileType("png") MultipartFile file) {
    return imageEntityService.attachAllSizesImage(menu, file, desktopQuickLinkImagePath);
  }

  public Optional<DesktopQuickLink> removeImage(DesktopQuickLink menu) {
    return imageEntityService.removeAllSizesImage(menu);
  }
}
