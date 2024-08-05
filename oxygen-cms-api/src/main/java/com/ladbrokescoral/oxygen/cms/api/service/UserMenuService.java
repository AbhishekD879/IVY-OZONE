package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.UserMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.UserMenuRepository;
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
public class UserMenuService extends AbstractMenuService<UserMenu> {

  private final UserMenuRepository userMenuRepository;
  private final ImageEntityService<UserMenu> imageEntityService;
  private final SvgEntityService<UserMenu> svgEntityService;
  private final ImagePath userMenuImagePath;

  @Autowired
  public UserMenuService(
      UserMenuRepository userMenuRepository,
      ImageEntityService<UserMenu> imageEntityService,
      SvgEntityService<UserMenu> svgEntityService,
      ImagePath userMenuImagePath) {
    super(userMenuRepository);
    this.userMenuRepository = userMenuRepository;
    this.imageEntityService = imageEntityService;
    this.svgEntityService = svgEntityService;

    this.userMenuImagePath = userMenuImagePath;
  }

  public List<UserMenu> findAllByBrandAndDisabled(String brand) {
    return userMenuRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE);
  }

  public Optional<UserMenu> attachImage(
      UserMenu menu, @ValidFileType({"png", "jpg", "jpeg"}) MultipartFile file) {
    return imageEntityService.attachAllSizesImage(menu, file, userMenuImagePath);
  }

  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public Optional<UserMenu> attachSvgImage(
      UserMenu menu, @ValidFileType("svg") MultipartFile file) {
    return svgEntityService.attachSvgImage(menu, file, userMenuImagePath.getSvgMenuPath());
  }

  public Optional<UserMenu> removeImage(UserMenu menu) {
    return imageEntityService.removeAllSizesImage(menu);
  }

  /**
   * @deprecated use SvgImages api to remove images delete after release-103.0.0 goes live (check
   *     with ui)
   */
  @Deprecated
  public Optional<UserMenu> removeSvgImage(UserMenu menu) {
    return svgEntityService.removeSvgImage(menu);
  }
}
