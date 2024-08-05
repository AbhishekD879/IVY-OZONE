package com.oxygen.publisher.model


import spock.lang.Specification

class RawIndexSpec extends Specification {

  def "Compare to left lower by Type"() {
    setup:
    RawIndex left = RawIndex.builder()
        .categoryId(16)
        .topLevelType("UPCOMING_EVENT")
        .marketSelector("HH")
        .typeId(1111)
        .build()
    RawIndex right = RawIndex.builder()
        .categoryId(16)
        .topLevelType("UPCOMING_EVENT")
        .marketSelector("HH")
        .build()

    expect:
    left < right
    right > left
  }

  def "Compare to left lower by Market"() {
    setup:
    RawIndex left = RawIndex.builder()
        .categoryId(16)
        .topLevelType("UPCOMING_EVENT")
        .marketSelector("HH")
        .typeId(1111)
        .build()
    RawIndex right = RawIndex.builder()
        .categoryId(16)
        .topLevelType("UPCOMING_EVENT")
        .typeId(2222)
        .build()

    expect:
    left < right
    right > left
  }

  def "Compare equals by Type"() {
    setup:
    RawIndex left = RawIndex.builder()
        .categoryId(16)
        .topLevelType("UPCOMING_EVENT")
        .marketSelector("HH")
        .build()
    RawIndex right = RawIndex.builder()
        .categoryId(16)
        .topLevelType("UPCOMING_EVENT")
        .marketSelector("wwqwwq")
        .build()

    expect:
    left == right
    right == left
  }

  def "Compare equals on Market"() {
    setup:
    RawIndex left = RawIndex.builder()
        .categoryId(16)
        .topLevelType("UPCOMING_EVENT")
        .typeId(2343)
        .build()
    RawIndex right = RawIndex.builder()
        .categoryId(16)
        .topLevelType("UPCOMING_EVENT")
        .typeId(123)
        .build()

    expect:
    left == right
    right == left
  }


  def "Compare equals by required Fields"() {
    setup:
    RawIndex left = RawIndex.builder()
        .categoryId(16)
        .topLevelType("LIVE")
        .build()
    RawIndex right = RawIndex.builder()
        .categoryId(16)
        .topLevelType("UPCOMING_EVENT")
        .build()

    expect:
    left == right
    right == left
  }

  def "Compare equals fully"() {
    setup:
    RawIndex left = RawIndex.builder()
        .categoryId(16)
        .topLevelType("LIVE")
        .typeId(12)
        .marketSelector("ds")
        .build()
    RawIndex right = RawIndex.builder()
        .categoryId(16)
        .topLevelType("UPCOMING_EVENT")
        .typeId(934)
        .marketSelector("sfd")
        .build()
    expect:
    left == right
    right == left
  }

  def "Compare left fully"() {
    setup:
    RawIndex left = RawIndex.builder()
        .categoryId(16)
        .topLevelType("LIVE")
        .marketSelector("ds")
        .build()
    RawIndex right = RawIndex.builder()
        .categoryId(16)
        .topLevelType("UPCOMING_EVENT")
        .typeId(934)
        .marketSelector("sfd")
        .build()

    expect:
    left > right
    right < left
  }
}
