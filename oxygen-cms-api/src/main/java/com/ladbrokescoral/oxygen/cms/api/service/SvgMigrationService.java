package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSport;
import com.ladbrokescoral.oxygen.cms.api.entity.ConnectMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterLogo;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.HighlightCarousel;
import com.ladbrokescoral.oxygen.cms.api.entity.OddsBoostConfigEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.RightMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.Sport;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportQuickLink;
import com.ladbrokescoral.oxygen.cms.api.entity.SurfaceBet;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgBackup;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgFilename;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgImage;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgMigration;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgSprite;
import com.ladbrokescoral.oxygen.cms.api.exception.SvgImageParseException;
import com.ladbrokescoral.oxygen.cms.api.repository.ConnectMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.FooterLogoRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.FooterMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.HighlightCarouselRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.OddsBoostConfigurationRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.RightMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportQuickLinkRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SurfaceBetRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SvgBackupRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SvgImageRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SvgMigrationRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.VirtualSportRepository;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.nio.file.FileSystem;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.EnumSet;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.regex.Pattern;
import java.util.stream.Stream;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.io.IOUtils;
import org.springframework.core.io.ClassPathResource;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.data.domain.Sort;
import org.springframework.data.domain.Sort.Direction;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@Component
@RequiredArgsConstructor
public class SvgMigrationService {

  private enum MigrationStatus {
    SCHEDULED,
    RUNNING,
    FAILED,
    HAS_WARNINGS,
    FINISHED_WITH_WARNINGS,
    FINISHED;

    private static MigrationStatus fromString(String value) {
      return valueOf(value);
    }
  }

  private static final int SPORT_CATEGORY_ICONS = 9;
  private static final int FOOTER_ICONS = 5;
  private static final Pattern clearSvgPattern =
      Pattern.compile("(class=\".*?\")|(fill=\".*?\")|(<style.*?>.*?</style>)");

  private final ExecutorService executor = Executors.newSingleThreadExecutor();
  private final SvgMigrationRepository repository;
  private final SvgImageService svgImageService;
  private final SvgBackupRepository svgBackupRepository;

  private final SvgImageRepository svgImageRepository;
  private final SportCategoryRepository sportCategoryRepository;
  private final FooterMenuRepository footerMenuRepository;
  private final SportRepository sportRepository;
  private final SportQuickLinkRepository sportQuickLinkRepository;
  private final HighlightCarouselRepository highlightCarouselRepository;
  private final SurfaceBetRepository surfaceBetRepository;
  private final RightMenuRepository rightMenuRepository;
  private final ConnectMenuRepository connectMenuRepository;
  private final OddsBoostConfigurationRepository oddsBoostConfigurationRepository;
  private final FooterLogoRepository footerLogoRepository;
  private final VirtualSportRepository virtualSportRepository;

  private final Map<String, String> signpostingMap =
      new HashMap<String, String>() {
        {
          put("icon-generic", "svg");
          put("boost-icon", "svg");
          put("byb-icon", "svg");
          put("cashout-icon", "svg");
          put("coral-logo", "svg");
          put("extra-place", "svg");
          put("extra-place-icon", "svg");
          put("icon-promotion-offers", "svg");
          put("icon-watch-live", "svg");
          put("live-icon", "svg");
          put("money-back", "svg");
          put("odds-boost-icon-dark", "svg");
          put("price-boost", "svg");
          put("retail-card", "svg");
          put("specials", "svg");
          put("star", "svg");
          put("yourcall-icon", "svg");
        }
      };
  private FileSystem fileSystem;

  public SvgMigration start(String brand) {
    Optional<SvgMigration> activeMigration = getActiveMigration(brand);

    return activeMigration.orElseGet(
        () -> {
          SvgMigration newMigration = new SvgMigration();
          newMigration.setBrand(brand);
          newMigration.setStatus(MigrationStatus.SCHEDULED.toString());
          return repository.save(newMigration);
        });
  }

  public SvgMigration active(String brand) {
    return getActiveMigration(brand)
        .orElseGet(
            () -> {
              SvgMigration tmpl = new SvgMigration();
              tmpl.setStatus("No active SVG migration JOB");
              return tmpl;
            });
  }

  public SvgMigration last(String brand) {
    Sort sort = Sort.by(Direction.DESC, "updatedAt");
    return repository
        .findFirstByBrand(brand, sort)
        .orElseGet(
            () -> {
              SvgMigration tmpl = new SvgMigration();
              tmpl.setStatus("No last SVG migration JOB");
              return tmpl;
            });
  }

  public SvgMigration showById(String id) {
    return repository.findById(id, SvgMigration.class);
  }

  public List<SvgMigration> findAllByBrand(String brand) {
    return repository.findByBrand(brand);
  }

  public void process(SvgMigration entity) {
    if (entity.getStatus().equals(MigrationStatus.SCHEDULED.toString())) {
      executor.execute(
          () -> {
            try {
              markAsRunning(entity);
              migrate(entity);
              markAsFinished(entity);
            } catch (Exception e) {
              markAsFailed(entity, e.toString());
            }
          });
    }
  }

  private Optional<SvgMigration> getActiveMigration(String brand) {
    List<SvgMigration> migrations = repository.findByBrand(brand);
    migrations.removeIf(
        entity ->
            EnumSet.of(
                    MigrationStatus.FAILED,
                    MigrationStatus.FINISHED_WITH_WARNINGS,
                    MigrationStatus.FINISHED)
                .contains(MigrationStatus.fromString(entity.getStatus())));

    return Optional.ofNullable(migrations.size() > 0 ? new ArrayList<>(migrations).get(0) : null);
  }

  private void markAsRunning(SvgMigration entity) {
    entity.setStatus(MigrationStatus.RUNNING.toString());
    addStatusMessage(entity, "Started SVG migration\n=====\n\n");
  }

  private void markAsFinished(SvgMigration entity) {
    if (MigrationStatus.fromString(entity.getStatus()).equals(MigrationStatus.RUNNING)) {
      entity.setStatus(MigrationStatus.FINISHED.toString());
    } else {
      entity.setStatus(MigrationStatus.FINISHED_WITH_WARNINGS.toString());
    }
    addStatusMessage(entity, "\n\n=====\nFinished");
  }

  private void markAsFailed(SvgMigration entity, String message) {
    if (EnumSet.of(MigrationStatus.RUNNING, MigrationStatus.HAS_WARNINGS)
        .contains(MigrationStatus.fromString(entity.getStatus()))) {
      entity.setStatus(MigrationStatus.FAILED.toString());
    }
    addStatusMessage(entity, message + "\n\n=====\nFailed");
  }

  private void addStatusMessage(SvgMigration entity, String message) {
    entity.setMessages(Optional.ofNullable(entity.getMessages()).orElse("") + message + "\n");
    repository.save(entity);
  }

  private void addWarningMessage(SvgMigration entity, String message) {
    entity.setStatus(MigrationStatus.HAS_WARNINGS.toString());
    addStatusMessage(entity, message);
  }

  private void migrate(SvgMigration entity) {
    migrateSportCategories(entity);
    migrateFooterMenus(entity);
    migrateSports(entity);
    migrateSportQuickLinks(entity);
    migrateHighlightCarousels(entity);
    migrateSurfaceBets(entity);
    migrateRightMenus(entity);
    migrateConnectMenus(entity);
    migrateOddsBoostConfigs(entity);
    migrateFooterLogos(entity);
    migrateVirtualSports(entity);
    migrateSvgFiles(entity);
  }

  private String getSvgId(String svgId) {
    return getNormilizedSvgField(svgId, "^#", "");
  }

  private String getSvg(String svg) {
    return getNormilizedSvgField(svg, "id=\"#", "id=\"");
  }

  private String getNormilizedSvgField(String svgValueToNormilize, String find, String replace) {
    return !Objects.isNull(svgValueToNormilize)
        ? svgValueToNormilize.replaceFirst(find, replace)
        : "";
  }

  private String sportCategoryInfo(SportCategory sportCategory) {
    return String.format(
        "%s/%s/%s/%s",
        sportCategory.getId(),
        sportCategory.getSsCategoryCode(),
        sportCategory.getSpriteClass(),
        sportCategory.getCategoryId());
  }

  private String cleanUpSportIcons(String svg) {
    // some sports icons shouldn't have class, fill attrs and/or style tag
    return clearSvgPattern.matcher(svg).replaceAll("");
  }

  private String sportInfo(Sport sport) {
    return String.format(
        "%s/%s/%s/%s",
        sport.getId(), sport.getSsCategoryCode(), sport.getSpriteClass(), sport.getCategoryId());
  }

  private String footerMenuInfo(FooterMenu footerMenu) {
    return footerMenu.getId() + "/" + footerMenu.getSpriteClass();
  }

  private String sportQLInfo(SportQuickLink sportQuickLink) {
    return sportQuickLink.getId() + "/" + sportQuickLink.getTitle();
  }

  private String highlightCarouselInfo(HighlightCarousel highlightCarousel) {
    return highlightCarousel.getId() + "/" + highlightCarousel.getTitle();
  }

  private String surfaceBetInfo(SurfaceBet surfaceBet) {
    return surfaceBet.getId() + "/" + surfaceBet.getTitle();
  }

  private String rightMenuInfo(RightMenu rightMenu) {
    return rightMenu.getId() + "/" + rightMenu.getSpriteClass();
  }

  private String connectMenuInfo(ConnectMenu connectMenu) {
    return connectMenu.getId() + "/" + connectMenu.getLinkTitle();
  }

  private String oddsBoostInfo(OddsBoostConfigEntity oddsBoostConfigEntity) {
    return oddsBoostConfigEntity.getId();
  }

  private String footerLogoInfo(FooterLogo footerLogo) {
    return footerLogo.getId();
  }

  private String virtualSportInfo(VirtualSport virtualSport) {
    return virtualSport.getId() + "/" + virtualSport.getTitle();
  }

  private void backupSvg(
      String brand, String collection, String collectionId, String svgId, String svg) {
    SvgBackup svgBackup = new SvgBackup();
    svgBackup.setBrand(brand);
    svgBackup.setCollectionName(collection);
    svgBackup.setCollectionId(collectionId);
    svgBackup.setSvgId(svgId);
    svgBackup.setSvg(svg);
    svgBackupRepository.save(svgBackup);
  }

  private void migrateSportCategories(SvgMigration entity) {
    addStatusMessage(entity, "\nSportCategories for " + entity.getBrand());
    AtomicInteger firstNIcons = new AtomicInteger(SPORT_CATEGORY_ICONS);
    Stream.concat(
            sportCategoryRepository
                .findAllByBrandAndDisabledOrderBySortOrderAsc(entity.getBrand(), Boolean.FALSE)
                .stream(),
            sportCategoryRepository
                .findAllByBrandAndDisabledOrderBySortOrderAsc(entity.getBrand(), Boolean.TRUE)
                .stream())
        .forEach(
            sportCategory -> {
              backupSvg(
                  entity.getBrand(),
                  "sportcategories",
                  sportCategory.getId(),
                  sportCategory.getSvgId(),
                  sportCategory.getSvg());
              if (Objects.isNull(sportCategory.getSvg())) {
                addStatusMessage(
                    entity,
                    "Skipping "
                        + sportCategoryInfo(sportCategory)
                        + " disabled: "
                        + sportCategory.isDisabled());
              } else {
                String svgId = getSvgId(sportCategory.getSvgId());
                String svg = cleanUpSportIcons(getSvg(sportCategory.getSvg()));
                if (svgId.length() > 0 && svg.length() > 0) {
                  String spriteName =
                      (firstNIcons.get() > 0 ? SvgSprite.INITIAL : SvgSprite.ADDITIONAL)
                          .getSpriteName();

                  try {
                    SvgImage svgImage = new SvgImage();
                    svgImage.setBrand(entity.getBrand());
                    svgImage.setSprite(spriteName);
                    svgImage.setSvg(svg);
                    svgImage.setSvgId(svgId);
                    svgImage.setSvgFilename(sportCategory.getSvgFilename());
                    svgImage.setDescription(
                        "Copied from sportCategory with ID " + sportCategoryInfo(sportCategory));
                    svgImageRepository.save(svgImage);
                    if (!sportCategory.isDisabled()) {
                      firstNIcons.decrementAndGet();
                    }
                  } catch (DuplicateKeyException e) {
                    addWarningMessage(
                        entity,
                        "Duplicate key exception "
                            + e.getMessage()
                            + " for "
                            + sportCategoryInfo(sportCategory));
                  }

                  addStatusMessage(entity, "Migrated " + sportCategoryInfo(sportCategory));

                  sportCategory.setSvgId(svgId);
                  sportCategory.setSvg(null);
                  sportCategory.setSvgFilename(null);
                  sportCategoryRepository.save(sportCategory);
                } else {
                  addStatusMessage(
                      entity,
                      "Skipping " + sportCategoryInfo(sportCategory) + " Empty svgId and/or svg");
                }
              }
            });
  }

  private void migrateFooterMenus(SvgMigration entity) {
    addStatusMessage(entity, "\nFooterMenu for " + entity.getBrand());
    AtomicInteger firstNIcons = new AtomicInteger(FOOTER_ICONS);

    Stream.concat(
            footerMenuRepository
                .findAllByBrandAndDisabledOrderBySortOrderAsc(entity.getBrand(), Boolean.FALSE)
                .stream(),
            footerMenuRepository
                .findAllByBrandAndDisabledOrderBySortOrderAsc(entity.getBrand(), Boolean.TRUE)
                .stream())
        .forEach(
            footerMenu -> {
              backupSvg(
                  entity.getBrand(),
                  "footermenus",
                  footerMenu.getId(),
                  footerMenu.getSvgId(),
                  footerMenu.getSvg());
              if (Objects.isNull(footerMenu.getSvg())) {
                addStatusMessage(
                    entity,
                    "Skipping "
                        + footerMenuInfo(footerMenu)
                        + " disabled: "
                        + footerMenu.isDisabled());
              } else {
                String svgId = getSvgId(footerMenu.getSvgId());
                String svg = getSvg(footerMenu.getSvg());
                if (svgId.length() > 0 && svg.length() > 0) {
                  String spriteName =
                      (firstNIcons.get() > 0 ? SvgSprite.INITIAL : SvgSprite.ADDITIONAL)
                          .getSpriteName();

                  try {
                    SvgImage svgImage = new SvgImage();
                    svgImage.setBrand(entity.getBrand());
                    svgImage.setSprite(spriteName);
                    svgImage.setSvg(svg);
                    svgImage.setSvgId(svgId);
                    svgImage.setSvgFilename(footerMenu.getSvgFilename());
                    svgImage.setDescription(
                        "Copied from footerMenu with ID " + footerMenuInfo(footerMenu));
                    svgImageRepository.save(svgImage);
                    if (!footerMenu.isDisabled()) {
                      firstNIcons.decrementAndGet();
                    }
                  } catch (DuplicateKeyException e) {
                    addWarningMessage(
                        entity,
                        "Duplicate key exception "
                            + e.getMessage()
                            + " for "
                            + footerMenuInfo(footerMenu));
                  }

                  addStatusMessage(entity, "Migrated " + footerMenuInfo(footerMenu));

                  footerMenu.setSvgId(svgId);
                  footerMenu.setSvg(null);
                  footerMenu.setSvgFilename(null);
                  footerMenuRepository.save(footerMenu);
                } else {
                  addStatusMessage(
                      entity, "Skipping " + footerMenuInfo(footerMenu) + " Empty svgId and/or svg");
                }
              }
            });
  }

  private void migrateSports(SvgMigration entity) {
    addStatusMessage(entity, "\nSports for " + entity.getBrand());
    sportRepository
        .findAllByBrandOrderBySortOrderAsc(entity.getBrand())
        .forEach(
            sport -> {
              backupSvg(
                  entity.getBrand(), "sports", sport.getId(), sport.getSvgId(), sport.getSvg());
              if (Objects.isNull(sport.getSvg())) {
                addStatusMessage(
                    entity, "Skipping " + sportInfo(sport) + " disabled: " + sport.isDisabled());
              } else {
                String svgId = getSvgId(sport.getSvgId());
                String svg = cleanUpSportIcons(getSvg(sport.getSvg()));
                if (svgId.length() > 0 && svg.length() > 0) {

                  try {
                    SvgImage svgImage = new SvgImage();
                    svgImage.setBrand(entity.getBrand());
                    svgImage.setSprite(SvgSprite.ADDITIONAL.getSpriteName());
                    svgImage.setSvg(svg);
                    svgImage.setSvgId(svgId);

                    Filename sportFilename = sport.getSvgFilename();
                    if (!Objects.isNull(sportFilename)) {
                      SvgFilename svgFilename = new SvgFilename();
                      svgFilename.setFilename(sportFilename.getFilename());
                      svgFilename.setFiletype(sportFilename.getFiletype());
                      svgFilename.setOriginalname(sportFilename.getOriginalname());
                      svgFilename.setPath(sportFilename.getPath());
                      svgFilename.setSize(Integer.valueOf(sportFilename.getSize()));

                      svgImage.setSvgFilename(svgFilename);
                    }
                    svgImage.setDescription("Copied from sport with ID " + sportInfo(sport));
                    svgImageRepository.save(svgImage);
                  } catch (DuplicateKeyException e) {
                    addWarningMessage(
                        entity,
                        "Duplicate key exception " + e.getMessage() + " for " + sportInfo(sport));
                  }

                  addStatusMessage(entity, "Migrated " + sportInfo(sport));

                  sport.setSvgId(svgId);
                  sport.setSvg(null);
                  sport.setSvgFilename(null);
                  sportRepository.save(sport);
                } else {
                  addStatusMessage(
                      entity, "Skipping " + sportInfo(sport) + " Empty svgId and/or svg");
                }
              }
            });
  }

  private void migrateSportQuickLinks(SvgMigration entity) {
    addStatusMessage(entity, "\nSportQuickLinks for " + entity.getBrand());
    sportQuickLinkRepository
        .findByBrand(entity.getBrand())
        .forEach(
            sportQuickLink -> {
              backupSvg(
                  entity.getBrand(),
                  "quicklinks",
                  sportQuickLink.getId(),
                  sportQuickLink.getSvgId(),
                  sportQuickLink.getSvg());
              if (Objects.isNull(sportQuickLink.getSvg())) {
                addStatusMessage(entity, "Skipping " + sportQLInfo(sportQuickLink));
              } else {
                String svgId = getSvgId(sportQuickLink.getSvgId());
                String svg = cleanUpSportIcons(getSvg(sportQuickLink.getSvg()));
                if (svgId.length() > 0 && svg.length() > 0) {

                  try {
                    SvgImage svgImage = new SvgImage();
                    svgImage.setBrand(entity.getBrand());
                    svgImage.setSprite(SvgSprite.FEATURED.getSpriteName());
                    svgImage.setSvg(svg);
                    svgImage.setSvgId(svgId);
                    svgImage.setSvgFilename(sportQuickLink.getSvgFilename());
                    svgImage.setDescription(
                        "Copied from QuickLink with ID " + sportQLInfo(sportQuickLink));
                    svgImageRepository.save(svgImage);
                  } catch (DuplicateKeyException e) {
                    addWarningMessage(
                        entity,
                        "Duplicate key exception "
                            + e.getMessage()
                            + " for "
                            + sportQLInfo(sportQuickLink));
                  }

                  addStatusMessage(entity, "Migrated " + sportQLInfo(sportQuickLink));

                  sportQuickLink.setSvgId(svgId);
                  sportQuickLink.setSvg(null);
                  sportQuickLink.setSvgFilename(null);
                  sportQuickLinkRepository.save(sportQuickLink);
                } else {
                  addStatusMessage(
                      entity,
                      "Skipping " + sportQLInfo(sportQuickLink) + " Empty svgId and/or svg");
                }
              }
            });
  }

  private void migrateHighlightCarousels(SvgMigration entity) {
    addStatusMessage(entity, "\nHighlightCarousel for " + entity.getBrand());
    highlightCarouselRepository
        .findByBrand(entity.getBrand())
        .forEach(
            highlightCarousel -> {
              backupSvg(
                  entity.getBrand(),
                  "highlightcarousels",
                  highlightCarousel.getId(),
                  highlightCarousel.getSvgId(),
                  highlightCarousel.getSvg());
              if (Objects.isNull(highlightCarousel.getSvg())) {
                addStatusMessage(entity, "Skipping " + highlightCarouselInfo(highlightCarousel));
              } else {
                String svgId = getSvgId(highlightCarousel.getSvgId());
                String svg = getSvg(highlightCarousel.getSvg());
                if (svgId.length() > 0 && svg.length() > 0) {

                  try {
                    SvgImage svgImage = new SvgImage();
                    svgImage.setBrand(entity.getBrand());
                    svgImage.setSprite(SvgSprite.FEATURED.getSpriteName());
                    svgImage.setSvg(svg);
                    svgImage.setSvgId(svgId);
                    svgImage.setSvgFilename(highlightCarousel.getSvgFilename());
                    svgImage.setDescription(
                        "Copied from HighlightCarousel with ID "
                            + highlightCarouselInfo(highlightCarousel));
                    svgImageRepository.save(svgImage);
                  } catch (DuplicateKeyException e) {
                    addWarningMessage(
                        entity,
                        "Duplicate key exception "
                            + e.getMessage()
                            + " for "
                            + highlightCarouselInfo(highlightCarousel));
                  }

                  addStatusMessage(entity, "Migrated " + highlightCarouselInfo(highlightCarousel));

                  highlightCarousel.setSvgId(svgId);
                  highlightCarousel.setSvg(null);
                  highlightCarousel.setSvgFilename(null);
                  highlightCarouselRepository.save(highlightCarousel);
                } else {
                  addStatusMessage(
                      entity,
                      "Skipping "
                          + highlightCarouselInfo(highlightCarousel)
                          + " Empty svgId and/or svg");
                }
              }
            });
  }

  private void migrateSurfaceBets(SvgMigration entity) {
    addStatusMessage(entity, "\nSurfaceBet for " + entity.getBrand());
    surfaceBetRepository
        .findByBrand(entity.getBrand())
        .forEach(
            surfaceBet -> {
              backupSvg(
                  entity.getBrand(),
                  "surfacebets",
                  surfaceBet.getId(),
                  surfaceBet.getSvgId(),
                  surfaceBet.getSvg());
              if (Objects.isNull(surfaceBet.getSvg())) {
                addStatusMessage(entity, "Skipping " + surfaceBetInfo(surfaceBet));
              } else {
                String svgId = getSvgId(surfaceBet.getSvgId());
                String svg = getSvg(surfaceBet.getSvg());
                if (svgId.length() > 0 && svg.length() > 0) {

                  try {
                    SvgImage svgImage = new SvgImage();
                    svgImage.setBrand(entity.getBrand());
                    svgImage.setSprite(SvgSprite.FEATURED.getSpriteName());
                    svgImage.setSvg(svg);
                    svgImage.setSvgId(svgId);
                    svgImage.setSvgFilename(surfaceBet.getSvgFilename());
                    svgImage.setDescription(
                        "Copied from SurfaceBet with ID " + surfaceBetInfo(surfaceBet));
                    svgImageRepository.save(svgImage);
                  } catch (DuplicateKeyException e) {
                    addWarningMessage(
                        entity,
                        "Duplicate key exception "
                            + e.getMessage()
                            + " for "
                            + surfaceBetInfo(surfaceBet));
                  }

                  addStatusMessage(entity, "Migrated " + surfaceBetInfo(surfaceBet));

                  surfaceBet.setSvgId(svgId);
                  surfaceBet.setSvg(null);
                  surfaceBet.setSvgFilename(null);
                  surfaceBetRepository.save(surfaceBet);
                } else {
                  addStatusMessage(
                      entity, "Skipping " + surfaceBetInfo(surfaceBet) + " Empty svgId and/or svg");
                }
              }
            });
  }

  private void migrateRightMenus(SvgMigration entity) {
    addStatusMessage(entity, "\nRightMenu for " + entity.getBrand());
    rightMenuRepository
        .findByBrand(entity.getBrand())
        .forEach(
            rightMenu -> {
              backupSvg(
                  entity.getBrand(),
                  "rightmenus",
                  rightMenu.getId(),
                  rightMenu.getSvgId(),
                  rightMenu.getSvg());
              if (Objects.isNull(rightMenu.getSvg())) {
                addStatusMessage(entity, "Skipping " + rightMenuInfo(rightMenu));
              } else {
                String svgId = getSvgId(rightMenu.getSvgId());
                String svg = getSvg(rightMenu.getSvg());
                if (svgId.length() > 0 && svg.length() > 0) {

                  try {
                    SvgImage svgImage = new SvgImage();
                    svgImage.setBrand(entity.getBrand());
                    svgImage.setSprite(SvgSprite.ADDITIONAL.getSpriteName());
                    svgImage.setSvg(svg);
                    svgImage.setSvgId(svgId);
                    svgImage.setSvgFilename(rightMenu.getSvgFilename());
                    svgImage.setDescription(
                        "Copied from RightMenu with ID " + rightMenuInfo(rightMenu));
                    svgImageRepository.save(svgImage);
                  } catch (DuplicateKeyException e) {
                    addWarningMessage(
                        entity,
                        "Duplicate key exception "
                            + e.getMessage()
                            + " for "
                            + rightMenuInfo(rightMenu));
                  }

                  addStatusMessage(entity, "Migrated " + rightMenuInfo(rightMenu));

                  rightMenu.setSvgId(svgId);
                  rightMenu.setSvg(null);
                  rightMenu.setSvgFilename(null);
                  rightMenuRepository.save(rightMenu);
                } else {
                  addStatusMessage(
                      entity, "Skipping " + rightMenuInfo(rightMenu) + " Empty svgId and/or svg");
                }
              }
            });
  }

  private void migrateConnectMenus(SvgMigration entity) {
    addStatusMessage(entity, "\nConnectMenu for " + entity.getBrand());
    connectMenuRepository
        .findByBrand(entity.getBrand())
        .forEach(
            connectMenu -> {
              backupSvg(
                  entity.getBrand(),
                  "connectmenus",
                  connectMenu.getId(),
                  connectMenu.getSvgId(),
                  connectMenu.getSvg());
              if (Objects.isNull(connectMenu.getSvg())) {
                addStatusMessage(entity, "Skipping " + connectMenuInfo(connectMenu));
              } else {
                String svgId = getSvgId(connectMenu.getSvgId());
                String svg = getSvg(connectMenu.getSvg());
                if (svgId.length() > 0 && svg.length() > 0) {

                  try {
                    SvgImage svgImage = new SvgImage();
                    svgImage.setBrand(entity.getBrand());
                    svgImage.setSprite(SvgSprite.ADDITIONAL.getSpriteName());
                    svgImage.setSvg(svg);
                    svgImage.setSvgId(svgId);
                    svgImage.setSvgFilename(connectMenu.getSvgFilename());
                    svgImage.setDescription(
                        "Copied from ConnectMenu with ID " + connectMenuInfo(connectMenu));
                    svgImageRepository.save(svgImage);
                  } catch (DuplicateKeyException e) {
                    addWarningMessage(
                        entity,
                        "Duplicate key exception "
                            + e.getMessage()
                            + " for "
                            + connectMenuInfo(connectMenu));
                  }

                  addStatusMessage(entity, "Migrated " + connectMenuInfo(connectMenu));

                  connectMenu.setSvgId(svgId);
                  connectMenu.setSvg(null);
                  connectMenu.setSvgFilename(null);
                  connectMenuRepository.save(connectMenu);
                } else {
                  addStatusMessage(
                      entity,
                      "Skipping " + connectMenuInfo(connectMenu) + " Empty svgId and/or svg");
                }
              }
            });
  }

  private void migrateOddsBoostConfigs(SvgMigration entity) {
    addStatusMessage(entity, "\nOddsBoostConfig for " + entity.getBrand());
    oddsBoostConfigurationRepository
        .findByBrand(entity.getBrand())
        .forEach(
            oddsBoostConfig -> {
              backupSvg(
                  entity.getBrand(),
                  "oddsboostconfiguration",
                  oddsBoostConfig.getId(),
                  oddsBoostConfig.getSvgId(),
                  oddsBoostConfig.getSvg());
              if (Objects.isNull(oddsBoostConfig.getSvg())) {
                addStatusMessage(entity, "Skipping " + oddsBoostInfo(oddsBoostConfig));
              } else {
                String svgId = getSvgId(oddsBoostConfig.getSvgId());
                String svg = getSvg(oddsBoostConfig.getSvg());
                if (svgId.length() > 0 && svg.length() > 0) {

                  try {
                    SvgImage svgImage = new SvgImage();
                    svgImage.setBrand(entity.getBrand());
                    svgImage.setSprite(SvgSprite.ADDITIONAL.getSpriteName());
                    svgImage.setSvg(svg);
                    svgImage.setSvgId(svgId);
                    svgImage.setSvgFilename(oddsBoostConfig.getSvgFilename());
                    svgImage.setDescription(
                        "Copied from OddsBoostConfig with ID " + oddsBoostInfo(oddsBoostConfig));
                    svgImageRepository.save(svgImage);
                  } catch (DuplicateKeyException e) {
                    addWarningMessage(
                        entity,
                        "Duplicate key exception "
                            + e.getMessage()
                            + " for "
                            + oddsBoostInfo(oddsBoostConfig));
                  }

                  addStatusMessage(entity, "Migrated " + oddsBoostInfo(oddsBoostConfig));

                  oddsBoostConfig.setSvgId(svgId);
                  oddsBoostConfig.setSvg(null);
                  oddsBoostConfig.setSvgFilename(null);
                  oddsBoostConfigurationRepository.save(oddsBoostConfig);
                } else {
                  addStatusMessage(
                      entity,
                      "Skipping " + oddsBoostInfo(oddsBoostConfig) + " Empty svgId and/or svg");
                }
              }
            });
  }

  private void migrateFooterLogos(SvgMigration entity) {
    addStatusMessage(entity, "\nFooterLogo for " + entity.getBrand());
    footerLogoRepository
        .findByBrand(entity.getBrand())
        .forEach(
            footerLogo -> {
              backupSvg(
                  entity.getBrand(),
                  "footerlogos",
                  footerLogo.getId(),
                  footerLogo.getSvgId(),
                  footerLogo.getSvg());
              if (Objects.isNull(footerLogo.getSvg())) {
                addStatusMessage(entity, "Skipping " + footerLogoInfo(footerLogo));
              } else {
                String svgId = getSvgId(footerLogo.getSvgId());
                String svg = getSvg(footerLogo.getSvg());
                if (svgId.length() > 0 && svg.length() > 0) {

                  try {
                    SvgImage svgImage = new SvgImage();
                    svgImage.setBrand(entity.getBrand());
                    svgImage.setSprite(SvgSprite.ADDITIONAL.getSpriteName());
                    svgImage.setSvg(svg);
                    svgImage.setSvgId(svgId);
                    svgImage.setSvgFilename(footerLogo.getSvgFilename());
                    svgImage.setDescription(
                        "Copied from FooterLogo with ID " + footerLogoInfo(footerLogo));
                    svgImageRepository.save(svgImage);
                  } catch (DuplicateKeyException e) {
                    addWarningMessage(
                        entity,
                        "Duplicate key exception "
                            + e.getMessage()
                            + " for "
                            + footerLogoInfo(footerLogo));
                  }

                  addStatusMessage(entity, "Migrated " + footerLogoInfo(footerLogo));

                  footerLogo.setSvgId(svgId);
                  footerLogo.setSvg(null);
                  footerLogo.setSvgFilename(null);
                  footerLogoRepository.save(footerLogo);
                } else {
                  addStatusMessage(
                      entity, "Skipping " + footerLogoInfo(footerLogo) + " Empty svgId and/or svg");
                }
              }
            });
  }

  private void migrateVirtualSports(SvgMigration entity) {
    addStatusMessage(entity, "\nVirtualSport for " + entity.getBrand());
    virtualSportRepository
        .findByBrand(entity.getBrand())
        .forEach(
            virtualSport -> {
              backupSvg(
                  entity.getBrand(),
                  "virtualsports",
                  virtualSport.getId(),
                  virtualSport.getSvgId(),
                  virtualSport.getSvg());
              if (Objects.isNull(virtualSport.getSvg())) {
                addStatusMessage(entity, "Skipping " + virtualSportInfo(virtualSport));
              } else {
                String svgId = getSvgId(virtualSport.getSvgId());
                String svg = getSvg(virtualSport.getSvg());
                if (svgId.length() > 0 && svg.length() > 0) {

                  try {
                    SvgImage svgImage = new SvgImage();
                    svgImage.setBrand(entity.getBrand());
                    svgImage.setSprite(SvgSprite.VIRTUAL.getSpriteName());
                    svgImage.setSvg(svg);
                    svgImage.setSvgId(svgId);
                    svgImage.setSvgFilename(virtualSport.getSvgFilename());
                    svgImage.setDescription(
                        "Copied from VirtualSport with ID " + virtualSportInfo(virtualSport));
                    svgImageRepository.save(svgImage);
                  } catch (DuplicateKeyException e) {
                    addWarningMessage(
                        entity,
                        "Duplicate key exception "
                            + e.getMessage()
                            + " for "
                            + virtualSportInfo(virtualSport));
                  }

                  addStatusMessage(entity, "Migrated " + virtualSportInfo(virtualSport));

                  virtualSport.setSvgId(svgId);
                  virtualSport.setSvg(null);
                  virtualSport.setSvgFilename(null);
                  virtualSportRepository.save(virtualSport);
                } else {
                  addStatusMessage(
                      entity,
                      "Skipping " + virtualSportInfo(virtualSport) + " Empty svgId and/or svg");
                }
              }
            });
  }

  private void migrateSvgFiles(SvgMigration entity) {
    addStatusMessage(entity, "\nMigrating SVG files for " + entity.getBrand());
    try {
      String migrationPath = PathUtil.normalize("svg-migration/" + entity.getBrand());
      URI uri = new ClassPathResource(migrationPath).getURI();
      Path migrationBase;

      if (uri.getScheme().equalsIgnoreCase("jar")) {
        if (fileSystem == null) {
          fileSystem = FileSystems.newFileSystem(uri, Collections.emptyMap());
        }
        migrationBase = fileSystem.getPath("/BOOT-INF/classes/" + migrationPath);
      } else {
        migrationBase = Paths.get(uri);
      }

      Files.walk(migrationBase)
          .sorted()
          .forEach(
              path -> {
                if (Files.isRegularFile(path)) {
                  String filename = path.getFileName().toString();
                  String filenameWithoutExt = filename.split("\\.")[0].toLowerCase();
                  addStatusMessage(entity, path.toString());

                  SvgSprite sprite =
                      signpostingMap.containsKey(filenameWithoutExt)
                          ? SvgSprite.FEATURED
                          : SvgSprite.ADDITIONAL;

                  SvgImage svgImage = new SvgImage();
                  svgImage.setSvgId(filenameWithoutExt);
                  svgImage.setBrand(entity.getBrand());
                  svgImage.setSprite(sprite.getSpriteName());
                  svgImage.setDescription("Migrated from BMA assets");

                  WrapPathToMultipartFile multipartFile = new WrapPathToMultipartFile(path);
                  addStatusMessage(entity, "Uploading SVG " + svgImage.getSvgId());
                  try {
                    SvgImage svgToSave =
                        svgImageService.createSvgImage(svgImage, multipartFile, "");
                    svgImageRepository.save(svgToSave);
                    addStatusMessage(
                        entity,
                        String.format(
                            "Uploaded and create SVG %s to sprite %s",
                            svgImage.getSvgId(), sprite));
                  } catch (DuplicateKeyException e) {
                    addWarningMessage(entity, e.toString());
                  } catch (SvgImageParseException e) {
                    addWarningMessage(
                        entity, "WARNING: Failed to parse/validate " + svgImage.getSvgId());
                  } finally {
                    multipartFile.deleteTempFile();
                  }
                }
              });
    } catch (IOException e) {
      addWarningMessage(entity, "WARNING: migrate SVG files throws IOException " + e.toString());
    }
  }

  private class WrapPathToMultipartFile implements MultipartFile {

    private Path path;
    private File file;

    public WrapPathToMultipartFile(Path path) {
      this.path = path;
      try {
        getInputStream();
      } catch (IOException e) {
        e.printStackTrace();
      }
    }

    @Override
    public String getName() {
      return path.getFileName().toString();
    }

    @Override
    public String getOriginalFilename() {
      return getName();
    }

    @Override
    public String getContentType() {
      return "image/svg+xml";
    }

    @Override
    public boolean isEmpty() {
      return getSize() <= 0;
    }

    @Override
    public long getSize() {
      return file.length();
    }

    @Override
    public byte[] getBytes() throws IOException {
      file = new File(PathUtil.normalize(file.getAbsolutePath()));
      try (InputStream io = new FileInputStream(file)) {
        byte[] bytes = new byte[(int) file.length()];
        int result = io.read(bytes);
        return result > -1 ? bytes : new byte[0];
      }
    }

    @Override
    public InputStream getInputStream() throws IOException {
      InputStream is = Files.newInputStream(path);
      file = File.createTempFile("prefix", getName());
      try (FileOutputStream out = new FileOutputStream(file)) {
        IOUtils.copy(is, out);
      }
      return is;
    }

    @Override
    public void transferTo(File dest) throws IOException, IllegalStateException {}

    public void deleteTempFile() {
      file.delete();
    }
  }
}
