package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.FileType;
import com.ladbrokescoral.oxygen.cms.api.entity.GameMenu;
import com.ladbrokescoral.oxygen.cms.api.exception.EntityOperationException;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.GameMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import java.util.List;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;
import org.springframework.web.multipart.MultipartFile;

@Service
public class GameMenuService extends SortableService<GameMenu> {
  private final GameMenuRepository gameMenuRepository;
  private final SvgEntityService<GameMenu> svgEntityService;
  private final String svgMenuPath;
  private final ImageService imageService;
  private String pngMenuPath;

  public GameMenuService(
      GameMenuRepository repository,
      SvgEntityService<GameMenu> svgEntityService,
      @Value("${images.gamemenu.svg}") String svgMenuPath,
      ImageService imageEntityService,
      @Value("${images.gamemenu.png}") String pngMenuPath) {
    super(repository);
    this.gameMenuRepository = repository;
    this.svgEntityService = svgEntityService;
    this.svgMenuPath = svgMenuPath;
    this.imageService = imageEntityService;
    this.pngMenuPath = pngMenuPath;
  }

  public List<GameMenu> findAllByUrl(String url) {
    return gameMenuRepository.findAllByUrl(url);
  }

  public List<GameMenu> findAllByUrlAndBrand(String url, String brand) {
    return gameMenuRepository.findAllByUrlAndBrand(url, brand);
  }

  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public GameMenu attachSvgImage(String id, @ValidFileType("svg") MultipartFile file) {
    GameMenu gameMenu = findOne(id).orElseThrow(NotFoundException::new);
    return svgEntityService
        .attachSvgImage(gameMenu, file, svgMenuPath)
        .map(gameMenuRepository::save)
        .orElseThrow(() -> new EntityOperationException("Couldn't upload an image"));
  }

  /**
   * @deprecated use SvgImages api to delete images and use update the menu endpoint to set the
   *     svgId to null delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public GameMenu removeSvgImage(String id) {
    GameMenu gameMenu = findOne(id).orElseThrow(NotFoundException::new);
    return svgEntityService
        .removeSvgImage(gameMenu)
        .map(gameMenuRepository::save)
        .orElseThrow(() -> new EntityOperationException("Couldn't remove an image"));
  }

  @Override
  public void delete(String id) {
    GameMenu gameMenu = findOne(id).orElseThrow(NotFoundException::new);
    gameMenuRepository.delete(gameMenu);
    svgEntityService.removeSvgImage(gameMenu);
    removePngImage(gameMenu);
  }

  private boolean removePngImage(GameMenu gameMenu) {
    boolean removed = false;
    if (!ObjectUtils.isEmpty(gameMenu.getPngFilename())) {
      removed =
          imageService.removeImage(gameMenu.getBrand(), gameMenu.getPngFilename().getFullPath());
    }
    return removed;
  }

  public GameMenu attachImage(String id, MultipartFile image, FileType fileType) {
    GameMenu gameMenu;
    switch (fileType) {
      case SVG:
        gameMenu = attachSvgImage(id, image);
        break;
      case IMAGE:
        gameMenu = attachPngImage(id, image);
        break;
      default:
        throw new UnsupportedOperationException("GameMenus supports only svg & png images");
    }
    return gameMenu;
  }

  private GameMenu attachPngImage(String id, MultipartFile image) {
    GameMenu gameMenu = findOne(id).orElseThrow(NotFoundException::new);
    return imageService
        .upload(gameMenu.getBrand(), image, pngMenuPath)
        .map(
            f -> {
              gameMenu.setPngFilename(f);
              return gameMenu;
            })
        .map(gameMenuRepository::save)
        .orElseThrow(() -> new EntityOperationException("Couldn't upload an image"));
  }

  public GameMenu removeImage(String id, FileType fileType) {
    GameMenu gameMenu;
    switch (fileType) {
      case SVG:
        gameMenu = removeSvgImage(id);
        break;
      case IMAGE:
        gameMenu = removePngImage(id);
        break;
      default:
        throw new UnsupportedOperationException("GameMenus supports only svg & png images");
    }
    return gameMenu;
  }

  private GameMenu removePngImage(String id) {
    GameMenu gameMenu = findOne(id).orElseThrow(NotFoundException::new);
    if (!removePngImage(gameMenu)) {
      throw new FileUploadException("Can't remove file");
    }
    gameMenu.setPngFilename(null);
    repository.save(gameMenu);
    return gameMenu;
  }
}
