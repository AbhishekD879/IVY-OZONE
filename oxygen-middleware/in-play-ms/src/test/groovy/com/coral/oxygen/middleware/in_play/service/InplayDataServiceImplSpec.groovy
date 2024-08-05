package com.coral.oxygen.middleware.in_play.service

import com.coral.oxygen.middleware.common.configuration.DistributedKey
import com.coral.oxygen.middleware.common.imdg.DistributedInstance
import com.coral.oxygen.middleware.common.service.GenerationKeyType
import com.coral.oxygen.middleware.common.service.GenerationStorageService
import com.coral.oxygen.middleware.in_play.service.model.InPlayCache
import com.coral.oxygen.middleware.in_play.service.model.RawIndex
import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportEvents
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportsRibbon
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportsRibbonItem
import com.google.gson.Gson
import spock.lang.Ignore
import spock.lang.Specification

class InplayDataServiceImplSpec extends Specification {

  GenerationStorageService generationStorageService = Mock()
  DistributedInstance distributedInstance = Mock()

  InplayDataServiceImpl inplayDataService
  String version = "123"
  Gson gson = new Gson()

  def setup() {
    inplayDataService = new InplayDataServiceImpl(gson,distributedInstance,generationStorageService)
  }

  def "Get Inplay Model"() {
    given:
    InPlayData inPlayData = new InPlayData()
    distributedInstance.getValue(DistributedKey.INPLAY_STRUCTURE_MAP, version) >> gson.toJson(inPlayData)

    expect:
    inPlayData.generation() == inplayDataService.getInPlayModel(version).generation()
  }

  def "Get Sports Ribbon"() {
    given:
    SportsRibbon sportsRibbon = new SportsRibbon()
    sportsRibbon.setItems(Arrays.asList(new SportsRibbonItem()))
    distributedInstance.getValue(DistributedKey.INPLAY_SPORTS_RIBBON_MAP, version) >> gson.toJson(sportsRibbon)

    expect:
    sportsRibbon.getItems().size() == inplayDataService.getSportsRibbon(version).getItems().size()
  }

  def "Get InPlay Cache"() {
    given:
    RawIndex rawIndex = new RawIndex("1::2::3")
    InPlayCache inPlayCache = new InPlayCache()
    InPlayCache.SportSegmentCache sportSegmentCache = new InPlayCache.SportSegmentCache(new SportSegment())
    sportSegmentCache.setStructuredKey(rawIndex)
    inPlayCache.setSportSegmentCaches(Arrays.asList(sportSegmentCache))
    distributedInstance.getValue(DistributedKey.INPLAY_CACHED_STRUCTURE_MAP, "1::2::3") >> gson.toJson(inPlayCache)

    expect:
    !inplayDataService.getInPlayCache("1::2::3").getSportSegmentCaches().isEmpty()
    inPlayCache.getSportSegmentCaches().get(0) == inplayDataService.getInPlayCache("1::2::3").getSportSegmentCaches().get(0)
  }

  def "Get Generation"() {
    given:
    generationStorageService.getLatest(GenerationKeyType.INPLAY_GENERATION) >> version

    expect:
    version == inplayDataService.getGeneration()
  }

  def "Get sport segment"() {
    given:
    SportSegment sportSegment = new SportSegment()
    sportSegment.setCategoryId(16)
    distributedInstance.getValue(DistributedKey.INPLAY_SPORT_SEGMENT_MAP, version) >> gson.toJson(sportSegment)

    expect:
    sportSegment.getCategoryId() == inplayDataService.getSportSegment(version).getCategoryId()
  }
  def "Get Virtual sport"() {
    given:
    VirtualSportEvents vs = new VirtualSportEvents("Cricket",2)
    List<VirtualSportEvents> vsList = Arrays.asList(vs)

    distributedInstance.getValue(DistributedKey.VIRTUAL_SPORTS_STRUCTURE_MAP, version) >> gson.toJson(vsList)

    expect:
    vsList.size() == inplayDataService.getVirtualSportData(version).size()
  }

  @Ignore
  def "Get Virtual sport Fail"() {
    given:
    VirtualSportEvents vs = new VirtualSportEvents("Cricket",2)
    List<VirtualSportEvents> vsList = Arrays.asList(vs)

    distributedInstance.getValue(DistributedKey.VIRTUAL_SPORTS_STRUCTURE_MAP, version) >> gson.toJson(vsList)
    inplayDataService.fromJson(gson.toJson(vsList)) >> new UnsupportedEncodingException()


    expect:
    inplayDataService.getVirtualSportData(version).isEmpty()
  }
}
