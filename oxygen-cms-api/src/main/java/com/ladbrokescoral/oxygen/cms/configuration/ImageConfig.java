package com.ladbrokescoral.oxygen.cms.configuration;

import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl.Size;
import lombok.Builder;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Slf4j
@Configuration
public class ImageConfig {

  @Builder
  @Getter
  public static class ImagePath {
    private String smallPath;
    private String mediumPath;
    private String largePath;
    private String imagesCorePath;
    private String svgMenuPath;

    private Size smallSize;
    private Size mediumSize;
    private Size largeSize;
  }

  @Bean(name = "bannerImagePath")
  public ImagePath getBannerImage(
      @Value("${images.core}") String imagesCorePath,
      @Value("${images.banners.small.path}") String smallBannersPath,
      @Value("${images.banners.medium.path}") String mediumBannersPath,
      @Value("${images.banners.desktop.path}") String desktopBannersPath,
      @Value("${images.banners.small.size}") String smallBannersSize,
      @Value("${images.banners.medium.size}") String mediumBannersSize,
      @Value("${images.banners.desktop.size}") String desktopBannersSize) {
    return ImagePath.builder()
        .imagesCorePath(imagesCorePath)
        .smallPath(smallBannersPath)
        .mediumPath(mediumBannersPath)
        .largePath(desktopBannersPath)
        .smallSize(new Size(smallBannersSize))
        .mediumSize(new Size(mediumBannersSize))
        .largeSize(new Size(desktopBannersSize))
        .build();
  }

  @Bean(name = "userMenuImagePath")
  public ImagePath getUserMenuImage(
      @Value("${images.usermenus.small.path}") String smallMenusPath,
      @Value("${images.usermenus.medium.path}") String mediumMenusPath,
      @Value("${images.usermenus.large.path}") String largeMenusPath,
      @Value("${images.usermenus.svg}") String svgMenuPath,
      @Value("${images.usermenus.small.size}") String smallMenuSize,
      @Value("${images.usermenus.medium.size}") String mediumMenuSize,
      @Value("${images.usermenus.large.size}") String largeMenuSize) {
    return ImagePath.builder()
        .svgMenuPath(svgMenuPath)
        .smallPath(smallMenusPath)
        .mediumPath(mediumMenusPath)
        .largePath(largeMenusPath)
        .smallSize(new Size(smallMenuSize))
        .mediumSize(new Size(mediumMenuSize))
        .largeSize(new Size(largeMenuSize))
        .build();
  }

  @Bean(name = "sportCategoryMenuImagePath")
  public ImagePath getSportCategoryMenuImage(
      @Value("${images.sportcategories.svg}") String svgMenuPath,
      @Value("${images.sportcategories.small.path}") String smallMenusPath,
      @Value("${images.sportcategories.medium.path}") String mediumMenusPath,
      @Value("${images.sportcategories.large.path}") String largeMenusPath,
      @Value("${images.sportcategories.small.size}") String smallMenuSize,
      @Value("${images.sportcategories.medium.size}") String mediumMenuSize,
      @Value("${images.sportcategories.large.size}") String largeMenuSize) {
    return ImagePath.builder()
        .svgMenuPath(svgMenuPath)
        .smallPath(smallMenusPath)
        .mediumPath(mediumMenusPath)
        .largePath(largeMenusPath)
        .smallSize(new Size(smallMenuSize))
        .mediumSize(new Size(mediumMenuSize))
        .largeSize(new Size(largeMenuSize))
        .build();
  }

  @Bean(name = "sportCategoryIcon")
  public ImagePath getSportCategoryIcon(
      @Value("${images.sportcategories.icon.small.path}") String smallIconsPath,
      @Value("${images.sportcategories.icon.medium.path}") String mediumIconsPath,
      @Value("${images.sportcategories.icon.large.path}") String largeIconsPath,
      @Value("${images.sportcategories.icon.small.size}") String smallIconSize,
      @Value("${images.sportcategories.icon.medium.size}") String mediumIconSize,
      @Value("${images.sportcategories.icon.large.size}") String largeIconSize) {
    return ImagePath.builder()
        .smallPath(smallIconsPath)
        .mediumPath(mediumIconsPath)
        .largePath(largeIconsPath)
        .smallSize(new Size(smallIconSize))
        .mediumSize(new Size(mediumIconSize))
        .largeSize(new Size(largeIconSize))
        .build();
  }

  @Bean(name = "topGameMenuImagePath")
  public ImagePath getTopGameMenuImage(
      @Value("${images.topgames.small.path}") String smallMenusPath,
      @Value("${images.topgames.medium.path}") String mediumMenusPath,
      @Value("${images.topgames.large.path}") String largeMenusPath,
      @Value("${images.topgames.small.size}") String smallMenuSize,
      @Value("${images.topgames.medium.size}") String mediumMenuSize,
      @Value("${images.topgames.large.size}") String largeMenuSize) {
    return ImagePath.builder()
        .smallPath(smallMenusPath)
        .mediumPath(mediumMenusPath)
        .largePath(largeMenusPath)
        .smallSize(new Size(smallMenuSize))
        .mediumSize(new Size(mediumMenuSize))
        .largeSize(new Size(largeMenuSize))
        .build();
  }

  @Bean(name = "topGameIcon")
  public ImagePath getTopGameIconImage(
      @Value("${images.topgames.icon.small.path}") String smallIconsPath,
      @Value("${images.topgames.icon.medium.path}") String mediumIconsPath,
      @Value("${images.topgames.icon.large.path}") String largeIconsPath,
      @Value("${images.topgames.icon.small.size}") String smallIconSize,
      @Value("${images.topgames.icon.medium.size}") String mediumIconSize,
      @Value("${images.topgames.icon.large.size}") String largeIconSize) {
    return ImagePath.builder()
        .smallPath(smallIconsPath)
        .mediumPath(mediumIconsPath)
        .largePath(largeIconsPath)
        .smallSize(new Size(smallIconSize))
        .mediumSize(new Size(mediumIconSize))
        .largeSize(new Size(largeIconSize))
        .build();
  }

  @Bean(name = "rightMenuImagePath")
  public ImagePath getRightMenuImage(
      @Value("${images.rightmenus.small.path}") String smallMenusPath,
      @Value("${images.rightmenus.medium.path}") String mediumMenusPath,
      @Value("${images.rightmenus.large.path}") String largeMenusPath,
      @Value("${images.rightmenus.svg}") String svgMenuPath,
      @Value("${images.core}") String corePath,
      @Value("${images.rightmenus.small.size}") String smallMenuSize,
      @Value("${images.rightmenus.medium.size}") String mediumMenuSize,
      @Value("${images.rightmenus.large.size}") String largeMenuSize) {
    return ImagePath.builder()
        .svgMenuPath(svgMenuPath)
        .imagesCorePath(corePath)
        .smallPath(smallMenusPath)
        .mediumPath(mediumMenusPath)
        .largePath(largeMenusPath)
        .smallSize(new Size(smallMenuSize))
        .mediumSize(new Size(mediumMenuSize))
        .largeSize(new Size(largeMenuSize))
        .build();
  }

  @Bean(name = "footerMenuImagePath")
  public ImagePath getFooterMenuImage(
      @Value("${images.footermenus.small.path}") String smallMenusPath,
      @Value("${images.footermenus.medium.path}") String mediumMenusPath,
      @Value("${images.footermenus.large.path}") String largeMenusPath,
      @Value("${images.footermenus.svg}") String svgMenuPath,
      @Value("${images.footermenus.small.size}") String smallMenuSize,
      @Value("${images.footermenus.medium.size}") String mediumMenuSize,
      @Value("${images.footermenus.large.size}") String largeMenuSize) {
    return ImagePath.builder()
        .svgMenuPath(svgMenuPath)
        .smallPath(smallMenusPath)
        .mediumPath(mediumMenusPath)
        .largePath(largeMenusPath)
        .smallSize(new Size(smallMenuSize))
        .mediumSize(new Size(mediumMenuSize))
        .largeSize(new Size(largeMenuSize))
        .build();
  }

  @Bean(name = "desktopQuickLinkImagePath")
  public ImagePath getDesktopQuickLinkImage(
      @Value("${images.lnquicklinks.small.path}") String smallMenusPath,
      @Value("${images.lnquicklinks.medium.path}") String mediumMenusPath,
      @Value("${images.lnquicklinks.large.path}") String largeMenusPath,
      @Value("${images.lnquicklinks.small.size}") String smallMenuSize,
      @Value("${images.lnquicklinks.medium.size}") String mediumMenuSize,
      @Value("${images.lnquicklinks.large.size}") String largeMenuSize) {
    return ImagePath.builder()
        .smallPath(smallMenusPath)
        .mediumPath(mediumMenusPath)
        .largePath(largeMenusPath)
        .smallSize(new Size(smallMenuSize))
        .mediumSize(new Size(mediumMenuSize))
        .largeSize(new Size(largeMenuSize))
        .build();
  }

  @Bean(name = "bankingMenuImagePath")
  public ImagePath getBankingMenuImagePath(
      @Value("${images.bankingmenus.small.path}") String smallMenusPath,
      @Value("${images.bankingmenus.medium.path}") String mediumMenusPath,
      @Value("${images.bankingmenus.large.path}") String largeMenusPath,
      @Value("${images.bankingmenus.svg}") String svgMenuPath,
      @Value("${images.bankingmenus.small.size}") String smallMenuSize,
      @Value("${images.bankingmenus.medium.size}") String mediumMenuSize,
      @Value("${images.bankingmenus.large.size}") String largeMenuSize) {
    return ImagePath.builder()
        .svgMenuPath(svgMenuPath)
        .smallPath(smallMenusPath)
        .mediumPath(mediumMenusPath)
        .largePath(largeMenusPath)
        .smallSize(new Size(smallMenuSize))
        .mediumSize(new Size(mediumMenuSize))
        .largeSize(new Size(largeMenuSize))
        .build();
  }
}
