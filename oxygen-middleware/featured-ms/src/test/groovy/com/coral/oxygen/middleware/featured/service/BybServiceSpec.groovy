package com.coral.oxygen.middleware.featured.service

import com.coral.oxygen.cms.api.CmsService
import com.coral.oxygen.cms.api.SystemConfigProvider
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig
import com.coral.oxygen.middleware.pojos.model.cms.CmsYcLeague
import com.ladbrokescoral.oxygen.byb.banach.client.BlockingBanachClient
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetLeaguesResponseDto
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.LeaguesResponse
import spock.lang.Specification

class BybServiceSpec extends Specification {
  static final int BYB_TYPE_ID = 14

  BybService bybService

  SystemConfigProvider systemConfigProvider
  CmsService cmsService
  BlockingBanachClient<GetLeaguesResponseDto, LeaguesResponse> leaguesClientMock

  def setup() {
    systemConfigProvider = Mock(SystemConfigProvider)
    cmsService = Mock(CmsService)
    leaguesClientMock = Mock(BlockingBanachClient)

    bybService = new BybService(systemConfigProvider, cmsService, leaguesClientMock)
  }

  def cleanup() {
    bybService = null
  }

  def "Test success"() {
    configureServices(BYB_TYPE_ID, true, true)

    when:
    bybService.reloadData()

    then:
    bybService.isBuildYourBetAvailableForType(BYB_TYPE_ID)
  }

  def "Test icons disabled"() {
    configureServices(BYB_TYPE_ID, false, true)

    when:
    bybService.reloadData()

    then:
    !bybService.isBuildYourBetAvailableForType(BYB_TYPE_ID)
  }

  def "Test Cms league disabled"() {
    configureServices(BYB_TYPE_ID, true, false)

    when:
    bybService.reloadData()

    then:
    !bybService.isBuildYourBetAvailableForType(BYB_TYPE_ID)
  }

  def "Test Cms league not found"() {
    configureServices(13, true, true)

    when:
    bybService.reloadData()

    then:
    !bybService.isBuildYourBetAvailableForType(BYB_TYPE_ID)
  }

  def "Test Yc league not found"() {
    mockCmsConfig(true)
    mockCmsYcLeagues(true, BYB_TYPE_ID)
    mockBybLeagues(13)

    when:
    bybService.reloadData()

    then:
    !bybService.isBuildYourBetAvailableForType(BYB_TYPE_ID)
  }

  def testIconsEnabledAndThenDisabled() {
    configureServices(BYB_TYPE_ID, true, true)
    bybService.reloadData()

    when:
    bybService.reloadData()

    then:
    systemConfigProvider.systemConfig() >> prepareCmsSystemConfigSetIconsEnabled(false)
    !bybService.isBuildYourBetAvailableForType(BYB_TYPE_ID)
  }

  private void configureServices(int bybLId, boolean cmsEnabled, boolean leagueEnabled) {
    mockCmsConfig(cmsEnabled)
    mockCmsYcLeagues(leagueEnabled, bybLId)
    mockBybLeagues(bybLId)
  }

  private CmsSystemConfig prepareCmsSystemConfigSetIconsEnabled(Boolean iconsEnabled){
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig()
    CmsSystemConfig.YourCallIconsAndTabs iconsAndTabs = new CmsSystemConfig.YourCallIconsAndTabs()
    iconsAndTabs.setEnableIcon(iconsEnabled)
    cmsSystemConfig.setYourCallIconsAndTabs(iconsAndTabs)

    return cmsSystemConfig
  }

  private void mockCmsConfig(Boolean iconsEnabled) {
    CmsSystemConfig cmsSystemConfig = prepareCmsSystemConfigSetIconsEnabled(iconsEnabled)
    systemConfigProvider.systemConfig() >> cmsSystemConfig
  }

  private void mockCmsYcLeagues(boolean enabled, int ... typeId) {
    List<CmsYcLeague> cmsLeagues = new ArrayList<>()
    for (int id : typeId) {
      CmsYcLeague league = new CmsYcLeague()
      league.setTypeId(id)
      league.setEnabled(enabled)
      cmsLeagues.add(league)
    }
    cmsService.requestYcLeagues() >> cmsLeagues
  }

  private void mockBybLeagues(long typeId) {
    GetLeaguesResponseDto dto = new GetLeaguesResponseDto()
    dto.setObTypeId(typeId)
    List<GetLeaguesResponseDto> leaguesResponseDtos = new ArrayList<>()
    leaguesResponseDtos.add(dto)
    LeaguesResponse bybResponse = new LeaguesResponse(leaguesResponseDtos)
    leaguesClientMock.execute(_ as String) >> bybResponse
  }
}
