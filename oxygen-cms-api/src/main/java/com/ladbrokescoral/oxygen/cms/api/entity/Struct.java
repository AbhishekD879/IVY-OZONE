package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonProperty;
import org.springframework.data.mongodb.core.mapping.Field;

public class Struct {
  @Field(value = "AtTheRaces")
  private AtTheRace atTheRaces;

  @Field(value = "IMGStreaming")
  private ImgStreaming imgStreaming;

  private PerformGroup performGroup;
  private NewGroup newGroup;

  @Field(value = "Terms")
  private Terms terms;

  @Field(value = "Scoreboard")
  private Scoreboard scoreboard;

  @Field(value = "Betslip")
  private Betslip betslip;

  @Field(value = "Header")
  private Header header;

  @Field(value = "Banners")
  private Banners banners;

  @Field(value = "Layouts")
  private Layouts layouts;

  @Field(value = "Generals")
  private General generals;

  @JsonProperty("RCOMBRequestTimeouts")
  private RCOMBRequestTimeouts rCOMBRequestTimeouts;

  @JsonProperty("smartBannersLinks")
  private SmartBannersLinks smartBannersLinks;

  @JsonProperty("RCOMB")
  private RCOMB rCOMB;

  @JsonProperty("RCOMBDelays")
  private RCOMBDelays rCOMBDelays;

  @JsonProperty("RetailGeoLocation")
  private RetailGeoLocation retailGeoLocation;

  @JsonProperty("RetailConfig")
  private RetailConfig retailConfig;

  @JsonProperty("RetailIpLocation")
  private RetailIpLocation retailIpLocation;

  @JsonProperty("RCOMBONLYTEST")
  private RcombOnlyTest rcombOnlyTest;

  @JsonProperty("RetailAuditCreds")
  private RetailAuditCreds retailAuditCreds;

  public AtTheRace getAtTheRaces() {
    return atTheRaces;
  }

  public void setAtTheRaces(AtTheRace atTheRaces) {
    this.atTheRaces = atTheRaces;
  }

  public ImgStreaming getImgStreaming() {
    return imgStreaming;
  }

  public void setImgStreaming(ImgStreaming imgStreaming) {
    this.imgStreaming = imgStreaming;
  }

  public PerformGroup getPerformGroup() {
    return performGroup;
  }

  public void setPerformGroup(PerformGroup performGroup) {
    this.performGroup = performGroup;
  }

  public NewGroup getNewGroup() {
    return newGroup;
  }

  public void setNewGroup(NewGroup newGroup) {
    this.newGroup = newGroup;
  }

  public Terms getTerms() {
    return terms;
  }

  public void setTerms(Terms terms) {
    this.terms = terms;
  }

  public Scoreboard getScoreboard() {
    return scoreboard;
  }

  public void setScoreboard(Scoreboard scoreboard) {
    this.scoreboard = scoreboard;
  }

  public Betslip getBetslip() {
    return betslip;
  }

  public void setBetslip(Betslip betslip) {
    this.betslip = betslip;
  }

  public Header getHeader() {
    return header;
  }

  public void setHeader(Header header) {
    this.header = header;
  }

  public Banners getBanners() {
    return banners;
  }

  public void setBanners(Banners banners) {
    this.banners = banners;
  }

  public Layouts getLayouts() {
    return layouts;
  }

  public void setLayouts(Layouts layouts) {
    this.layouts = layouts;
  }

  public General getGenerals() {
    return generals;
  }

  public void setGenerals(General generals) {
    this.generals = generals;
  }

  public class AtTheRace {
    @Field(value = "Secret")
    private String secret;

    @Field(value = "Password")
    private String password;

    @Field(value = "PartnerCode")
    private String partnerCode;

    public String getSecret() {
      return secret;
    }

    public void setSecret(String secret) {
      this.secret = secret;
    }

    public String getPassword() {
      return password;
    }

    public void setPassword(String password) {
      this.password = password;
    }

    public String getPartnerCode() {
      return partnerCode;
    }

    public void setPartnerCode(String partnerCode) {
      this.partnerCode = partnerCode;
    }
  }

  public class ImgStreaming {
    @Field(value = "IMGSecret")
    private String imgSecret;

    @Field(value = "operatorId")
    private String operatorId;

    public String getImgSecret() {
      return imgSecret;
    }

    public void setImgSecret(String imgSecret) {
      this.imgSecret = imgSecret;
    }

    public String getOperatorId() {
      return operatorId;
    }

    public void setOperatorId(String operatorId) {
      this.operatorId = operatorId;
    }
  }

  public class PerformGroup {
    private String mobileUserId;
    private String mobilePartnerId;
    private String desktopUserId;
    private String desktopPartnerId;

    public String getMobileUserId() {
      return mobileUserId;
    }

    public void setMobileUserId(String mobileUserId) {
      this.mobileUserId = mobileUserId;
    }

    public String getMobilePartnerId() {
      return mobilePartnerId;
    }

    public void setMobilePartnerId(String mobilePartnerId) {
      this.mobilePartnerId = mobilePartnerId;
    }

    public String getDesktopUserId() {
      return desktopUserId;
    }

    public void setDesktopUserId(String desktopUserId) {
      this.desktopUserId = desktopUserId;
    }

    public String getDesktopPartnerId() {
      return desktopPartnerId;
    }

    public void setDesktopPartnerId(String desktopPartnerId) {
      this.desktopPartnerId = desktopPartnerId;
    }
  }

  public class NewGroup {
    private String newName;

    public String getNewName() {
      return newName;
    }

    public void setNewName(String newName) {
      this.newName = newName;
    }
  }

  public class Terms {
    @Field(value = "TermsLink")
    private String termsLink;

    public String getTermsLink() {
      return termsLink;
    }

    public void setTermsLink(String termsLink) {
      this.termsLink = termsLink;
    }
  }

  public class Scoreboard {
    private String updateTime;
    private String scoreboardUrl;
    private String showScoreboard;

    public String getUpdateTime() {
      return updateTime;
    }

    public void setUpdateTime(String updateTime) {
      this.updateTime = updateTime;
    }

    public String getScoreboardUrl() {
      return scoreboardUrl;
    }

    public void setScoreboardUrl(String scoreboardUrl) {
      this.scoreboardUrl = scoreboardUrl;
    }

    public String getShowScoreboard() {
      return showScoreboard;
    }

    public void setShowScoreboard(String showScoreboard) {
      this.showScoreboard = showScoreboard;
    }
  }

  public class Betslip {
    private String minBetNumber;
    private String maxBetNumber;

    public String getMinBetNumber() {
      return minBetNumber;
    }

    public void setMinBetNumber(String minBetNumber) {
      this.minBetNumber = minBetNumber;
    }

    public String getMaxBetNumber() {
      return maxBetNumber;
    }

    public void setMaxBetNumber(String maxBetNumber) {
      this.maxBetNumber = maxBetNumber;
    }
  }

  public class Header {
    private String showInApp;
    private String gameButtonLink;

    public String getShowInApp() {
      return showInApp;
    }

    public void setShowInApp(String showInApp) {
      this.showInApp = showInApp;
    }

    public String getGameButtonLink() {
      return gameButtonLink;
    }

    public void setGameButtonLink(String gameButtonLink) {
      this.gameButtonLink = gameButtonLink;
    }
  }

  public class Banners {
    private String transitionDelay;

    public String getTransitionDelay() {
      return transitionDelay;
    }

    public void setTransitionDelay(String transitionDelay) {
      this.transitionDelay = transitionDelay;
    }
  }

  public class Layouts {
    @Field(value = "ShowRightMenu")
    private String showRightMenu;

    @Field(value = "ShowTopMenu")
    private String showTopMenu;

    @Field(value = "ShowLeftMenu")
    private String showLeftMenu;

    public String getShowRightMenu() {
      return showRightMenu;
    }

    public void setShowRightMenu(String showRightMenu) {
      this.showRightMenu = showRightMenu;
    }

    public String getShowTopMenu() {
      return showTopMenu;
    }

    public void setShowTopMenu(String showTopMenu) {
      this.showTopMenu = showTopMenu;
    }

    public String getShowLeftMenu() {
      return showLeftMenu;
    }

    public void setShowLeftMenu(String showLeftMenu) {
      this.showLeftMenu = showLeftMenu;
    }
  }

  public class General {
    private String title;

    public String getTitle() {
      return title;
    }

    public void setTitle(String title) {
      this.title = title;
    }
  }

  public class RCOMBRequestTimeouts {

    @JsonProperty("readTimeout")
    private String readTimeout;

    @JsonProperty("connectTimeout")
    private String connectTimeout;

    public String getReadTimeout() {
      return readTimeout;
    }

    public void setReadTimeout(String readTimeout) {
      this.readTimeout = readTimeout;
    }

    public String getConnectTimeout() {
      return connectTimeout;
    }

    public void setConnectTimeout(String connectTimeout) {
      this.connectTimeout = connectTimeout;
    }
  }

  public class SmartBannersLinks {

    @JsonProperty("subtitleLine2")
    private String subtitleLine2;

    @JsonProperty("subtitleLine1")
    private String subtitleLine1;

    @JsonProperty("bannerImage")
    private String bannerImage;

    @JsonProperty("title")
    private String title;

    @JsonProperty("showWindowsSmartBanner")
    private String showWindowsSmartBanner;

    @JsonProperty("showIosSmartBanner")
    private String showIosSmartBanner;

    @JsonProperty("showAndroidSmartBanner")
    private String showAndroidSmartBanner;

    @JsonProperty("windows")
    private String windows;

    @JsonProperty("ios")
    private String ios;

    @JsonProperty("android")
    private String android;

    public String getSubtitleLine2() {
      return subtitleLine2;
    }

    public void setSubtitleLine2(String subtitleLine2) {
      this.subtitleLine2 = subtitleLine2;
    }

    public String getSubtitleLine1() {
      return subtitleLine1;
    }

    public void setSubtitleLine1(String subtitleLine1) {
      this.subtitleLine1 = subtitleLine1;
    }

    public String getBannerImage() {
      return bannerImage;
    }

    public void setBannerImage(String bannerImage) {
      this.bannerImage = bannerImage;
    }

    public String getTitle() {
      return title;
    }

    public void setTitle(String title) {
      this.title = title;
    }

    public String getShowWindowsSmartBanner() {
      return showWindowsSmartBanner;
    }

    public void setShowWindowsSmartBanner(String showWindowsSmartBanner) {
      this.showWindowsSmartBanner = showWindowsSmartBanner;
    }

    public String getShowIosSmartBanner() {
      return showIosSmartBanner;
    }

    public void setShowIosSmartBanner(String showIosSmartBanner) {
      this.showIosSmartBanner = showIosSmartBanner;
    }

    public String getShowAndroidSmartBanner() {
      return showAndroidSmartBanner;
    }

    public void setShowAndroidSmartBanner(String showAndroidSmartBanner) {
      this.showAndroidSmartBanner = showAndroidSmartBanner;
    }

    public String getWindows() {
      return windows;
    }

    public void setWindows(String windows) {
      this.windows = windows;
    }

    public String getIos() {
      return ios;
    }

    public void setIos(String ios) {
      this.ios = ios;
    }

    public String getAndroid() {
      return android;
    }

    public void setAndroid(String android) {
      this.android = android;
    }
  }

  public class RCOMB {

    @JsonProperty("helpUri")
    private String helpUri;

    @JsonProperty("helpText")
    private String helpText;

    @JsonProperty("shopCashOutHeader")
    private String shopCashOutHeader;

    @JsonProperty("helpIcon")
    private String helpIcon;

    @JsonProperty("contactUsText")
    private String contactUsText;

    @JsonProperty("contactUsUri")
    private String contactUsUri;

    @JsonProperty("contactUsIcon")
    private String contactUsIcon;

    @JsonProperty("cashOutInstructionsTitle")
    private String cashOutInstructionsTitle;

    @JsonProperty("cashOutInstructionsText")
    private String cashOutInstructionsText;

    @JsonProperty("whatIsShopCashOutTitle")
    private String whatIsShopCashOutTitle;

    @JsonProperty("betSlipCodeImage")
    private String betSlipCodeImage;

    @JsonProperty("collectCashOutIcon")
    private String collectCashOutIcon;

    public String getHelpUri() {
      return helpUri;
    }

    public void setHelpUri(String helpUri) {
      this.helpUri = helpUri;
    }

    public String getHelpText() {
      return helpText;
    }

    public void setHelpText(String helpText) {
      this.helpText = helpText;
    }

    public String getShopCashOutHeader() {
      return shopCashOutHeader;
    }

    public void setShopCashOutHeader(String shopCashOutHeader) {
      this.shopCashOutHeader = shopCashOutHeader;
    }

    public String getHelpIcon() {
      return helpIcon;
    }

    public void setHelpIcon(String helpIcon) {
      this.helpIcon = helpIcon;
    }

    public String getContactUsText() {
      return contactUsText;
    }

    public void setContactUsText(String contactUsText) {
      this.contactUsText = contactUsText;
    }

    public String getContactUsUri() {
      return contactUsUri;
    }

    public void setContactUsUri(String contactUsUri) {
      this.contactUsUri = contactUsUri;
    }

    public String getContactUsIcon() {
      return contactUsIcon;
    }

    public void setContactUsIcon(String contactUsIcon) {
      this.contactUsIcon = contactUsIcon;
    }

    public String getCashOutInstructionsTitle() {
      return cashOutInstructionsTitle;
    }

    public void setCashOutInstructionsTitle(String cashOutInstructionsTitle) {
      this.cashOutInstructionsTitle = cashOutInstructionsTitle;
    }

    public String getCashOutInstructionsText() {
      return cashOutInstructionsText;
    }

    public void setCashOutInstructionsText(String cashOutInstructionsText) {
      this.cashOutInstructionsText = cashOutInstructionsText;
    }

    public String getWhatIsShopCashOutTitle() {
      return whatIsShopCashOutTitle;
    }

    public void setWhatIsShopCashOutTitle(String whatIsShopCashOutTitle) {
      this.whatIsShopCashOutTitle = whatIsShopCashOutTitle;
    }

    public String getBetSlipCodeImage() {
      return betSlipCodeImage;
    }

    public void setBetSlipCodeImage(String betSlipCodeImage) {
      this.betSlipCodeImage = betSlipCodeImage;
    }

    public String getCollectCashOutIcon() {
      return collectCashOutIcon;
    }

    public void setCollectCashOutIcon(String collectCashOutIcon) {
      this.collectCashOutIcon = collectCashOutIcon;
    }
  }

  public class RCOMBDelays {
    @JsonProperty("noOfInvalidCodes")
    private String noOfInvalidCodes;

    @JsonProperty("firstDelay")
    private String firstDelay;

    @JsonProperty("incrementsBy")
    private String incrementsBy;

    @JsonProperty("stopIncrements")
    private String stopIncrements;

    @JsonProperty("timeoutInvalid")
    private String timeoutInvalid;

    public String getNoOfInvalidCodes() {
      return noOfInvalidCodes;
    }

    public void setNoOfInvalidCodes(String noOfInvalidCodes) {
      this.noOfInvalidCodes = noOfInvalidCodes;
    }

    public String getFirstDelay() {
      return firstDelay;
    }

    public void setFirstDelay(String firstDelay) {
      this.firstDelay = firstDelay;
    }

    public String getIncrementsBy() {
      return incrementsBy;
    }

    public void setIncrementsBy(String incrementsBy) {
      this.incrementsBy = incrementsBy;
    }

    public String getStopIncrements() {
      return stopIncrements;
    }

    public void setStopIncrements(String stopIncrements) {
      this.stopIncrements = stopIncrements;
    }

    public String getTimeoutInvalid() {
      return timeoutInvalid;
    }

    public void setTimeoutInvalid(String timeoutInvalid) {
      this.timeoutInvalid = timeoutInvalid;
    }
  }

  public class RetailGeoLocation {
    @JsonProperty("deviceLocationEndpoint")
    private String deviceLocationEndpoint;

    @JsonProperty("deviceLocationUsername")
    private String deviceLocationUsername;

    public String getDeviceLocationEndpoint() {
      return deviceLocationEndpoint;
    }

    public void setDeviceLocationEndpoint(String deviceLocationEndpoint) {
      this.deviceLocationEndpoint = deviceLocationEndpoint;
    }

    public String getDeviceLocationUsername() {
      return deviceLocationUsername;
    }

    public void setDeviceLocationUsername(String deviceLocationUsername) {
      this.deviceLocationUsername = deviceLocationUsername;
    }
  }

  public class RetailConfig {
    @JsonProperty("checkLocation")
    private String checkLocation;

    @JsonProperty("disableDeviceLocation")
    private String disableDeviceLocation;

    @JsonProperty("deniedLocationText")
    private String deniedLocationText;

    @JsonProperty("waitingLocationText")
    private String waitingLocationText;

    @JsonProperty("disableIPLocation")
    private String disableIPLocation;

    @JsonProperty("allowedCountries")
    private String allowedCountries;

    public String getCheckLocation() {
      return checkLocation;
    }

    public void setCheckLocation(String checkLocation) {
      this.checkLocation = checkLocation;
    }

    public String getDisableDeviceLocation() {
      return disableDeviceLocation;
    }

    public void setDisableDeviceLocation(String disableDeviceLocation) {
      this.disableDeviceLocation = disableDeviceLocation;
    }

    public String getDeniedLocationText() {
      return deniedLocationText;
    }

    public void setDeniedLocationText(String deniedLocationText) {
      this.deniedLocationText = deniedLocationText;
    }

    public String getWaitingLocationText() {
      return waitingLocationText;
    }

    public void setWaitingLocationText(String waitingLocationText) {
      this.waitingLocationText = waitingLocationText;
    }

    public String getDisableIPLocation() {
      return disableIPLocation;
    }

    public void setDisableIPLocation(String disableIPLocation) {
      this.disableIPLocation = disableIPLocation;
    }

    public String getAllowedCountries() {
      return allowedCountries;
    }

    public void setAllowedCountries(String allowedCountries) {
      this.allowedCountries = allowedCountries;
    }
  }

  public class RetailIpLocation {
    @JsonProperty("IPLocationEndpoint")
    private String iPLocationEndpoint;

    @JsonProperty("IPLocationApiKey")
    private String iPLocationApiKey;

    public String getIPLocationEndpoint() {
      return iPLocationEndpoint;
    }

    public void setIPLocationEndpoint(String iPLocationEndpoint) {
      this.iPLocationEndpoint = iPLocationEndpoint;
    }

    public String getIPLocationApiKey() {
      return iPLocationApiKey;
    }

    public void setIPLocationApiKey(String iPLocationApiKey) {
      this.iPLocationApiKey = iPLocationApiKey;
    }
  }

  public class RcombOnlyTest {
    @JsonProperty("newName")
    private String newName;

    public String getNewName() {
      return newName;
    }

    public void setNewName(String newName) {
      this.newName = newName;
    }
  }

  public class RetailAuditCreds {
    @JsonProperty("username")
    private String username;

    @JsonProperty("password")
    private String password;

    public String getUsername() {
      return username;
    }

    public void setUsername(String username) {
      this.username = username;
    }

    public String getPassword() {
      return password;
    }

    public void setPassword(String password) {
      this.password = password;
    }
  }
}
