package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.TopGame;
import com.ladbrokescoral.oxygen.cms.api.repository.TopGameRepository;
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
public class TopGameService extends SortableService<TopGame> {

  private final TopGameRepository topGameRepository;
  private final ImageEntityService<TopGame> imageEntityService;
  private final IconEntityService<TopGame> iconEntityService;

  private final ImagePath topGameMenuImagePath;
  private final ImagePath topGameIcon;

  @Autowired
  public TopGameService(
      TopGameRepository topGameRepository,
      ImageEntityService<TopGame> imageEntityService,
      IconEntityService<TopGame> iconEntityService,
      ImagePath topGameMenuImagePath,
      ImagePath topGameIcon) {
    super(topGameRepository);
    this.topGameRepository = topGameRepository;
    this.imageEntityService = imageEntityService;
    this.iconEntityService = iconEntityService;
    this.topGameIcon = topGameIcon;
    this.topGameMenuImagePath = topGameMenuImagePath;
  }

  public List<TopGame> findAllByBrandSorted(String brand) {
    return topGameRepository.findAllByBrandOrderBySortOrderAsc(brand);
  }

  public Optional<TopGame> attachImage(TopGame menu, @ValidFileType("png") MultipartFile file) {
    return imageEntityService.attachAllSizesImage(menu, file, topGameMenuImagePath);
  }

  public Optional<TopGame> attachIcon(TopGame menu, @ValidFileType("png") MultipartFile file) {
    return iconEntityService.attachAllSizesIcon(menu, file, topGameIcon);
  }

  public Optional<TopGame> removeImage(TopGame menu) {
    return imageEntityService.removeAllSizesImage(menu);
  }

  public Optional<TopGame> removeIcon(TopGame menu) {
    return iconEntityService.removeAllSizesIcon(menu);
  }
}
