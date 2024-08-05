package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.ConnectMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.ConnectMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@Component
@Validated
public class ConnectMenuService extends AbstractMenuService<ConnectMenu> {

  private final ConnectMenuRepository connectMenuRepository;
  private final SvgEntityService<ConnectMenu> svgEntityService;
  private String connectMenuImagePath;

  @Autowired
  public ConnectMenuService(
      ConnectMenuRepository connectMenuRepository,
      SvgEntityService<ConnectMenu> svgEntityService,
      @Value("${images.connectmenus}") String connectMenuImagePath) {
    super(connectMenuRepository);
    this.connectMenuRepository = connectMenuRepository;
    this.svgEntityService = svgEntityService;
    this.connectMenuImagePath = connectMenuImagePath;
  }

  public List<ConnectMenu> findAllByBrandAndDisabled(String brand) {
    return connectMenuRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE);
  }

  /**
   * @deprecated use SvgImages api to create new images and use update the menu endpoint to set the
   *     svg Id delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public Optional<ConnectMenu> attachImage(
      ConnectMenu menu, @ValidFileType("svg") MultipartFile file) {
    return svgEntityService.attachSvgImage(menu, file, connectMenuImagePath);
  }

  /**
   * @deprecated use SvgImages api to delete images and use update the menu endpoint to set the
   *     svgId to null delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public Optional<ConnectMenu> removeImage(ConnectMenu menu) {
    return svgEntityService.removeSvgImage(menu);
  }
}
