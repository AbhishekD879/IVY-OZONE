package com.coral.oxygen.middleware.in_play.service

import com.coral.oxygen.middleware.in_play.service.injector.TypeSectionTitleDataInjector
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment
import spock.lang.Specification

class TypeSectionTitleDataInjectorSpec extends Specification {
  TypeSectionTitleDataInjector dataInjector

  InPlayData data
  TypeSegment type
  SportSegment sport

  def setup() {
    dataInjector = new TypeSectionTitleDataInjector()

    data = new InPlayData()
    type = new TypeSegment()
    sport = new SportSegment()
  }

  def cleanup() {
    dataInjector = null
  }

  def "Test type section title connect app"() {
    type.setTypeName("ABC")

    sport.setEventsByTypeName(new ArrayList<>())
    sport.getEventsByTypeName().add(type)

    data.getLivenow().getSportEvents().add(sport)

    when:
    dataInjector.injectData(data)

    then:
    "ABC" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleConnectApp()
  }

  def "Test non-specific sport"() {
    type.setTypeName("TN")
    type.setCategoryName("CN")

    sport.setCategoryPath("some_sport")
    sport.setEventsByTypeName(new ArrayList<>())
    sport.getEventsByTypeName().add(type)

    data.getLivenow().getSportEvents().add(sport)

    when:
    dataInjector.injectData(data)

    then:
    "TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleAllSports()
    "CN - TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleOneSport()
  }

  def "Test non-specific sport null category name"() {
    type.setTypeName("TN")

    sport.setCategoryPath("some_sport")
    sport.setEventsByTypeName(new ArrayList<>())
    sport.getEventsByTypeName().add(type)

    data.getLivenow().getSportEvents().add(sport)

    when:
    dataInjector.injectData(data)

    then:
    "TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleAllSports()
    "TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleOneSport()
  }

  def "Test non specific sport empty category name"() {
    type.setTypeName("TN")
    type.setCategoryName("")

    sport.setCategoryPath("some_sport")
    sport.setEventsByTypeName(new ArrayList<>())
    sport.getEventsByTypeName().add(type)

    data.getLivenow().getSportEvents().add(sport)

    when:
    dataInjector.injectData(data)

    then:
    "TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleAllSports()
    "TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleOneSport()
  }

  def "Test non specific sport null type name"() {
    type.setCategoryName("CN")

    sport.setCategoryPath("some_sport")
    sport.setEventsByTypeName(new ArrayList<>())
    sport.getEventsByTypeName().add(type)

    data.getLivenow().getSportEvents().add(sport)

    when:
    dataInjector.injectData(data)

    then:
    null == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleAllSports()
    "CN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleOneSport()
  }

  def "Test non specific sport empty typeName"() {
    type.setTypeName("")
    type.setCategoryName("CN")

    sport.setCategoryPath("some_sport")
    sport.setEventsByTypeName(new ArrayList<>())
    sport.getEventsByTypeName().add(type)

    data.getLivenow().getSportEvents().add(sport)

    when:
    dataInjector.injectData(data)

    then:
    "" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleAllSports()
    "CN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleOneSport()
  }

  def "Test specific sport"() {
    type.setTypeName("TN")
    type.setCategoryName("CN")
    type.setClassName("CLSN")

    sport.setCategoryPath("football")
    sport.setEventsByTypeName(new ArrayList<>())
    sport.getEventsByTypeName().add(type)

    data.getLivenow().getSportEvents().add(sport)

    when:
    dataInjector.injectData(data)

    then:
    "CLSN - TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleAllSports()
    "CLSN - TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleOneSport()
  }

  def "Test specific sport remove category name"() {
    type.setTypeName("TN")
    type.setCategoryName("CN")
    type.setClassName("CN CLSN")

    sport.setCategoryPath("football")
    sport.setEventsByTypeName(new ArrayList<>())
    sport.getEventsByTypeName().add(type)

    data.getLivenow().getSportEvents().add(sport)

    when:
    dataInjector.injectData(data)

    then:
    "CLSN - TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleAllSports()
    "CLSN - TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleOneSport()
  }

  def "Test specific sport remove category name and all"() {
    type.setTypeName("TN")
    type.setCategoryName("CN")
    type.setClassName("CN All CLSN")

    sport.setCategoryPath("football")
    sport.setEventsByTypeName(new ArrayList<>())
    sport.getEventsByTypeName().add(type)

    data.getLivenow().getSportEvents().add(sport)

    when:
    dataInjector.injectData(data)

    then:
    "CLSN - TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleAllSports()
    "CLSN - TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleOneSport()
  }

  def "Test specific sport remove category name but left all"() {
    type.setTypeName("TN")
    type.setCategoryName("CN")
    type.setClassName("CN AllCLSN")

    sport.setCategoryPath("football")
    sport.setEventsByTypeName(new ArrayList<>())
    sport.getEventsByTypeName().add(type)

    data.getLivenow().getSportEvents().add(sport)

    when:
    dataInjector.injectData(data)

    then:
    "AllCLSN - TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleAllSports()
    "AllCLSN - TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleOneSport()
  }

  def "Test specific sport null className"() {
    type.setTypeName("TN")
    type.setCategoryName("CN")
    type.setClassName(null)

    sport.setCategoryPath("football")
    sport.setEventsByTypeName(new ArrayList<>())
    sport.getEventsByTypeName().add(type)

    data.getLivenow().getSportEvents().add(sport)

    when:
    dataInjector.injectData(data)

    then:
    "TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleAllSports()
    "TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleOneSport()
  }

  def "Test specific sport empty className"() {
    type.setTypeName("TN")
    type.setCategoryName("CN")
    type.setClassName("")

    sport.setCategoryPath("football")
    sport.setEventsByTypeName(new ArrayList<>())
    sport.getEventsByTypeName().add(type)

    data.getLivenow().getSportEvents().add(sport)

    when:
    dataInjector.injectData(data)

    then:
    "TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleAllSports()
    "TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleOneSport()
  }

  def "Test specific sport className equals category name"() {
    type.setTypeName("TN")
    type.setCategoryName("Some Name")
    type.setClassName("Some Name")

    sport.setCategoryPath("football")
    sport.setEventsByTypeName(new ArrayList<>())
    sport.getEventsByTypeName().add(type)

    data.getLivenow().getSportEvents().add(sport)

    when:
    dataInjector.injectData(data)

    then:
    "Some Name - TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleAllSports()
    "Some Name - TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleOneSport()
  }

  def "Test specific sport remove category name and all but not second category name_PHX_15"() {
    type.setTypeName("TN")
    type.setCategoryName("CN")
    type.setClassName("CN All CN CLSN")

    sport.setCategoryPath("football")
    sport.setEventsByTypeName(new ArrayList<>())
    sport.getEventsByTypeName().add(type)

    data.getLivenow().getSportEvents().add(sport)

    when:
    dataInjector.injectData(data)

    then:
    "CN CLSN - TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleAllSports()
    "CN CLSN - TN" == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeSectionTitleOneSport()
  }
}
