package com.coral.oxygen.cms.api.impl

import com.coral.oxygen.cms.api.CmsService
import com.coral.oxygen.cms.api.HealthStatus
import com.coral.oxygen.middleware.pojos.model.cms.*
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContent
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContentItem
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPage
import com.coral.oxygen.middleware.pojos.model.output.AssetManagement
import okhttp3.MediaType
import okhttp3.OkHttpClient
import okhttp3.ResponseBody

import org.springframework.test.util.ReflectionTestUtils

import retrofit2.Call
import retrofit2.Response

import spock.lang.Specification

class CmsServiceImplSpec extends Specification {

  CmsEndpoint cmsEndpoint = Mock()
  Call<ModularContent> call = Mock()

  CmsService cmsService

  void setup() {
    cmsService = new CmsServiceImpl('https://invictus.coral.co.uk', new OkHttpClient())
  }

  def "Request Modular Content"() {
    given:
    List<Long> eventsIds = Arrays.asList(1L, 2L, 3L)
    ModularContentItem modularContentItem = new ModularContentItem()
    modularContentItem.setEventsIds(eventsIds)
    ModularContent content = new ModularContent()
    content.add(modularContentItem)

    Response<ModularContent> response = Response.success(content)

    call.execute() >> response

    cmsEndpoint.getModularContent() >> call

    ReflectionTestUtils.setField(cmsService, 'cmsEndpoint', cmsEndpoint)

    when:
    ModularContent result = cmsService.requestModularContent()

    then:
    cmsService.getHealthStatus() == HealthStatus.OK
    result.getEventsIds() != null
    result.getEventsIds().size() == 3
    result.getEventsIds().containsAll(eventsIds)
  }

  def "Request Modular Content 404 response"() {
    given:
    Response<String> response = Response.error(
        404,
        ResponseBody.create(
        MediaType.parse('application/json'),
        "{\"key\":[\"errorMessage\"]}"
        )
        )

    call.execute() >> response

    cmsEndpoint.getModularContent() >> call

    ReflectionTestUtils.setField(cmsService, 'cmsEndpoint', cmsEndpoint)

    when:
    ModularContent result = cmsService.requestModularContent()

    then:
    thrown RuntimeException
    cmsService.getHealthStatus() == HealthStatus.OK
  }

  def "Request Modular Content - Fail"() {
    given:
    call.execute() >> { throw new IOException() }

    cmsEndpoint.getModularContent() >> call

    ReflectionTestUtils.setField(cmsService, 'cmsEndpoint', cmsEndpoint)

    when:
    cmsService.requestModularContent()

    then:
    thrown RuntimeException
    cmsService.getHealthStatus() == HealthStatus.OUT_OF_SERVICE
  }

  def "Request Inplay Data - Fail"() {
    given:
    call.execute() >> { throw new IOException() }

    cmsEndpoint.getInplayData() >> call

    ReflectionTestUtils.setField(cmsService, 'cmsEndpoint', cmsEndpoint)

    when:
    cmsService.requestInplayData()

    then:
    thrown RuntimeException
    cmsService.getHealthStatus() == HealthStatus.OUT_OF_SERVICE
  }

  def "Request System Config"() {
    given:
    CmsSystemConfig systemConfig = new CmsSystemConfig()
    CmsSystemConfig.YourCallIconsAndTabs yourCallIconsAndTabs = new CmsSystemConfig.YourCallIconsAndTabs()
    yourCallIconsAndTabs.setEnableIcon(true)
    systemConfig.setYourCallIconsAndTabs(yourCallIconsAndTabs)

    Response<CmsSystemConfig> response = Response.success(systemConfig)

    call.execute() >> response

    cmsEndpoint.getSystemConfig() >> call

    ReflectionTestUtils.setField(cmsService, 'cmsEndpoint', cmsEndpoint)

    when:
    CmsSystemConfig result = cmsService.requestSystemConfig()

    then:
    cmsService.getHealthStatus() == HealthStatus.OK
    result.getYourCallIconsAndTabs() != null
    result.getYourCallIconsAndTabs().isEnableIcon()
  }

  def "Request System Config - Fail"() {
    given:
    call.execute() >> { throw new IOException() }

    cmsEndpoint.getSystemConfig() >> call

    ReflectionTestUtils.setField(cmsService, 'cmsEndpoint', cmsEndpoint)

    when:
    CmsSystemConfig result = cmsService.requestSystemConfig()

    then:
    cmsService.getHealthStatus() == HealthStatus.OUT_OF_SERVICE
    result.getYourCallIconsAndTabs() == null
  }

  def "Request Get YC Leagues"() {
    given:
    CmsYcLeague cmsYcLeague = new CmsYcLeague()
    cmsYcLeague.setName('league')
    cmsYcLeague.setTypeId(1)
    cmsYcLeague.setEnabled(true)

    List<CmsYcLeague> cmsYcLeagueList = Arrays.asList(cmsYcLeague)

    Response<CmsSystemConfig> response = Response.success(cmsYcLeagueList)

    call.execute() >> response

    cmsEndpoint.getYcLeagues() >> call

    ReflectionTestUtils.setField(cmsService, 'cmsEndpoint', cmsEndpoint)

    when:
    List<CmsYcLeague> result = cmsService.requestYcLeagues()

    then:
    cmsService.getHealthStatus() == HealthStatus.OK
    result != null
    result.size() == 1
    result.get(0).getEnabled()
    result.get(0).getName() == 'league'
    result.get(0).getTypeId() == 1
  }

  def "Request Get YC Leagues - Fail"() {
    given:
    CmsYcLeague cmsYcLeague = new CmsYcLeague()
    cmsYcLeague.setName('league')
    cmsYcLeague.setTypeId(1)
    cmsYcLeague.setEnabled(true)

    call.execute() >> { throw new IOException() }

    cmsEndpoint.getYcLeagues() >> call

    ReflectionTestUtils.setField(cmsService, 'cmsEndpoint', cmsEndpoint)

    when:
    List<CmsYcLeague> result = cmsService.requestYcLeagues()

    then:
    cmsService.getHealthStatus() == HealthStatus.OUT_OF_SERVICE
    result != null
    result.isEmpty()
  }

  def "Request Pages"() {
    given:
    SportPage sportPage = new SportPage(null,null)
    Collection<SportPage> sportPages = Arrays.asList(sportPage)

    Response<Collection<SportPage>> response = Response.success(sportPages)

    call.execute() >> response

    cmsEndpoint.findAllPagesByBrand(1640176190014) >> call

    ReflectionTestUtils.setField(cmsService, 'cmsEndpoint', cmsEndpoint)

    when:
    Collection<SportPage> result = cmsService.requestPages(1640176190014)

    then:
    cmsService.getHealthStatus() == HealthStatus.OK
  }

  def "Get Fanzones"() {
    given:
    Fanzone fanzone = new Fanzone()
    Collection<Fanzone> fanzoneList = Arrays.asList(fanzone)

    Response<Collection<Fanzone>> response = Response.success(fanzoneList)

    call.execute() >> response

    cmsEndpoint.findAllFanzoneByBrand() >> call

    ReflectionTestUtils.setField(cmsService, 'cmsEndpoint', cmsEndpoint)

    when:
    Collection<Fanzone> result = cmsService.getFanzones()

    then:
    cmsService.getHealthStatus() == HealthStatus.OK
  }

  def "Get Fanzones - Fail"() {
    given:
    call.execute() >> { throw new IOException() }

    cmsEndpoint.findAllFanzoneByBrand() >> call

    ReflectionTestUtils.setField(cmsService, 'cmsEndpoint', cmsEndpoint)

    when:
    Collection<Fanzone> result = cmsService.getFanzones()

    then:
    cmsService.getHealthStatus() == HealthStatus.OUT_OF_SERVICE
  }

  def "Request Pages - Fail"() {
    given:
    call.execute() >> { throw new IOException() }

    cmsEndpoint.findAllPagesByBrand(1640176190014) >> call

    ReflectionTestUtils.setField(cmsService, 'cmsEndpoint', cmsEndpoint)

    when:
    Collection<SportPage> result = cmsService.requestPages(1640176190014)

    then:
    cmsService.getHealthStatus() == HealthStatus.OUT_OF_SERVICE
  }

  def "get AssetManagementInfo ByBrand"() {
    given:
    AssetManagement assetManagement = new AssetManagement()
    Collection<SportPage> assetManagements = Arrays.asList(assetManagement)

    Response<Collection<SportPage>> response = Response.success(assetManagements)

    call.execute() >> response

    cmsEndpoint.getAssetManagementInfo() >> call

    ReflectionTestUtils.setField(cmsService, 'cmsEndpoint', cmsEndpoint)

    when:
    Collection<AssetManagement> result = cmsService.getAssetManagementInfoByBrand()

    then:
    cmsService.getHealthStatus() == HealthStatus.OK
  }

  def "get AssetManagementInfo ByBrand Fail"() {
    given:

    call.execute() >> { throw new IOException() }

    cmsEndpoint.getAssetManagementInfo() >> call

    ReflectionTestUtils.setField(cmsService, 'cmsEndpoint', cmsEndpoint)

    when:
    Collection<AssetManagement> result = cmsService.getAssetManagementInfoByBrand()

    then:
    cmsService.getHealthStatus() == HealthStatus.OUT_OF_SERVICE
  }
  def "Get Virtual Sports"() {
    given:
    VirtualSportEvents vs = new VirtualSportEvents("Football",4)

    List<VirtualSportEvents> vsList = Arrays.asList(vs)

    Response<List<VirtualSportEvents>> response = Response.success(vsList)

    call.execute() >> response

    cmsEndpoint.findVirtualSportsConfigs() >> call

    ReflectionTestUtils.setField(cmsService, 'cmsEndpoint', cmsEndpoint)

    when:
    List<VirtualSportEvents> result = cmsService.getVirtualSportsByBrand()

    then:
    cmsService.getHealthStatus() == HealthStatus.OK
    vsList.size() == result.size()
  }
  def "Get Virtual Sports Fail"() {
    given:
    VirtualSportEvents vs = new VirtualSportEvents("Football",4)

    List<VirtualSportEvents> vsList = Arrays.asList(vs)

    Response<List<VirtualSportEvents>> response = Response.success(vsList)

    call.execute() >> { throw new IOException() }

    cmsEndpoint.findVirtualSportsConfigs() >> call

    ReflectionTestUtils.setField(cmsService, 'cmsEndpoint', cmsEndpoint)

    when:
    List<VirtualSportEvents> result = cmsService.getVirtualSportsByBrand()

    then:
    cmsService.getHealthStatus() == HealthStatus.OUT_OF_SERVICE
  }
}
