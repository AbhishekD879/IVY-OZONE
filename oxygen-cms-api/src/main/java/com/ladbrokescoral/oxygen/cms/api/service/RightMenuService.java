package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.RightMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.RightMenuExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.RightMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig.ImagePath;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@Component
@Validated
public class RightMenuService extends AbstractMenuService<RightMenu> {

  private final RightMenuExtendedRepository extendedRepository;
  private final ImageEntityService<RightMenu> imageEntityService;
  private final SvgEntityService<RightMenu> svgEntityService;
  private final ImagePath rightMenuImagePath;

  @Autowired
  public RightMenuService(
      RightMenuRepository repository,
      RightMenuExtendedRepository extendedRepository,
      ImageEntityService<RightMenu> imageEntityService,
      SvgEntityService<RightMenu> svgEntityService,
      ImagePath rightMenuImagePath) {
    super(repository);
    this.extendedRepository = extendedRepository;
    this.imageEntityService = imageEntityService;
    this.svgEntityService = svgEntityService;
    this.rightMenuImagePath = rightMenuImagePath;
  }

  public List<RightMenu> findAllByBrand(String brand) {
    return extendedRepository.findRightMenus(brand);
  }

  public Optional<RightMenu> attachImage(RightMenu menu, @ValidFileType("png") MultipartFile file) {
    return imageEntityService.attachAllSizesImage(menu, file, rightMenuImagePath);
  }

  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public Optional<RightMenu> attachSvgImage(
      RightMenu menu, @ValidFileType("svg") MultipartFile file) {
    return svgEntityService.attachSvgImage(menu, file, rightMenuImagePath.getSvgMenuPath());
  }

  public Optional<RightMenu> removeImage(RightMenu menu) {
    return imageEntityService.removeAllSizesImage(menu);
  }

  /**
   * @deprecated use SvgImages api to remove images and use update the menu endpoint to set the
   *     svgId to null delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public Optional<RightMenu> removeSvgImage(RightMenu menu) {
    return svgEntityService.removeSvgImage(menu);
  }
}
