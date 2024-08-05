package com.coral.oxygen.middleware.in_play.service


import com.coral.oxygen.middleware.common.imdg.DistributedAtomicLong
import com.coral.oxygen.middleware.common.imdg.DistributedInstance
import com.coral.oxygen.middleware.common.service.ErrorsStorageService
import com.coral.oxygen.middleware.common.service.GenerationKeyType
import com.coral.oxygen.middleware.common.service.GenerationStorageService
import com.coral.oxygen.middleware.in_play.service.model.InPlayCache
import com.coral.oxygen.middleware.in_play.service.scoreboards.ScoreboardCache
import com.coral.oxygen.middleware.pojos.model.InPlayTopLevelType
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayModel
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportsRibbon
import spock.lang.Specification

import java.util.function.Function
import java.util.stream.Collectors

import static com.coral.oxygen.middleware.common.configuration.DistributedKey.*
import static com.coral.oxygen.middleware.common.service.GenerationKeyType.INPLAY_GENERATION

class InPlayStorageServiceSpec extends Specification {
  InPlayStorageService storageService
  DistributedInstance distributedInstance
  GenerationStorageService generationStorage
  ErrorsStorageService errorsStorage
  DistributedAtomicLong atomicLong

  def setup() {
    distributedInstance = Mock(DistributedInstance)
    generationStorage = Mock(GenerationStorageService)
    errorsStorage = Mock(ErrorsStorageService)
    atomicLong = Mock(DistributedAtomicLong)

    distributedInstance.getAtomicLong(ATOMIC_INPLAY_DATA) >> atomicLong

    storageService = new InPlayStorageService(distributedInstance, generationStorage, errorsStorage,TestTools.GSON)
  }

  def cleanup() {
    storageService = null
  }

  def "Saving - verify maps filling and methods calls"() {
    List<SportSegment> segments = new ArrayList<>()

    SportSegment sportSegment1 = new SportSegment()
    sportSegment1.setCategoryId(1)
    sportSegment1.setTopLevelType(InPlayTopLevelType.LIVE_EVENT)
    segments.add(sportSegment1)

    SportSegment sportSegment3 = new SportSegment()
    sportSegment3.setCategoryId(3)
    sportSegment3.setTopLevelType(InPlayTopLevelType.STREAM_EVENT)
    segments.add(sportSegment3)

    SportSegment sportSegment1_stream = new SportSegment()
    sportSegment1_stream.setCategoryId(1)
    sportSegment1_stream.setTopLevelType(InPlayTopLevelType.STREAM_EVENT)
    segments.add(sportSegment1_stream)

    SportSegment sportSegment2 = new SportSegment()
    sportSegment2.setCategoryId(2)
    sportSegment2.setTopLevelType(InPlayTopLevelType.UPCOMING_EVENT)
    segments.add(sportSegment2)

    SportSegment sportSegment4 = new SportSegment()
    sportSegment4.setCategoryId(4)
    sportSegment4.setTopLevelType(InPlayTopLevelType.UPCOMING_STREAM_EVENT)
    segments.add(sportSegment4)

    SportsRibbon sportsRibbon = new SportsRibbon()
    InPlayData structure = new InPlayData(new InPlayModel(), new InPlayModel(), new InPlayModel(), new InPlayModel())


    atomicLong.addAndGet(_ as Long) >> 13L

    when:
    storageService.save(structure, segments, sportsRibbon)

    then:
    1 * distributedInstance.updateExpirableValue(INPLAY_CACHED_STRUCTURE_MAP, "13", _ as String)
    1 * distributedInstance.updateExpirableValue(INPLAY_SPORT_SEGMENT_MAP, "13::1::LIVE_EVENT", TestTools.GSON.toJson(sportSegment1))
    1 * distributedInstance.updateExpirableValue(INPLAY_SPORT_SEGMENT_MAP, "13::1::STREAM_EVENT", TestTools.GSON.toJson(sportSegment1_stream))
    1 * distributedInstance.updateExpirableValue(INPLAY_SPORT_SEGMENT_MAP, "13::3::STREAM_EVENT", TestTools.GSON.toJson(sportSegment3))
    1 * distributedInstance.updateExpirableValue(INPLAY_SPORT_SEGMENT_MAP, "13::2::UPCOMING_EVENT", TestTools.GSON.toJson(sportSegment2))
    1 * distributedInstance.updateExpirableValue(INPLAY_SPORT_SEGMENT_MAP, "13::4::UPCOMING_STREAM_EVENT", TestTools.GSON.toJson(sportSegment4))
    1 * distributedInstance.updateExpirableValue(INPLAY_SPORTS_RIBBON_MAP, "13", TestTools.GSON.toJson(sportsRibbon))
    1 * generationStorage.putLatest(GenerationKeyType.INPLAY_GENERATION, "13")
  }

  def "Get latest in-play data - result string checking"() {
    InPlayData structure = new InPlayData(new InPlayModel(), new InPlayModel(), new InPlayModel(), new InPlayModel())
    String structureJson = TestTools.GSON.toJson(structure)

    generationStorage.getLatest(GenerationKeyType.INPLAY_GENERATION) >> 13L
    distributedInstance.getValue(INPLAY_STRUCTURE_MAP, "13") >> structureJson

    when:
    String result = storageService.getLatestInPlayData()

    then:
    structureJson == result
  }

  def "Get latest in-play data - result object checking"() {
    InPlayData structure = new InPlayData(new InPlayModel(), new InPlayModel(), new InPlayModel(), new InPlayModel())
    String structureJson = TestTools.GSON.toJson(structure)

    generationStorage.getLatest(GenerationKeyType.INPLAY_GENERATION) >> 13L
    distributedInstance.getValue(INPLAY_STRUCTURE_MAP, "13") >> structureJson

    when:
    InPlayData result = storageService.getLatestInPlayDataObject()

    then:
    structureJson == TestTools.GSON.toJson(result)
  }

  def "Get latest in-play data - object null"() {
    generationStorage.getLatest(GenerationKeyType.INPLAY_GENERATION) >> 13L
    distributedInstance.getValue(INPLAY_STRUCTURE_MAP, "13") >> null

    when:
    InPlayData result = storageService.getLatestInPlayDataObject()

    then:
    result == null
  }

  def "Get latest in-play data - object corrupted"() {
    generationStorage.getLatest(GenerationKeyType.INPLAY_GENERATION) >> 13L
    distributedInstance.getValue(INPLAY_STRUCTURE_MAP, "13") >> "aBC"

    when:
    InPlayData result = storageService.getLatestInPlayDataObject()

    then:
    result == null
  }

  def "Get latest sports ribbon"() {
    SportsRibbon sportsRibbon = new SportsRibbon()
    String ribbonJson = TestTools.GSON.toJson(sportsRibbon)

    generationStorage.getLatest(GenerationKeyType.INPLAY_GENERATION) >> "13"
    distributedInstance.getValue(INPLAY_SPORTS_RIBBON_MAP, "13") >> ribbonJson

    when:
    String result = storageService.getLatestSportsRibbon()

    then:
    ribbonJson == result
  }

  def "Get latest sports ribbon object"() {
    SportsRibbon sportsRibbon = new SportsRibbon()
    String ribbonJson = TestTools.GSON.toJson(sportsRibbon)

    generationStorage.getLatest(GenerationKeyType.INPLAY_GENERATION) >> "13"
    distributedInstance.getValue(INPLAY_SPORTS_RIBBON_MAP, "13") >> ribbonJson

    when:
    SportsRibbon result = storageService.getLatestSportsRibbonObject()

    then:
    ribbonJson == TestTools.GSON.toJson(result)
  }

  def "Get latest sports ribbon - object null"() {
    generationStorage.getLatest(GenerationKeyType.INPLAY_GENERATION) >> "13"
    distributedInstance.getValue(INPLAY_SPORTS_RIBBON_MAP, "13") >> null

    when:
    SportsRibbon result = storageService.getLatestSportsRibbonObject()

    then:
    result == null
  }

  def "Get latest sports ribbon - object corrupted"() {
    generationStorage.getLatest(GenerationKeyType.INPLAY_GENERATION) >> "13"
    distributedInstance.getValue(INPLAY_SPORTS_RIBBON_MAP, "13") >> "ABC"

    when:
    SportsRibbon result = storageService.getLatestSportsRibbonObject()

    then:
    result == null
  }

  def "Get latest sport segment"() {
    SportSegment segment = new SportSegment()
    String segmentJson = TestTools.GSON.toJson(segment)

    generationStorage.getLatest(GenerationKeyType.INPLAY_GENERATION) >> "13"
    distributedInstance.getValue(INPLAY_SPORT_SEGMENT_MAP, "13::1::UPCOMING_EVENT") >> segmentJson

    when:
    String result = storageService.getLatestSportSegment("1::UPCOMING_EVENT")

    then:
    segmentJson == result
  }

  def "Get latest sport segments objects"() {
    InPlayData structure = new InPlayData(new InPlayModel(), new InPlayModel(), new InPlayModel(), new InPlayModel())
    SportSegment sportSegment1 = new SportSegment()
    sportSegment1.setCategoryId(1)
    sportSegment1.setTopLevelType(InPlayTopLevelType.LIVE_EVENT)
    SportSegment sportSegment2 = new SportSegment()
    sportSegment2.setCategoryId(2)
    sportSegment2.setTopLevelType(InPlayTopLevelType.UPCOMING_EVENT)
    SportSegment sportSegment3 = new SportSegment()
    sportSegment3.setCategoryId(3)
    sportSegment3.setTopLevelType(InPlayTopLevelType.STREAM_EVENT)
    SportSegment sportSegment4 = new SportSegment()
    sportSegment4.setCategoryId(4)
    sportSegment4.setTopLevelType(InPlayTopLevelType.UPCOMING_STREAM_EVENT)

    structure.getLivenow().getSportEvents().add(sportSegment1)
    structure.getUpcoming().getSportEvents().add(sportSegment2)
    structure.getLiveStream().getSportEvents().add(sportSegment3)
    structure.getUpcomingLiveStream().getSportEvents().add(sportSegment4)

    generationStorage.getLatest(GenerationKeyType.INPLAY_GENERATION) >> "13"
    distributedInstance.getValue(INPLAY_STRUCTURE_MAP, "13") >> TestTools.GSON.toJson(structure)
    distributedInstance.getValues(INPLAY_SPORT_SEGMENT_MAP,
        [
          "13::1::LIVE_EVENT",
          "13::2::UPCOMING_EVENT",
          "13::3::STREAM_EVENT",
          "13::4::UPCOMING_STREAM_EVENT"
        ]) >>
        [
          TestTools.GSON.toJson(sportSegment1),
          TestTools.GSON.toJson(sportSegment2),
          TestTools.GSON.toJson(sportSegment3),
          TestTools.GSON.toJson(sportSegment4)
        ]

    when:
    Map<Integer, SportSegment> segments = storageService.getLatestSportSegmentsObjects().stream()
        .collect(Collectors.toMap({ sportSegment->sportSegment.getCategoryId()}, Function.identity()))

    then:
    4 == segments.size()
    TestTools.GSON.toJson(sportSegment1) == TestTools.GSON.toJson(segments.get(1))
    TestTools.GSON.toJson(sportSegment2) == TestTools.GSON.toJson(segments.get(2))
    TestTools.GSON.toJson(sportSegment3) == TestTools.GSON.toJson(segments.get(3))
    TestTools.GSON.toJson(sportSegment4) == TestTools.GSON.toJson(segments.get(4))
  }

  def "Get latest sport segments objects - nullJson"() {
    InPlayData structure = new InPlayData(new InPlayModel(), new InPlayModel(), new InPlayModel(), new InPlayModel())
    SportSegment sportSegment1 = new SportSegment()
    sportSegment1.setCategoryId(1)
    sportSegment1.setTopLevelType(InPlayTopLevelType.LIVE_EVENT)
    SportSegment sportSegment2 = new SportSegment()
    sportSegment2.setCategoryId(2)
    sportSegment2.setTopLevelType(InPlayTopLevelType.UPCOMING_EVENT)
    SportSegment sportSegment3 = new SportSegment()
    sportSegment3.setCategoryId(3)
    sportSegment3.setTopLevelType(InPlayTopLevelType.STREAM_EVENT)
    SportSegment sportSegment4 = new SportSegment()
    sportSegment4.setCategoryId(4)
    sportSegment4.setTopLevelType(InPlayTopLevelType.UPCOMING_STREAM_EVENT)

    structure.getLivenow().getSportEvents().add(sportSegment1)
    structure.getUpcoming().getSportEvents().add(sportSegment2)
    structure.getLiveStream().getSportEvents().add(sportSegment3)
    structure.getUpcomingLiveStream().getSportEvents().add(sportSegment4)

    generationStorage.getLatest(GenerationKeyType.INPLAY_GENERATION) >> "13"
    distributedInstance.getValue(INPLAY_STRUCTURE_MAP, "13") >> TestTools.GSON.toJson(structure)
    distributedInstance.getValues(INPLAY_SPORT_SEGMENT_MAP,
        [
          "13::1::LIVE_EVENT",
          "13::2::UPCOMING_EVENT",
          "13::3::STREAM_EVENT",
          "13::4::UPCOMING_STREAM_EVENT"
        ]) >> [
          TestTools.GSON.toJson(sportSegment1)
        ]

    when:
    Map<Integer, SportSegment> segments = storageService.getLatestSportSegmentsObjects().stream()
        .collect(Collectors.toMap({ sportSegment->sportSegment.getCategoryId()}, Function.identity()))

    then:
    1 == segments.size()
    TestTools.GSON.toJson(sportSegment1) == TestTools.GSON.toJson(segments.get(1))
  }

  def "Get latest sport segments objects - corruptedJson"() {
    InPlayData structure = new InPlayData(new InPlayModel(), new InPlayModel(), new InPlayModel(), new InPlayModel())

    SportSegment sportSegment1 = new SportSegment()
    sportSegment1.setCategoryId(1)
    sportSegment1.setTopLevelType(InPlayTopLevelType.LIVE_EVENT)

    SportSegment sportSegment2 = new SportSegment()
    sportSegment2.setCategoryId(2)
    sportSegment2.setTopLevelType(InPlayTopLevelType.UPCOMING_EVENT)

    SportSegment sportSegment3 = new SportSegment()
    sportSegment3.setCategoryId(3)
    sportSegment3.setTopLevelType(InPlayTopLevelType.STREAM_EVENT)

    SportSegment sportSegment4 = new SportSegment()
    sportSegment4.setCategoryId(4)
    sportSegment4.setTopLevelType(InPlayTopLevelType.UPCOMING_STREAM_EVENT)

    structure.getLivenow().getSportEvents().add(sportSegment1)
    structure.getUpcoming().getSportEvents().add(sportSegment2)
    structure.getLiveStream().getSportEvents().add(sportSegment3)
    structure.getUpcomingLiveStream().getSportEvents().add(sportSegment4)

    generationStorage.getLatest(GenerationKeyType.INPLAY_GENERATION) >> "13"
    distributedInstance.getValue(INPLAY_STRUCTURE_MAP, "13") >> TestTools.GSON.toJson(structure)
    distributedInstance.getValues(INPLAY_SPORT_SEGMENT_MAP, _ as List<String>) >> [
      TestTools.GSON.toJson(sportSegment1),
      "ABCD",
      "ABCD"
    ]

    when:
    Map<Integer, SportSegment> segments = storageService.getLatestSportSegmentsObjects().stream()
        .collect(Collectors.toMap({ sportSegment->sportSegment.getCategoryId()}, Function.identity()))

    then:
    1 == segments.size()
    TestTools.GSON.toJson(sportSegment1) == TestTools.GSON.toJson(segments.get(1))
  }

  def "Test clear error"() {
    when:
    storageService.clearError()

    then:
    1 * errorsStorage.removeError(InPlayStorageService.INPLAY_ERROR_KEY)
  }

  def "Test save error"() {
    Exception e = new RuntimeException("Some message")

    when:
    storageService.saveError(e)

    then:
    1 * errorsStorage.saveError(InPlayStorageService.INPLAY_ERROR_KEY, _) >> { arguments ->
      def argument1 = arguments[1]
      Map<String, Object> error = TestTools.GSON.fromJson(argument1 as String, Map.class) as Map<String, Object>
      assert e.getClass().getName() == error.get("class")
      assert e.getMessage() == error.get("message")
    }
  }


  def "Test getLatestInPlayCache"() {

    given:
    generationStorage.getLatest(INPLAY_GENERATION)>>"12121"
    distributedInstance.getValue(INPLAY_CACHED_STRUCTURE_MAP, "12121")>>null;

    when:
    InPlayCache cache=storageService.getLatestInPlayCache()

    then:
    cache==null
  }
}
