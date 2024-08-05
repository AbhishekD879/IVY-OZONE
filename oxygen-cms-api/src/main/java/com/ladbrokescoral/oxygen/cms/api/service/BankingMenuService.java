package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.BankingMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.BankingMenuExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.BankingMenuRepository;
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
public class BankingMenuService extends AbstractMenuService<BankingMenu> {

  private final BankingMenuExtendedRepository extendedRepository;
  private final ImageEntityService<BankingMenu> imageEntityService;
  private final SvgEntityService<BankingMenu> svgEntityService;

  private final ImagePath bankingMenuImagePath;

  @Autowired
  public BankingMenuService(
      BankingMenuRepository repository,
      BankingMenuExtendedRepository extendedRepository,
      ImageEntityService<BankingMenu> imageEntityService,
      SvgEntityService<BankingMenu> svgEntityService,
      ImagePath bankingMenuImagePath) {
    super(repository);
    this.extendedRepository = extendedRepository;
    this.imageEntityService = imageEntityService;
    this.svgEntityService = svgEntityService;

    this.bankingMenuImagePath = bankingMenuImagePath;
  }

  public List<BankingMenu> findAllByBrand(String brand) {
    return extendedRepository.findMenus(brand);
  }

  public Optional<BankingMenu> attachImage(
      BankingMenu menu, @ValidFileType("png") MultipartFile file) {
    return imageEntityService.attachAllSizesImage(menu, file, bankingMenuImagePath);
  }

  /**
   * @deprecated use SvgImages api to create new images and use update the menu endpoint to set the
   *     svg Id delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public Optional<BankingMenu> attachSvgImage(
      BankingMenu menu, @ValidFileType("svg") MultipartFile file) {
    return svgEntityService.attachSvgImage(menu, file, bankingMenuImagePath.getSvgMenuPath());
  }

  public Optional<BankingMenu> removeImage(BankingMenu menu) {
    return imageEntityService.removeAllSizesImage(menu);
  }

  /**
   * @deprecated use SvgImages api to delete images and use update the menu endpoint to set the
   *     svgId to null delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public Optional<BankingMenu> removeSvgImage(BankingMenu menu) {
    return svgEntityService.removeSvgImage(menu);
  }
}
