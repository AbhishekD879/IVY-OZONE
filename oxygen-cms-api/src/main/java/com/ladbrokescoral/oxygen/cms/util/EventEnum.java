package com.ladbrokescoral.oxygen.cms.util;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSport;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSportTrack;
import com.ladbrokescoral.oxygen.cms.api.entity.ConnectMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.ModuleRibbonTab;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.entity.OddsBoostConfigEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import com.ladbrokescoral.oxygen.cms.api.entity.QuizPopupSetting;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoPage;
import com.ladbrokescoral.oxygen.cms.api.entity.Sport;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgImage;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfiguration;
import com.ladbrokescoral.oxygen.cms.api.entity.YourCallLeague;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Quiz;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Campaign;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Config;

public enum EventEnum {
  CONNECT_MENU(ConnectMenu.class, "connectmenus"),
  FOOTER_MENU(FooterMenu.class, "footermenus", true),
  HOME_MODULE(HomeModule.class, "homemodules"),
  MODULE_RIBBON(ModuleRibbonTab.class, "moduleribbontabs"),
  NAVIGATION_POINT(NavigationPoint.class, "navigationPoint"),
  ODDS_BOOST(OddsBoostConfigEntity.class, "odds-boost-configuration"),
  PROMOTION(Promotion.class, "promotions"),
  QUIZ_POPUP_SETTINGS(QuizPopupSetting.class, "quiz-popup-setting"),
  QUIZ(Quiz.class, "quiz"),
  SEO_PAGE(SeoPage.class, "seopages"),
  SPORT_CATEGORY(SportCategory.class, "sportcategories"),
  SPORT_INIT(Sport.class, "sports"),
  SVG_IMG(SvgImage.class, "svgimages"),
  SYSTEM_CONFIG(SystemConfiguration.class, "systemconfigurations"),
  TIME_LINE_CAMPAIGN(Campaign.class, "timelineCampaign"),
  TIME_LINE_CONFIG(Config.class, "timelineConfig"),
  VIRTUAL_SPORT(VirtualSport.class, "virtualSport"),
  VIRTUAL_SPORT_TRACK(VirtualSportTrack.class, "virtualSportTrack"),
  YC_LEAGUE(YourCallLeague.class, "ycleagues");

  private final Class<?> clazz;
  private final String collectionName;
  private boolean publishEvent = false;

  private EventEnum(Class<?> clazz, String collectionName) {
    this.clazz = clazz;
    this.collectionName = collectionName;
  }

  private EventEnum(Class<?> clazz, String collectionName, boolean publishEvent) {
    this.clazz = clazz;
    this.collectionName = collectionName;
    this.publishEvent = publishEvent;
  }

  public Class<?> getClazz() {
    return clazz;
  }

  public String getCollectionName() {
    return collectionName;
  }

  public boolean isPublishEvent() {
    return publishEvent;
  }
}
